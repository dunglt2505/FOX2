---
name: fox2-tech-execution-recovery
description: "Reconcile failed/uncertain native or Bridge execution and preserve accepted evidence without replay."
---

# fox2-tech-execution-recovery

**FOX2 Layer 3 — Technical and safety methods — Agile Lite 0.5.0**

## Activate when
A task execution fails, hangs, times out, leaves a disputed result or has uncertain post-start side effects.

## Input
Original task and accepted PASS, actual host/ledger stage, worktree/Git remote, relevant result/error.

## Work to perform
1. Isolate earliest causal failure; preserve accepted and unaffected PASS and immutable history. Reversible native DEV: correct inside SAME task, rerun focused + impacted tests.
2. For Bridge, inspect poll/fetch, Dispatch validation, ledger claim, PreExec, Agent started/exited, publication checkpoint, observed remote SHA and result store. Timeout ≠ not started. Distinguish NOT_STARTED, CLAIMED, RUNNING, AGENT_EXITED, PUBLISHING, PUSHED_UNREVIEWED, FAILED and NEEDS_RECONCILIATION.
3. Never replay a consumed/claimed Dispatch or irreversible/broker/LIVE action. Before any new attempt, reconcile actual side effects and authority; if permitted, bind a NEW immutable attempt under SAME logical task.
4. No blind reset on dirty worktree or silent rebind of prior Policy/prompt/source. Report REWORK / RECONCILE / BLOCKED with the next actionable safe step, not another administrative WP.

## Output
One observed execution-state verdict and smallest safe recovery action; no fake retry PASS.

## Responsibility boundary
Owns recovery diagnosis/advice and checks. Runtime ledger/worker performs host actions; CHAT Result Acceptance alone marks product DONE.

## Common rules
One logical Kanban task; only material checks for selected action. Ordinary native DEV has no mandatory Bridge/PreExec/R0–R7 paperwork. For actual Bridge execution the installed Bridge enforces its own machine protocol and no-replay; never fabricate PASS, permissions or host actions. CHAT owns result acceptance; no broker/LIVE, protected branch or irreversible side effects without real authority. 
