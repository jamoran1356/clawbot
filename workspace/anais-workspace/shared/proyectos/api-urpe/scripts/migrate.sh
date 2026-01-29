#!/bin/bash
# scripts/migrate.sh
# Ejecuta migraciones de base de datos Prisma
# Uso: ./scripts/migrate.sh [ambiente]

set -e

ENVIRONMENT=${1:-development}

echo "🗄️  Starting database migration for environment: $ENVIRONMENT"

# Cargar variables de entorno según ambiente
if [ "$ENVIRONMENT" != "production" ]; then
  # Development/Staging
  echo "📦 Generating Prisma client..."
  npx prisma generate

  echo "🚀 Running migrations..."
  npx prisma migrate dev --name auto_migration

  echo "✅ Migration completed successfully"
  echo "💡 Tip: Use 'npm run prisma:studio' to explore the database"
else
  # Production (usar deploy sin crear nuevas migraciones)
  echo "⚠️  PRODUCTION MODE - Using prisma migrate deploy"
  npx prisma migrate deploy

  echo "✅ Production migration completed"
fi

echo "🎉 Database is ready!"
