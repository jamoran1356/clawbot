# 🚀 Guía de Deployment - API-URPE Production

## Pre-requisitos

- [ ] Docker & Docker Compose (v2.0+)
- [ ] Server Linux (Ubuntu 20.04+ o similar)
- [ ] Domain + SSL Certificate (Let's Encrypt)
- [ ] SMTP Server credentials
- [ ] PostgreSQL backup strategy
- [ ] Redis monitoring
- [ ] Logs centralized (opcional)

## Paso 1: Preparar el Servidor

```bash
# SSH al servidor
ssh root@your-server.com

# Update packages
apt-get update && apt-get upgrade -y

# Install Docker
curl -fsSL https://get.docker.com -o get-docker.sh
sh get-docker.sh

# Install Docker Compose
apt-get install docker-compose-plugin -y

# Verify installations
docker --version
docker compose version

# Create app directory
mkdir -p /opt/api-urpe
cd /opt/api-urpe
```

## Paso 2: Clone & Setup

```bash
# Clone the project (ajusta según tu repo)
git clone https://github.com/your-org/api-urpe.git .
# O si usas privado
git clone git@github.com:your-org/api-urpe.git .

# Copy environment file
cp .env.production .env

# Edit with real credentials
nano .env

# Debe contener:
# - DATABASE_URL (con credenciales fuertes)
# - REDIS_PASSWORD
# - JWT_SECRET (mínimo 32 chars, use: openssl rand -base64 32)
# - JWT_REFRESH_SECRET
# - SMTP credentials
# - CORS_ORIGINS (tu dominio)
```

## Paso 3: Database Setup

```bash
# Create init script
mkdir -p scripts
cat > scripts/init-db.sql << 'EOF'
-- Create extensions
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";
CREATE EXTENSION IF NOT EXISTS "pg_trgm";

-- Set up connection limits
ALTER SYSTEM SET max_connections = 200;
EOF

# Build images
docker compose -f docker-compose.production.yml build

# Run migrations
docker compose -f docker-compose.production.yml run --rm api \
  npx prisma migrate deploy

# Create initial admin user (opcional - agregar después)
# Puedes crear via API o script separado
```

## Paso 4: SSL Certificate

```bash
# Install Certbot
apt-get install certbot python3-certbot-nginx -y

# Generate certificate (sin nginx, solo para validación)
certbot certonly --standalone \
  -d api.urpeailab.com \
  -d app.urpeailab.com

# Certificate files en:
# /etc/letsencrypt/live/api.urpeailab.com/

# Copy to docker volume (si usas nginx en container)
sudo cp -r /etc/letsencrypt/live /opt/api-urpe/certs/
sudo chown -R 1000:1000 /opt/api-urpe/certs/
```

## Paso 5: Nginx Configuration

```bash
cat > nginx.conf << 'EOF'
user nginx;
worker_processes auto;
error_log /var/log/nginx/error.log warn;
pid /var/run/nginx.pid;

events {
    worker_connections 2048;
}

http {
    include /etc/nginx/mime.types;
    default_type application/octet-stream;

    log_format main '$remote_addr - $remote_user [$time_local] "$request" '
                    '$status $body_bytes_sent "$http_referer" '
                    '"$http_user_agent" "$http_x_forwarded_for"';

    access_log /var/log/nginx/access.log main;

    sendfile on;
    tcp_nopush on;
    tcp_nodelay on;
    keepalive_timeout 65;
    types_hash_max_size 2048;
    client_max_body_size 20M;

    # Gzip compression
    gzip on;
    gzip_vary on;
    gzip_proxied any;
    gzip_comp_level 6;
    gzip_types text/plain text/css text/xml text/javascript 
               application/json application/javascript application/xml+rss 
               application/atom+xml image/svg+xml;

    # Rate limiting
    limit_req_zone $binary_remote_addr zone=api_limit:10m rate=10r/s;
    limit_req_zone $binary_remote_addr zone=auth_limit:10m rate=5r/m;

    # Upstream API
    upstream api_backend {
        server api:3000;
    }

    # HTTP to HTTPS redirect
    server {
        listen 80;
        server_name api.urpeailab.com app.urpeailab.com;
        return 301 https://$server_name$request_uri;
    }

    # HTTPS API Server
    server {
        listen 443 ssl http2;
        server_name api.urpeailab.com;

        # SSL Configuration
        ssl_certificate /etc/nginx/certs/live/api.urpeailab.com/fullchain.pem;
        ssl_certificate_key /etc/nginx/certs/live/api.urpeailab.com/privkey.pem;
        ssl_protocols TLSv1.2 TLSv1.3;
        ssl_ciphers HIGH:!aNULL:!MD5;
        ssl_prefer_server_ciphers on;
        ssl_session_cache shared:SSL:10m;
        ssl_session_timeout 10m;

        # Security headers
        add_header Strict-Transport-Security "max-age=31536000; includeSubDomains" always;
        add_header X-Content-Type-Options "nosniff" always;
        add_header X-Frame-Options "SAMEORIGIN" always;
        add_header X-XSS-Protection "1; mode=block" always;
        add_header Referrer-Policy "strict-origin-when-cross-origin" always;

        # API routes
        location /api/v1/ {
            limit_req zone=api_limit burst=20 nodelay;
            
            proxy_pass http://api_backend;
            proxy_http_version 1.1;
            proxy_set_header Host $host;
            proxy_set_header X-Real-IP $remote_addr;
            proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
            proxy_set_header X-Forwarded-Proto $scheme;
            
            # Timeouts
            proxy_connect_timeout 30s;
            proxy_send_timeout 30s;
            proxy_read_timeout 30s;
            
            # Buffering
            proxy_buffering on;
            proxy_buffer_size 4k;
            proxy_buffers 8 4k;
        }

        # Auth endpoints con límite más estricto
        location /api/v1/auth/ {
            limit_req zone=auth_limit burst=2 nodelay;
            proxy_pass http://api_backend;
            proxy_http_version 1.1;
            proxy_set_header Host $host;
            proxy_set_header X-Real-IP $remote_addr;
            proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
            proxy_set_header X-Forwarded-Proto $scheme;
        }

        # Health check (sin límite)
        location /api/v1/health {
            proxy_pass http://api_backend;
            access_log off;
        }
    }
}
EOF
```

## Paso 6: Start Services

```bash
# Start everything in background
docker compose -f docker-compose.production.yml up -d

# Verify services are running
docker compose ps

# Check logs
docker compose logs -f api

# Test health endpoint
curl https://api.urpeailab.com/api/v1/health
```

## Paso 7: Create Admin User

```bash
# Access container
docker compose exec api sh

# Dentro del container:
npx ts-node -e "
const { PrismaClient } = require('@prisma/client');
const { hash } = require('@node-rs/argon2');

(async () => {
  const prisma = new PrismaClient();
  
  const password = await hash('your-strong-password-here');
  
  const admin = await prisma.user.create({
    data: {
      email: 'admin@urpeailab.com',
      name: 'Admin',
      password,
      role: 'ADMIN',
      isActive: true,
    },
  });
  
  console.log('Admin creado:', admin.email);
  await prisma.$disconnect();
})();
"
```

## Paso 8: SSL Auto-renewal

```bash
# Create renewal script
cat > /opt/api-urpe/scripts/renew-ssl.sh << 'EOF'
#!/bin/bash
certbot renew --quiet
cp -r /etc/letsencrypt/live /opt/api-urpe/certs/
docker compose -f docker-compose.production.yml kill -s HUP nginx
EOF

chmod +x /opt/api-urpe/scripts/renew-ssl.sh

# Add cron job (ejecutar a las 3 AM todos los días)
echo "0 3 * * * /opt/api-urpe/scripts/renew-ssl.sh >> /var/log/api-urpe-ssl-renewal.log 2>&1" | crontab -
```

## Paso 9: Monitoring & Logs

```bash
# View logs en tiempo real
docker compose logs -f api worker

# Check disk usage
docker system df

# Prune old images (monthly)
docker image prune -a

# Backup database (daily)
cat > /opt/api-urpe/scripts/backup-db.sh << 'EOF'
#!/bin/bash
DATE=$(date +%Y%m%d_%H%M%S)
BACKUP_DIR="/opt/api-urpe/backups"
mkdir -p $BACKUP_DIR

docker compose exec -T db pg_dump \
  -U api_user api_urpe | gzip > $BACKUP_DIR/api_urpe_$DATE.sql.gz

# Keep only last 7 days
find $BACKUP_DIR -name "api_urpe_*.sql.gz" -mtime +7 -delete
EOF

chmod +x /opt/api-urpe/scripts/backup-db.sh

# Add to crontab (1 AM every day)
echo "0 1 * * * /opt/api-urpe/scripts/backup-db.sh" | crontab -
```

## Troubleshooting

### API no arranca
```bash
# Check logs
docker compose logs api

# Verify database connectivity
docker compose exec api npm run prisma:studio

# Check Redis
docker compose exec redis redis-cli ping
```

### Requests lentos
```bash
# Check database performance
docker compose exec db psql -U api_user api_urpe -c "SELECT * FROM pg_stat_statements LIMIT 10;"

# Check Redis
docker compose exec redis redis-cli INFO stats
```

### SSL issues
```bash
# Verify certificate
openssl s_client -connect api.urpeailab.com:443

# Check renewal logs
cat /var/log/letsencrypt/letsencrypt.log
```

## Checklist de Producción

- [ ] Database backups configurados
- [ ] SSL certificate válido
- [ ] Email SMTP probado (test email)
- [ ] Admin user creado
- [ ] CORS origins configurados correctamente
- [ ] Logs centralizados (opcional: ELK, DataDog)
- [ ] Monitoring de salud (opcional: Uptime Robot)
- [ ] Rate limiting activo
- [ ] Firewall configurado (solo puertos 80, 443)
- [ ] SSH keys configuradas (no password login)
- [ ] fail2ban instalado para brute-force protection
- [ ] Documentación accesible
- [ ] Plan de rollback listo

---

**Última actualización:** 2026-01-29
