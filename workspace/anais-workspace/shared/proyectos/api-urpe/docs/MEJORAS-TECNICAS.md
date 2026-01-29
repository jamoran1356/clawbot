# 🛠️ Mejoras Técnicas Requeridas - API-URPE

## Fase 1: Bug Fixes & Refactoring

### 1. ProxyService - SSRF Prevention ⚠️ CRÍTICO
**Ubicación:** `apps/api/src/modules/proxy/proxy.service.ts`

**Problema:** No valida que targetUrl no sea localhost, IP privada o metadata.

**Solución:**
```typescript
// Agregar validación SSRF
private validateTargetUrl(url: string): boolean {
  const parsed = new URL(url);
  const hostname = parsed.hostname;
  
  // Blocklist de dominios peligrosos
  const blocked = [
    'localhost',
    '127.0.0.1',
    '0.0.0.0',
    '169.254.169.254', // AWS metadata
    '::1', // IPv6 localhost
  ];
  
  if (blocked.includes(hostname)) {
    throw new UnauthorizedException('Target URL not allowed');
  }
  
  // Validar que no sea IP privada (sin usar ipaddr.js aún)
  if (this.isPrivateIp(hostname)) {
    throw new UnauthorizedException('Private IP addresses not allowed');
  }
  
  return true;
}

private isPrivateIp(ip: string): boolean {
  const privateRanges = [
    /^10\./,
    /^172\.(1[6-9]|2[0-9]|3[01])\./,
    /^192\.168\./,
    /^fc[0-9a-f]{2}:/i, // IPv6 ULA
  ];
  
  return privateRanges.some(range => range.test(ip));
}
```

### 2. API Key Hashing ⚠️ CRÍTICO
**Problema:** API Keys se almacenan en plaintext en DB.

**Solución:**
```typescript
// Crear service
// apps/api/src/shared/services/api-key-crypto.service.ts

import { Injectable } from '@nestjs/common';
import { hash, verify } from '@node-rs/argon2';

@Injectable()
export class ApiKeyCryptoService {
  async hashKey(key: string): Promise<string> {
    return hash(key, {
      memory: 19,
      timeCost: 2,
      parallelism: 1,
    });
  }

  async verifyKey(plainKey: string, hashedKey: string): Promise<boolean> {
    return verify(hashedKey, plainKey);
  }

  generateKey(): string {
    const { nanoid } = require('nanoid');
    return nanoid(32); // 189 bits de entropía
  }
}
```

**Cambios en DB:**
```sql
-- Agregar migración
ALTER TABLE api_keys ADD COLUMN hashed_key TEXT UNIQUE;
ALTER TABLE api_keys DROP COLUMN key;
RENAME COLUMN hashed_key TO key;
```

### 3. Error Handling Mejorado
**Problema:** Expone detalles internos en errores.

**Solución:**
```typescript
// apps/api/src/common/filters/http-exception.filter.ts

import { ArgumentsHost, Catch, ExceptionFilter, HttpException, Logger } from '@nestjs/common';
import { Response } from 'express';

@Catch(HttpException)
export class HttpExceptionFilter implements ExceptionFilter {
  private logger = new Logger('HttpExceptionFilter');

  catch(exception: HttpException, host: ArgumentsHost) {
    const ctx = host.switchToHttp();
    const response = ctx.getResponse<Response>();
    const request = ctx.getRequest();
    const status = exception.getStatus();
    const message = exception.message;

    // Log con contexto
    this.logger.error({
      timestamp: new Date().toISOString(),
      status,
      message,
      path: request.url,
      method: request.method,
      ip: request.ip,
    });

    // Respuesta genérica en producción
    const isProduction = process.env.NODE_ENV === 'production';
    
    response.status(status).json({
      statusCode: status,
      error: this.getPublicMessage(status),
      ...(isProduction ? {} : { detail: message }),
      timestamp: new Date().toISOString(),
    });
  }

  private getPublicMessage(status: number): string {
    const messages: Record<number, string> = {
      400: 'Bad Request',
      401: 'Unauthorized',
      403: 'Forbidden',
      404: 'Not Found',
      429: 'Too Many Requests',
      500: 'Internal Server Error',
    };
    return messages[status] || 'Error';
  }
}
```

### 4. Database Connection Pooling
**Problema:** Sin PgBouncer en producción, conexiones agotadas.

