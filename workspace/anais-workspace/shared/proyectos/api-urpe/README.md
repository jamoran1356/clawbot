# 🚀 URPE API Lab - Plataforma de Gestión de APIs No-Code

Una plataforma completa para crear y gestionar APIs de forma visual, **sin necesidad de programar**. Perfecta para equipos que usan n8n, Supabase o webhooks.

## ✨ Características Principales

### Backend (NestJS + TypeScript)
- ✅ **Autenticación JWT** con argon2 (más seguro que bcrypt)
- ✅ **Gestión de Usuarios** con roles (ADMIN/USER)
- ✅ **Creación dinámica de APIs** con slugs únicos
- ✅ **Sistema de Proxy inteligente** que rutea requests
- ✅ **Rate Limiting** configurable por endpoint
- ✅ **Transformaciones** de request/response sobre la marcha
- ✅ **Logging completo** de todas las peticiones
- ✅ **📧 Campañas de Email Masivas** con SMTP propio ([Ver docs](docs/EMAIL_CAMPAIGNS.md))
- ✅ **Worker Queue** con BullMQ para trabajos async

### Frontend (Next.js 16 + React 19)
- ✅ **Interfaz No-Code** para crear APIs en segundos
- ✅ **Dashboard interactivo** con estadísticas en tiempo real
- ✅ **Gestión automática** de API Keys
- ✅ **Copy-to-clipboard** de URLs generadas
- ✅ **Separación de roles** (Admin vs Usuario)
- ✅ **Diseño responsive** con Tailwind CSS 4

## 📦 Stack Tecnológico

```
Backend:
├── NestJS 10.4.20
├── TypeScript 5.9.3
├── Prisma 5.22.0 (PostgreSQL 16)
├── @node-rs/argon2 2.0.2
├── BullMQ 5.66.4 (Redis 7)
├── Nodemailer 7.0.12 (SMTP)
└── axios 1.13.2

Frontend:
├── Next.js 16.1.1
├── React 19.2.3
├── Tailwind CSS 4.1.18
└── Turbopack (build tool)

Infraestructura:
├── PostgreSQL 16 (puerto 5434)
├── Redis 7 (puerto 6379)
├── Docker + Docker Compose
└── pnpm 10.18.1
```

## 🛠️ Instalación

### Requisitos Previos
- Node.js 20+
- pnpm (recomendado) o npm
- Docker Desktop (para PostgreSQL y Redis)

### 1. Clonar el repositorio

```bash
git clone <url>
cd api-urpe
```

### 2. Instalar pnpm (si no lo tienes)

```bash
npm install -g pnpm
```

### 3. Instalar dependencias

```bash
# Backend
cd apps/api
pnpm install

# Frontend
cd ../web
pnpm install

# Worker
cd ../worker
pnpm install
```

### 4. Configurar variables de entorno

Copia el archivo `.env` en la raíz y ajusta los valores:

```env
# Database
DB_USER=apiurpeailab
DB_PASSWORD=tu_password_seguro_aqui
DB_NAME=apiplatform
DB_HOST=localhost
DB_PORT=5434

# Redis
REDIS_HOST=localhost
REDIS_PORT=6379
REDIS_PASSWORD=tu_password_redis_aqui

# API
NODE_ENV=development
PORT=4000
API_PREFIX=/api/v1

# JWT
JWT_SECRET=tu_jwt_secret_muy_largo_y_seguro_aqui
JWT_EXPIRES_IN=7d

# Worker
QUEUE_NAME=email-queue
```

### 5. Iniciar servicios Docker

```bash
cd docker
cp ../.env .env  # Copiar .env al directorio docker
docker-compose up -d postgres redis
```

### 6. Ejecutar migraciones de base de datos

```bash
cd apps/api
pnpm prisma migrate dev
```

### 7. Iniciar aplicaciones en desarrollo

