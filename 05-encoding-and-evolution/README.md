# Chapter 5 — Encoding and Evolution

**DDIA 2nd Edition, Chapter 5**

> "Everything changes and nothing stands still."

## Topics

- Evolvability: rolling upgrades, staged rollouts, backward and forward compatibility
- Formats for encoding data: language-specific formats, JSON/XML/CSV, JSON Schema, binary encodings (MessagePack)
- Schema-driven binary encodings: Protocol Buffers, Avro — field tags, schema evolution rules, writer's vs reader's schema
- Dynamically generated schemas and the merits of schema-based encodings
- Modes of dataflow: through databases (data outlives code, archival storage), through services (REST, RPC, web services, service discovery, load balancing, service meshes), through workflows and durable execution
- Event-driven architectures: message brokers, distributed actor frameworks
- Data encoding and evolution for RPC: API versioning, backward/forward compatibility on requests and responses

## Assignment

Design the schema evolution and data encoding strategy for a multi-service payment processing platform. The platform has several independently deployed services (fraud detection, credit card processing, bank integration, notifications) that communicate via both synchronous RPCs and asynchronous message queues. Services are upgraded via rolling deployments, meaning old and new code versions coexist during each rollout.

Your job is to choose encoding formats, define schema evolution rules, design the dataflow between services, and reason through what happens when schemas change in a system where you can't upgrade everything at once.

1. **Theory pass** — conversational interview on encoding formats, schema evolution, compatibility guarantees, and dataflow patterns
2. **Design pass** — produce a `DESIGN.md` for the payment platform: choose encoding formats for each communication channel (service-to-service RPC, message queue events, database storage, archival), define schema evolution policies, design the dataflow graph between services, explain what happens during a rolling upgrade when a new field is added. Include rejected alternatives with reasoning.
3. **Implementation pass** — build a working prototype that demonstrates schema evolution across services with rolling upgrades
4. **Review** — defend your reasoning in a reviewer session
