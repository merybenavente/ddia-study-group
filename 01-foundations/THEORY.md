# Theory pass — Trade-Offs in Data Systems Architecture

## Core tradeoff (learner's own words)
There are no perfect solutions, only tradeoffs. The chapter covers OLTP vs OLAP systems, cloud vs self-hosting, and distributed vs single-node architectures. Each choice has costs — distributed systems add partial failures, latency, and consistency challenges; cloud gives elasticity but costs control and money; OLAP systems serve different access patterns than OLTP.

## Concepts the learner can apply
- **OLTP vs OLAP:** Correctly identified access pattern differences (read/write/update/delete vs aggregation/complex querying) and that derived datasets can feed back into OLTP (e.g., fraud detection)
- **Distributed system costs:** Named partial failures, latency, and data synchronization as core costs; applied this reasoning to reject an unnecessary microservices migration for a small-scale system
- **Proportionate architecture:** When given a scenario of a 50k-user startup, self-corrected from "split into microservices" to "add an OLAP layer alongside existing Postgres" — correct application of tradeoff reasoning
- **GDPR and system design:** Identified that data deletion must cascade across derived systems and pipelines, making it an architectural concern

## Open gaps acknowledged by the learner
- **OLTP/OLAP terminology:** Had to look up the terms; concepts were understood but naming wasn't retained
- **Distributed vs single-node:** Wants to re-read for deeper understanding of when distribution is actually warranted
- **Cloud vs self-hosting:** Wants to solidify understanding of the full tradeoff space beyond elasticity vs cost/control
