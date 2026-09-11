# Chapter 12 — Stream Processing

**DDIA 2nd Edition, Chapter 12**

> "A complex system that works is invariably found to have evolved from a simple system that works. The inverse proposition also appears to be true: A complex system designed from scratch never works and cannot be made to work."

## Topics

- From batch to stream: bounded vs unbounded data, artificial time-slicing of batch jobs, events as the streaming counterpart of records (small, self-contained, immutable, timestamped), producers/consumers, topics and streams, why polling a datastore doesn't scale and consumers need notification
- Transmitting event streams: messaging systems and the two defining questions (what happens when producers outpace consumers — drop, buffer, or backpressure; what happens when nodes crash — are messages lost?)
  - Direct messaging from producers to consumers: UDP multicast for stock market feeds, brokerless libraries (ZeroMQ, nanomsg), StatsD-style unreliable metrics collection, webhooks; why direct messaging assumes everyone is constantly online
  - Message brokers: broker as a database optimized for message streams, asynchronous consumption, durability moved to the broker
  - Message brokers compared to databases: deletion after delivery, small working-set assumption, topic-pattern subscription vs query languages, notification vs point-in-time snapshots; JMS/AMQP standards and implementations (RabbitMQ, ActiveMQ, IBM MQ, Azure Service Bus, Google Cloud Pub/Sub)
  - Multiple consumers: load balancing (shared subscriptions) vs fan-out (topic subscriptions), combining both with Kafka consumer groups
  - Acknowledgments and redelivery: lost acks, how load balancing plus redelivery reorders messages, poison messages and dead letter queues (DLQs)
- Log-based message brokers: the hybrid of durable database storage and low-latency notification
  - Using logs for message storage: append-only logs, sharding a topic into partitions, monotonically increasing offsets, total order within a partition (but not across partitions); Apache Kafka, Amazon Kinesis Streams
  - Logs compared to traditional messaging: trivial fan-out, coarse-grained load balancing by assigning shards, parallelism limited by partition count, head-of-line blocking, when JMS/AMQP style is preferable vs when log-based wins, routing related events with a partition key
  - Consumer offsets: analogy with the log sequence number in single-leader replication (broker = leader, consumer = follower), reprocessing after failover
  - Disk space usage: segment deletion, the log as a circular buffer, back-of-the-envelope buffering capacity, tiered storage and object-storage-backed brokers (Kafka/Redpanda tiered storage, WarpStream, Bufstream, Iceberg tables)
  - When consumers cannot keep up: log-based buffering as a large fixed-size buffer, monitoring consumer lag, why one slow consumer doesn't disrupt others
  - Replaying old messages: consuming as a read-only operation, manipulating offsets to reprocess, log-based messaging as repeatable batch-like transformation
