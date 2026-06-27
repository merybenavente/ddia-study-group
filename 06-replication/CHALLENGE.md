# System Design Interview — Replication

## The scenario

You're the tech lead for a collaborative note-taking app with 500,000 active users spread across the world. The app lets users create, edit, and share notes in real time. Key characteristics of the system:

- **Real-time collaboration**: multiple users can edit the same note simultaneously, and they expect to see each other's changes within a second.
- **Offline support**: the mobile app must work without an internet connection. Users can create and edit notes offline, and changes sync when they reconnect — which might be hours or days later.
- **Multi-device**: users access their notes from a phone, laptop, and tablet. If they edit a note on their phone and then open it on their laptop, they expect to see their changes.
- **Shared notes**: notes can be shared with teams. A team of 10 people might all be editing a project plan simultaneously.

The system currently runs in a single region (us-east-1) with a single PostgreSQL database. Users in Europe and Asia are complaining about high latency (300-500ms round trips for every keystroke), and last month a 4-hour database outage caused a complete service outage. Leadership wants you to fix both problems.

Walk me through how you'd design the replication strategy for this system.
