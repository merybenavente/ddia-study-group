# Chapter 8 — Transactions

**DDIA 2nd Edition, Chapter 8**

> "Some authors have claimed that general two-phase commit is too expensive to support, because of the performance or availability problems that it brings."

## Topics

- What is a transaction: grouping reads and writes into a logical unit, commit and abort, safety guarantees
- The meaning of ACID: atomicity (abortability), consistency (application invariants), isolation (concurrency), durability (persistence guarantees and their limits)
- Single-object vs multi-object operations: atomic writes, compare-and-set, the need for multi-object transactions
- Handling errors and aborts: retry pitfalls (duplicate side effects, overload amplification, lost client state)
- Weak isolation levels and their race conditions:
  - Read committed: no dirty reads, no dirty writes, implementation with row locks and old-value snapshots
  - Snapshot isolation and repeatable read: read skew, MVCC (multiversion concurrency control), visibility rules, indexes and snapshot isolation, naming confusion across databases
  - Preventing lost updates: atomic operations, explicit locking (SELECT FOR UPDATE), automatic detection, compare-and-set, conflict resolution in replicated databases
  - Write skew and phantoms: the check-then-act pattern, materializing conflicts
- Serializability — three approaches:
  - Actual serial execution: stored procedures, sharding for throughput, constraints and limitations
  - Two-phase locking (2PL): shared/exclusive locks, deadlocks, performance costs, predicate locks, index-range locks
  - Serializable snapshot isolation (SSI): optimistic concurrency control, detecting stale MVCC reads, detecting writes that affect prior reads, performance tradeoffs
- Distributed transactions:
  - Two-phase commit (2PC): coordinator, prepare/commit phases, the commit point, coordinator failure, in-doubt transactions
  - XA transactions: the standard, holding locks while in doubt, coordinator as single point of failure
  - Database-internal vs heterogeneous distributed transactions
  - Exactly-once message processing: idempotency via message IDs

## Assignment

Design the concurrency control and transaction strategy for an online event ticketing platform. The platform sells tickets for concerts, sports events, and theater shows. It must handle bursts of concurrent purchases (popular events sell out in seconds), enforce seat inventory constraints, process payments atomically with ticket reservations, and provide consistent views of seat availability to users browsing the system.

Your job is to choose isolation levels, design the transaction boundaries, prevent race conditions, and reason through what happens when things go wrong.

1. **Theory pass** — conversational interview on ACID guarantees, isolation levels, race conditions (dirty reads, lost updates, write skew, phantoms), and serializability approaches
2. **Design pass** — produce a `DESIGN.md`: choose isolation levels for each operation (browsing availability, reserving seats, processing payments), define transaction boundaries, identify and prevent specific race conditions (double-selling, lost updates on seat counts, phantom bookings), design the distributed transaction strategy for payment+reservation atomicity. Include rejected alternatives with reasoning.
3. **Implementation pass** — build a working prototype that demonstrates concurrency control with observable race conditions under weak isolation and their prevention under stronger isolation
4. **Review** — defend your reasoning in a reviewer session

## Scenario

You're a backend engineer at a ticketing company that sells tickets for live events. The platform handles about 2,000 events per month, with total sales of ~500,000 tickets per month. Most of the time, traffic is moderate — a few hundred concurrent users browsing and buying. But when a popular artist announces a tour, tens of thousands of users hit the system simultaneously, and 50,000 tickets can sell out in under 90 seconds.

The system has three main operations:

- **Browse availability**: users view which seats or ticket tiers are available for an event. This is read-heavy and needs to be fast, but showing slightly stale data (a seat that was just sold still appearing available for a few seconds) is acceptable.
- **Reserve and purchase**: a user selects seats and completes payment. This must be atomic — either the seats are reserved AND the payment succeeds, or neither happens. Two users must never be able to buy the same seat.
- **Admin operations**: event organizers adjust pricing, release additional seat blocks, or cancel events. These operations modify data that concurrent purchases depend on (e.g., releasing 500 new seats while purchases are in flight).

The current system uses a single PostgreSQL database with the default isolation level (read committed). The team has been seeing two types of bugs in production:

1. **Overselling**: during high-demand sales, more tickets are sold than available. The team suspects a race condition in the "check availability then decrement count" logic.
2. **Payment ghosts**: occasionally a payment is charged but no ticket is issued, or a ticket is issued but the payment fails. The team suspects this is related to the non-atomic interaction between the ticketing database and the payment gateway.

Walk me through how you'd redesign the transaction and concurrency control strategy for this system.
