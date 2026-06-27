# System Design Interview — Sharding

## The scenario

You're a senior engineer at a social media analytics company. Your platform processes events from 50 million users across a social network: every post, like, comment, share, and profile view is ingested and stored. The system serves two main workloads:

- **Real-time dashboards**: show what's trending right now — the most-liked posts in the last hour, viral content spreading across regions, and live engagement metrics. These queries need to respond within 200ms.
- **Historical analytics**: marketers and content teams run queries like "show me engagement by age group and region for the last 90 days" or "which content categories grew fastest last quarter." These queries can take a few seconds but shouldn't take minutes.

The current setup is a single PostgreSQL instance with 8TB of data, growing by ~50GB per day. The events table alone has 12 billion rows. Queries that used to take 500ms now take 15 seconds, and some analytical queries time out entirely. Adding more read replicas helped for a while, but write throughput is now also hitting limits — the single leader can't keep up during peak hours (200,000 events per second).

Your team has decided that sharding is necessary. Walk me through how you'd design the sharding strategy for this system.
