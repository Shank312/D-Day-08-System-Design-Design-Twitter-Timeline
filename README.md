

# Twitter Timeline System Design (Starter)

A reference implementation of a Twitter-like **timeline** using a **hybrid fanout** approach (fanout-on-write to HTL for normals, fanout-on-read for celebs), with FastAPI microservices, Kafka, Cassandra, and Redis.

## Features
- Tweet write path with durable ID generation (Snowflake-like).
- Hybrid fanout service over Kafka topics.
- Home/User timeline reads with simple recency + score ranking.
- Follow graph operations.
- Counters (likes) with eventual consistency.
- OpenAPI spec, k6 & Locust load tests, Docker Compose for local dev.

## Quick Start
```bash
cp configs/app.example.env .env
make dev   # docker compose up (infra + services)
