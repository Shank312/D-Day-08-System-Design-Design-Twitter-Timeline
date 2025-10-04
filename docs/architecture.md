

# Architecture

This system implements a **hybrid fanout** timeline:
- **Fanout-on-write** to Home Timeline (HTL) for most users.
- **Fanout-on-read** for celebrities/high-degree nodes to avoid massive write amplification.

Core components:
- **Gateway** (FastAPI): Auth, routing.
- **Tweet Write**: Validates + writes tweet to Cassandra; emits `tweet_created` to Kafka.
- **Fanout**: Consumes `tweet_created`, fetches author degree from Graph, decides:
  - If normal: push to followers' HTL (Redis/Cassandra).
  - If celeb: mark as celeb in HTL or defer to read-path.
- **Timeline Read**: Reads HTL/UTL, queries Ranker, merges recency + score.
- **Graph**: Manage follow/unfollow; degree queries.
- **Counters**: Like events aggregation (Kafka); eventual consistency updates.
- **IDGen**: Snowflake-compatible IDs.
- **Search**: Stub for indexing tweets.

See diagram below (Mermaid source in `docs/diagrams/architecture.mmd`):

```mermaid
%%{init: {'theme':'neutral'}}%%
flowchart LR
  GW[Gateway] --> TW[Tweet Write]
  TW -->|Kafka: tweet_created| FO[Fanout]
  FO -->|HTL updates| HTL[(Redis/Cassandra)]
  GW --> TR[Timeline Read]
  TR --> HTL
  TR --> RK[Ranker]
  GW --> GR[Graph]
  GW --> CT[Counters]
  GW --> ID[IDGen]
  TW --> DB[(Cassandra)]
  GR --> DB
  CT --> DB