- Databases and streams: replication logs as event streams, state machine replication
  - Keeping systems in sync: heterogeneous data systems (OLTP database, cache, search index, data warehouse), ETL, dual writes and their failure modes (race conditions producing permanent inconsistency, partial failure without atomic commit)
  - Change data capture (CDC): making one database the leader and derived systems followers, transporting change events through a log-based broker, implementations (Debezium, Kafka Connect, Maxwell, GoldenGate, pgcapture), asynchrony and replication lag
  - Initial snapshots: consistent snapshot tied to a log offset, incremental snapshots (Netflix's DBLog watermarking)
  - Log compaction: keeping only the latest value per key, tombstones, rebuilding a derived system from offset 0 of a compacted topic
  - API support for change streams: first-class change streams in modern databases, CDC on quorum-based stores (Cassandra's raw per-node log segments)
  - CDC versus event sourcing: low-level state changes vs application-level intent events, why event-sourced logs can't be compacted the same way, snapshots as a performance optimization
  - CDC and database schemas: schemas becoming public APIs, breaking downstream consumers, data contracts, the outbox pattern (a deliberate dual write kept inside one transaction) and its trade-offs
- State, streams, and immutability: changelog as the evolution of state, state as the integral of an event stream (and streams as the derivative of state)
  - Advantages of immutable events: the accounting ledger analogy, compensating transactions, auditability, easier recovery from buggy code, capturing more than the current state (cart add/remove analytics)
  - Deriving several views from the same event log: multiple read-optimized representations, CQRS, side-by-side migration instead of schema migration, why normalization debates fade when write and read forms are separated
  - Concurrency control: asynchronous view updates and read-your-writes, single self-contained events making atomicity easy, single-threaded log consumers per shard needing no write concurrency control
  - Limitations of immutability: dataset churn and compaction/GC pressure, legal deletion requirements (GDPR), excision (Datomic) and shunning (Fossil), why truly deleting data is hard, crypto-shredding and its key-granularity problem
- Processing streams: three options (write to storage, push to humans, derive new streams), operators/jobs, what changes when input never ends (no sort-merge joins, restart-from-scratch fault tolerance no longer viable)
  - Uses of stream processing: monitoring (fraud detection, trading, manufacturing), complex event processing (CEP — stored queries matching against passing events, Esper, Apama), stream analytics (rates, rolling averages, windows; probabilistic algorithms: Bloom filters, HyperLogLog, percentile estimation), frameworks (Storm, Spark Streaming, Flink, Samza, Beam, Kafka Streams; Google Cloud Dataflow, Azure Stream Analytics)
  - Maintaining materialized views: windows that stretch back to the beginning of time, incremental view maintenance (IVM) vs periodic REFRESH, IVM databases (Materialize, RisingWave, ClickHouse, Feldera)
  - Search on streams: stored queries evaluated against documents (Elasticsearch percolator), media monitoring
  - Event-driven architectures and RPC: actor frameworks vs stream processors, distributed RPC in Storm
- Reasoning about time: event time vs processing time, why windowing by processing time creates artifacts (backlog processing looks like a request spike), the Star Wars analogy
  - Handling straggler events: when is a window complete, dropping stragglers vs publishing corrections/retractions, special "no more messages before t" watermark-style messages and their multi-producer complications
  - Whose clock are you using: buffered mobile events, untrusted device clocks, the three-timestamp technique for estimating clock offset
  - Types of windows: tumbling, hopping, sliding, session windows; window state and its memory/disk cost
- Stream joins: why unbounded input makes joins harder
  - Stream–stream joins (window joins): search/click click-through-rate example, buffering events indexed by join key, emitting on match or expiry
  - Stream–table joins (enrichment): remote lookup vs local copy (hash join), keeping the local copy fresh via CDC, the conceptually infinite window on the table side
  - Table–table joins (materialized view maintenance): the social-network timeline cache, joins over two changelogs, the product rule (u·v)′ = u′v + uv′
  - Time dependence of joins: nondeterministic joins when cross-stream ordering is undefined, slowly changing dimensions (SCD), versioned record identifiers vs denormalizing the joined value into the event
- Fault tolerance and exactly-once semantics: why "wait until finished" doesn't work for infinite streams, exactly-once (effectively-once) semantics
  - Microbatching (Spark Streaming) and checkpointing (Flink's barrier-triggered rolling checkpoints), why both break down once output leaves the framework (external side effects happen twice)
  - Atomic commit revisited: making outputs, state changes, and offset acknowledgments atomic; restricted-environment implementations (Google Cloud Dataflow, VoltDB, Kafka transactions) vs heterogeneous XA
  - Idempotence: naturally idempotent operations, adding metadata (writing the message offset alongside the value), the assumptions it relies on (deterministic processing, ordered replay, no concurrent updaters, fencing)
  - Rebuilding state after a failure: remote replicated state vs local state replicated periodically, Flink snapshots to durable storage, Kafka Streams changelog topics with log compaction, VoltDB redundant processing, rebuilding from input streams

## Assignment

Design the streaming data integration and processing pipeline for an e-commerce platform. A single system-of-record database feeds several derived data systems (a search index, a cache, and a real-time analytics view), and the pipeline must also compute windowed aggregations over an order-event stream. Your design has to confront this chapter's core problems: getting changes out of a database without dual writes, preserving ordering where it matters, rebuilding a derived view from scratch, distinguishing event time from processing time, handling stragglers, and ensuring that a crashed and restarted processor doesn't lose events or apply their effects twice.

1. **Theory pass** — conversational interview on messaging system trade-offs (AMQP/JMS-style vs log-based brokers), partitioning and ordering, consumer offsets and redelivery, change data capture vs event sourcing, log compaction, event time vs processing time, window types, the three kinds of stream joins, and exactly-once semantics
2. **Design pass** — produce a `DESIGN.md`: choose a messaging model and justify it against the alternatives, decide how changes get out of the source database and in what order, pick partitioning keys and state where ordering is and isn't guaranteed, design the rebuild path for a new or corrupted derived view, define your timestamping and windowing strategy including straggler handling, design the join(s) your analytics require, and specify your fault-tolerance mechanism — what happens at every point a processor can crash, and what guarantee the output actually carries. Include rejected alternatives with reasoning.
3. **Implementation pass** — build a working prototype that demonstrates change events flowing from a source of record to at least two derived views, a windowed aggregation using event time, replay/rebuild of a derived view from the log, and correct behavior under simulated faults (consumer crash mid-batch, duplicate delivery, out-of-order and straggler events)
4. **Review** — defend your reasoning in a reviewer session

## Scenario

You're a staff engineer at an online marketplace that handles about 2 million orders per day across 40,000 merchants. The system of record is a PostgreSQL cluster; around it sit an Elasticsearch cluster for product search, a Redis cache for product pages, and a real-time analytics dashboard that merchants use to watch their sales. Application code currently keeps all of these in sync by writing to each system directly, and a fleet of consumers processes an order-event stream for notifications and metrics.

The past two quarters have produced three incidents that keep coming up in postmortems:

1. **Permanently inconsistent search results**: two admin tools updated the same product's price within milliseconds of each other. The database applied the writes in one order and the search index applied them in the other, so search showed one price and checkout charged another — for three weeks, until a customer complaint surfaced it. No error was ever logged. This is the classic dual-write race condition: two systems, no single leader deciding the order of writes.
2. **The phantom flash sale**: a routine redeploy took the metrics consumer offline for four minutes. When it came back, it churned through the backlog, and because the pipeline windows by processing time rather than event time, the merchant dashboard showed a massive order spike. The anomaly detector fired, on-call was paged, and one large merchant halted their ad spend over "suspicious traffic" that never existed.
3. **The double-shipment email storm**: a notification consumer crashed after sending "your order has shipped" emails for a batch of messages but before committing its consumer offset. On restart, it reprocessed the batch and re-sent roughly 18,000 emails. The same reprocessing double-counted revenue in the analytics view, which had to be manually corrected.

Leadership has approved a project to rebuild data integration and stream processing around a single, coherent architecture. They want derived systems that are guaranteed to converge with the database, merchant-facing metrics that are correct even during backlogs and reprocessing, and side effects that happen exactly once from the customer's point of view — and they want to know precisely which guarantees are real and which are best-effort.

Walk me through how you'd design the streaming data integration and processing pipeline for this system.