**Solución:**
```typescript
// Agregar a .env.production
DATABASE_POOL_MIN=5
DATABASE_POOL_MAX=20
DATABASE_POOL_IDLE_TIMEOUT=30000

// apps/api/src/config/database.config.ts
export const databaseConfig = () => ({
  database: {
    url: process.env.DATABASE_URL,
    connectionPoolSize: parseInt(process.env.DATABASE_POOL_MAX || '20'),
    connectionIdleTimeout: parseInt(process.env.DATABASE_POOL_IDLE_TIMEOUT || '30000'),
  },
});
```

---

## Fase 2: Features Producción

### 5. Webhook Module para N8N
**Ubicación:** `apps/api/src/modules/webhook/`

```typescript
// webhook.service.ts
@Injectable()
export class WebhookService {
  constructor(private prisma: PrismaService) {}

  async handleN8nWebhook(
    endpointSlug: string,
    payload: any,
    headers: any,
  ) {
    const endpoint = await this.prisma.apiEndpoint.findUnique({
      where: { slug: endpointSlug },
    });

    if (!endpoint || endpoint.status !== 'ACTIVE') {
      throw new BadRequestException('Endpoint not found');
    }

    // Verificar signature si está configurado
    if (endpoint.headers?.['n8n-signature']) {
      this.verifyN8nSignature(payload, headers);
    }

    // Procesar payload
    const transformed = this.transformData(payload, endpoint.requestTransform);

    // Guardar para auditoría
    await this.prisma.request.create({
      data: {
        endpointId: endpoint.id,
        method: 'WEBHOOK',
        path: `/webhook/${endpointSlug}`,
        headers,
        body: payload,
        statusCode: 200,
        responseTime: 0,
      },
    });

    return { success: true, id: nanoid() };
  }
}
```

### 6. Email Service Mejorado
**Ubicación:** `apps/api/src/modules/email/`

```typescript
// email.service.ts - Agregar validaciones

@Injectable()
export class EmailService {
  constructor(
    private prisma: PrismaService,
    private emailQueue: Queue,
  ) {}

  async sendEmail(to: string, subject: string, body: string) {
    // Validación
    if (!this.isValidEmail(to)) {
      throw new BadRequestException('Invalid email address');
    }

    if (subject.length > 255) {
      throw new BadRequestException('Subject too long');
    }

    if (body.length > 10000) {
      throw new BadRequestException('Email body too long');
    }

    // Agregar a queue
    const job = await this.emailQueue.add('send-email', {
      to,
      subject,
      body,
      timestamp: new Date().toISOString(),
    });

    return { jobId: job.id, status: 'QUEUED' };
  }

  private isValidEmail(email: string): boolean {
    const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    return emailRegex.test(email) && email.length <= 254;
  }
}
```

### 7. Request/Response Logging Structured
**Ubicación:** `apps/api/src/common/middleware/`

```typescript
// logging.middleware.ts
@Injectable()
export class LoggingMiddleware implements NestMiddleware {
  private logger = new Logger('HTTP');

  use(req: Request, res: Response, next: NextFunction) {
    const start = Date.now();
    
    res.on('finish', () => {
      const duration = Date.now() - start;
      
      this.logger.log(
        JSON.stringify({
          timestamp: new Date().toISOString(),
          method: req.method,
          path: req.path,
          statusCode: res.statusCode,
          duration,
          ip: req.ip,
          userAgent: req.get('user-agent'),
          userId: req.user?.id || null,
        }),
      );
    });

    next();
  }
}
```

### 8. Health Check Detallado
**Ubicación:** `apps/api/src/modules/health/`

```typescript
@Controller('health')
export class HealthController {
  constructor(
    private prisma: PrismaService,
    private redis: Redis,
  ) {}

  @Get()
  async check() {
    const health = {
      status: 'ok',
      timestamp: new Date().toISOString(),
      uptime: process.uptime(),
      checks: {
        database: await this.checkDatabase(),
        redis: await this.checkRedis(),
        memory: this.checkMemory(),
      },
    };

    const allHealthy = Object.values(health.checks).every(
      (check: any) => check.status === 'ok',
    );

    return {
      ...health,
      status: allHealthy ? 'ok' : 'degraded',
    };
  }

  private async checkDatabase() {
    try {
      await this.prisma.$queryRaw`SELECT 1`;
      return { status: 'ok' };
    } catch (error) {
      return { status: 'error', message: error.message };
    }
  }

  private async checkRedis() {
    try {
      await this.redis.ping();
      return { status: 'ok' };
    } catch (error) {
      return { status: 'error', message: error.message };
    }
  }

  private checkMemory() {
    const used = process.memoryUsage();
    return {
      status: used.heapUsed / used.heapTotal > 0.9 ? 'warning' : 'ok',
      heapUsed: Math.round(used.heapUsed / 1024 / 1024) + 'MB',
      heapTotal: Math.round(used.heapTotal / 1024 / 1024) + 'MB',
    };
  }
}
```

