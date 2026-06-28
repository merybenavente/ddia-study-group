# Chapter 1 — Trade-Offs in Data Systems Architecture

**DDIA 2nd Edition, Chapter 1**

> "There are no solutions; there are only trade-offs."

## Topics

- Operational (OLTP) vs analytical (OLAP) systems
- Data warehouses, data lakes, and derived data
- Cloud services vs self-hosting
- Distributed vs single-node systems
- Microservices and serverless
- Data systems, law, and society (GDPR, data minimization)

## Assignment (paper exercise)

This chapter has no code deliverable. The assignment is to demonstrate trade-off reasoning on the concepts covered:

1. **Theory pass** — conversational interview on the chapter's core concepts
2. **Design pass** — given a scenario, produce a written `DESIGN.md` analyzing which system architecture trade-offs apply and why, with explicit alternatives considered and rejected
3. **Review** — defend your reasoning in a reviewer session

## Scenario

You've just joined a mid-size e-commerce company — about 2 million active users, 50,000 orders per day. The company has been running everything on a single PostgreSQL database: the product catalog, order processing, user accounts, and all the analytics reporting. The CEO has two complaints: the nightly analytics reports are getting slower every month and sometimes cause the checkout flow to slow down, and the data science team says they can't do the ML-based recommendation work they want because they don't have the right access to the data.

Your job is to propose a new architecture. Walk me through how you'd think about this.
