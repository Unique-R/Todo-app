#!/bin/bash

# Диагностика
echo "Checking for backup file..."
ls -la /tmp/ || echo "No /tmp directory"
ls -la /backup/ || echo "No /backup directory"

# Ждем готовности БД
until pg_isready -U $POSTGRES_USER -d $POSTGRES_DB; do
  sleep 1
done

# Проверяем оба возможных пути
if [ -f /tmp/backup.sql ]; then
    echo "Restoring from /tmp/backup.sql..."
    psql -U $POSTGRES_USER -d $POSTGRES_DB -f /tmp/backup.sql
elif [ -f /backup/backup.sql ]; then
    echo "Restoring from /backup/backup.sql..."
    psql -U $POSTGRES_USER -d $POSTGRES_DB -f /backup/backup.sql
else
    echo "No backup found, loading default data..."
    psql -U $POSTGRES_USER -d $POSTGRES_DB -c "
    INSERT INTO users (username, password) VALUES 
    ('igor', 'passwd'),
    ('testuser', 'testpass')
    ON CONFLICT (username) DO NOTHING;
    "
fi
