

# ADR-0001: Hybrid Fanout (Write for normals, Read for celebs)

## Status
Accepted

## Context
Pure fanout-on-write causes massive write amp for high-degree users; pure fanout-on-read increases read latency.

## Decision
Adopt **hybrid fanout**:
- **Normals**: fanout-on-write to HTL (Redis/Cassandra).
- **Celebs**: fanout-on-read; HTL stores a marker to fetch from author bucket at read time.

## Consequences
- Bounded write load for celebs.
- Slightly higher read complexity; mitigated by caching and ranker precompute windows.
