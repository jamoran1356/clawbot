# 🔐 GitHub Actions - Secrets Requeridos

Para que el workflow de deployment funcione, configura estos Secrets en:
**GitHub → Settings → Secrets and variables → Actions**

---

## Secrets Obligatorios

### 1. **VPS_HOST**
- **Valor:** IP o dominio del servidor de producción
- **Ejemplo:** `production.example.com` o `1.2.3.4`
- **Tipo:** String

### 2. **VPS_USER**
- **Valor:** Usuario SSH en el servidor (ej: `root`, `deploy`, `ubuntu`)
- **Ejemplo:** `ubuntu`
- **Tipo:** String

### 3. **VPS_PASS**
- **Valor:** Contraseña SSH del usuario
- **Ejemplo:** `tu-password-aqui`
- **Tipo:** String (sensitivo - usar GitHub Secrets encryption)

### 4. **SLACK_WEBHOOK** (Opcional)
- **Valor:** URL del webhook de Slack (para notificaciones)
- **Cómo obtener:** 
  1. Ve a tu workspace de Slack
  2. Crea una app → Activar Incoming Webhooks
  3. Copia la URL
- **Tipo:** String
- **Si no tienes:** Comentar la parte de Slack en el workflow

---

## Configuración del Servidor

En el servidor de producción (`DEPLOY_HOST`), necesitas:

```bash
# 1. Usuario y SSH key ya configurados
ssh deploy@production.example.com

# 2. Directorio del proyecto
sudo mkdir -p /opt/api-urpe
sudo chown deploy:deploy /opt/api-urpe

# 3. Git inicializado
cd /opt/api-urpe
git init
git remote add origin https://github.com/your-org/api-urpe.git
git config --global user.email "deploy@example.com"
git config --global user.name "Deploy Bot"

# 4. .env file (CRÍTICO - no debe estar en Git)
touch .env
# Editar con: nano .env
# Agregar todas las variables de .env.production

# 5. Docker instalado
docker --version
docker compose version

# 6. Logs directory
mkdir -p /var/log/api-urpe
```

---

## Paso a Paso: Setup Inicial

### En GitHub

1. Ve a tu repositorio
2. **Settings → Secrets and variables → Actions → New repository secret**
3. Agrega cada Secret:

| Name | Value |
|------|-------|
| `VPS_HOST` | Tu IP/dominio |
| `VPS_USER` | Usuario SSH |
| `VPS_PASS` | Contraseña |
| `SLACK_WEBHOOK` | (Opcional) URL webhook |

### En el Servidor

```bash
# 1. Clona el repo (primera vez)
cd /opt/api-urpe
git clone https://github.com/your-org/api-urpe.git .

# 2. Prepara .env
cp .env.production .env
nano .env  # Edita con valores reales

# 3. Pull Docker images
docker compose -f docker-compose.production.yml pull

# 4. Crea la base de datos (primera vez)
docker compose -f docker-compose.production.yml up -d db
docker compose -f docker-compose.production.yml run --rm api \
  npx prisma migrate deploy

# 5. Inicia todos los servicios
docker compose -f docker-compose.production.yml up -d

# 6. Verifica
curl http://localhost:3000/api/v1/health
```

---

## Workflow Automático

Cada vez que hagas `git push` a `main` o `production`:

1. ✅ Build Docker image
2. ✅ Run tests
3. ✅ Deploy a servidor (SSH)
4. ✅ Run migrations
5. ✅ Start services
6. ✅ Health check
7. 📢 Notificar en Slack

---

## Troubleshooting

**Error: "Authentication failed"**
- Verifica que `VPS_USER` y `VPS_PASS` son correctos
- Prueba conectarte manualmente: `ssh VPS_USER@VPS_HOST`

**Error: "docker compose not found"**
- Instala Docker Compose v2: `sudo apt-get install docker-compose-plugin`

**Error: "migrations failed"**
- SSH al servidor y corre manualmente:
  ```bash
  docker compose -f docker-compose.production.yml run --rm api \
    npx prisma migrate deploy
  ```

**Error: ".env file not found"**
- Crea `.env` manualmente en el servidor (no puede estar en Git por seguridad)

---

## Testing Localmente

Antes de hacer push, puedes testear el workflow:

```bash
# Instalar act (ejecuta workflows en local)
brew install act  # macOS
# o
curl https://raw.githubusercontent.com/nektos/act/master/install.sh | bash

# Corre el workflow
act push -s VPS_HOST=your-vps-ip -s VPS_USER=ubuntu -s VPS_PASS=your-password
```

---

## Security Best Practices

✅ **NUNCA commits .env a Git** - siempre git-ignore  
✅ **Usa SSH keys** sin password  
✅ **Rota secrets** cada 3 meses  
✅ **Limita permisos SSH** (user deploy, no root)  
✅ **Valida commits** con GPG signing (opcional)  

---

## Resources

- [GitHub Actions SSH Deploy](https://github.com/appleboy/ssh-action)
- [Docker Compose Deployments](https://docs.docker.com/compose/production/)
- [Slack Webhooks](https://api.slack.com/messaging/webhooks)

---

**Status:** Setup required before first deployment  
**Tiempo estimado:** 15-20 minutos
