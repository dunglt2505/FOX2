---
name: fox2-thread-handoff
description: Prepare thread handoff with source lock, decisions, open items and evidence.
---
# Transfer usable task context without replay

- Read the current task state, frozen source lock, WIP, completed effects, decisions, evidence and next action. Keep existing bindings distinct from proposed updates.
- Produce a self-contained handoff that lets the next conversation continue the same work package. Label conditional or unverified provenance explicitly.
- List the completed effects that must not be replayed and the exact remaining acceptance work. A newer source does not automatically rebind an in-flight task.
- Drafting the handoff may proceed now. Dispatching implementation, replaying a consumed task or rebinding material sources requires the appropriate authority and impact review.

Read [scope and source guidance](../../shared/host_guidance.md) when authority, canonical sources, task state or effects matter.
