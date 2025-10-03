#!/bin/bash
echo "=== PostgreSQL Replication Status ==="

# Check master
echo "Master:"
docker-compose exec db-master psql -U postgres -c "
SELECT 
    client_addr,
    application_name,
    state,
    sync_state,
    write_lag,
    flush_lag,
    replay_lag
FROM pg_stat_replication;"

# Check replica
echo -e "\nReplica:"
docker-compose exec db-replica psql -U postgres -c "SELECT pg_is_in_recovery();"

echo -e "\nData sync test:"
docker-compose exec db-master psql -U postgres -d todo_db -c "SELECT COUNT(*) as master_users FROM users;"
docker-compose exec db-replica psql -U postgres -d todo_db -c "SELECT COUNT(*) as replica_users FROM users;"
