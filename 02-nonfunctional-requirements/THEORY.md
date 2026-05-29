# Theory pass — Defining Nonfunctional Requirements

## Core tradeoff (learner's own words)
The four nonfunctional requirements (performance, reliability, scalability, maintainability) pull against each other. Pursuing reliability means adding retries and replication, which costs latency. Optimizing for performance can make the system more brittle. They're not an independent checklist — choosing how much of each to pursue forces tradeoffs against the others.

## Concepts the learner can apply
- **Faults vs failures:** A fault is a component deviating from spec; a failure is the system stopping its service. Goal is fault tolerance, not fault prevention. Handled faults have no user-facing impact.
- **Human error as dominant fault source:** Most outages are human-caused; response is guardrails and blameless postmortems, not blame.
- **Percentiles over averages:** Averages are dragged up by slow outliers; p95/p99 tell you what most users actually experience.
- **Tail latency amplification:** When requests fan out to multiple services, p99 is dominated by the slowest call; more services means worse tail latency.
- **Reliability vs performance tension:** Retries double response time, replication adds coordination overhead.

## Open gaps acknowledged by the learner
- **Scalability and load parameters:** The distinction between scalability (handling increased load) and evolvability (ease of change) was initially conflated. The concept of load parameters and identifying specific bottlenecks needs re-reading — particularly the Twitter fan-out example.

## Interview duration
~10 exchanges

Phase complete. Proceed to design phase.
