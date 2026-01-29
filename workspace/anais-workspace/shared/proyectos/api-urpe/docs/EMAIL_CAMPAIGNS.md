# Sistema de Envío Masivo de Correos Electrónicos

Este documento describe cómo usar el sistema de envío masivo de correos electrónicos implementado en la API.

## Características

- ✅ Envío masivo mediante SMTP propio de la empresa
- ✅ Procesamiento asíncrono con colas (BullMQ + Redis)
- ✅ Envío por lotes configurable
- ✅ Seguimiento de estado en tiempo real
- ✅ Reintentos automáticos en caso de fallos
- ✅ Cancelación de campañas
- ✅ Gestión de destinatarios

## Configuración

### 1. Variables de Entorno

Copia `.env.example` a `.env` y configura las siguientes variables:

```bash
# SMTP Configuration
SMTP_HOST=smtp.tuempresa.com
SMTP_PORT=587
SMTP_SECURE=false
SMTP_USER=tu-email@empresa.com
SMTP_PASSWORD=tu-password-smtp

# Email Defaults
SMTP_FROM_EMAIL=noreply@empresa.com
SMTP_FROM_NAME="Mi Empresa"

# Email Campaign Settings
EMAIL_BATCH_SIZE=100                  # Emails por lote
EMAIL_DELAY_BETWEEN_BATCHES=1000     # Delay en ms entre lotes

# Redis (para colas)
REDIS_HOST=localhost
REDIS_PORT=6379
REDIS_PASSWORD=
```

### 2. Migración de Base de Datos

```bash
pnpm prisma:generate
pnpm prisma:migrate
```

### 3. Iniciar Servicios

**Opción A: Desarrollo local**

Terminal 1 - API:
```bash
pnpm start:api
```

Terminal 2 - Worker:
```bash
pnpm start:worker
```

Terminal 3 - Redis (si no está en Docker):
```bash
redis-server
```

**Opción B: Docker**

```bash
cd docker
docker-compose up -d
```

## API Endpoints

### Autenticación

Todos los endpoints requieren autenticación JWT. Incluye el token en el header:

```
Authorization: Bearer <tu-token-jwt>
```

### 1. Crear Campaña

`POST /email-campaigns`

```json
{
  "name": "Newsletter Enero 2026",
  "subject": "Novedades del mes",
  "body": "<h1>Hola!</h1><p>Contenido HTML del email</p>",
  "fromEmail": "marketing@empresa.com",
  "fromName": "Equipo Marketing",
  "recipients": [
    "usuario1@example.com",
    "usuario2@example.com"
  ]
}
```

**Respuesta:**
```json
{
  "id": "clx123abc",
  "name": "Newsletter Enero 2026",
  "status": "DRAFT",
  "sentCount": 0,
  "failedCount": 0,
  "createdAt": "2026-01-12T10:00:00Z"
}
```

### 2. Listar Campañas

`GET /email-campaigns`

**Respuesta:**
```json
[
  {
    "id": "clx123abc",
    "name": "Newsletter Enero 2026",
    "status": "DRAFT",
    "sentCount": 0,
    "totalRecipients": 2,
    "createdAt": "2026-01-12T10:00:00Z"
  }
]
```

### 3. Obtener Campaña

`GET /email-campaigns/:id`

### 4. Actualizar Campaña

`PUT /email-campaigns/:id`

Solo se pueden actualizar campañas en estado `DRAFT`.

### 5. Añadir Destinatarios

`POST /email-campaigns/:id/recipients`

```json
{
  "emails": [
    "nuevo1@example.com",
    "nuevo2@example.com"
  ]
}
```

### 6. Enviar Campaña

`POST /email-campaigns/:id/send`

Encola la campaña para envío asíncrono.

```json
{
  "batchSize": 50,              // Opcional: emails por lote
  "delayBetweenBatches": 2000   // Opcional: delay en ms
}
```

**Respuesta:**
```json
{
  "message": "Campaign queued for sending",
  "campaignId": "clx123abc",
  "jobId": "123456",
  "recipientCount": 100
}
```

### 7. Consultar Estado

`GET /email-campaigns/:id/status`

```json
{
  "campaign": {
    "id": "clx123abc",
    "name": "Newsletter Enero 2026",
    "status": "SENDING",
    "sentCount": 45,
    "failedCount": 2,
    "totalRecipients": 100,
    "createdAt": "2026-01-12T10:00:00Z"
  },
  "job": {
    "id": "123456",
    "state": "active",
    "progress": 47,
    "attemptsMade": 1
  }
}
```

**Estados posibles:**
- `DRAFT`: Borrador, aún no enviada
- `QUEUED`: En cola, esperando procesamiento
- `SENDING`: Enviándose actualmente
- `SENT`: Enviada completamente
- `FAILED`: Falló el envío
- `CANCELLED`: Cancelada por el usuario

