#!/bin/bash
# BUILD.sh - Compilar API-URPE

set -e

echo "🔨 Building API-URPE..."
echo ""

echo "📦 Step 1: Installing dependencies..."
npm install --legacy-peer-deps

echo ""
echo "🏗️  Step 2: Generating Prisma client..."
npx prisma generate

echo ""
echo "📦 Step 3: Building NestJS application..."
npm run build

echo ""
echo "✅ Build completed successfully!"
echo ""
echo "📁 Output: dist/"
echo ""
echo "Next steps:"
echo "  1. Copy .env.production to .env"
echo "  2. docker compose up -d"
echo "  3. curl http://localhost:3000/api/v1/health"
