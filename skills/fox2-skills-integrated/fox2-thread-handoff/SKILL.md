---
name: fox2-thread-handoff
description: Preserve exactly enough context for real continuation or a new Agent assignment without extra ceremony.
---

# fox2-thread-handoff

## Activate when
A thread change or actual different executor requires continuity information.

## Work to perform
Distinguish `CONTEXT_TRANSFER` (same goal, no new execution), `NEW_AGENT_ASSIGNMENT` (Prompt Builder only if delegation actually needed), `RESULT_RETURN` (Result Review, no new prompt) and `REWORK` (same logical task, bounded fix). Keep objective, last observed source/commit, accepted evidence, blocker, next authorized actor and STOP. Do not copy entire Policy library or restart completed work.

For Bridge, also preserve original `dispatch_id`, prompt/task SHA, branch/worktree, selected actor/model/effort, delivery owner, ledger claim/consumed state, actual result and whether new attempt is legally safe. When Owner must manually execute host CLI, Prompt Builder alone produces copy-ready verified PowerShell 7+ script; no guessed WORK CLI. Old Dispatch cannot be replayed just because context is moved to another thread.

## Completion / stop
Produce the concrete deliverable and actual proof with DONE/REWORK/BLOCKED or a precisely named lower execution state. Do not mark completed because a prompt, Dispatch, tool invocation or plan exists. CHAT owns the end-to-end result.

## Shared operating and Bridge applicability
Apply shared `../../shared/operating_rules.md`. A routine reversible independent native task needs no Bridge Dispatch, manual R0–R7 artifact or immutable prompt publication. When and only when the actual execution is Bridge-controlled, follow `../../shared/bridge_e2e_v041.md` and the **installed** runtime contract, not an assumed current version. All source/receipt/test evidence must be observed, not invented. Old consumed attempts remain immutable and non-replayable. Complete outcomes in the SAME logical task; do not create administrative micro-WPs.
