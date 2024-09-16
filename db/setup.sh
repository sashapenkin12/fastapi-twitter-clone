set -e

psql -v ON_ERROR_STOP=1 --username "$POSTGRES_USER" --dbname "$POSTGRES_DB" <<-EOSQL
  ALTER SYSTEM SET log_destination TO 'stderr';
  ALTER SYSTEM SET logging_collector TO 'on';
  ALTER SYSTEM SET log_directory TO '/var/log/postgresql';
EOSQL
