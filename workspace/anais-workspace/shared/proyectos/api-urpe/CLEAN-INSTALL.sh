#!/bin/bash
# CLEAN-INSTALL.sh - Limpia e instala todo desde cero

set -e

echo "🧹 Cleaning old installation..."
find node_modules -type f -exec chmod 644 {} \; 2>/dev/null || true
find node_modules -type d -exec chmod 755 {} \; 2>/dev/null || true
rm -rf node_modules pnpm-lock.yaml package-lock.json || true

echo "📦 Clearing npm cache..."
npm cache clean --force

echo "📥 Installing dependencies..."
npm install

echo "🔨 Generating Prisma client..."
npx prisma generate

echo "✅ Installation complete!"
echo ""
echo "Next: npm run build"