**Terminal 1 - Backend:**
```bash
cd apps/api
pnpm run start:dev
```

**Terminal 2 - Frontend:**
```bash
cd apps/web
pnpm run dev
```

**Terminal 3 - Worker (opcional):**
```bash
cd apps/worker
pnpm run start:dev
```

## 🚀 Acceso a la Aplicación

- **Frontend**: http://localhost:3000
- **Backend API**: http://localhost:4000
- **Health Check**: http://localhost:4000/health

## 📖 Guía de Uso

### 1. Registrar tu primer usuario

```bash
POST http://localhost:4000/api/v1/auth/register
Content-Type: application/json

{
  "email": "admin@urpeailab.com",
  "password": "password123",
  "name": "Admin",
  "role": "ADMIN"
}
```

### 2. Login en el frontend

1. Abre http://localhost:3000
2. Ingresa tu email y contraseña
3. Serás redirigido al Dashboard

### 3. Crear tu primera API (No-Code)

1. Click en **"+ Crear Nueva API"**
2. Completa el formulario:
   - **Nombre**: Mi API de n8n
   - **Descripción**: Conecta con mi workflow de n8n
   - **URL Destino**: https://n8n.urpeailab.com/webhook/abc123
   - **Método HTTP**: POST
   - **Headers** (opcional): Authorization: Bearer token123
3. Click en **"Crear API"**
4. ¡Listo! Obtendrás una URL como: `https://api.urpeailab.com/proxy/xyz789abc`

### 4. Usar tu API creada

```bash
curl -X POST https://api.urpeailab.com/proxy/xyz789abc \\
  -H "x-api-key: tu_api_key_generada_automaticamente" \\
  -H "Content-Type: application/json" \\
  -d '{"nombre": "Juan", "edad": 30}'
```

El sistema automáticamente:
- Valida tu API key
- Aplica rate limiting
- Transforma el request (si configuraste)
- Envía a tu URL destino
- Registra todo en la base de datos
- Devuelve la respuesta transformada

## 🐳 Deploy con Docker Compose (Producción)

Para producción, ejecuta todos los servicios en contenedores:

```bash
cd docker
docker-compose up -d
```

Esto iniciará:
- ✅ PostgreSQL (puerto 5434)
- ✅ Redis (puerto 6379)
- ✅ API Backend (puerto 4000)
- ✅ Worker (background jobs)
- ✅ Frontend Web (puerto 3000)

## 📊 Arquitectura del Sistema

```
┌─────────────────┐
│   Frontend      │
│   (Next.js)     │ → http://localhost:3000
└────────┬────────┘
         │ API Calls
         ↓
┌─────────────────┐
│   Backend API   │
│   (NestJS)      │ → http://localhost:4000
└────────┬────────┘
         │
    ┌────┴─────┬──────────┬──────────┐
    ↓          ↓          ↓          ↓
┌─────┐  ┌─────────┐  ┌──────┐  ┌───────┐
│ PG  │  │  Redis  │  │ Proxy│  │Worker │
│ SQL │  │  Cache  │  │System│  │ Queue │
└─────┘  └─────────┘  └──────┘  └───────┘
                         │
                         ↓
              ┌──────────────────┐
              │  n8n / Supabase  │
              │  / Webhooks      │
              └──────────────────┘
```

### Flujo de una petición:

```
1. Usuario → Frontend → Crea API con formulario visual
2. Frontend → Backend → POST /api/v1/api-endpoints
3. Backend → Database → Crea endpoint + API key + Slug único
4. Backend → Usuario → Devuelve URL: /proxy/abc123

Cuando alguien usa la API:
5. Cliente → GET/POST /proxy/abc123 + API Key header
6. Proxy Service → Valida API key + Rate limit
7. Proxy Service → Aplica transformaciones
8. Proxy Service → axios → n8n/Supabase
9. n8n → Respuesta → Proxy Service
10. Proxy Service → Log en DB + Stats
11. Proxy Service → Cliente (respuesta transformada)
```

