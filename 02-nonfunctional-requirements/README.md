# Chapter 2 — Defining Nonfunctional Requirements

**DDIA 2nd Edition, Chapter 2**

## Topics

- Performance: response time vs throughput, latency vs service time, percentiles (p50, p95, p99), tail latency amplification
- Reliability: faults vs failures, fault tolerance, single points of failure, hardware faults, software faults, human error, blameless postmortems
- Scalability: understanding load, fan-out, materialized views, vertical vs horizontal scaling, shared-memory/shared-disk/shared-nothing architectures
- Maintainability: operability, simplicity, evolvability, irreversibility

## Assignment

Design a ride-sharing dispatch system that matches riders with nearby drivers in real time. Reason through the nonfunctional requirements: what does "fast" mean (percentiles, not averages), what faults do you tolerate, how do you handle demand spikes, and how maintainable is your design two years from now.

1. **Theory pass** — conversational interview on performance, reliability, scalability, and maintainability
2. **Design pass** — produce a `DESIGN.md` for the dispatch system: define your SLOs with real numbers, choose a matching strategy, identify faults and your tolerance for each, explain your scaling approach for rainstorm-Friday spikes. Include rejected alternatives with reasoning.
3. **Review** — defend your reasoning in a reviewer session

## Scenario

You're building the dispatch system for a ride-sharing app in a city with 2 million active users. The system matches riders with nearby drivers in real time. On a normal day you handle about 500 ride requests per minute, but during rush hour that spikes to 5,000 per minute, and during a rainstorm on a Friday evening it can hit 15,000 per minute. Riders expect to see a driver assigned within 10 seconds of requesting a ride.

Walk me through how you'd design the dispatch system and what nonfunctional requirements you'd set for it.
