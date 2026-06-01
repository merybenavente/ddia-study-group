# Chapter 3 — Data Models and Query Languages

**DDIA 2nd Edition, Chapter 3**

> "The limits of my language mean the limits of my world."

## Topics

- Relational vs document models: impedance mismatch, ORMs, one-to-many vs many-to-many relationships
- Normalization, denormalization, and joins: tradeoffs in data duplication, consistency, and query performance
- Schema-on-read vs schema-on-write: when flexibility helps and when it hurts
- Data locality for reads and writes
- Graph-like data models: property graphs, triple stores, and when relationships dominate
- Query languages: SQL, Cypher, SPARQL, Datalog, GraphQL, MongoDB aggregation pipeline
- Stars and snowflakes: schemas for analytics (fact tables, dimension tables, OBT)
- Event sourcing and CQRS: separating write-optimized and read-optimized representations
- DataFrames, matrices, and arrays: data models for analytics and ML

## Assignment

Design the data model layer for a knowledge management platform (think Notion or Confluence). The platform has documents with nested, variable structure; users and teams with permissions; cross-references and links between documents; change history; and usage analytics dashboards.

Different parts of this system pull toward different data models. Your job is to identify which parts of the domain fit which model, justify your choices with explicit tradeoffs, and design the query patterns that support the core use cases.

1. **Theory pass** — conversational interview on data models, query languages, and the tradeoffs that drive model selection
2. **Design pass** — produce a `DESIGN.md` for the knowledge management platform: choose data models for each subdomain (documents, relationships, history, analytics), design schemas with concrete examples, specify query patterns, explain normalization/denormalization decisions with rejected alternatives
3. **Implementation pass** — build a working prototype that demonstrates your data model choices and query patterns
4. **Review** — defend your reasoning in a reviewer session
