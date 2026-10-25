#!/usr/bin/env bash
set -euo pipefail

curl -fsS -X DELETE http://localhost:8083/connectors/analytics-orders >/dev/null 2>&1 || true

curl -fsS -X POST http://localhost:8083/connectors \
  -H 'Content-Type: application/json' \
  -d '{
    "name": "analytics-orders",
    "config": {
      "connector.class": "io.debezium.connector.postgresql.PostgresConnector",
      "database.hostname": "host.docker.internal",
      "database.port": "5432",
      "database.user": "debezium",
      "database.password": "debezium",
      "database.dbname": "analytics",
      "topic.prefix": "analytics",
      "plugin.name": "pgoutput",
      "publication.name": "analytics_pub",
      "publication.autocreate.mode": "disabled",
      "slot.name": "debezium_analytics",
      "table.include.list": "public.orders"
    }
  }'

echo
echo "Debezium connector analytics-orders registered."
