# Theory pass — Data Models and Query Languages

## Core tradeoff (learner's own words)
The core tension is on what each of the data models offer, along with the different ways of querying the data on them. Different data shapes and access patterns pull toward different models — relational for many-to-many relationships and joins, document for self-contained variable-structure records, graph for highly connected data with multi-hop queries, DataFrames for analytical transformations. No single model is ideal for everything — forcing a domain into the wrong model creates unnecessary complexity and inefficiency.

## Concepts the learner can apply
- **Event sourcing and CQRS**: Explained immutable append-only logs with past-tense events, commands vs events distinction, and materialized views for read optimization. Identified downsides including determinism with external data (currency example) and privacy challenges (crypto-shredding).
- **Document vs graph model selection**: Applied both models to an unseen law firm scenario — document model for varied evidence records (emails, contracts, photos) with different internal structure, graph model for case-citation and jurisdiction relationships requiring multi-hop traversal. Recognized that different parts of a domain pull toward different models.
- **Normalization tradeoffs**: Understood that graph queries like "alumni of X who know someone at Anthropic" become slow recursive joins in relational models.

## Open gaps acknowledged by the learner
- **Triple stores**: Doesn't yet see why someone would want the (subject, predicate, object) format. Re-read the triple stores, RDF/SPARQL, and Turtle sections.
- **Star and snowflake schemas for analytics**: The OLTP/OLAP distinction within Chapter 3's scope (fact tables, dimension tables, OBT) wasn't explored in depth.

## Interview duration
~15 exchanges

Phase complete. Proceed to design phase.
