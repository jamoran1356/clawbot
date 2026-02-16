FROM node:22-alpine

ARG CLAWDBOT_VERSION=latest

# Instalar dependencias del sistema incluyendo Chromium y PHP
RUN apk add --no-cache \
    git \
    python3 \
    py3-pip \
    docker-cli \
    chromium \
    chromium-chromedriver \
    nss \
    freetype \
    harfbuzz \
    ca-certificates \
    ttf-freefont \
    php \
    php-cli \
    php-curl \
    php-json \
    php-mbstring \
    php-xml \
    php-dom \
    php-openssl \
    php-phar \
    php-session \
    php-tokenizer \
    php-fileinfo \
    curl \
    wget \
    py3-requests \
    py3-beautifulsoup4

# Variable de entorno para Puppeteer
ENV PUPPETEER_SKIP_CHROMIUM_DOWNLOAD=true \
    PUPPETEER_EXECUTABLE_PATH=/usr/bin/chromium-browser

# Instalar clawbot
RUN npm i -g clawdbot@${CLAWDBOT_VERSION}

# Script de arranque para actualizar config persistente
COPY entrypoint.sh /usr/local/bin/clawbot-entrypoint.sh
RUN chmod +x /usr/local/bin/clawbot-entrypoint.sh

# Crear directorio de trabajo
RUN mkdir -p /workspace

# Configurar usuario y permisos
WORKDIR /workspace

# Exponer puertos
EXPOSE 19000

# Comando por defecto - usa la configuración de /root/.clawdbot/clawdbot.json
ENTRYPOINT ["/usr/local/bin/clawbot-entrypoint.sh"]
CMD ["clawdbot", "gateway", "run"]
