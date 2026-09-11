# Chapter 8 — Transactions

**DDIA 2nd Edition, Chapter 8**

> "Some authors have claimed that general two-phase commit is too expensive to support, because of the performance or availability problems that it brings."

This chapter is long (pp. 301–368), so it is split into two weeks. The assignment spans both: design the concurrency control and transaction strategy for an online event ticketing platform. The platform sells tickets for concerts, sports events, and theater shows. It must handle bursts of concurrent purchases (popular events sell out in seconds), enforce seat inventory constraints, process payments atomically with ticket reservations, and provide consistent views of seat availability to users browsing the system.

Your job is to choose isolation levels, design the transaction boundaries, prevent race conditions, and reason through what happens when things go wrong. Week 1 covers single-node transaction fundamentals and weak isolation; week 2 covers serializability and distributed transactions, building on your week 1 artifacts rather than starting over.

## Week 1 — Transaction Fundamentals and Weak Isolation

*Covers "What Exactly Is a Transaction?" and "Weak Isolation Levels" (through write skew and phantoms).*

### Topics

- What is a transaction: grouping reads and writes into a logical unit, commit and abort, safety guarantees
- The meaning of ACID: atomicity (abortability), consistency (application invariants), isolation (concurrency), durability (persistence guarantees and their limits — disk writes, fsync, replication)
- Single-object vs multi-object operations: atomic writes, compare-and-set, the need for multi-object transactions
- Handling errors and aborts: retry pitfalls (duplicate side effects, overload amplification, lost client state)
- Weak isolation levels and their race conditions:
  - Read committed: no dirty reads, no dirty writes, implementation with row locks and old-value snapshots; read uncommitted as an even weaker level
  - Snapshot isolation and repeatable read: read skew, MVCC (multiversion concurrency control), visibility rules, indexes and snapshot isolation, naming confusion across databases
  - Preventing lost updates: atomic operations, explicit locking (SELECT FOR UPDATE), automatic detection, compare-and-set, conflict resolution in replicated databases
  - Write skew and phantoms: the check-then-act pattern, materializing conflicts

### Assignment

1. **Theory pass** — conversational interview on ACID guarantees, weak isolation levels (read committed, snapshot isolation, MVCC), and race conditions (dirty reads, dirty writes, read skew, lost updates, write skew, phantoms)
2. **Design pass** — start a `DESIGN.md` scoped to this week's material: choose isolation levels for browsing availability and reserving seats, define transaction boundaries, identify the specific race conditions the scenario is vulnerable to (double-selling, lost updates on seat counts, phantom bookings), and decide how to prevent the ones that this week's mechanisms can address — flagging the ones that require week 2's serializability material. Include rejected alternatives with reasoning.
3. **Implementation pass** — build a working prototype that demonstrates observable race conditions under weak isolation and their prevention using the mechanisms you chose in your design
4. **Review** — defend your week 1 reasoning in a reviewer session

## Week 2 — Serializability and Distributed Transactions

*Covers "Serializability" and "Distributed Transactions" (through exactly-once message processing).*

### Topics

- Serializability — three approaches:
  - Actual serial execution: stored procedures, sharding for throughput, constraints and limitations
  - Two-phase locking (2PL): shared/exclusive locks, deadlocks, performance costs, predicate locks, index-range locks
  - Serializable snapshot isolation (SSI): pessimistic vs optimistic concurrency control, detecting stale MVCC reads, detecting writes that affect prior reads, performance tradeoffs
- Distributed transactions:
  - Two-phase commit (2PC): coordinator, prepare/commit phases, the commit point, coordinator failure, in-doubt transactions; why three-phase commit doesn't work in practice
  - XA transactions: the standard, holding locks while in doubt, coordinator as single point of failure, heuristic decisions
  - Database-internal vs heterogeneous distributed transactions
  - Exactly-once message processing: idempotency via message IDs

### Assignment

Builds on your week 1 `DESIGN.md` and prototype — do not start over.

1. **Theory pass** — conversational interview on the three serializability approaches (serial execution, 2PL, SSI) and distributed transactions (2PC, in-doubt transactions, XA, exactly-once semantics)
2. **Design pass** — extend your week 1 `DESIGN.md`: revisit the race conditions you flagged as unresolved and decide whether any operation warrants serializable isolation and, if so, which approach; design the distributed transaction strategy for payment+reservation atomicity; and reason through how admin operations (releasing seat blocks mid-sale) interact with in-flight purchases. Include rejected alternatives with reasoning.
3. **Implementation pass** — extend the week 1 prototype: demonstrate prevention of the remaining race conditions under your chosen strategy, and the payment+reservation atomicity behavior including its failure cases
4. **Review** — defend your combined reasoning in a reviewer session

## Scenario

You're a backend engineer at a ticketing company that sells tickets for live events. The platform handles about 2,000 events per month, with total sales of ~500,000 tickets per month. Most of the time, traffic is moderate — a few hundred concurrent users browsing and buying. But when a popular artist announces a tour, tens of thousands of users hit the system simultaneously, and 50,000 tickets can sell out in under 90 seconds.

The system has three main operations:

- **Browse availability**: users view which seats or ticket tiers are available for an event. This is read-heavy and needs to be fast, but showing slightly stale data (a seat that was just sold still appearing available for a few seconds) is acceptable.
- **Reserve and purchase**: a user selects seats and completes payment. This must be atomic — either the seats are reserved AND the payment succeeds, or neither happens. Two users must never be able to buy the same seat.
- **Admin operations**: event organizers adjust pricing, release additional seat blocks, or cancel events. These operations modify data that concurrent purchases depend on (e.g., releasing 500 new seats while purchases are in flight).

The current system uses a single PostgreSQL database with the default isolation level (read committed). The team has been seeing two types of bugs in production:

1. **Overselling**: during high-demand sales, more tickets are sold than available. The team suspects a race condition in the "check availability then decrement count" logic.
2. **Payment ghosts**: occasionally a payment is charged but no ticket is issued, or a ticket is issued but the payment fails. The team suspects this is related to the non-atomic interaction between the ticketing database and the payment gateway.

Of these two bugs, the overselling race condition is week 1's problem (weak isolation and its race conditions), while the payment ghosts — and the question of whether any operation warrants full serializability — are week 2's.

Walk me through how you'd redesign the transaction and concurrency control strategy for this system.
