# System Design Interview — Encoding and Evolution

## The scenario

You're the tech lead for a payment processing platform at a fintech company processing about 50,000 transactions per day. The platform is built as a set of five independently deployed microservices:

- **Gateway** — accepts payment requests from merchants via a REST API
- **Fraud detection** — scores each transaction for fraud risk
- **Card processor** — communicates with credit card networks to authorize and capture charges
- **Bank integration** — handles ACH transfers and bank account deposits
- **Notifications** — sends receipts, alerts, and status updates to merchants and customers

The services communicate via a mix of gRPC calls (for synchronous request/response) and Kafka topics (for asynchronous events like "payment authorized," "fraud detected," "deposit completed"). Each service is deployed independently using rolling upgrades — at any given moment during a deploy, both the old and new versions of a service are running simultaneously.

Your team is about to make a significant schema change: adding support for multi-currency payments. This requires adding new fields (currency code, exchange rate, original amount) to several message types that flow between services. Some services will be updated before others, and the rollout will happen over the course of a week.

Walk me through how you'd handle the encoding, schema evolution, and compatibility concerns for this change across the platform.
