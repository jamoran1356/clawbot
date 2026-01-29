#!/bin/bash
# scripts/health-check.sh
# Verifica la salud de la API
# Uso: ./scripts/health-check.sh [url] [timeout]

set -e

API_URL=${1:-http://localhost:3000/api/v1/health}
TIMEOUT=${2:-5}

echo "🏥 Checking API health: $API_URL"

# Hacer solicitud HTTP
RESPONSE=$(curl -s -w "\n%{http_code}" --max-time $TIMEOUT "$API_URL" 2>&1 || echo -e "\n000")

# Separar response y status code
HTTP_STATUS=$(echo "$RESPONSE" | tail -n1)
BODY=$(echo "$RESPONSE" | head -n-1)

# Validar respuesta
if [ "$HTTP_STATUS" -ge 200 ] && [ "$HTTP_STATUS" -lt 300 ]; then
  echo "✅ API is healthy (HTTP $HTTP_STATUS)"
  echo ""
  echo "Response:"
  echo "$BODY" | jq . 2>/dev/null || echo "$BODY"
  exit 0
elif [ "$HTTP_STATUS" -ge 400 ] && [ "$HTTP_STATUS" -lt 500 ]; then
  echo "⚠️  API returned client error (HTTP $HTTP_STATUS)"
  echo "$BODY"
  exit 1
elif [ "$HTTP_STATUS" -ge 500 ]; then
  echo "❌ API returned server error (HTTP $HTTP_STATUS)"
  echo "$BODY"
  exit 1
else
  echo "❌ API is unreachable or timed out"
  exit 1
fi
