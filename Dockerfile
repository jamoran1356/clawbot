FROM node:22-alpine

# Instalar dependencias del sistema
RUN apk add --no-cache \
    git \
    python3 \
    py3-pip \
    docker-cli

# Instalar clawbot
RUN npm i -g clawdbot

# Crear directorio de trabajo
RUN mkdir -p /workspace

# Configurar usuario y permisos
WORKDIR /workspace

# Exponer puertos
EXPOSE 19000

# Comando por defecto
CMD ["clawdbot", "gateway", "run", "--bind", "lan", "--port", "19000"]