## 📂 Estructura del Código

```
api-urpe/
├── apps/
│   ├── api/                              # Backend NestJS
│   │   └── src/
│   │       ├── main.ts                   # Entry point
│   │       ├── app.module.ts             # Root module
│   │       ├── modules/
│   │       │   ├── auth/                 # JWT auth (argon2)
│   │       │   ├── users/                # User CRUD + RBAC
│   │       │   ├── api-endpoints/        # Core: API management
│   │       │   ├── proxy/                # Proxy system
│   │       │   └── email-campaigns/      # Mass emails
│   │       └── infra/
│   │           ├── prisma/               # Database layer
│   │           ├── redis/                # Redis client
│   │           └── queue/                # BullMQ setup
│   │
│   ├── worker/                           # Background worker
│   │   └── src/main.ts
│   │
│   └── web/                              # Frontend Next.js
│       └── src/
│           ├── app/                      # Pages (App Router)
│           │   ├── page.tsx              # Home (redirect)
│           │   ├── login/                # Login page
│           │   └── dashboard/            # Protected area
│           │       ├── layout.tsx        # Nav + auth check
│           │       ├── page.tsx          # Dashboard stats
│           │       ├── apis/
│           │       │   ├── page.tsx      # API list
│           │       │   └── new/
│           │       │       └── page.tsx  # Visual API builder
│           │       └── emails/           # Email campaigns
│           ├── contexts/
│           │   └── AuthContext.tsx       # Global auth state
│           └── lib/
│               └── api.ts                # Axios client
│
├── prisma/
│   └── schema.prisma                     # Database models
│
├── docker/
│   ├── docker-compose.yml                # All services
│   ├── api.Dockerfile
│   └── worker.Dockerfile
│
└── .env                                  # Environment vars
```

## 🔐 Seguridad Implementada

- ✅ **Argon2** para hashing de contraseñas (ganador del Password Hashing Competition)
- ✅ **JWT Tokens** con expiración configurable
- ✅ **API Keys únicas** generadas automáticamente por endpoint
- ✅ **Rate Limiting** configurable (default: 100 req/min)
- ✅ **Validación estricta** con class-validator en todos los DTOs
- ✅ **CORS** configurado para dominios permitidos
- ✅ **Environment Variables** para secrets (nunca hardcoded)
- ✅ **Roles y Guards** para separar ADMIN vs USER

## 📝 Endpoints del Backend

### Autenticación
- `POST /api/v1/auth/register` - Registrar nuevo usuario
- `POST /api/v1/auth/login` - Login (devuelve JWT)
- `GET /api/v1/auth/profile` - Perfil del usuario actual (requiere JWT)

### Usuarios (solo ADMIN)
- `GET /api/v1/users` - Listar todos los usuarios
- `GET /api/v1/users/:id` - Ver un usuario
- `PUT /api/v1/users/:id` - Actualizar usuario
- `DELETE /api/v1/users/:id` - Eliminar usuario
- `GET /api/v1/users/:id/stats` - Estadísticas del usuario

### API Endpoints
- `GET /api/v1/api-endpoints` - Listar mis endpoints (filtro por status)
- `POST /api/v1/api-endpoints` - Crear nuevo endpoint (auto-genera slug + key)
- `GET /api/v1/api-endpoints/:id` - Ver detalles de un endpoint
- `PUT /api/v1/api-endpoints/:id` - Actualizar endpoint
- `DELETE /api/v1/api-endpoints/:id` - Eliminar endpoint
- `GET /api/v1/api-endpoints/:id/stats` - Estadísticas del endpoint

### Proxy (público, requiere API key)
- `* /proxy/:slug` - Proxy dinámico (soporta GET, POST, PUT, PATCH, DELETE)

