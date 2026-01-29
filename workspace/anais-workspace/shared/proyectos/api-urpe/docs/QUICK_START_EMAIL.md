# 🚀 Inicio Rápido - Sistema de Envío Masivo de Correos

## Configuración Inicial (5 minutos)

### 1. Configura las variables de entorno

Edita tu archivo `.env` y añade:

```env
# SMTP Configuration (ejemplo con Gmail)
SMTP_HOST=smtp.gmail.com
SMTP_PORT=587
SMTP_SECURE=false
SMTP_USER=tu-email@gmail.com
SMTP_PASSWORD=tu-app-password

# Para usar Gmail:
# 1. Activa la verificación en 2 pasos
# 2. Genera una contraseña de aplicación en: https://myaccount.google.com/apppasswords
# 3. Usa esa contraseña en SMTP_PASSWORD

# Email Defaults
SMTP_FROM_EMAIL=tu-email@empresa.com
SMTP_FROM_NAME="Tu Empresa"

# Redis (necesario para las colas)
REDIS_HOST=localhost
REDIS_PORT=6379
REDIS_PASSWORD=
```

### 2. Inicia los servicios

**Opción A: Con Docker (recomendado)**

```bash
cd docker
docker-compose up -d
```

**Opción B: Sin Docker**

Terminal 1 - Redis:
```bash
redis-server
```

Terminal 2 - PostgreSQL (asegúrate de que está corriendo)

Terminal 3 - API:
```bash
pnpm start:api
```

Terminal 4 - Worker:
```bash
pnpm start:worker
```

### 3. Prueba el sistema

```bash
node scripts/test-email-campaign.js
```

## Ejemplo de Uso con cURL

### 1. Login

```bash
curl -X POST http://localhost:3000/auth/login \
  -H "Content-Type: application/json" \
  -d '{
    "email": "admin@example.com",
    "password": "tu-password"
  }'
```

Respuesta:
```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
}
```

### 2. Crear Campaña

```bash
curl -X POST http://localhost:3000/email-campaigns \
  -H "Authorization: Bearer TU_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Newsletter Enero",
    "subject": "Novedades del mes",
    "body": "<h1>Hola!</h1><p>Aquí están las novedades...</p>",
    "fromEmail": "marketing@empresa.com",
    "fromName": "Equipo Marketing",
    "recipients": [
      "cliente1@example.com",
      "cliente2@example.com"
    ]
  }'
```

### 3. Enviar Campaña

```bash
curl -X POST http://localhost:3000/email-campaigns/CAMPAIGN_ID/send \
  -H "Authorization: Bearer TU_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "batchSize": 50,
    "delayBetweenBatches": 1000
  }'
```

### 4. Ver Estado

```bash
curl -X GET http://localhost:3000/email-campaigns/CAMPAIGN_ID/status \
  -H "Authorization: Bearer TU_TOKEN"
```

## Endpoints Disponibles

| Método | Endpoint | Descripción |
|--------|----------|-------------|
| POST | `/email-campaigns` | Crear campaña |
| GET | `/email-campaigns` | Listar campañas |
| GET | `/email-campaigns/:id` | Ver campaña |
| PUT | `/email-campaigns/:id` | Actualizar campaña |
| DELETE | `/email-campaigns/:id` | Eliminar campaña |
| POST | `/email-campaigns/:id/send` | Enviar campaña |
| GET | `/email-campaigns/:id/status` | Ver estado |
| POST | `/email-campaigns/:id/cancel` | Cancelar envío |
| POST | `/email-campaigns/:id/recipients` | Añadir destinatarios |

## Estados de Campaña

- **DRAFT**: Borrador, no enviada
- **QUEUED**: En cola de envío
- **SENDING**: Enviándose
- **SENT**: Enviada
- **FAILED**: Falló
- **CANCELLED**: Cancelada

## Solución de Problemas

### Error: "SMTP connection failed"

1. Verifica credenciales SMTP
2. Si usas Gmail, necesitas App Password
3. Revisa firewall/antivirus

### Worker no procesa

1. Verifica que Redis está corriendo: `redis-cli ping`
2. Revisa logs del worker
3. Verifica que el worker está iniciado

### Emails no llegan

1. Revisa spam
2. Verifica SMTP_FROM_EMAIL es válido
3. Consulta logs del worker para errores

## Siguiente Paso

Lee la documentación completa: [docs/EMAIL_CAMPAIGNS.md](EMAIL_CAMPAIGNS.md)
