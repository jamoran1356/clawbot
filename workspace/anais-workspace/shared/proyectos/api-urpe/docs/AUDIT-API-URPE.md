# 📋 AUDIT DETALLADO - PROYECTO API-URPE

**Fecha del Audit:** 29 de Enero, 2025  
**Proyecto:** URPE API Lab - Plataforma de Gestión de APIs No-Code  
**Stack:** NestJS 10.4.20 + Next.js 16.1.1 + PostgreSQL 16 + Redis 7 + BullMQ

---

## 📑 ÍNDICE

1. [Estructura del Proyecto](#1-estructura-del-proyecto)
2. [Package.json Principal y Dependencias](#2-packagejson-principal-y-dependencias)
3. [Configuración](#3-configuración)
4. [Módulos Existentes](#4-módulos-existentes)
5. [DTOs y Validación](#5-dtos-y-validación)
6. [Seguridad](#6-seguridad)
7. [Database (Prisma Schema)](#7-database-prisma-schema)
8. [Documentación](#8-documentación)
9. [Scripts de Build/Deploy](#9-scripts-de-builddeploy)
10. [Problemas Encontrados](#10-problemas-encontrados)
11. [Mejoras Necesarias](#11-mejoras-necesarias)
12. [Recomendaciones Críticas](#12-recomendaciones-críticas)

---

## 1. ESTRUCTURA DEL PROYECTO

### 1.1 Estructura General (Monorepo)

```
api-urpe/
├── apps/
│   ├── api/                    # Backend NestJS (aplicación principal)
│   │   └── src/
│   │       ├── main.ts
│   │       ├── app.module.ts
│   │       ├── common/         # Guards, decorators, utilidades comunes
│   │       ├── config/         # Configuración por módulo
│   │       ├── infra/          # Infraestructura (Prisma, Redis)
│   │       ├── modules/        # Módulos de negocio
│   │       └── shared/         # Servicios compartidos
│   │
│   ├── web/                    # Frontend Next.js 16
│   │   ├── src/app/            # Pages (App Router)
│   │   ├── src/components/
│   │   └── src/lib/
│   │
│   └── worker/                 # Background worker (BullMQ)
│       └── src/
│
├── prisma/
│   └── schema.prisma           # Database schema
│
├── docker/
│   ├── docker-compose.yml      # Orquestación de servicios
│   ├── api.Dockerfile
│   └── worker.Dockerfile
│
├── docs/
│   ├── EMAIL_CAMPAIGNS.md
│   └── QUICK_START_EMAIL.md
│
├── scripts/
│   └── test-email-campaign.js
│
├── .env                        # Variables de entorno
├── .env.example
├── README.md
├── package.json               # Root workspace
├── pnpm-lock.yaml
├── nest-cli.json              # Configuración NestJS
└── tsconfig.base.json         # TypeScript base

```

### 1.2 Monorepo Configuration

- **Package Manager:** pnpm 9.0.0 (definido explícitamente)
- **Type:** Monorepo NestJS con módulos separados
- **Root Config:**
  - `nest-cli.json`: Define proyectos "api" y "worker"
  - `tsconfig.base.json`: Compilación ES2021, strict mode habilitado
  - Configuración centralizada de build y compilación

### 1.3 Estructura de Módulos Backend

El backend está organizado en 6 módulos principales:

```
modules/
├── auth/                       # Autenticación JWT + Argon2
├── users/                      # Gestión de usuarios (CRUD + RBAC)
├── api-endpoints/              # Gestión de endpoints creados
├── proxy/                      # Sistema proxy inteligente
├── email-campaigns/            # Sistema masivo de emails
└── health/                     # Health check

infra/
├── prisma/                     # ORM y base de datos
└── (redis, queue están en config)

common/
├── guards/
│   ├── jwt-auth.guard.ts
│   └── roles.guard.ts
├── decorators/
│   ├── current-user.decorator.ts
│   └── roles.decorator.ts
└── exceptions/

shared/
├── services/
│   ├── email.service.ts        # Servicio de email (Nodemailer)
│   └── (otros servicios compartidos)
├── utils/
│   └── response.util.ts
├── constants/
│   └── app.constants.ts
└── errors/
    └── api.error.ts
```

---

## 2. PACKAGE.JSON PRINCIPAL Y DEPENDENCIAS

### 2.1 Root Package.json

```json
{
  "name": "api-platform",
  "version": "1.0.0",
  "description": "Scalable API Platform with NestJS",
  "private": true,
  "packageManager": "pnpm@9.0.0",
  "scripts": {
    "build": "nest build",
    "build:api": "nest build api",
    "build:worker": "nest build worker",
    "start": "nest start",
    "start:dev": "nest start --watch",
    "start:api": "nest start api --watch",
    "start:worker": "nest start worker --watch",
    "start:debug": "nest start --debug --watch",
    "start:prod": "node dist/apps/api/main",
    "prisma:generate": "prisma generate",
    "prisma:migrate": "prisma migrate dev",
    "prisma:studio": "prisma studio"
  },
  "packageManager": "pnpm@9.0.0"
}
```

### 2.2 Dependencias de Producción

#### Backend Core
| Dependencia | Versión | Propósito |
|------------|---------|----------|
| `@nestjs/core` | 10.4.20 | Framework backend |
| `@nestjs/common` | 10.4.20 | Decoradores y pipes comunes |
| `@nestjs/platform-express` | 10.4.20 | Middleware Express.js |
| `@nestjs/config` | 3.3.0 | Gestión variables de entorno |

#### Autenticación & Seguridad
| Dependencia | Versión | Propósito |
|------------|---------|----------|
| `@nestjs/jwt` | 10.2.0 | JWT tokens |
| `@nestjs/passport` | 10.0.3 | Estrategia Passport |
| `passport` | 0.7.0 | Autenticación |
| `passport-jwt` | 4.0.1 | JWT strategy |
| `@node-rs/argon2` | 2.0.2 | **Hash de contraseñas (ganador Password Hashing Competition)** |

#### Base de Datos
| Dependencia | Versión | Propósito |
|------------|---------|----------|
| `@prisma/client` | 5.22.0 | ORM |
| `prisma` | 5.22.0 | CLI migrations |

#### Queue & Background Jobs
| Dependencia | Versión | Propósito |
|------------|---------|----------|
| `@nestjs/bullmq` | 11.0.4 | Integración BullMQ |
| `bullmq` | 5.66.4 | Queue processor |
| `redis` | 4.7.1 | Redis client |

#### Email & HTTP
| Dependencia | Versión | Propósito |
|------------|---------|----------|
| `nodemailer` | 7.0.12 | Envío de emails SMTP |
| `@types/nodemailer` | 7.0.5 | Tipos TypeScript |
| `axios` | 1.13.2 | HTTP client |

#### Utilidades
| Dependencia | Versión | Propósito |
|------------|---------|----------|
| `class-validator` | 0.14.1 | Validación DTOs |
| `class-transformer` | 0.5.1 | Transformación de datos |
| `nanoid` | 5.1.6 | Generador de IDs únicos |
| `reflect-metadata` | 0.2.2 | Metadata reflection |
| `rxjs` | 7.8.2 | Programación reactiva |

### 2.3 Dependencias de Desarrollo

| Dependencia | Versión | Propósito |
|------------|---------|----------|
| `@nestjs/cli` | 11.0.14 | CLI NestJS |
| `@nestjs/schematics` | 11.0.9 | Generadores de código |
| `@types/express` | 5.0.6 | Tipos Express |
| `@types/node` | 25.0.3 | Tipos Node.js |
| `typescript` | 5.9.3 | Compilador TypeScript |

### 2.4 Frontend Dependencies

```json
{
  "dependencies": {
    "next": "16.1.1",
    "react": "19.2.3",
    "react-dom": "19.2.3"
  },
  "devDependencies": {
    "@tailwindcss/postcss": "^4",
    "@types/node": "^20",
    "@types/react": "^19",
    "@types/react-dom": "^19",
    "tailwindcss": "^4",
    "typescript": "^5"
  }
}
```

### 2.5 Análisis de Dependencias

**Fortalezas:**
✅ Todas las dependencias en versiones modernas y stabiliadas  
✅ Uso de Argon2 (más seguro que bcrypt)  
✅ BullMQ para trabajos en background  
✅ Prisma para type-safe database queries  
✅ Validación con class-validator + class-transformer  

**Problemas:**
⚠️ Falta: `helmet` para headers de seguridad HTTP  
⚠️ Falta: `compression` para compresión de responses  
⚠️ Falta: `joi` o `zod` para validación en variables de entorno  
⚠️ Falta: `rate-limiter-flexible` o `express-rate-limit`  
⚠️ Falta: `morgan` para logging de HTTP requests  

---

## 3. CONFIGURACIÓN

### 3.1 Variables de Entorno (.env.example)

```env
# Database
DATABASE_URL="postgresql://user:password@localhost:5432/api_urpe?schema=public"

# Redis (para BullMQ)
REDIS_HOST=localhost
REDIS_PORT=6379
REDIS_PASSWORD=

# JWT
JWT_SECRET=your-super-secret-jwt-key-change-this-in-production
JWT_EXPIRES_IN=7d

# SMTP Configuration
SMTP_HOST=smtp.gmail.com
SMTP_PORT=587
SMTP_SECURE=false
SMTP_USER=tu-email@empresa.com
SMTP_PASSWORD=tu-password-smtp

# Email Defaults
SMTP_FROM_EMAIL=noreply@empresa.com
SMTP_FROM_NAME="API Platform"

# Email Campaign Settings
EMAIL_BATCH_SIZE=100
EMAIL_DELAY_BETWEEN_BATCHES=1000

# Server
PORT=3000
```

### 3.2 Config Modules

#### auth.config.ts
```typescript
export const authConfig = () => ({
  jwtSecret: process.env.JWT_SECRET || 'default-secret',
  jwtExpiresIn: process.env.JWT_EXPIRES_IN || '1d',
});
```

#### database.config.ts
```typescript
export const databaseConfig = () => ({
  url: process.env.DATABASE_URL,
});
```

#### redis.config.ts
```typescript
export const redisConfig = () => ({
  host: process.env.REDIS_HOST || 'localhost',
  port: parseInt(process.env.REDIS_PORT || '6379', 10),
  password: process.env.REDIS_PASSWORD,
});
```

#### email.config.ts
```typescript
export default registerAs('email', () => ({
  smtp: {
    host: process.env.SMTP_HOST || 'localhost',
    port: parseInt(process.env.SMTP_PORT || '587', 10),
    secure: process.env.SMTP_SECURE === 'true',
    auth: {
      user: process.env.SMTP_USER,
      pass: process.env.SMTP_PASSWORD,
    },
  },
  from: {
    email: process.env.SMTP_FROM_EMAIL || 'noreply@example.com',
    name: process.env.SMTP_FROM_NAME || 'API Platform',
  },
  batchSize: parseInt(process.env.EMAIL_BATCH_SIZE || '100', 10),
  delayBetweenBatches: parseInt(process.env.EMAIL_DELAY_BETWEEN_BATCHES || '1000', 10),
}));
```

### 3.3 App Module Configuration

```typescript
@Module({
  imports: [
    ConfigModule.forRoot({
      isGlobal: true,
      envFilePath: '.env',
      load: [authConfig, databaseConfig, redisConfig, emailConfig],
    }),
    BullModule.forRoot({
      connection: {
        host: process.env.REDIS_HOST || 'localhost',
        port: parseInt(process.env.REDIS_PORT || '6379', 10),
        password: process.env.REDIS_PASSWORD,
      },
    }),
    PrismaModule,
    HealthModule,
    AuthModule,
    UsersModule,
    ApiEndpointsModule,
    ProxyModule,
    EmailCampaignsModule,
  ],
})
```

### 3.4 Bootstrap Configuration (main.ts)

```typescript
async function bootstrap() {
  const app = await NestFactory.create(AppModule);
  
  // CORS
  app.enableCors({
    origin: ['http://localhost:3000', 'http://localhost:5173', 'https://urpeailab.com'],
    credentials: true,
  });

  // Global validation
  app.useGlobalPipes(
    new ValidationPipe({
      whitelist: true,
      forbidNonWhitelisted: true,
      transform: true,
    }),
  );
  
  app.setGlobalPrefix(process.env.API_PREFIX || 'api/v1');
  
  const port = process.env.PORT || 3000;
  await app.listen(port);
  console.log(`🚀 API running on: http://localhost:${port}`);
}
```

---

## 4. MÓDULOS EXISTENTES

### 4.1 Auth Module

**Responsabilidades:**
- Registro de usuarios
- Login con JWT
- Validación de tokens
- Estrategia Passport-JWT

**Archivos:**
- `auth.controller.ts` - Endpoints: POST /register, POST /login, GET /profile
- `auth.service.ts` - Lógica de autenticación
- `auth.module.ts` - Configuración del módulo
- `strategies/jwt.strategy.ts` - Estrategia JWT personalizada

**Endpoints Clave:**
```
POST   /api/v1/auth/register      - Registrar nuevo usuario
POST   /api/v1/auth/login         - Login (devuelve JWT)
GET    /api/v1/auth/profile       - Perfil actual (requiere JWT)
```

**Características:**
✅ Uso de Argon2 para hashing (memoryCost: 19456, timeCost: 2)  
✅ JWT tokens con expiración configurable  
✅ Validación de usuario activo  
✅ Manejo de errores (ConflictException, UnauthorizedException)

### 4.2 Users Module

**Responsabilidades:**
- CRUD de usuarios
- Gestión de roles (ADMIN/USER)
- Control de acceso basado en roles
- Estadísticas por usuario

**Endpoints Clave:**
```
GET    /api/v1/users              - Listar usuarios (ADMIN only)
POST   /api/v1/users              - Crear usuario (ADMIN only)
GET    /api/v1/users/:id          - Ver usuario (ADMIN only)
PUT    /api/v1/users/:id          - Actualizar usuario (ADMIN only)
DELETE /api/v1/users/:id          - Eliminar usuario (ADMIN only)
GET    /api/v1/users/:id/stats    - Estadísticas (ADMIN only)
GET    /api/v1/users/me           - Perfil propio
PUT    /api/v1/users/me           - Actualizar perfil propio
```

**Guards:**
- `JwtAuthGuard` - Requiere autenticación
- `RolesGuard` - Valida roles específicos

### 4.3 API Endpoints Module

**Responsabilidades:**
- Crear endpoints de proxy dinámicos
- Gestión de slugs únicos
- Generación automática de API keys
- Transformación de requests/responses
- Rate limiting
- Estadísticas por endpoint

**Endpoints Clave:**
```
GET    /api/v1/api-endpoints           - Listar endpoints del usuario
POST   /api/v1/api-endpoints           - Crear nuevo endpoint
GET    /api/v1/api-endpoints/:id       - Ver detalles
PUT    /api/v1/api-endpoints/:id       - Actualizar
DELETE /api/v1/api-endpoints/:id       - Eliminar
GET    /api/v1/api-endpoints/:id/stats - Estadísticas (24h, 7d)
```

**Características Clave:**
✅ Generación automática de slugs (ej: "my-api-abc123")  
✅ API keys únicas por endpoint (formato: sk_xxxxx)  
✅ URL proxy automática: `https://api.urpeailab.com/api/v1/proxy/{slug}`  
✅ Rate limiting por endpoint (configurable, default: 100 req/min)  
✅ Headers personalizados  
✅ Transformaciones de request/response (JSON path simple)  
✅ Estadísticas: total requests, últimas 24h, últimos 7 días, avg response time

**Algoritmo de Slug:**
```typescript
const nanoid = customAlphabet('0123456789abcdefghijklmnopqrstuvwxyz', 12);
const slug = dto.slug || `${dto.name.toLowerCase().replace(/\s+/g, '-')}-${nanoid(6)}`;
```

### 4.4 Proxy Module

**Responsabilidades:**
- Ruteo dinámico de requests
- Validación de API keys
- Rate limiting en tiempo real
- Transformación de datos
- Logging de todas las peticiones
- Manejo de errores

**Endpoints Clave:**
```
*      /api/v1/proxy/:slug/*       - Proxy dinámico (GET, POST, PUT, DELETE, PATCH)
*      /api/v1/proxy/:slug         - Proxy dinámico (sin path adicional)
```

**Flujo de una Request:**
1. Cliente → `GET /proxy/my-api-abc123?x=1` con header `x-api-key: sk_xxxxx`
2. Validación: ¿Endpoint existe?
3. Validación: ¿API key válida?
4. Validación: ¿Rate limit?
5. Transformación: Request → según config
6. HTTP: axios → targetUrl
7. Transformación: Response ← según config
8. Logging: Registrar en DB
9. Response: Devolver al cliente

**Características:**
✅ Soporta todos los métodos HTTP (GET, POST, PUT, DELETE, PATCH)  
✅ Preserva headers originales  
✅ Agrega `User-Agent: URPE-API-Gateway/1.0`  
✅ Manejo especial para Supabase (agrega apikey header)  
✅ Timeout: 30 segundos  
✅ Logging completo de requests/responses  
✅ Manejo de errores con status codes HTTP  

### 4.5 Email Campaigns Module

**Responsabilidades:**
- Crear campañas de email
- Gestión de destinatarios
- Envío masivo con BullMQ
- Procesamiento en batches
- Monitoreo de estado

**Endpoints Clave:**
```
GET    /api/v1/email-campaigns              - Listar campañas
POST   /api/v1/email-campaigns              - Crear campaña
GET    /api/v1/email-campaigns/:id          - Ver detalles
PUT    /api/v1/email-campaigns/:id          - Actualizar
DELETE /api/v1/email-campaigns/:id          - Eliminar
POST   /api/v1/email-campaigns/:id/send     - Enviar (cola BullMQ)
GET    /api/v1/email-campaigns/:id/status   - Estado & progreso
POST   /api/v1/email-campaigns/:id/cancel   - Cancelar envío
```

**Estados de Campaña:**
- `DRAFT` - Borrador (puede editarse)
- `QUEUED` - En cola de envío
- `SENDING` - Enviándose actualmente
- `SENT` - Completada exitosamente
- `FAILED` - Error en envío
- `CANCELLED` - Cancelada por usuario

**Características:**
✅ Envío masivo asincrónico con BullMQ  
✅ Procesamiento por batches (configurable)  
✅ Delay entre batches (configurable)  
✅ Reintentos automáticos (hasta 3 veces)  
✅ Backoff exponencial  
✅ Contador de enviados/fallidos  
✅ Monitoreo de progreso en tiempo real  
✅ Validación: no enviar campaña duplicada

### 4.6 Health Module

**Responsabilidades:**
- Health check del servidor

**Endpoints Clave:**
```
GET    /api/v1/health    - { status: 'ok' }
```

---

## 5. DTOs Y VALIDACIÓN

### 5.1 Auth DTOs

```typescript
// Register
export class RegisterDto {
  @IsEmail()
  email: string;

  @IsString()
  @MinLength(6)
  password: string;

  @IsString()
  @IsOptional()
  name?: string;

  @IsEnum(['ADMIN', 'USER'])
  @IsOptional()
  role?: 'ADMIN' | 'USER';
}

// Login
export class LoginDto {
  @IsEmail()
  email: string;

  @IsString()
  password: string;
}
```

### 5.2 API Endpoints DTOs

```typescript
export class CreateApiEndpointDto {
  @IsString()
  @IsNotEmpty()
  name: string;                    // Ej: "Mi API de n8n"

  @IsString()
  @IsOptional()
  slug?: string;                   // Ej: "mi-api-abc123" (auto-generado si no especifica)

  @IsString()
  @IsOptional()
  description?: string;            // Descripción opcional

  @IsEnum(['GET', 'POST', 'PUT', 'DELETE', 'PATCH'])
  @IsOptional()
  method?: string;                 // Method HTTP (default: POST)

  @IsUrl()
  @IsNotEmpty()
  targetUrl: string;               // URL destino (n8n, Supabase, etc)

  @IsOptional()
  requestTransform?: any;          // Transformación entrada

  @IsOptional()
  responseTransform?: any;         // Transformación salida

  @IsOptional()
  headers?: any;                   // Headers personalizados

  @IsBoolean()
  @IsOptional()
  requireApiKey?: boolean;         // Requerir API key (default: true)

  @IsOptional()
  allowedOrigins?: any;            // CORS whitelist

  @IsInt()
  @IsOptional()
  rateLimit?: number;              // Limit requests/min (default: 100)

  @IsString()
  @IsOptional()
  connectionId?: string;           // ID de conexión preconfigurada
}

export class UpdateApiEndpointDto {
  @IsString()
  @IsOptional()
  name?: string;

  @IsString()
  @IsOptional()
  description?: string;

  @IsEnum(['ACTIVE', 'INACTIVE', 'SUSPENDED'])
  @IsOptional()
  status?: 'ACTIVE' | 'INACTIVE' | 'SUSPENDED';

  @IsUrl()
  @IsOptional()
  targetUrl?: string;

  @IsOptional()
  requestTransform?: any;

  @IsOptional()
  responseTransform?: any;

  @IsOptional()
  headers?: any;

  @IsInt()
  @IsOptional()
  rateLimit?: number;
}
```

### 5.3 Email Campaign DTOs

```typescript
export class CreateEmailCampaignDto {
  @IsString()
  @IsNotEmpty()
  name: string;                    // Ej: "Campaña Enero 2025"

  @IsString()
  @IsNotEmpty()
  subject: string;                 // Asunto del email

  @IsString()
  @IsNotEmpty()
  body: string;                    // Contenido HTML

  @IsEmail()
  @IsNotEmpty()
  fromEmail: string;               // Email remitente

  @IsString()
  @IsOptional()
  fromName?: string;               // Nombre remitente

  @IsArray()
  @IsNotEmpty()
  recipients: string[];            // Array de emails destinatarios

  @IsDateString()
  @IsOptional()
  scheduledAt?: string;            // Programado para enviar
}

export class SendCampaignDto {
  @IsNumber()
  @IsOptional()
  batchSize?: number;              // Tamaño de lote (default: 100)

  @IsNumber()
  @IsOptional()
  delayBetweenBatches?: number;    // Delay en ms (default: 1000)
}
```

### 5.4 User DTOs

```typescript
export class CreateUserDto {
  @IsEmail()
  email: string;

  @IsString()
  @MinLength(6)
  password: string;

  @IsString()
  @IsOptional()
  name?: string;

  @IsEnum(['ADMIN', 'USER'])
  @IsOptional()
  role?: 'ADMIN' | 'USER';
}

export class UpdateUserDto {
  @IsString()
  @IsOptional()
  name?: string;

  @IsString()
  @MinLength(6)
  @IsOptional()
  password?: string;

  @IsBoolean()
  @IsOptional()
  isActive?: boolean;

  @IsEnum(['ADMIN', 'USER'])
  @IsOptional()
  role?: 'ADMIN' | 'USER';
}
```

### 5.5 Validación Global

Se implementa en `main.ts`:
```typescript
app.useGlobalPipes(
  new ValidationPipe({
    whitelist: true,              // Elimina propiedades no definidas
    forbidNonWhitelisted: true,   // Rechaza si hay props extra
    transform: true,              // Transforma a DTO
  }),
);
```

**Fortalezas:**
✅ Uso de `class-validator` + `class-transformer`  
✅ Validación automática en todos los endpoints  
✅ Tipos TypeScript strict  

---

## 6. SEGURIDAD

### 6.1 Autenticación JWT

**Implementación:**
```typescript
// JWT Strategy
@Injectable()
export class JwtStrategy extends PassportStrategy(Strategy) {
  constructor(
    private configService: ConfigService,
    private authService: AuthService,
  ) {
    super({
      jwtFromRequest: ExtractJwt.fromAuthHeaderAsBearerToken(),
      ignoreExpiration: false,
      secretOrKey: configService.get('JWT_SECRET'),
    });
  }

  async validate(payload: any) {
    const user = await this.authService.validateUser(payload.sub);
    if (!user || !user.isActive) {
      throw new UnauthorizedException();
    }
    return user;
  }
}
```

**Configuración:**
- Secret: `process.env.JWT_SECRET`
- Expiración: `process.env.JWT_EXPIRES_IN` (default: 7d)
- Payload: `{ sub: userId, email, role }`
- Verificación: Token en header `Authorization: Bearer <token>`

**Fortalezas:**
✅ Extracción automática desde Bearer token  
✅ Validación de expiración automática  
✅ Validación de usuario activo en cada request  
✅ Payload contiene rol (para RBAC)

### 6.2 Hashing de Contraseñas

**Implementación:**
```typescript
const hashedPassword = await hash(dto.password, {
  memoryCost: 19456,    // 19 MB
  timeCost: 2,          // iterations
  outputLen: 32,        // bytes
  parallelism: 1,
});

const isValid = await verify(user.password, dto.password);
```

**Tecnología:** `@node-rs/argon2` (ganador Password Hashing Competition)

**Configuración:**
- memoryCost: 19456 (19 MB) - Robusto contra ataques GPU
- timeCost: 2 - Compilaciones
- outputLen: 32 bytes
- parallelism: 1

**Fortalezas:**
✅ Argon2 es más seguro que bcrypt  
✅ Configuración moderna recomendada por OWASP  
✅ Resistencia a ataques GPU/ASIC

### 6.3 API Key Validation

**Generación:**
```typescript
const apiKey = await this.prisma.apiKey.create({
  data: {
    key: `sk_${nanoid(32)}`,      // Formato: sk_xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
    name: `${dto.name} - Default Key`,
    userId,
    endpointId: endpoint.id,
  },
});
```

**Validación (en Proxy):**
```typescript
if (endpoint.requireApiKey) {
  if (!apiKey) {
    throw new UnauthorizedException('API Key required');
  }

  validApiKey = await this.prisma.apiKey.findFirst({
    where: {
      key: apiKey,
      isActive: true,
      OR: [
        { endpointId: endpoint.id },
        { endpointId: null },  // Keys globales
      ],
    },
  });

  if (!validApiKey) {
    throw new UnauthorizedException('Invalid API Key');
  }

  // Actualizar lastUsedAt
  await this.prisma.apiKey.update({
    where: { id: validApiKey.id },
    data: { lastUsedAt: new Date() },
  });
}
```

**Características:**
✅ API keys únicas por endpoint (o globales)  
✅ Formato prefijado: `sk_`  
✅ Tracking de último uso  
✅ Soporte para expiración (campo en DB)  
✅ Activación/desactivación

### 6.4 Role-Based Access Control (RBAC)

**Roles:**
- `ADMIN` - Acceso total, puede gestionar usuarios
- `USER` - Acceso limitado, solo su contenido

**Decorador Custom:**
```typescript
@Roles('ADMIN')
```

**Guard Custom:**
```typescript
@Injectable()
export class RolesGuard implements CanActivate {
  constructor(private reflector: Reflector) {}

  canActivate(context: ExecutionContext): boolean {
    const requiredRoles = this.reflector.get<string[]>('roles', context.getHandler());
    
    if (!requiredRoles) {
      return true;  // Sin restricción
    }

    const request = context.switchToHttp().getRequest();
    const user = request.user;

    return requiredRoles.includes(user?.role);
  }
}
```

**Aplicación:**
```typescript
@Controller('users')
@UseGuards(JwtAuthGuard, RolesGuard)
export class UsersController {
  @Get()
  @Roles('ADMIN')
  findAll() { /* ... */ }
}
```

**Características:**
✅ Separación clara entre ADMIN y USER  
✅ Guards aplicados globalmente en controllers  
✅ Validación por endpoint  

### 6.5 Rate Limiting

**Implementación:**
```typescript
private async checkRateLimit(endpointId: string, limit: number) {
  const oneMinuteAgo = new Date(Date.now() - 60000);
  
  const count = await this.prisma.request.count({
    where: {
      endpointId,
      createdAt: { gte: oneMinuteAgo },
    },
  });

  if (count >= limit) {
    throw new HttpException('Rate limit exceeded', 429);
  }
}
```

**Configuración:**
- Rate limit por endpoint (default: 100 requests/min)
- Ventana: 1 minuto deslizante
- Status code: 429 Too Many Requests
- Almacenamiento: Directamente en DB

**Problemas:**
⚠️ Consulta a DB en cada request (rendimiento)  
⚠️ No distribuido en múltiples instancias  

### 6.6 CORS Configuration

```typescript
app.enableCors({
  origin: [
    'http://localhost:3000',
    'http://localhost:5173',
    'https://urpeailab.com'
  ],
  credentials: true,
});
```

**Problemas:**
⚠️ Hardcoded en código, debería venir de ENV  
⚠️ No hay soporte para dominios dinámicos

### 6.7 Guards & Decorators

**JWT Auth Guard:**
```typescript
@Injectable()
export class JwtAuthGuard extends AuthGuard('jwt') {}
```

**Current User Decorator:**
```typescript
export const CurrentUser = createParamDecorator(
  (data: unknown, ctx: ExecutionContext) => {
    const request = ctx.switchToHttp().getRequest();
    return request.user;
  },
);
```

**Uso:**
```typescript
@Get('me')
@UseGuards(JwtAuthGuard)
getProfile(@CurrentUser() user: any) {
  return user;
}
```

### 6.8 Seguridad: Estado Actual

**✅ Implementado:**
- Autenticación JWT con validación en cada request
- Hashing robusto con Argon2
- API keys personalizadas por endpoint
- RBAC (ADMIN/USER)
- Rate limiting (por endpoint)
- Validación estricta de DTOs
- Whitelist de CORS
- Gestión de usuarios activos/inactivos

**⚠️ No Implementado:**
- ❌ `helmet` para headers de seguridad HTTP
- ❌ `compression` para compresión de responses
- ❌ HTTPS redirect (dev mode)
- ❌ CSRF protection
- ❌ SQL injection prevention (Prisma lo hace, pero sin validación adicional)
- ❌ XSS protection headers
- ❌ Rate limiting distribuido (Redis)
- ❌ Autenticación de dos factores (2FA)
- ❌ Logging de intentos fallidos
- ❌ Passwordless authentication
- ❌ IP Whitelisting

---

## 7. DATABASE (PRISMA SCHEMA)

### 7.1 Modelos Principales

#### User
```prisma
model User {
  id        String   @id @default(cuid())
  email     String   @unique
  name      String?
  password  String
  role      UserRole @default(USER)  // ADMIN | USER
  isActive  Boolean  @default(true)
  createdAt DateTime @default(now())
  updatedAt DateTime @updatedAt

  apis      ApiEndpoint[]
  apiKeys   ApiKey[]
  emails    EmailCampaign[]
  
  @@map("users")
}

enum UserRole {
  ADMIN
  USER
}
```

#### ApiEndpoint
```prisma
model ApiEndpoint {
  id          String    @id @default(cuid())
  name        String
  slug        String    @unique
  description String?
  status      ApiStatus @default(ACTIVE)  // ACTIVE | INACTIVE | SUSPENDED
  
  // Configuración del endpoint
  method      String    @default("POST")
  targetUrl   String
  
  // Transformación
  requestTransform  Json?
  responseTransform Json?
  headers           Json?
  
  // Seguridad
  requireApiKey     Boolean @default(true)
  allowedOrigins    Json?
  rateLimit         Int     @default(100)
  
  // Relaciones
  connectionId      String?
  connection        Connection? @relation(fields: [connectionId], references: [id])
  userId            String
  user              User      @relation(fields: [userId], references: [id], onDelete: Cascade)
  
  // Metadata
  createdAt         DateTime  @default(now())
  updatedAt         DateTime  @updatedAt
  
  apiKeys           ApiKey[]
  requests          Request[]
  
  @@map("api_endpoints")
}

enum ApiStatus {
  ACTIVE
  INACTIVE
  SUSPENDED
}
```

#### ApiKey
```prisma
model ApiKey {
  id          String   @id @default(cuid())
  key         String   @unique
  name        String
  isActive    Boolean  @default(true)
  
  endpointId  String?
  endpoint    ApiEndpoint? @relation(fields: [endpointId], references: [id], onDelete: Cascade)
  
  userId      String
  user        User     @relation(fields: [userId], references: [id], onDelete: Cascade)
  
  lastUsedAt  DateTime?
  expiresAt   DateTime?
  createdAt   DateTime @default(now())
  
  requests    Request[]
  
  @@map("api_keys")
}
```

#### Connection
```prisma
model Connection {
  id          String         @id @default(cuid())
  name        String
  type        ConnectionType
  config      Json           // { apiUrl, apiKey, etc }
  
  userId      String
  isActive    Boolean        @default(true)
  
  createdAt   DateTime       @default(now())
  updatedAt   DateTime       @updatedAt
  
  endpoints   ApiEndpoint[]
  
  @@map("connections")
}

enum ConnectionType {
  SUPABASE
  N8N
  WEBHOOK
  REST_API
  SMTP
  CUSTOM
}
```

#### Request
```prisma
model Request {
  id          String   @id @default(cuid())
  
  endpointId  String
  endpoint    ApiEndpoint @relation(fields: [endpointId], references: [id], onDelete: Cascade)
  
  apiKeyId    String?
  apiKey      ApiKey?  @relation(fields: [apiKeyId], references: [id])
  
  method      String
  path        String
  headers     Json?
  body        Json?
  query       Json?
  
  statusCode  Int?
  responseTime Int?
  responseBody Json?
  
  ipAddress   String?
  userAgent   String?
  
  createdAt   DateTime @default(now())
  
  @@index([endpointId, createdAt])
  @@index([apiKeyId])
  @@map("requests")
}
```

#### EmailCampaign
```prisma
model EmailCampaign {
  id          String   @id @default(cuid())
  name        String
  subject     String
  body        String   @db.Text
  
  fromEmail   String
  fromName    String?
  
  status      String   @default("DRAFT")  // DRAFT|QUEUED|SENDING|SENT|FAILED|CANCELLED
  
  recipients  Json     // Array de emails
  sentCount   Int      @default(0)
  failedCount Int      @default(0)
  
  scheduledAt DateTime?
  sentAt      DateTime?
  
  userId      String
  user        User     @relation(fields: [userId], references: [id], onDelete: Cascade)
  
  createdAt   DateTime @default(now())
  updatedAt   DateTime @updatedAt
  
  @@map("email_campaigns")
}
```

### 7.2 Relaciones & Cascadas

| Relación | Comportamiento |
|----------|----------------|
| User → ApiEndpoint | onDelete: Cascade |
| User → ApiKey | onDelete: Cascade |
| User → EmailCampaign | onDelete: Cascade |
| ApiEndpoint → Request | onDelete: Cascade |
| ApiEndpoint → ApiKey | onDelete: Cascade |
| Connection → ApiEndpoint | No cascade |

### 7.3 Índices

```prisma
@@index([endpointId, createdAt])  // Para queries de stats
@@index([apiKeyId])               // Para validación de keys
```

### 7.4 Características de Prisma

✅ Type-safe queries  
✅ Generación automática de client  
✅ Migraciones versionadas  
✅ Studio para visualización  
✅ Soporte para PostgreSQL 16  

---

## 8. DOCUMENTACIÓN

### 8.1 README.md

**Contenido:**
- ✅ Feature overview (autenticación, proxy, campaigns, etc)
- ✅ Stack tecnológico completo
- ✅ Instalación paso a paso
- ✅ Variables de entorno
- ✅ Guía de uso con ejemplos
- ✅ Casos de uso reales (n8n, Supabase, transformaciones)
- ✅ Arquitectura del sistema con diagrama ASCII
- ✅ Endpoints del backend listados
- ✅ Troubleshooting
- ✅ Roadmap de features

**Longitud:** ~500 líneas, muy comprehensive

### 8.2 docs/EMAIL_CAMPAIGNS.md

**Documentación específica de campañas de email con:**
- Flujo de envío
- Configuración SMTP
- Ejemplos de uso
- Monitoreo de progreso

### 8.3 docs/QUICK_START_EMAIL.md

**Guía rápida para empezar con emails**

### 8.4 scripts/test-email-campaign.js

**Script de prueba completo que:**
- Autentica usuario
- Crea campaña
- Añade destinatarios
- Envía campaña
- Monitorea progreso

### 8.5 Estado de Documentación

**✅ Bueno:**
- README muy completo
- Diagrama de arquitectura
- Casos de uso claros
- Guías de instalación

**⚠️ Mejorable:**
- Falta documentación de API (OpenAPI/Swagger)
- Falta guía de desarrollo internal
- Falta diagrama ER de base de datos
- Falta documentación técnica de módulos
- Falta security best practices doc

---

## 9. SCRIPTS DE BUILD/DEPLOY

### 9.1 NPM Scripts (package.json)

```json
{
  "build": "nest build",
  "build:api": "nest build api",
  "build:worker": "nest build worker",
  "start": "nest start",
  "start:dev": "nest start --watch",
  "start:api": "nest start api --watch",
  "start:worker": "nest start worker --watch",
  "start:debug": "nest start --debug --watch",
  "start:prod": "node dist/apps/api/main",
  "prisma:generate": "prisma generate",
  "prisma:migrate": "prisma migrate dev",
  "prisma:studio": "prisma studio"
}
```

### 9.2 Docker Setup

#### docker-compose.yml

**Servicios:**
- `postgres:16-alpine` - Base de datos
- `redis:7-alpine` - Cache y queue
- `api` - Backend NestJS
- `worker` - Background jobs
- `web` - Frontend Next.js

**Volúmenes:**
- `postgres_data` - Persistencia DB
- `redis_data` - Persistencia Redis

**Redes:**
- `default` - Comunicación interna

#### api.Dockerfile

```dockerfile
FROM node:20-alpine AS base
WORKDIR /app
COPY package*.json ./
RUN npm ci --only=production

FROM base AS build
RUN npm ci
COPY . .
RUN npm run build:api
RUN npx prisma generate

FROM node:20-alpine AS production
WORKDIR /app
COPY --from=base /app/node_modules ./node_modules
COPY --from=build /app/dist ./dist
COPY --from=build /app/package*.json ./
COPY --from=build /app/prisma ./prisma

ENV NODE_ENV=production
EXPOSE 3000

CMD ["node", "dist/apps/api/main"]
```

**Características:**
✅ Multi-stage build (optimización de size)  
✅ Usa alpine (imagen pequeña)  
✅ Instala en etapa correcta  
✅ Copia prisma schema  

#### worker.Dockerfile

Similar a api.Dockerfile

### 9.3 Configuración NestJS (nest-cli.json)

```json
{
  "$schema": "https://json.schemastore.org/nest-cli",
  "collection": "@nestjs/schematics",
  "sourceRoot": "apps/api/src",
  "compilerOptions": {
    "deleteOutDir": true,
    "webpack": false,
    "tsConfigPath": "apps/api/tsconfig.app.json"
  },
  "monorepo": true,
  "root": "apps/api",
  "projects": {
    "api": {
      "type": "application",
      "root": "apps/api",
      "entryFile": "main",
      "sourceRoot": "apps/api/src",
      "compilerOptions": {
        "tsConfigPath": "apps/api/tsconfig.app.json"
      }
    },
    "worker": {
      "type": "application",
      "root": "apps/worker",
      "entryFile": "main",
      "sourceRoot": "apps/worker/src",
      "compilerOptions": {
        "tsConfigPath": "apps/worker/tsconfig.app.json"
      }
    }
  }
}
```

### 9.4 Build & Deploy Workflow

**Development:**
```bash
# Terminal 1
cd apps/api && pnpm run start:dev

# Terminal 2
cd apps/web && pnpm run dev

# Terminal 3
cd apps/worker && pnpm run start:dev
```

**Production (Docker):**
```bash
cd docker
docker-compose up -d
```

**Deploy Steps:**
1. `nodejs install -g pnpm` (si es necesario)
2. `pnpm install` (instalar dependencias)
3. `pnpm prisma generate` (generar client)
4. `pnpm prisma migrate deploy` (migraciones)
5. `pnpm build` (compilar)
6. `docker-compose up -d` (levantar servicios)

---

## 10. PROBLEMAS ENCONTRADOS

### 10.1 Críticos 🔴

#### 1. **JWT Secret y URL hardcodeados**
**Ubicación:** `main.ts` (linea con https://urpeailab.com)  
**Problema:** CORS origin hardcodeado en el código  
**Impacto:** No se puede cambiar en diferentes ambientes  
**Solución:** Mover a `.env`

```typescript
// ❌ Actual
app.enableCors({
  origin: ['http://localhost:3000', 'http://localhost:5173', 'https://urpeailab.com'],
  credentials: true,
});

// ✅ Correcto
app.enableCors({
  origin: process.env.CORS_ORIGINS?.split(',') || ['http://localhost:3000'],
  credentials: true,
});
```

#### 2. **Rate Limiting en DB (escalabilidad)**
**Ubicación:** `proxy.service.ts` - `checkRateLimit()`  
**Problema:** Consulta a DB por cada request en el proxy (N+1 queries)  
**Impacto:** Rendimiento degradado con tráfico alto  
**Solución:** Usar Redis con TTL o `express-rate-limit`

#### 3. **Transformaciones de datos débiles**
**Ubicación:** `proxy.service.ts` - `transformData()`  
**Problema:** Solo soporta JSON path simple, no JSONata o JMESPath  
**Impacto:** Transformaciones limitadas  
**Solución:** Implementar JSONata o permitir funciones custom

#### 4. **Error handling incompleto en emailCampaigns**
**Ubicación:** `email-campaigns.service.ts`  
**Problema:** Validación insuficiente de recipients (no valida emails)  
**Impacto:** Envío a emails inválidos  
**Solución:** Validar con regex antes de encolar

#### 5. **Logging insuficiente**
**Ubicación:** Todo el proyecto  
**Problema:** No hay logger centralizado (solo console.log)  
**Impacto:** Debugging difícil en producción  
**Solución:** Usar `winston` o `pino` logger

### 10.2 Altos ⚠️

#### 6. **Variables de entorno sin validación**
**Ubicación:** `config/*.ts`  
**Problema:** No hay validación de variables requeridas al startup  
**Impacto:** Errores tardíos en runtime  
**Solución:** Usar `joi` o `zod` para validar ENV en bootstrap

```typescript
// ✅ Agregar en main.ts
const envSchema = Joi.object({
  DATABASE_URL: Joi.string().required(),
  JWT_SECRET: Joi.string().required(),
  REDIS_HOST: Joi.string().required(),
  PORT: Joi.number().default(3000),
});

const { error, value: envVars } = envSchema.validate(process.env);
if (error) throw new Error(`Env validation error: ${error}`);
```

#### 7. **No hay testes**
**Ubicación:** N/A  
**Problema:** 0 tests unitarios o e2e  
**Impacto:** Regresiones sin detectar  
**Solución:** Implementar tests con `jest` o `vitest`

#### 8. **Passwords en .env visible**
**Ubicación:** `.env`  
**Problema:** Archivo .env con credenciales está en el repo  
**Impacto:** Credenciales expuestas  
**Solución:** `.env` en `.gitignore` (ya está bien), pero mejorar docs

#### 9. **Worker sin implementación visible**
**Ubicación:** `apps/worker/src/`  
**Problema:** No se ve el consumer de BullMQ en el worker  
**Impacto:** Email campaigns podrían no procesarse  
**Solución:** Verificar worker implementation

#### 10. **Transformación de response insegura**
**Ubicación:** `proxy.service.ts`  
**Problema:** `transformData()` podría exponer info sensible  
**Impacto:** Data breach potencial  
**Solución:** Whitelist de campos permitidos

### 10.3 Medios ℹ️

#### 11. **Falta documentación de API (Swagger)**
**Problema:** No hay OpenAPI spec  
**Solución:** Integrar `@nestjs/swagger`

#### 12. **Email Service sin retry logic**
**Ubicación:** `email.service.ts`  
**Problema:** Si falla nodemailer, no hay reintentos  
**Solución:** Implementar retry con backoff exponencial

#### 13. **Falta validación de Email en DTOs**
**Ubicación:** Email campaign DTOs  
**Problema:** No hay regex para validar emails en recipients array  
**Solución:** `@IsEmail({ each: true })`

#### 14. **Comparación de emails case-insensitive**
**Ubicación:** `auth.service.ts` - login  
**Problema:** `findUnique({ email: dto.email })` puede fallar con case diferente  
**Impacto:** Usuarios no pueden loguearse con diferente case  
**Solución:** Convertir email a lowercase en registro y login

#### 15. **Falta endpoint para listar API Keys**
**Ubicación:** `api-endpoints.service.ts`  
**Problema:** No hay forma de listar/rotar keys sine ir a la DB  
**Impacto:** UX pobre  
**Solución:** Agregar endpoints GET/DELETE para keys

### 10.4 Bajos 💡

#### 16. **Slugs truncados**
**Ubicación:** `api-endpoints.service.ts`  
**Problema:** Si el nombre es muy largo, el slug puede ser problemático  
**Solución:** Validar longitud y truncar si es necesario

#### 17. **No hay soft delete**
**Ubicación:** Modelos Prisma  
**Problema:** Eliminar datos es permanente  
**Impacto:** Auditoría difícil  
**Solución:** Agregar campo `deletedAt` para soft delete

#### 18. **API para editar API Keys limitada**
**Problema:** No se puede editar nombre de key sin borrar/crear  
**Solución:** Agregar PATCH endpoint para keys

#### 19. **Metricas dashboard ausentes**
**Solución:** Agregar endpoints para gráficas (requests over time, etc)

#### 20. **Frontend no tiene state management**
**Solución:** Agregar Zustand o Context API mejorado

---

## 11. MEJORAS NECESARIAS

### 11.1 Seguridad (CRÍTICO)

```typescript
// 1. Agregar Helmet
npm install helmet
// En main.ts
import helmet from 'helmet';
app.use(helmet());

// 2. Agregar Rate Limiter Global
npm install @nestjs/rate-limit
import { RateLimitGuard } from '@nestjs/rate-limit';
app.useGlobalGuards(new RateLimitGuard());

// 3. Agregar Compression
npm install compression
import compression from 'compression';
app.use(compression());

// 4. Validar ENV en bootstrap
npm install joi
const envSchema = Joi.object({
  DATABASE_URL: Joi.string().required(),
  JWT_SECRET: Joi.string().length(32).required(),
  // ...
});

// 5. Convertir emails a lowercase
// auth.service.ts
async register(dto: RegisterDto) {
  const email = dto.email.toLowerCase(); // ← AGREGAR
  const exists = await this.prisma.user.findUnique({
    where: { email },
  });
  // ...
}
```

### 11.2 Logging & Monitoring

```typescript
// Agregar Winston Logger
npm install nest-winston winston

// Reemplazar console.log con logger
import { Logger } from '@nestjs/common';
private readonly logger = new Logger(ClassName.name);

// En main.ts
import { WinstonModule } from 'nest-winston';
const instance = WinstonModule.createLogger({
  transports: [
    new winston.transports.Console({ format: logFormat }),
    new winston.transports.File({ filename: 'logs/error.log', level: 'error' }),
    new winston.transports.File({ filename: 'logs/combined.log' }),
  ],
});
app.useLogger(instance);
```

### 11.3 Testing

```typescript
// Agregar tests unitarios
npm install -D jest @types/jest ts-jest

// Agregar tests e2e
npm install -D @nestjs/testing

// Ejemplo test para auth.service.ts
describe('AuthService', () => {
  let service: AuthService;

  beforeEach(async () => {
    const module: TestingModule = await Test.createTestingModule({
      providers: [AuthService, PrismaService],
    }).compile();

    service = module.get<AuthService>(AuthService);
  });

  it('should hash password with argon2', async () => {
    const dto = { email: 'test@example.com', password: 'Test123!' };
    const result = await service.register(dto);
    expect(result.user.email).toBe(dto.email);
  });
});
```

### 11.4 API Documentation

```typescript
// Agregar Swagger
npm install @nestjs/swagger swagger-ui-express

// En main.ts
import { SwaggerModule, DocumentBuilder } from '@nestjs/swagger';

const config = new DocumentBuilder()
  .setTitle('URPE API')
  .setDescription('The URPE API Platform')
  .setVersion('1.0')
  .addBearerAuth()
  .build();

const document = SwaggerModule.createDocument(app, config);
SwaggerModule.setup('api/docs', app, document);

// En controllers
@ApiOperation({ summary: 'Login user' })
@ApiResponse({ status: 200, description: 'JWT token' })
@Post('login')
login(@Body() dto: LoginDto) { }
```

### 11.5 Database Improvements

```prisma
// Agregar soft delete
model User {
  id        String   @id @default(cuid())
  email     String   @unique
  // ... otros campos
  deletedAt DateTime?  // ← AGREGAR
  
  @@index([deletedAt])  // ← AGREGAR ÍNDICE
}

// Agregar auditoría
model AuditLog {
  id        String   @id @default(cuid())
  userId    String
  action    String
  resource  String
  oldValue  Json?
  newValue  Json?
  createdAt DateTime @default(now())
  
  @@index([userId, createdAt])
}
```

### 11.6 Email Service Improvements

```typescript
// Agregar validación de emails
import isEmail from 'isemail';

async addRecipients(emails: string[]) {
  const validEmails = emails.filter(e => isEmail.validate(e));
  if (validEmails.length !== emails.length) {
    throw new BadRequestException('Invalid email addresses');
  }
  // ...
}

// Agregar retry logic con exponential backoff
async sendEmail(options: EmailOptions, attempt = 1): Promise<boolean> {
  try {
    await this.transporter.sendMail({...});
    return true;
  } catch (error) {
    if (attempt < 3) {
      const delay = Math.pow(2, attempt) * 1000;
      await new Promise(r => setTimeout(r, delay));
      return this.sendEmail(options, attempt + 1);
    }
    return false;
  }
}
```

### 11.7 Proxy Service Improvements

```typescript
// Mejor transformación con JSONata
npm install jsonata

private transformData(data: any, transform: any): any {
  if (typeof transform === 'string') {
    try {
      return jsonata(transform).evaluate(data);
    } catch (error) {
      this.logger.error('Transform failed', error);
      return data;
    }
  }
  return data;
}

// Rate limiter con Redis
async checkRateLimit(endpointId: string, limit: number) {
  const key = `rate-limit:${endpointId}:${new Date().getMinutes()}`;
  const current = await this.redis.incr(key);
  if (current === 1) {
    await this.redis.expire(key, 60);
  }
  if (current > limit) {
    throw new HttpException('Rate limit exceeded', 429);
  }
}
```

### 11.8 Frontend Improvements

```typescript
// Agregar Zustand para state management
npm install zustand

// store/auth.ts
import create from 'zustand';

export const useAuthStore = create((set) => ({
  user: null,
  token: null,
  login: (user, token) => set({ user, token }),
  logout: () => set({ user: null, token: null }),
}));

// Agregar SWR para data fetching
npm install swr

// Agregar Dark Mode
npm install next-themes
```

---

## 12. RECOMENDACIONES CRÍTICAS

### 12.1 Seguridad Inmediata (Antes de Producción)

**P0 - CRÍTICO:**
1. ✅ Mover CORS origins a `.env`
2. ✅ Validar JWT_SECRET (mínimo 32 chars)
3. ✅ Implementar rate limiting global (no sólo en proxy)
4. ✅ Agregar Helmet para security headers
5. ✅ Validar email case-insensitive en auth
6. ✅ Implementar logging centralizado
7. ✅ Validar ENV variables en bootstrap

**P1 - IMPORTANTE:**
8. ✅ Agregar tests unitarios core (auth, proxy)
9. ✅ Implementar OpenAPI/Swagger docs
10. ✅ Agregar compression de responses
11. ✅ Mejorar error handling y no exponer stack traces

### 12.2 Performance

**Optimizaciones Recomendadas:**
1. **Rate Limiting:** Mover de DB a Redis
2. **Caching:** Agregar Redis para:
   - API endpoint metadata
   - User roles/permissions
   - Email SMTP connection
3. **Database:** 
   - Agregar más índices
   - Implementar query caching
   - Considerar read replicas

4. **API Response Caching:**
```typescript
npm install cache-manager

@Get('api-endpoints')
@UseInterceptors(CacheInterceptor)
findAll() { }
```

### 12.3 Escalabilidad

**Para múltiples instancias:**
1. Usar Redis para rate limiting (distribuido)
2. Usar Redis para session storage (si se agrega)
3. Usar Redis para caching
4. Agregar health checks en todos los servicios
5. Agregar graceful shutdown

```typescript
async function bootstrap() {
  // ... app setup

  // Graceful shutdown
  process.on('SIGTERM', async () => {
    console.log('SIGTERM received, shutting down gracefully');
    await app.close();
    process.exit(0);
  });
}
```

### 12.4 Operaciones

**CI/CD Pipeline Recomendado:**
1. Linting: ESLint + Prettier
2. Type checking: TypeScript strict
3. Tests: Jest (unitarios + e2e)
4. Build: Multi-stage Docker
5. Deploy: Docker Compose o Kubernetes

### 12.5 Monitoreo

**Agregar:**
```typescript
npm install @nestjs/terminus prom-client

// Health checks
@Get('health/db')
@HealthCheck()
healthDb() {
  return this.health.check([
    () => this.prisma.$queryRaw`SELECT 1`,
  ]);
}

// Métricas Prometheus
npm install prom-client
export const httpRequestDuration = new Histogram({
  name: 'http_request_duration_seconds',
  help: 'Duration of HTTP requests in seconds',
  labelNames: ['method', 'route', 'status_code'],
});
```

### 12.6 Roadmap Técnico (6 meses)

| Timeframe | Feature | Priority |
|-----------|---------|----------|
| Semana 1-2 | Security fixes (Helmet, rate limit, env validation) | P0 |
| Semana 3-4 | Unit tests + logging | P0 |
| Semana 5-6 | OpenAPI/Swagger + tests e2e | P1 |
| Semana 7-8 | Redis caching layer | P1 |
| Mes 2 | 2FA authentication | P2 |
| Mes 2 | Email template system | P2 |
| Mes 3 | GraphQL support | P3 |
| Mes 3 | Webhooks for notifications | P3 |
| Mes 4 | Payment integration (Stripe) | P3 |
| Mes 5-6 | UI dark mode + improvements | P3 |

---

## RESUMEN EJECUTIVO

### Estado General

**Proyecto:** URPE API Lab - Plataforma No-Code para crear APIs  
**Madurez:** MVP / Early Alpha  
**Stack:** Moderno (NestJS 10 + Next.js 16 + PostgreSQL 16 + Redis 7)  

### Fortalezas

✅ Arquitectura limpia y modular  
✅ Uso de Argon2 para seguridad de passwords  
✅ Sistema de proxy dinámico funcional  
✅ Email campaigns con BullMQ asincrónico  
✅ RBAC implementado (ADMIN/USER)  
✅ DTOs con validación estricta  
✅ Documentación README comprehensive  

### Debilidades Críticas

❌ Rate limiting en DB (escalabilidad)  
❌ Falta logging centralizado  
❌ Sin validación de ENV variables  
❌ 0 tests (unitarios/e2e)  
❌ CORS hardcodeado en código  
❌ Sin headers de seguridad (Helmet)  
❌ Sin API documentation (Swagger)  

### Recomendaciones Top 3

1. **Implementar validación de ENV variables con Joi en bootstrap**
2. **Mover rate limiting de DB a Redis para escalabilidad**
3. **Agregar testes unitarios para auth, proxy y email services**

### Effort Estimate

- Seguridad: 1-2 semanas
- Testing: 2-3 semanas
- Documentation: 1 semana
- Scalability improvements: 2-3 semanas
- **Total:** 6-9 semanas para "Production Ready"

---

**Audit realizado:** 29 de Enero, 2025  
**Auditor:** Sistema de Auditoría Automático  
**Estado:** ✅ COMPLETO
