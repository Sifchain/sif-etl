#!/bin/bash
set -e
echo '****************IMPORTING SIFCHAIN DATA INTO TIMESCALEDB****************'
echo psql -v --username "$POSTGRES_USER" --dbname "$POSTGRES_DB" <<-EOSQL
\copy tokenprices FROM '001_tokenprices.csv' CSV HEADER;
\copy events_audit FROM '002_events_audit.csv' CSV HEADER;
\copy token_registry FROM '003_token_registry.csv' CSV HEADER;
\copy tokenvolumes FROM '004_tokenvolumes.csv' CSV HEADER;

EOSQL
