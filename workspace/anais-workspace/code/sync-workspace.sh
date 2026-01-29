#!/bin/bash
# sync-workspace.sh - Sincronizar /workspace/anais-workspace bidireccional

WORKSPACE="/workspace/anais-workspace"
LOG="$WORKSPACE/.sync.log"

# Crear log si no existe
touch "$LOG"

echo "[$(date -u '+%Y-%m-%d %H:%M:%S UTC')] Sincronización iniciada" >> "$LOG"

# Sincronizar desde mi workspace local hacia shared
rsync -av --delete /root/clawd/ "$WORKSPACE/code/" 2>&1 | tee -a "$LOG"

# Sincronizar archivos compartidos por Jesús
rsync -av "$WORKSPACE/shared/" /root/clawd/shared/ 2>&1 | tee -a "$LOG"

echo "[$(date -u '+%Y-%m-%d %H:%M:%S UTC')] Sincronización completada" >> "$LOG"
