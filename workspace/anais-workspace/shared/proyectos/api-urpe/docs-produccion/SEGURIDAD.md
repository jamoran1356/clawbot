# 🔒 Guía de Seguridad - API-URPE

## Principios Generales

1. **Never trust user input** — Validar y sanitizar todo
2. **Principle of least privilege** — Roles granulares
3. **Defense in depth** — Múltiples capas de seguridad
4. **Secure by default** — Configuración segura es la predeterminada

---

## 1. Autenticación & Autorización

### JWT Configuration
```typescript
// ✅ BIEN
JWT_SECRET: min 32 chars, rotado cada 6 meses
JWT_EXPIRATION: 15 minutos (tokens cortos + refresh)
JWT_REFRESH_EXPIRATION: 7 días

// ❌ MAL
JWT_SECRET: hardcoded en código
JWT_EXPIRATION: 30 días
Mismo secret para múltiples ambientes
```

### Password Hashing
```typescript
// Usar Argon2 (bcrypt es lento)
import { hash, verify } from '@node-rs/argon2';

const hashedPassword = await hash(plainPassword, {
  memory: 19, // 64MB
  timeCost: 2,
  parallelism: 1,
});
```

### API Key Management
```typescript
// Generar keys seguras y almacenarlas hasheadas
const apiKey = nanoid(32); // Ej: "h7x9k2m_qw4zt5jb_6np_1rs"
const hashedKey = hashApiKey(apiKey);

// Retornar key UNA SOLA VEZ (user debe guardar)
// Si la pierden, generar nueva

// Almacenar en DB: hashedKey (nunca plaintext)
// Request: Authorization: Bearer <api-key>
```

### Roles & Permissions
```typescript
// Decorador para validar roles
@UseGuards(JwtAuthGuard, RolesGuard)
@Roles(UserRole.ADMIN)
deleteUser(@Param('id') id: string) { }

// Roles disponibles:
// - ADMIN: Acceso total
// - USER: Solo sus datos
// - API_CLIENT: Solo endpoints específicos
```

---

## 2. Input Validation & Sanitization

### Class Validator (Obligatorio)
```typescript
import { IsEmail, IsString, MinLength, IsURL } from 'class-validator';

export class CreateApiEndpointDto {
  @IsString()
  @MinLength(3)
  name: string;

  @IsURL()
  targetUrl: string;

  @IsEmail()
  contactEmail: string;
}
```

### SQL Injection Prevention
```typescript
// ✅ BIEN - Prisma con parameterized queries
const user = await prisma.user.findUnique({
  where: { email: userInput }, // Safe
});

// ❌ MAL - Raw query (NUNCA)
// query(`SELECT * FROM users WHERE email = '${email}'`)
```

### XSS Prevention
```typescript
// Express integrado + helmet
app.use(helmet());

// Content-Security-Policy header
// X-Content-Type-Options: nosniff
// X-Frame-Options: SAMEORIGIN
// X-XSS-Protection: 1; mode=block
```

### CSRF Protection (si usa cookies)
```typescript
// Para requests stateless con JWT: no es necesario
// Si agregás cookies: usar csrf middleware
import csurf from 'csurf';

app.use(csurf()); // Token verificado en POST/PUT/DELETE
```

---

## 3. HTTPS & Transport Security

### Certificado SSL
```bash
# Let's Encrypt (gratuito)
certbot certonly --standalone -d api.urpeailab.com

# Renovación automática
0 3 * * * certbot renew --quiet
```

### HSTS (HTTP Strict Transport Security)
```typescript
// Nginx o middleware
add_header Strict-Transport-Security "max-age=31536000; includeSubDomains" always;
```

### TLS Configuration
```nginx
ssl_protocols TLSv1.2 TLSv1.3;
ssl_ciphers HIGH:!aNULL:!MD5;
ssl_prefer_server_ciphers on;
```

---

## 4. CORS (Cross-Origin Resource Sharing)

### Configuración Restrictiva
```typescript
// ✅ BIEN
app.enableCors({
  origin: [
    'https://urpeailab.com',
    'https://app.urpeailab.com',
  ],
  credentials: true,
  methods: ['GET', 'POST', 'PUT', 'DELETE'],
  allowedHeaders: ['Content-Type', 'Authorization'],
  maxAge: 3600,
});

// ❌ MAL
app.enableCors({
  origin: '*', // Permite cualquier origen!
  credentials: true,
});
```

---

## 5. Rate Limiting

### Implementación
```typescript
import { ThrottlerModule } from '@nestjs/throttler';

@Module({
  imports: [
    ThrottlerModule.forRoot({
      ttl: 60, // 60 segundos
      limit: 10, // máx 10 requests
    }),
  ],
})
export class AppModule {}
```

### Por Endpoint
```typescript
@Throttle({ default: { limit: 100, ttl: 60000 } })
@Post('/api/proxy')
async proxyRequest() { }

@Throttle({ default: { limit: 5, ttl: 60000 } })
@Post('/auth/login')
async login() { }
```

### Por IP (Nginx)
```nginx
limit_req_zone $binary_remote_addr zone=api_limit:10m rate=10r/s;
limit_req_zone $binary_remote_addr zone=auth_limit:10m rate=5r/m;

location /api/v1/auth/login {
    limit_req zone=auth_limit burst=2 nodelay;
}
```

---

## 6. Database Security

### Connection Pool
```typescript
// .env
DATABASE_URL="postgresql://user:pass@localhost/db?schema=public&sslmode=require"
// sslmode=require: conexión SSL obligatoria
```

### Credentials Management
```bash
# ✅ BIEN - Environment variables
POSTGRES_PASSWORD=<generated-strong-password>

# ❌ MAL - Hardcoded
const password = "admin123"; // NO!
```

