# Chapter 4 — Storage and Retrieval

**DDIA 2nd Edition, Chapter 4**

> "One of the miseries of life is that everybody names things a little bit wrong."

## Topics

- Storage and indexing for OLTP: the trade-off between speeding up reads (indexes) and slowing down writes
- Log-structured storage: append-only logs, hash indexes, SSTables, memtables, LSM-trees, Bloom filters, compaction strategies (size-tiered vs leveled)
- B-trees: pages, branching factor, page splits, write-ahead log (WAL), copy-on-write, B-tree variants
- Comparing B-trees and LSM-trees: read vs write performance, write amplification, sequential vs random writes, disk space usage, fragmentation
- Multicolumn and secondary indexes, clustered indexes, covering indexes, heap files
- In-memory databases: durability approaches, performance characteristics
- Data storage for analytics: OLTP vs OLAP internals, cloud data warehouses (query engines, storage formats, table formats, data catalogs)
- Column-oriented storage: column compression, bitmap encoding, run-length encoding, sort order in column stores, writing to column storage
- Query execution: compilation vs vectorized processing
- Materialized views and data cubes
- Multidimensional indexes: concatenated indexes, R-trees, space-filling curves
- Full-text search: inverted indexes, postings lists, n-grams, edit distance, Lucene
- Vector embeddings: semantic search, cosine similarity, IVF indexes, HNSW indexes

## Assignment

Design the storage and indexing strategy for an observability platform that ingests, stores, and queries infrastructure metrics and application logs. The platform must handle both high-throughput writes (metrics and logs arriving continuously from thousands of services) and diverse read patterns (real-time dashboards, ad-hoc debugging queries, long-term trend analysis, and log search).

Your job is to choose storage engines, design indexing strategies, and reason through the trade-offs between write throughput, read latency, disk usage, and query flexibility across different parts of the system.

1. **Theory pass** — conversational interview on storage engines, indexing structures, OLTP vs OLAP storage internals, and the trade-offs between them
2. **Design pass** — produce a `DESIGN.md` for the observability platform: choose storage engines for each data path (recent metrics for dashboards, historical metrics for trend analysis, log storage and search), design the indexing strategy, explain compaction and retention trade-offs. Include rejected alternatives with reasoning.
3. **Implementation pass** — build a working prototype that demonstrates the core storage and retrieval mechanisms (e.g., an LSM-tree-based storage engine with memtable, SSTable segments, compaction, and Bloom filters)
4. **Review** — defend your reasoning in a reviewer session

## Scenario

You're the infrastructure lead at a mid-size SaaS company running about 200 microservices across multiple regions. The engineering team needs an internal observability platform to replace a patchwork of tools that has become too expensive and too limited. The platform must handle three types of data:

- **Metrics** — numeric time-series data (CPU usage, request latency percentiles, error rates, queue depths) arriving at ~500,000 data points per second. Dashboards need sub-second reads of the last hour's data. Trend analysis queries span weeks or months and aggregate across many services.

- **Logs** — semi-structured text (JSON log lines from application services) arriving at ~50,000 lines per second. Engineers need to search logs by keyword, filter by service/severity/time range, and sometimes grep for arbitrary strings during incident debugging. Logs older than 30 days can be moved to cheaper storage.

- **Traces** (stretch goal) — request traces linking spans across services, used for debugging latency. Lower volume (~10,000 traces/second) but queries are by trace ID (point lookup) or by service + latency threshold (range query).

The current system uses a single PostgreSQL instance for metrics (which is falling over) and ships logs to a third-party service. You have budget for a small cluster of machines with SSDs, and the team is comfortable with open-source tools, but leadership wants to understand *why* specific storage engines are appropriate for each workload rather than just picking whatever is popular.

Walk me through how you'd design the storage layer for this platform.
