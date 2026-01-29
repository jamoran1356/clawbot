#!/bin/bash
# backup-db.sh - Daily database backup script

set -e

# Configuration
DATABASE_URL="${DATABASE_URL:-postgresql://api_user:password@localhost:5432/api_urpe}"
BACKUP_DIR="${BACKUP_DIR:-.}/backups"
RETENTION_DAYS="${RETENTION_DAYS:-7}"
DATE=$(date +%Y%m%d_%H%M%S)

# Extract connection details
DB_HOST=$(echo $DATABASE_URL | grep -oP '(?<=@)[^:/]+')
DB_PORT=$(echo $DATABASE_URL | grep -oP '(?<=:)[0-9]+(?=/)')
DB_USER=$(echo $DATABASE_URL | grep -oP '(?://)[^:]+' | sed 's|//||')
DB_NAME=$(echo $DATABASE_URL | grep -oP '[^/]*$')

# Create backup directory
mkdir -p "$BACKUP_DIR"

echo "📦 Starting database backup..."
echo "   Host: $DB_HOST"
echo "   Database: $DB_NAME"
echo "   Timestamp: $DATE"

# Perform backup
export PGPASSWORD=$(echo $DATABASE_URL | grep -oP '(?<=:)[^@]+(?=@)')

pg_dump \
  -h "$DB_HOST" \
  -p "${DB_PORT:-5432}" \
  -U "$DB_USER" \
  -d "$DB_NAME" \
  --format=custom \
  | gzip > "$BACKUP_DIR/api_urpe_$DATE.dump.gz"

echo "✅ Backup created: $BACKUP_DIR/api_urpe_$DATE.dump.gz"

# Cleanup old backups
echo "🧹 Cleaning up backups older than $RETENTION_DAYS days..."
find "$BACKUP_DIR" -name "api_urpe_*.dump.gz" -mtime +$RETENTION_DAYS -delete

echo "✨ Backup completed successfully!"
