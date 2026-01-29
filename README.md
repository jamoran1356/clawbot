# Clawbot - Instalación Simplificada

## Configuración
- **Puerto Gateway**: 19000
- **Workspace**: `./workspace` montado en `/workspace`
- **Acceso**: http://localhost:19000

## Pasos de Instalación

### 1. Crear carpeta de trabajo
```powershell
New-Item -Path .\workspace -ItemType Directory -Force
```

### 2. Construir y levantar contenedor
```powershell
docker compose up -d --build
```

### 3. ⚠️ PROBAR ACCESO A ARCHIVOS INMEDIATAMENTE
```powershell
# Crear archivo de prueba
"Test de acceso a archivos" | Out-File .\workspace\test.txt

# Verificar desde el contenedor
docker exec clawbot ls -la /workspace
docker exec clawbot cat /workspace/test.txt
```

### 4. Si el test funciona, inicializar clawbot
```powershell
docker exec -it clawbot clawdbot init
```

### 5. Configurar Gateway
```powershell
docker exec -it clawbot clawdbot gateway config --mode local --bind lan --port 19000
```

### 6. Ver logs
```powershell
docker logs -f clawbot
```

## Verificación
Abre: http://localhost:19000

## Comandos Útiles

### Reiniciar
```powershell
docker compose restart
```

### Ver estado
```powershell
docker compose ps
docker logs clawbot
```

### Entrar al contenedor
```powershell
docker exec -it clawbot sh
```

### Detener
```powershell
docker compose down
```

### Limpiar todo
```powershell
docker compose down -v --rmi all
```

## Estructura de Archivos
```
clawbot/
├── Dockerfile              # Imagen del contenedor
├── docker-compose.yml      # Orquestación
├── workspace/              # ⭐ Archivos compartidos
└── README.md              # Esta documentación
```

## ⚠️ IMPORTANTE
**ANTES de configurar Telegram o cualquier otra cosa, PRIMERO verifica que el bot puede ver archivos en /workspace.**

Si el bot no ve los archivos desde el inicio, ninguna configuración posterior lo arreglará.
