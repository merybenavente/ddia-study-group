# System Design Interview — Trade-Offs in Data Systems Architecture

## The scenario

You've just joined a mid-size e-commerce company — about 2 million active users, 50,000 orders per day. The company has been running everything on a single PostgreSQL database: the product catalog, order processing, user accounts, and all the analytics reporting. The CEO has two complaints: the nightly analytics reports are getting slower every month and sometimes cause the checkout flow to slow down, and the data science team says they can't do the ML-based recommendation work they want because they don't have the right access to the data.

Your job is to propose a new architecture. Walk me through how you'd think about this.
