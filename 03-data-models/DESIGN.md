- clear need for an event log, were we would commit all the contributions to the documents so we can reconstruct previous states (history navigation) and that we can solve concurrency (eg by checking for each user command if it's possible to generate that fact).
- in terms of data model i would go for a document based DB.
- scenario constraints: im optimizing for concurrent writes/updates on each document, and for reads of full documents. i'm not storing here cross-document interconnections, i'll be storing in a separete table that information. i'm also not planning for heavy queries on a lot of documents that share a specific common feature.
- design decisions:
    - i chose event log over not having it as it will help with history and concurrency of so many events, as well as for having CQRS for the different data views.
    — i chose document models over others like graphDB or relational DB as want we want to prioritize is 1) storing pieces of information that highly vary in shape and 2) work with each of the documents individually intead of performing cross-document operations.
- failure model:
    — concurrent updates: i will include as a fact any update command if there's nothing on the event log signaling that there's already an edit live, and reject meanwhile the other requests. User wont be able to write (UI will block it) and if there was sync issues we will notify the user that they recent changes have not been saved.
    — the amount of data that needs store, the different views and the complex navigation that we require from this data is error prone. we will need to have failure recovery mechanism that rebuilds from logs carefully, ensuring consistency across users and changes. eventlog is useful in this case as we will have registered user commands that wont have materialized in facts, so we will use that information to notify the users whose changes didnt make it to the document.
    — when working with large documents or too many concurrent changes, a machine may break. we can use the event log to carefully reconstruct the latest version on the new machine to avoid information loss. While this happens, users will see a stale, read-only version of the document and an error informing them of the existing failure.

key decisions:
  - Event sourcing for history and concurrency
  - Document model for content
  - Separate relational table for links/backlinks and users/teams/permissions.
  - for live analytics i will use a separate OLAP db, that can be a DF where we stora metrics (stats of every write like length of content and person/team, opened files, contributions as comments, etc) so they can be queried/aggragated for analytical work.