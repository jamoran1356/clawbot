#!/bin/sh
set -e

CONFIG_FILE="/root/.clawdbot/clawdbot.json"
MODEL_DEFAULT="openrouter/anthropic/claude-3.5-sonnet"

if [ -f "$CONFIG_FILE" ]; then
  # Update the primary model in-place while preserving the rest of the config.
  python3 - "$CONFIG_FILE" "$MODEL_DEFAULT" <<'PY'
import json
import sys

path = sys.argv[1]
model = sys.argv[2]

with open(path, "r", encoding="utf-8") as f:
    data = json.load(f)

data.setdefault("agents", {}).setdefault("defaults", {}).setdefault("model", {})
current = data["agents"]["defaults"]["model"].get("primary")

if not current or "haiku" in current:
    data["agents"]["defaults"]["model"]["primary"] = model

with open(path, "w", encoding="utf-8") as f:
    json.dump(data, f, ensure_ascii=False, indent=2)
    f.write("\n")
PY
fi

exec "$@"
