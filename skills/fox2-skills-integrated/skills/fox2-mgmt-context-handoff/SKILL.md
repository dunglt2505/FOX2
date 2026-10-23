---
name: fox2-mgmt-context-handoff
description: "Preserve task context during FOX2 thread or actor transitions without creating a new execution workflow."
---

# fox2-mgmt-context-handoff

**FOX2 Layer 1 — Project management — Agile Lite 0.5.0**

## Activate when
A FOX2 task must continue in another thread or transfer context to an actor.

## Input
Existing task, last accepted evidence, immutable attempt when any, real next safe action.

## Work to perform
1. Classify `CONTEXT_TRANSFER`, `NEW_AGENT_ASSIGNMENT`, `RESULT_RETURN` or `REWORK`. Context transfer is not automatically a new task or a reason to write a prompt.
2. Carry only goal, observed result, **authorized Git result branch and pushed commit SHA for delegated Agent work**, source commit when material, next action, actor and STOP. If no observed pushed result exists, label `GIT_DELIVERY_PENDING`; never treat a local Agent message as final Git handoff. Do not paste entire Policy corpus or reopen accepted evidence.
3. For genuine Agent assignment, ask Prompt Builder for task wording after Router chooses actor. For existing result return, use Result Acceptance, not a fresh Prompt Builder cycle.
4. If Bridge was used, retain the exact Dispatch ID, source/prompt identity, consumed state and no-replay limitation; do not reuse or rebind it for a new thread.

## Output
One compact context handoff with exact verified state and next owner.

## Responsibility boundary
Transfers context only. No new authorization, Agent selection, issuance, report acceptance or Bridge execution.

## Common rules
One logical Kanban task; only material checks for selected action. Ordinary native DEV has no mandatory Bridge/PreExec/R0–R7 paperwork. For actual Bridge execution the installed Bridge enforces its own machine protocol and no-replay; never fabricate PASS, permissions or host actions. CHAT owns result acceptance; no broker/LIVE, protected branch or irreversible side effects without real authority. 
