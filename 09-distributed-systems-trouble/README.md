# Chapter 9 — The Trouble with Distributed Systems

**DDIA 2nd Edition, Chapter 9**

> "They're funny things, Accidents. You never have them till you're having them."

## Topics

- Faults and partial failures: deterministic single-node behavior vs nondeterministic distributed behavior, partial failures, the challenge of not knowing whether something succeeded
- Unreliable networks: asynchronous packet networks, request/response failures (lost requests, queued requests, crashed nodes, lost responses), the impossibility of distinguishing failure modes
  - The limitations of TCP: congestion control, flow control, backpressure, why TCP "reliability" doesn't eliminate network unreliability at the application level
  - Network faults in practice: frequency of network faults in datacenters, asymmetric faults, the need for deliberate fault testing
  - Fault detection: load balancers, leader failover, explicit crash notifications, ICMP limitations, timeouts as the only reliable option
  - Timeouts and unbounded delays: the tradeoff between premature declarations and slow detection, cascading failures from aggressive timeouts
  - Network congestion and queueing: switch queue saturation, OS-level queueing, VM scheduling delays, TCP sender-side queueing
  - TCP vs UDP: tradeoff between reliability and latency variability
  - Synchronous vs asynchronous networks: circuit-switched (bounded delay) vs packet-switched (unbounded delay), why datacenter networks use packet switching (bursty traffic, better utilization), static vs dynamic resource partitioning
- Unreliable clocks: why time matters in distributed systems (durations vs points in time), NTP synchronization and its limitations
  - Monotonic vs time-of-day clocks: wall-clock time (CLOCK_REALTIME), monotonic clocks (CLOCK_MONOTONIC), why monotonic clocks are safe for measuring durations but time-of-day clocks are not
  - Clock synchronization and accuracy: quartz drift, NTP limitations (network delay, misconfigured servers, leap seconds), VM clock virtualization issues, GPS and PTP for high accuracy
  - Relying on synchronized clocks: the danger of silent clock failures, the need for monitoring clock offsets
  - Timestamps for ordering events: last write wins (LWW) and clock skew, why LWW can silently lose data, logical clocks vs physical clocks
  - Clock readings with a confidence interval: timestamps as ranges not points, Google Spanner's TrueTime API, Amazon ClockBound
  - Synchronized clocks for global snapshots: MVCC and transaction IDs across distributed databases, Spanner's approach to snapshot isolation using clock confidence intervals
  - Process pauses: lease expiration dangers, GC pauses, VM suspension, context switches, disk I/O, swapping/paging, SIGSTOP, why a node must assume it can be paused at any point
  - Providing response time guarantees: real-time operating systems (RTOS) vs regular systems, why real-time constraints are impractical for most data systems
  - Limiting the impact of garbage collection: language-level solutions (Rust, Swift), treating GC pauses as planned outages, short-lived object collection strategies
- Knowledge, truth, and lies: the philosophical challenge of knowing system state when the only source of information is unreliable messages
  - The majority rules: asymmetric faults, nodes declared dead despite being alive, quorum-based decision making, majority voting
  - Distributed locks and leases: lease expiration bugs, process pause + expired lease = split brain, fencing tokens as the solution
  - Fencing off zombies and delayed requests: monotonically increasing tokens, STONITH, conditional writes (Amazon S3, Azure Blob Storage), fencing with multiple replicas using token-embedded timestamps
  - Byzantine faults: nodes that actively lie or send corrupted data, the Byzantine Generals Problem, when Byzantine fault tolerance matters (aerospace, blockchains, peer-to-peer), when it doesn't (controlled datacenter environments), weak forms of Byzantine protection (checksums, input validation)
  - System model and reality: three timing models (synchronous, partially synchronous, asynchronous), three node failure models (crash-stop, crash-recovery, Byzantine), mapping models to real systems
  - Correctness of algorithms: defining correctness via properties (safety and liveness), the distinction between safety properties (nothing bad happens) and liveness properties (something good eventually happens)
  - Formal methods and randomized testing: model checkers, property-based testing, Jepsen, fault injection frameworks

## Assignment

Design a distributed lock service for coordinating access to shared resources across a microservices architecture. The lock service must provide mutual exclusion guarantees despite network partitions, process pauses, and clock skew. Your system needs to handle the fundamental problems this chapter identifies: you cannot trust the network, you cannot trust the clocks, and you cannot even trust that a process is still running when it believes it holds a lock.

1. **Theory pass** — conversational interview on network unreliability, clock unreliability, process pauses, partial failures, truth and knowledge in distributed systems, and fencing mechanisms
2. **Design pass** — produce a `DESIGN.md`: choose a system model (timing assumptions, failure model), design the lock acquisition and release protocol, implement fencing tokens to prevent split-brain scenarios, define timeout and lease strategies, handle network partition behavior, specify what guarantees your system provides and what it explicitly does not. Include rejected alternatives with reasoning.
3. **Implementation pass** — build a working prototype that demonstrates lock acquisition, lease expiration, fencing token validation, and behavior under simulated faults (network delays, process pauses, clock skew)
4. **Review** — defend your reasoning in a reviewer session

## Scenario

You're a platform engineer at a fintech company that processes payments across a microservices architecture. The system has 12 backend services running across 3 availability zones, processing about 50,000 payment transactions per hour. Several of these services need to coordinate access to shared resources — for example, only one service instance should process a given payment at a time, only one instance should run the end-of-day reconciliation batch job, and only one instance should hold the "leader" role for each customer account shard.

The team has been using Redis-based locks (SETNX with TTL) for coordination, but they've been hit by three incidents in the past quarter:

1. **Double-processing**: during a GC pause on one service instance, its lock expired, another instance acquired the lock and started processing the same payment. When the paused instance resumed, it completed its processing too — resulting in a duplicate charge to the customer. The fenced token mechanism described in the chapter would have prevented this.
2. **Split-brain leader election**: after a network partition between availability zones, two instances both believed they were the leader for the same account shard. Both accepted writes, leading to conflicting state that required manual reconciliation. The issue was that the lock service couldn't distinguish between a slow node and a dead one.
3. **Clock skew TTL bug**: one service instance had a clock that was 30 seconds ahead of the Redis server. Its lock appeared to have 60 seconds remaining from the service's perspective, but Redis had already expired it. Another instance acquired the lock while the first still believed it held it.

Leadership wants you to redesign the distributed locking strategy. They want to understand what guarantees are actually achievable given the realities of unreliable networks, clocks, and processes — and what tradeoffs you're making.

Walk me through how you'd design a distributed lock service that handles these failure modes.
