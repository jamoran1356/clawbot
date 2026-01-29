# 🏗️ Arquitectura API-URPE - Producción Ready

## Visión General

**API Gateway** que actúa como intermediaria segura entre clientes y servicios externos (N8N, Supabase, etc):
- Clientes se conectan a `api.urpeailab.com/api/v1/proxy/*`
- No conocen URLs reales de servicios
- Pueden enviar correos vía endpoints configurable
- Integración directa con N8N para automatización

```
┌─────────────────────────────────────────────────────────────┐
│                    CLIENTES EXTERNOS                        │
│              (Web, Mobile, N8N Workflows)                   │
└──────────────────────────┬──────────────────────────────────┘
                           │
                    HTTP/HTTPS (JWT)
                           │
                    API Gateway (URPE)
            ┌──────────────┼──────────────┐
            ▼              ▼              ▼
        ┌────────┐    ┌────────┐    ┌────────┐
        │ N8N    │    │Supabase│    │ Email  │
        │ Server │    │        │    │ Server │
        └────────┘    └────────┘    └────────┘
```

## Stack Técnico

- **Runtime:** Node.js 22
- **Framework:** NestJS 10.4
- **ORM:** Prisma 5.22
- **Database:** PostgreSQL
- **Cache/Queue:** Redis + BullMQ
- **Auth:** JWT + Passport
- **Email:** Nodemailer (SMTP configurable)
- **HTTP Client:** Axios
- **Password Hashing:** Argon2
- **Deployment:** Docker + Docker Compose

## Módulos

### 1. **Auth Module** (Autenticación)
- Login/Register con JWT
- Roles (ADMIN, USER)
- Guards JWT + Roles
- Refresh tokens

### 2. **API Endpoints Module** (Gestión de APIs)
- CRUD de endpoints
- Transformación de request/response
- Rate limiting por endpoint
- Metadata y auditoría

### 3. **Proxy Module** (Gateway) ⭐
- Proxea peticiones a servicios externos
- Transforma request/response según configuración
- Logging de cada request
- Manejo de errores y timeouts
- Headers personalizados

### 4. **Email Module** (Envios de correo)
- SMTP configurable
- Email campaigns
- Plantillas
- BullMQ para cola de envios
- Endpoint para N8N

### 5. **Webhook Module** (N8N Integration)
- Recibe eventos de N8N
- Procesa y ejecuta
- Historial de ejecuciones

### 6. **Users Module**
- CRUD de usuarios
- Gestión de API keys
- Permisos

### 7. **Health Module**
- Health checks
- Liveness/Readiness probes
- Status de servicios externos

## Base de Datos

### Tablas Principales

```
users
├── id (PK)
├── email (UNIQUE)
├── name
├── password (hashed)
├── role (ADMIN|USER)
├── isActive
└── timestamps

api_endpoints
├── id (PK)
├── name, slug (UNIQUE)
├── method (GET|POST|PUT|DELETE)
├── targetUrl (destino real)
├── requestTransform (JSON)
├── responseTransform (JSON)
├── headers (JSON)
├── requireApiKey
├── rateLimit
├── userId (FK)
└── connectionId (FK)

api_keys
├── id (PK)
├── key (UNIQUE, generado)
├── userId (FK)
├── endpointId (FK, opcional)
├── expiresAt
└── lastUsedAt

connections
├── id (PK)
├── type (SUPABASE|N8N|WEBHOOK|REST_API|SMTP|CUSTOM)
├── config (JSON)
└── isActive

requests (auditoría)
├── id (PK)
├── endpointId (FK)
├── apiKeyId (FK)
├── method, path, headers, body
├── statusCode, responseTime
└── timestamps

email_campaigns
├── id (PK)
├── name, subject, body
├── fromEmail, fromName
├── status (DRAFT|QUEUED|SENDING|SENT|FAILED)
├── recipients (JSON array)
├── scheduledAt, sentAt
└── userId (FK)
```

## Flujo de Autenticación

```
1. Usuario hace login
   POST /api/v1/auth/login
   ├─ Email + Password
   └─ Retorna: JWT token + refresh token

2. Cliente incluye token en headers
   Authorization: Bearer <JWT>

3. Guard JWT valida en cada request
   ├─ Extrae el payload
   ├─ Obtiene el usuario
   └─ Inyecta en @CurrentUser()

4. Decorador @Roles() valida permisos
   └─ Si no tiene rol, rechaza (403)
```

## Flujo de Proxy

```
1. Cliente hace request a endpoint proxy
   POST /api/v1/proxy/mi-api
   ├─ Body: { data: ... }
   └─ Header: Authorization: Bearer <API_KEY>

2. API valida:
   ├─ API key válida
   ├─ Endpoint existe y está ACTIVE
   ├─ Rate limit no excedido
   └─ Usuario tiene permisos

3. Transforma request (si hay reglas)
   ├─ Aplica requestTransform
   ├─ Agrega headers personalizados
   └─ Valida contra schema

4. Proxea a targetUrl
   ├─ Timeout: 30s
   ├─ Reintentos: 1 (on 5xx)
   └─ Logging completo

5. Transforma response (si hay reglas)
   ├─ Aplica responseTransform
   ├─ Extrae datos específicos
   └─ Retorna al cliente

6. Registra request para auditoría
   ├─ Timestamps
   ├─ Response time
   ├─ Status
   └─ IP, User-Agent
```

## Flujo de Email

```
1. Usuario crea campaña
   POST /api/v1/email/campaigns
   ├─ name, subject, body
   ├─ fromEmail, recipients
   └─ scheduledAt (opcional)

2. Si es inmediato:
   ├─ Agrega a queue (BullMQ + Redis)
   └─ Status: QUEUED

3. Worker procesa:
   ├─ Lee de Redis
   ├─ Conecta a SMTP
   ├─ Envía batch de emails
   ├─ Registra éxito/error
   └─ Status: SENT o FAILED

4. N8N puede usar endpoint
   POST /api/v1/email/send-n8n
   ├─ Requiere API key
   ├─ Agrega a queue
   └─ Retorna: { campaignId, status }
```

## Seguridad - Checklist

- ✅ Passwords hasheados con Argon2
- ✅ JWT con expiración (15 min) + refresh
- ✅ CORS restrictivo (solo dominios configurados)
- ✅ Rate limiting por endpoint
- ✅ Validación de inputs (class-validator)
- ✅ Logs de auditoría (todos los requests)
- ✅ API keys separadas por usuario/endpoint
- ✅ Roles y permisos granulares
- ✅ HTTPS en producción (+ HSTS)
- ✅ Database: sin exposición de contraseñas
- ✅ Environment variables (no hardcoded)
- ⚠️ PENDIENTE: 2FA (optional)
- ⚠️ PENDIENTE: Encryption de campos sensibles

## Escalabilidad

- **Horizontal:** Múltiples instancias detrás de load balancer
- **Redis:** Cache de sessions + Queue de jobs
- **BullMQ:** Workers separados para email, webhooks
- **Prisma:** Connection pooling (PgBouncer en producción)
- **CDN:** Assets + API responses cacheable

## Monitoreo

- Health endpoint: `GET /api/v1/health`
- Logs: Stdout (estructurados para ELK/DataDog)
- Métricas: Prometheus (opcional)
- Alertas: Sentry (opcional)

---

**Última actualización:** 2026-01-29