### Migrations
```bash
# Versionadas en Git
pnpm run prisma:migrate
# Genera archivo SQL en prisma/migrations/
```

### Regular Backups
```bash
# Daily backup script
0 1 * * * pg_dump -U user dbname | gzip > backup_$(date +%Y%m%d).sql.gz

# Test restore regularmente
pg_restore -U user -d test_db backup.sql
```

---

## 7. Secrets Management

### Rotation Schedule
```
JWT_SECRET:        Cada 6 meses
JWT_REFRESH_SECRET: Cada 6 meses
API_KEYS:          Usuario puede generar nuevas
SMTP_PASSWORD:     Anual (usar app passwords si es Gmail)
```

### Environment Variables
```bash
# Production: usar secretos de:
# - AWS Secrets Manager
# - HashiCorp Vault
# - Google Secret Manager
# - Azure Key Vault

# Desarrollo: .env (en .gitignore)
# Producción: CI/CD variables o servicio de secretos
```

### No Versionés Secretos
```bash
# .gitignore
.env
.env.*.local
*.key
*.pem
```

---

## 8. Proxy Security (Critical)

### Validación de URLs
```typescript
// ✅ BIEN
const allowed = ['https://n8n.company.com', 'https://supabase.co'];
if (!allowed.some(url => targetUrl.startsWith(url))) {
  throw new UnauthorizedException('Target not allowed');
}

// ❌ MAL
// Permitir cualquier URL que el user envíe (SSRF!)
```

### SSRF Prevention (Server-Side Request Forgery)
```typescript
// No permitir:
// - localhost, 127.0.0.1, 0.0.0.0
// - IPs privadas (10.0.0.0/8, 172.16.0.0/12, 192.168.0.0/16)
// - IPs metadata (169.254.169.254 en AWS)

const ipaddr = require('ipaddr.js');

function isSafeUrl(url: string): boolean {
  const parsed = new URL(url);
  const hostname = parsed.hostname;
  
  if (!ipaddr.isValid(hostname)) {
    // Domain name - check DNS
    // Implementar DNS validation
    return true;
  }
  
  const ip = ipaddr.process(hostname);
  
  return !(
    ip.isLoopback() ||
    ip.isPrivate() ||
    ip.isReserved() ||
    ip.isLinkLocal()
  );
}
```

### Timeout & Size Limits
```typescript
// Prevenir DoS
PROXY_TIMEOUT_MS: 30000, // 30 segundos máximo
MAX_REQUEST_BODY_SIZE: '20mb',
MAX_RESPONSE_BODY_SIZE: '20mb',
```

---

## 9. API Key Security

### Generación
```typescript
// Usar nanoid o uuid
const apiKey = nanoid(32); // 32 caracteres = ~189 bits de entropía

// Dividir y almacenar hasheado
const [prefix, secret] = splitKey(apiKey);
// Mostrar solo: prefix_xxxxxxxxxxxxxxxxxxxx (último 6 chars visible)
```

### Almacenamiento
```typescript
// DB: almacenar SOLO el hash
const hashedKey = await hashApiKey(apiKey);
await prisma.apiKey.create({
  data: {
    hashedKey, // Nunca plaintext
    prefix: apiKey.substring(0, 8),
    userId,
  },
});
```

### Validación en Requests
```typescript
// Extraer del header Authorization
const apiKey = req.headers.authorization?.replace('Bearer ', '');
const hashedKey = await hashApiKey(apiKey);

// Buscar en DB
const apiKeyRecord = await prisma.apiKey.findUnique({
  where: { hashedKey },
});
```

---

## 10. Logging & Monitoring

### Qué Loguear
```typescript
// ✅ BIEN
- Intentos de login (exitosos y fallidos)
- Cambios de contraseña
- Generación de API keys
- Acceso a endpoints sensibles
- Errores de sistema

// ❌ MAL
- Passwords
- API keys plaintext
- Tokens JWT
- Datos sensibles de usuarios
```

### Structured Logging
```typescript
import * as winston from 'winston';

const logger = winston.createLogger({
  format: winston.format.json(),
  transports: [
    new winston.transports.File({ filename: 'error.log', level: 'error' }),
    new winston.transports.File({ filename: 'combined.log' }),
  ],
});

// Uso
logger.info('User login', {
  userId: user.id,
  email: user.email,
  timestamp: new Date().toISOString(),
  ipAddress: req.ip,
});
```

### Monitoring Alertas
```bash
# Alertar si:
- Más de 10 intentos de login fallidos en 5 min (IP)
- API key creada
- Usuario eliminado
- Database connection lost
- Proceso worker caído
```

---

## 11. Checklist de Seguridad

Pre-Deploy:
- [ ] HTTPS/SSL configurado
- [ ] CORS restrictivo
- [ ] JWT secrets seguros (>32 chars)
- [ ] Contraseñas hasheadas con Argon2
- [ ] Rate limiting activo
- [ ] Input validation (class-validator)
- [ ] SSRF prevention en proxy
- [ ] Database backups tested
- [ ] No secretos en Git
- [ ] Helmet middleware activo

Post-Deploy (Mensual):
- [ ] Revisar logs de seguridad
- [ ] Verificar acceso sin autorizar
- [ ] Probar backup restoration
- [ ] Actualizar dependencias
- [ ] Scan de vulnerabilidades (npm audit)
- [ ] Rotar secrets importantes

Anual:
- [ ] Audit de seguridad externo
- [ ] Penetration testing
- [ ] Revew de permisos de usuarios
- [ ] Documentación actualizada

---

**Última actualización:** 2026-01-29
