# System Design Interview — Data Models and Query Languages

## The scenario

You're building a knowledge management platform — something like Notion or Confluence — for a company with about 10,000 employees. The platform has several core features:

- **Documents** with rich, nested structure: pages can contain text, tables, embedded media, code blocks, and nested sub-pages. The structure of each document varies widely.
- **Collaboration**: users belong to teams, documents have owners and editors, and there's a permissions model (who can view, edit, comment).
- **Cross-references**: documents link to other documents, and users want to see both outgoing links ('this page links to...') and backlinks ('these pages link here'). Tags and categories connect documents across teams.
- **Change history**: every edit is tracked. Users want to see who changed what and when, and roll back to previous versions.
- **Analytics dashboards**: leadership wants to know which documents are most viewed, which teams produce the most content, and how content usage changes over time.

Walk me through how you'd model the data for this system. What data models would you use and why?