### Email Campaigns
- `GET /api/v1/email-campaigns` - Listar campañas
- `POST /api/v1/email-campaigns` - Crear nueva campaña
- `GET /api/v1/email-campaigns/:id` - Ver campaña
- `PUT /api/v1/email-campaigns/:id` - Actualizar campaña
- `DELETE /api/v1/email-campaigns/:id` - Eliminar campaña
- `POST /api/v1/email-campaigns/:id/send` - Enviar campaña (queue)

## 🎯 Casos de Uso Reales

### 1. Conectar n8n Workflows
```
Problema: Tu workflow de n8n está expuesto públicamente
Solución: Crea un endpoint en URPE API Lab con:
  - Rate limiting: 50 req/min
  - API key requerida
  - Headers personalizados para autenticar con n8n
```

### 2. Proteger Supabase Functions
```
Problema: Tus Edge Functions son públicas y cualquiera puede llamarlas
Solución: Crea un proxy que:
  - Valide API keys únicas por cliente
  - Agregue headers de autenticación a Supabase
  - Registre quién y cuándo hace cada llamada
```

### 3. Transformar Webhooks
```
Problema: Un servicio externo envía webhooks en formato incompatible
Solución: Configura Request Transform:
  {
    "mapFields": {
      "external_id": "id",
      "full_name": "name"
    }
  }
```

### 4. App Móvil Flutter
```
Problema: Necesitas APIs para tu app pero no quieres configurar servidor
Solución: Crea endpoints desde el panel web, obtén las URLs y API keys,
         úsalas en tu app Flutter
```

### 5. Envío Masivo de Emails
```
Problema: Necesitas enviar campañas de email a tu base de datos
Solución: Crea una campaña, sube tu lista, el Worker procesa todo en background
```

## 🚧 Roadmap (Próximas Funcionalidades)

- [ ] **Panel de Logs en tiempo real** (WebSockets)
- [ ] **Webhooks para notificaciones** (cuando hay errors)
- [ ] **Exportar logs** (CSV/JSON)
- [ ] **Gráficas avanzadas** (Charts.js)
- [ ] **Billing con Stripe** (planes Free/Pro/Enterprise)
- [ ] **Soporte GraphQL** (además de REST)
- [ ] **Temas personalizables** (dark mode)
- [ ] **API de administración** (CLI tool)
- [ ] **Marketplace de transformaciones** (templates)
- [ ] **Integración con Zapier/Make**

## 🐛 Troubleshooting

### Error: Puerto 5434 ya en uso
```bash
# Ver qué proceso usa el puerto
netstat -ano | findstr :5434

# Cambiar puerto en .env
DB_PORT=5435
```

### Error: Cannot find module '@/contexts/AuthContext'
```bash
# Verificar que Next.js tiene el alias configurado
# Ver apps/web/tsconfig.json → paths
```

### Error: Prisma Client no está sincronizado
```bash
cd apps/api
pnpm prisma generate
pnpm prisma migrate dev
```

### Frontend no se conecta al Backend
```bash
# Verificar que apps/web/.env.local tiene:
NEXT_PUBLIC_API_URL=http://localhost:4000/api/v1
```

## 🤝 Contribuir

1. Fork el proyecto
2. Crea una rama (`git checkout -b feature/nueva-funcionalidad`)
3. Haz tus cambios
4. Commit (`git commit -m 'feat: añadir nueva funcionalidad'`)
5. Push (`git push origin feature/nueva-funcionalidad`)
6. Abre un Pull Request

## 📄 Licencia

MIT License - Este proyecto es de código abierto

## 👥 Equipo

Desarrollado con ❤️ por **URPE AI Lab**

---

**¿Necesitas ayuda?** 
- 📧 Email: soporte@urpeailab.com
- 🌐 Web: https://urpeailab.com
- 💬 Discord: [Únete a la comunidad](https://discord.gg/urpeailab)

---

⭐️ Si este proyecto te es útil, déjanos una estrella en GitHub
