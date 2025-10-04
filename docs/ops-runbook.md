

# Ops Runbook

## SLOs
- HTL p50 < 80ms, p95 < 200ms (local/dev)
- Write latency p95 < 150ms

## Monitors
- Kafka consumer lag (Fanout)
- Redis/Cassandra read latencies
- Error rates by service

## Failure Handling
- Kafka outage: buffer writes in TweetWrite (retry/backoff)
- Redis miss: fallback to Cassandra HTL table
- Ranker down: degrade to recency ordering

## On-call Cheats
- Scale Fanout consumers on lag spikes
- Toggle celeb threshold via feature flag (ENV: CELEB_DEGREE_THRESHOLD)
