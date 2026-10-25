# data-platform

A modern, containerized data engineering platform featuring CDC ingestion, streaming, data transformation, and lineage tracking.

## Architecture & Tech Stack
- **Ingestion & CDC:** Debezium CDC capturing change data streams
- **Streaming & Messaging:** Redpanda (Kafka-compatible event streaming)
- **Transformation:** dbt (data build tool) for modular dimensional modeling & schema testing
- **Metadata & Lineage:** Marquez / OpenLineage integration for end-to-end data governance
- **Database / Warehouse:** PostgreSQL & analytics schemas
