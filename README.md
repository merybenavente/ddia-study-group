# DDIA Study Group

A common conversation at [Recurse Center](https://www.recurse.com/) is how much to delegate to AI vs implement yourself when you're trying to learn. Let AI do everything and you learn nothing. Write every line by hand and it takes forever.

As Kleppmann would say, there are no right answers, only trade-offs.

But that's for system architecture.

For learning, I think there's actually a good balance: AI handles the typing, you handle the thinking. This repo sets up that balance for working through *Designing Data-Intensive Applications*. You make the design decisions, do the failure analysis, and reason about trade-offs. Claude writes the code you specify, and refuses to do more.

## Before each session

Read the chapter, optionally do the theory review with Claude, and try to solve the main assignment. If you're short on time or want extra practice, Claude can also generate shorter, customized challenges for you.

The assignments are designed to give concrete examples to reference even when you don't have professional experience with these systems.

## How Claude works in this repo

Open Claude Code inside this repo and It will guide you through each phase. Claude adapts Its behavior depending on where you are:

- **theory-interview** — Socratic interview on the chapter's concepts; produces `THEORY.md` when you demonstrate understanding
- **design-coach** — interrogates your design decisions without proposing alternatives
- **atomic-implementer** — writes code one unit at a time, stops for you to inspect
- **debug-helper** — helps you locate bugs by asking what you expected vs what happened
- **failure-experiment** — you pick what to break and predict the result; Claude implements the chaos
- **review-prep** — mechanical checklist before the final review
- **meta** — project setup, dependencies, tooling (not learning content)

Claude will not make design decisions for you, will not skip phases, and will not write code you haven't specified. If you want to understand why, read [`LEARNER_GUIDE.md`](LEARNER_GUIDE.md).

## The chapters

- [Ch. 1: Trade-Offs in Data Systems Architecture](01-foundations/README.md)
- [Ch. 2: Defining Nonfunctional Requirements](02-nonfunctional-requirements/README.md)
- [Ch. 3: Data Models and Query Languages](03-data-models/README.md)
- [Ch. 4: Storage and Retrieval](04-storage-and-retrieval/README.md)
- [Ch. 5: Encoding and Evolution](05-encoding-and-evolution/README.md)
- [Ch. 6: Replication](06-replication/README.md)
- [Ch. 7: Sharding](07-sharding/README.md)
- [Ch. 8: Transactions, Part I: Fundamentals and Weak Isolation](08-transactions/README.md)
- [Ch. 8: Transactions, Part II: Serializability and Distributed Transactions](08-transactions/README.md)
- [Ch. 9: The Trouble with Distributed Systems](09-distributed-systems-trouble/README.md)
- [Ch. 10: Consistency and Consensus](10-consistency-and-consensus/README.md)
- [Ch. 11: Batch Processing](11-batch-processing/README.md)
- [Ch. 12: Stream Processing](12-stream-processing/README.md)
- [Ch. 13: A Philosophy of Streaming Systems](13-philosophy-of-streaming-systems/README.md)
- [Ch. 14: Doing the Right Thing](14-doing-the-right-thing/README.md)
