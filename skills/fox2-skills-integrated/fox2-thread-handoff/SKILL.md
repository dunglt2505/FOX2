---
name: fox2-thread-handoff
description: Carry forward verified context across conversations or actors without redefining the task.
---

# fox2-thread-handoff

## Activate when
A chat or actor context must move or the user explicitly asks for a continuation handoff.

## Work to perform
Produce compact objective, current task ID, accepted evidence, last verified source/commit, real blocker, next action and relevant STOP conditions. Clearly distinguish `CONTEXT_TRANSFER` (no new task), `NEW_AGENT_ASSIGNMENT` (Router and Prompt Builder when genuinely delegated), `RESULT_RETURN` (Result Review, no new prompt), and `REWORK` (same logical task). For consumed Bridge Dispatch include its immutable identity and no-replay status; do not recreate or reassign it merely due to thread change.

## Completion / stop
One complete context-transfer summary with real pointers, not an executable task unless expressly routed.

## Responsibility boundary
Own **context continuity**, not new route/Agent assignment, standalone Prompt Builder or Bridge execution.

## Shared operating and Bridge applicability
FOX2 Agile Lite: one logical task, Build → Test → Deliver, CHAT owns outcome. Use only relevant methods and real evidence. Ordinary native DEV has no mandatory R0–R7/PreExec/Dispatch/extra approval; if the selected real route is Bridge or high-risk, its installed technical controls remain authoritative. No unrelated version churn, protected operations or consumed-attempt replay. This Skill does not authorize execution or grant external rights.