### 8. Cancelar Campaña

`POST /email-campaigns/:id/cancel`

Solo se pueden cancelar campañas en estado `QUEUED` o `SENDING`.

### 9. Eliminar Campaña

`DELETE /email-campaigns/:id`

## Ejemplos de Uso

### Flujo Completo con cURL

```bash
# 1. Login (obtener token)
TOKEN=$(curl -X POST http://localhost:3000/auth/login \
  -H "Content-Type: application/json" \
  -d '{"email":"admin@example.com","password":"password"}' \
  | jq -r '.access_token')

# 2. Crear campaña
CAMPAIGN_ID=$(curl -X POST http://localhost:3000/email-campaigns \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Test Campaign",
    "subject": "Hola desde la API",
    "body": "<h1>Test Email</h1>",
    "fromEmail": "test@empresa.com",
    "recipients": ["user@example.com"]
  }' | jq -r '.id')

# 3. Enviar campaña
curl -X POST http://localhost:3000/email-campaigns/$CAMPAIGN_ID/send \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"batchSize": 50}'

# 4. Verificar estado
curl -X GET http://localhost:3000/email-campaigns/$CAMPAIGN_ID/status \
  -H "Authorization: Bearer $TOKEN"
```

## Arquitectura

```
┌─────────────┐      ┌──────────────┐      ┌─────────────┐
│   Cliente   │─────▶│  API (NestJS)│─────▶│Redis (BullMQ)│
└─────────────┘      └──────────────┘      └─────────────┘
                            │                      │
                            │                      ▼
                            ▼                ┌──────────────┐
                     ┌────────────┐          │Worker (NestJS)│
                     │ PostgreSQL │◀─────────└──────────────┘
                     └────────────┘                 │
                                                    ▼
                                            ┌──────────────┐
                                            │Servidor SMTP │
                                            └──────────────┘
```

### Flujo de Envío

1. **Cliente** crea una campaña (`POST /email-campaigns`)
2. **API** guarda en PostgreSQL con estado `DRAFT`
3. **Cliente** envía la campaña (`POST /email-campaigns/:id/send`)
4. **API** encola job en Redis/BullMQ y cambia estado a `QUEUED`
5. **Worker** toma el job de la cola
6. **Worker** actualiza estado a `SENDING`
7. **Worker** procesa emails en lotes:
   - Envía batch de N emails
   - Espera X ms
   - Repite hasta completar
8. **Worker** actualiza contadores en tiempo real
9. **Worker** marca campaña como `SENT` o `FAILED`

## Consideraciones de Producción

### Límites SMTP

- Configura `EMAIL_BATCH_SIZE` según los límites de tu servidor SMTP
- Ajusta `EMAIL_DELAY_BETWEEN_BATCHES` para evitar throttling
- Ejemplo para Gmail: 100 emails/batch, 2000ms delay

### Escalabilidad

- Puedes ejecutar múltiples workers en paralelo
- Redis maneja la distribución automática de jobs
- Cada worker procesa campañas independientes

### Monitoreo

Para monitorear las colas, instala BullMQ Board:

```bash
pnpm add @bull-board/api @bull-board/nestjs
```

### Reintentos

El sistema reintenta automáticamente 3 veces con backoff exponencial:
- Intento 1: inmediato
- Intento 2: +5 segundos
- Intento 3: +10 segundos

## Solución de Problemas

### Error: "SMTP connection failed"

Verifica:
- Credenciales SMTP correctas
- Firewall no bloquea el puerto
- TLS/SSL configurado correctamente

```bash
# Test manual de conexión SMTP
curl -v telnet://smtp.tuempresa.com:587
```

### Worker no procesa jobs

Verifica:
- Redis está corriendo
- Worker está iniciado
- Logs del worker: `pnpm start:worker`

### Emails quedan en cola

Revisa:
- Estado de Redis: `redis-cli KEYS "bull:email-campaigns:*"`
- Jobs fallidos: consulta `/email-campaigns/:id/status`

## Seguridad

- ✅ Autenticación JWT requerida
- ✅ Usuarios solo ven sus campañas (excepto ADMIN)
- ✅ Validación de emails
- ✅ Rate limiting recomendado (pendiente implementar)
- ✅ Sanitización de HTML en emails (recomendado)

## Mejoras Futuras

- [ ] Subida de CSV con destinatarios
- [ ] Templates de emails reutilizables
- [ ] Personalización con variables ({{nombre}}, etc)
- [ ] Estadísticas: aperturas, clicks
- [ ] Webhooks para eventos
- [ ] Panel de administración en web app
- [ ] Rate limiting por usuario
- [ ] Scheduled campaigns (envío programado)
