---
name: fox2-execution-recovery
description: Recover blocked execution without repeating completed dispatches.
---
# Recover from partial execution without repeating effects

- Read actual state and evidence before proposing retries. Separate confirmed completed effects, confirmed failures and uncertain/consumed execution.
- Build a bounded recovery plan excluding completed effects and preserving WIP/source locks. Identify the smallest readback needed to resolve uncertainty.
- Execute a retry only when state, scope and the existing grant make it safe; otherwise hold that effect and continue independent diagnosis.
- Deliver the recovery analysis despite conditional governance provenance. Never blind replay, automatically switch Agents or infer that an interrupted process made no changes.

Read [scope and source guidance](../../shared/host_guidance.md) when authority, canonical sources, task state or effects matter.
