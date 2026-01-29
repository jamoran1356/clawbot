# Package.json Updates

## Agregar estas dependencias al package.json

```json
{
  "dependencies": {
    // Existentes - NO CAMBIAR
    "@nestjs/bullmq": "^11.0.4",
    "@nestjs/common": "^10.4.20",
    "@nestjs/config": "^3.3.0",
    "@nestjs/core": "^10.4.20",
    "@nestjs/jwt": "^10.2.0",
    "@nestjs/passport": "^10.0.3",
    "@nestjs/platform-express": "^10.4.20",
    "@node-rs/argon2": "^2.0.2",
    "axios": "^1.13.2",
    "bullmq": "^5.66.4",
    "class-transformer": "^0.5.1",
    "class-validator": "^0.14.1",
    "nanoid": "^5.1.6",
    "nodemailer": "^7.0.12",
    "passport": "^0.7.0",
    "passport-jwt": "^4.0.1",
    "redis": "^4.7.1",
    "reflect-metadata": "^0.2.2",
    "rxjs": "^7.8.2",
    
    // NUEVAS - AGREGAR ESTAS
    "helmet": "^7.1.0",           // Security headers
    "joi": "^17.11.0",             // Env validation
    "ipaddr.js": "^2.2.0",         // IP validation
    "winston": "^3.11.0",          // Structured logging
    "@nestjs/throttler": "^4.1.1" // Rate limiting
  },
  
  "devDependencies": {
    // Existentes
    "@nestjs/cli": "^11.0.14",
    "@nestjs/schematics": "^11.0.9",
    "@prisma/client": "^5.22.0",
    "@types/express": "^5.0.6",
    "@types/node": "^25.0.3",
    "@types/nodemailer": "^7.0.5",
    "@types/passport-jwt": "^4.0.1",
    "prisma": "^5.22.0",
    "typescript": "^5.9.3",
    
    // NUEVAS - AGREGAR ESTAS
    "@nestjs/testing": "^10.4.20",  // Para tests
    "@types/jest": "^29.5.10",      // Jest types
    "@types/ipaddr.js": "^1.0.1",   // ipaddr types
    "jest": "^29.7.0"                // Testing framework
  }
}
```

## Comando para instalar

```bash
cd /workspace/anais-workspace/shared/proyectos/api-urpe

# Con pnpm (recomendado)
pnpm add helmet joi ipaddr.js winston @nestjs/throttler
pnpm add -D @nestjs/testing @types/jest @types/ipaddr.js jest

# O con npm
npm install helmet joi ipaddr.js winston @nestjs/throttler
npm install -D @nestjs/testing @types/jest @types/ipaddr.js jest

# O con yarn
yarn add helmet joi ipaddr.js winston @nestjs/throttler
yarn add -D @nestjs/testing @types/jest @types/ipaddr.js jest
```

## Verificar instalación

```bash
npm list helmet joi ipaddr.js winston @nestjs/throttler
```

Deberías ver todas con versiones @latest o similares.
