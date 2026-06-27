# Chapter 6 — Replication

**DDIA 2nd Edition, Chapter 6**

> "The major difference between a thing that might go wrong and a thing that cannot possibly go wrong is that when a thing that cannot possibly go wrong goes wrong, it usually turns out to be impossible to get at or repair."

## Topics

- Why replicate: availability, durability, latency, read scalability
- Single-leader replication: leader/follower model, synchronous vs asynchronous replication, semisynchronous, setting up new followers, handling node outages (follower catch-up, leader failover, split brain)
- Implementation of replication logs: statement-based, WAL shipping, logical (row-based) log replication
- Problems with replication lag: eventual consistency, read-your-writes, monotonic reads, consistent prefix reads
- Solutions for replication lag: reading from the leader, logical timestamps, causal consistency
- Multi-leader replication: geographically distributed operation, sync engines and local-first software, replication topologies (circular, star, all-to-all), dealing with conflicting writes (conflict avoidance, LWW, manual resolution, automatic resolution)
- CRDTs and operational transformation
- Leaderless replication: quorum reads and writes (w + r > n), read repair, hinted handoff, anti-entropy, limitations of quorum consistency, sloppy quorums
- Detecting concurrent writes: happens-before relation, version vectors, capturing causal dependencies

## Assignment

Design the replication strategy for a collaborative note-taking application (like Google Docs or Notion) that supports both online real-time editing and offline usage. Users can edit notes from multiple devices, and the system needs to handle conflicting edits gracefully. The application must work across multiple geographic regions with low latency for reads and writes.

1. **Theory pass** — conversational interview on replication models, consistency guarantees, conflict resolution, and the tradeoffs between them
2. **Design pass** — produce a `DESIGN.md`: choose replication topology for each part of the system (user metadata, document content, edit history), define consistency guarantees per use case, design conflict resolution for concurrent edits, explain what happens during various failure scenarios. Include rejected alternatives with reasoning.
3. **Implementation pass** — build a working prototype that demonstrates replication with conflict detection and resolution
4. **Review** — defend your reasoning in a reviewer session
