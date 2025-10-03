#Todo-app
Test CI/CD

# Todo App with PostgreSQL Replication

Простое Flask приложение с настройкой master-slave репликации PostgreSQL.

## Архитектура
- **Web**: Nginx как reverse proxy
- **App**: Flask + Gunicorn  
- **DB Master**: PostgreSQL с репликацией
- **DB Replica**: Read-only реплика

## Запуск
```bash
docker-compose up -d
