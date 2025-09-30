-- Создаем пользователя репликации
CREATE USER replicator WITH REPLICATION PASSWORD 'replicate123';

-- Настраиваем параметры репликации
ALTER SYSTEM SET wal_level = replica;
ALTER SYSTEM SET max_wal_senders = 10;
ALTER SYSTEM SET wal_keep_size = '1GB';
ALTER SYSTEM SET listen_addresses = '*';

-- Перезагружаем конфигурацию
SELECT pg_reload_conf();

-- Ждем применения настроек
SELECT pg_sleep(2);

-- Добавляем правило в pg_hba.conf через shell команду
\! echo "host replication replicator 0.0.0.0/0 md5" >> /var/lib/postgresql/data/pg_hba.conf

-- Еще раз перезагружаем конфигурацию
SELECT pg_reload_conf();
