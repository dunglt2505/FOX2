---
name: fox2-governance-preflight
description: Enforce governance source verification and pre-execution permissions.
---
# Evaluate the actual task grant and applicable controls

- Identify the requested operation, current task state, explicit Owner grant, allowed paths and proposed effects. Do not derive permissions from a request's own status fields.
- Apply available governing instructions and report their authority honestly. Check project routing requirements before an actual Agent assignment or executable handoff.
- Separate expressly authorized independent technical work from actions requiring certified current sources or release approval. Permit only the former when the latter are unresolved.
- Return a bounded operation-level decision: what may proceed now, what is held, and why. Routing does not grant DEV, merge, LIVE or release rights.

Read [scope and source guidance](../../shared/host_guidance.md) when authority, canonical sources, task state or effects matter.
