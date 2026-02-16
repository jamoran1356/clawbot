#!/bin/sh
set -e

CONFIG_DIR="/root/.clawdbot"
CONFIG_FILE="$CONFIG_DIR/clawdbot.json"

mkdir -p "$CONFIG_DIR"

if [ ! -f "$CONFIG_FILE" ]; then
  echo "Creating clawdbot config from ENV..."

  cat <<EOF > "$CONFIG_FILE"
{
  "gateway": {
    "mode": "${GATEWAY_MODE:-local}"
  },
  "agents": {
    "defaults": {
      "model": {
        "primary": "${MODEL:-openrouter/anthropic/claude-3.5-sonnet}"
      }
    }
  },
  "api_keys": {
    "brave": "${BRAVE_API_KEY}",
    "openrouter": "${OPENROUTER_API_KEY}"
  }
}
EOF
fi

exec "$@"
