---
name: fox2-agent-route-runtime
description: Route tasks according to current effective routing policy and execution capabilities.
---
# Compare routes and recommend one eligible execution path

- Establish the real task stage, dependencies, material capability requirements and any pinned Agent/model. Follow the project's routing precheck before final assignment.
- Compare CHAT, COPILOT, CODEX, WORK and any relevant alternatives using observed access, capability and quota. Mark unprobed facts UNKNOWN rather than assuming failure or readiness.
- Recommend one supported route, with scope, sequence and STOP conditions. Preserve a pinned material capability; never silently substitute another Agent.
- A conditional technical recommendation can be drafted without certified source authority. Hold final executable dispatch when its material source or capability gates are unresolved; do not launch an Agent or change permissions merely from this analysis.

Read [scope and source guidance](../../shared/host_guidance.md) when authority, canonical sources, task state or effects matter.
