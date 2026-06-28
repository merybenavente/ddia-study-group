# Chapter 7 — Sharding

**DDIA 2nd Edition, Chapter 7**

> "Clearly, we must break away from the sequential and not limit the computers. We must state definitions and provide for priorities and descriptions of data. We must state relationships, not procedures."

## Topics

- Why shard: scalability beyond a single node, pros and cons of sharding vs staying single-node
- Sharding for multitenancy: resource isolation, permission isolation, cell-based architecture, regulatory compliance, gradual schema rollout
- Sharding of key-value data: partition keys, skew, hot spots
- Sharding by key range: sorted keys, range queries, hot spots from sequential writes, rebalancing by splitting
- Sharding by hash of key: hash functions, hash modulo N (and why it's bad), fixed number of shards, hash-range sharding, consistent hashing
- Skewed workloads and relieving hot spots: splitting hot keys, application-level techniques
- Operations: automatic vs manual rebalancing, cascading failure risks
- Request routing: routing tier, ZooKeeper/etcd coordination, gossip protocols, DNS
- Sharding and secondary indexes: local (document-partitioned) vs global (term-partitioned) secondary indexes, scatter/gather queries

## Assignment

Design the sharding strategy for a large-scale social media analytics platform. The platform ingests events (posts, likes, comments, shares) from 50 million users and serves both real-time dashboards ("trending now") and historical analytics queries ("engagement by region over the last 90 days"). The data volume has outgrown a single database node, and queries are slowing down as the dataset grows.

1. **Theory pass** — conversational interview on sharding strategies, partition key selection, rebalancing, hot spots, and secondary index tradeoffs
2. **Design pass** — produce a `DESIGN.md`: choose partition keys for each data type (events, user profiles, aggregations), design the sharding scheme (range vs hash, fixed vs dynamic shards), plan rebalancing strategy, handle secondary indexes for analytics queries, design request routing. Include rejected alternatives with reasoning.
3. **Implementation pass** — build a working prototype that demonstrates sharding with request routing and rebalancing
4. **Review** — defend your reasoning in a reviewer session

## Scenario

You're a senior engineer at a social media analytics company. Your platform processes events from 50 million users across a social network: every post, like, comment, share, and profile view is ingested and stored. The system serves two main workloads:

- **Real-time dashboards**: show what's trending right now — the most-liked posts in the last hour, viral content spreading across regions, and live engagement metrics. These queries need to respond within 200ms.
- **Historical analytics**: marketers and content teams run queries like "show me engagement by age group and region for the last 90 days" or "which content categories grew fastest last quarter." These queries can take a few seconds but shouldn't take minutes.

The current setup is a single PostgreSQL instance with 8TB of data, growing by ~50GB per day. The events table alone has 12 billion rows. Queries that used to take 500ms now take 15 seconds, and some analytical queries time out entirely. Adding more read replicas helped for a while, but write throughput is now also hitting limits — the single leader can't keep up during peak hours (200,000 events per second).

Your team has decided that sharding is necessary. Walk me through how you'd design the sharding strategy for this system.
