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

| Week | Chapter | Status |
|---|---|---|
| 1 | Trade-Offs in Data Systems Architecture | Available |
| 2 | Defining Nonfunctional Requirements | Coming soon |
| 3 | Data Models and Query Languages | Coming soon |
| 4 | Storage and Retrieval | Coming less soon |
| 5 | Encoding and Evolution | Eventually consistent |
| 6 | Replication | Replicating effort to get here |
| 7 | Sharding | Partitioned from reality |
| 8 | Transactions | No guarantees of isolation |
| 9 | The Trouble with Distributed Systems | The trouble with finishing this |
| 10 | Consistency and Consensus | We haven't reached consensus on this yet |
| 11 | Batch Processing | Batched for later |
| 12 | Stream Processing | Streaming in eventually |
| 13 | A Philosophy of Streaming Systems | Philosophically distant |
| 14 | Review | If we survive |