---

## Fase 3: Testing

### 9. Unit Tests
**Ubicación:** `apps/api/src/**/*.spec.ts`

```typescript
// proxy.service.spec.ts
describe('ProxyService', () => {
  let service: ProxyService;
  let prisma: PrismaService;

  beforeEach(async () => {
    const module = await Test.createTestingModule({
      providers: [ProxyService, PrismaService],
    }).compile();

    service = module.get<ProxyService>(ProxyService);
    prisma = module.get<PrismaService>(PrismaService);
  });

  describe('validateTargetUrl', () => {
    it('should reject localhost', () => {
      expect(() => service['validateTargetUrl']('http://localhost:3000/'))
        .toThrow();
    });

    it('should reject private IPs', () => {
      expect(() => service['validateTargetUrl']('http://192.168.1.1/'))
        .toThrow();
    });

    it('should accept public URLs', () => {
      expect(() => service['validateTargetUrl']('https://example.com/'))
        .not.toThrow();
    });
  });
});
```

### 10. Integration Tests
**Ubicación:** `apps/api/test/`

```typescript
// proxy.e2e-spec.ts
describe('Proxy Endpoints (e2e)', () => {
  let app: INestApplication;

  beforeAll(async () => {
    const moduleRef = await Test.createTestingModule({
      imports: [AppModule],
    }).compile();

    app = moduleRef.createNestApplication();
    await app.init();
  });

  it('POST /api/v1/proxy/test-endpoint', () => {
    return request(app.getHttpServer())
      .post('/api/v1/proxy/test-endpoint')
      .set('Authorization', `Bearer ${testApiKey}`)
      .send({ data: 'test' })
      .expect(200);
  });
});
```

---

## Fase 4: Performance

### 11. Caching Estratégico
```typescript
// usar Redis para:
- Session tokens
- API key lookups
- Endpoint configurations
- Rate limit counters

// TTLs recomendados:
- API Keys: 1 hora
- Endpoints: 5 minutos
- User sessions: 24 horas
```

### 12. Database Indexes
```sql
-- Agregar índices para queries frecuentes
CREATE INDEX idx_requests_endpointid_createdat ON requests(endpoint_id, created_at DESC);
CREATE INDEX idx_apikeys_hashedkey ON api_keys(hashed_key);
CREATE INDEX idx_apiendpoints_userid_slug ON api_endpoints(user_id, slug);
CREATE INDEX idx_emailcampaigns_userid_status ON email_campaigns(user_id, status);
```

---

## Fase 5: Deployment Helpers

### 13. Migration Scripts
```bash
# scripts/migrate.sh
#!/bin/bash
set -e

echo "Running database migrations..."
npx prisma migrate deploy

echo "Seeding initial data..."
npx prisma db seed

echo "Done!"
```

### 14. Health Check Script
```bash
# scripts/health-check.sh
#!/bin/bash

API_URL="${1:-http://localhost:3000}"

response=$(curl -s -w "\n%{http_code}" "$API_URL/api/v1/health")
http_code=$(echo "$response" | tail -n1)
body=$(echo "$response" | head -n-1)

if [ "$http_code" = "200" ]; then
  echo "✅ API is healthy"
  exit 0
else
  echo "❌ API health check failed (HTTP $http_code)"
  echo "$body"
  exit 1
fi
```

---

## Dependencias a Agregar

```json
{
  "dependencies": {
    "helmet": "^7.1.0",           // Security headers
    "class-validator": "^0.14.1",  // Input validation
    "class-transformer": "^0.5.1",
    "@nestjs/throttler": "^4.1.1", // Rate limiting
    "winston": "^3.11.0",          // Logging
    "joi": "^17.11.0",             // Env validation
    "ipaddr.js": "^2.2.0",         // IP validation
    "axios-retry": "^3.8.0"        // Retry logic
  },
  "devDependencies": {
    "@nestjs/testing": "^10.4.20",
    "@types/jest": "^29.5.10",
    "jest": "^29.7.0"
  }
}
```

---

## Timeline Estimado

- **Fase 1 (Bug Fixes):** 3-4 días
- **Fase 2 (Features):** 5-7 días
- **Fase 3 (Testing):** 3-4 días
- **Fase 4 (Performance):** 2-3 días
- **Fase 5 (Deployment):** 2 días

**Total:** 2-3 semanas para production-ready

---

**Última actualización:** 2026-01-29
