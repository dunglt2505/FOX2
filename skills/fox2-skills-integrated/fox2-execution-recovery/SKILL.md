---
name: fox2-execution-recovery
description: Recover bounded failures without re-running consumed Bridge attempts or invalidating unaffected PASS.
---

# fox2-execution-recovery

## Activate when
A task/Bridge run fails, times out, produces conflicting results or becomes uncertain.

## Work to perform
Identify the earliest causal failing step and observed changed dependencies. Preserve accepted, unaffected PASS and all original hashes, branch positions and ledger states. For reversible native DEV, repair in same task and rerun focused plus impacted tests.

Bridge: inspect transport fetch/poll, candidate validation, PreExec receipt, ledger claim/ACK, agent start, exit metadata, output, publishing checkpoint, Git remote branch and result store. Distinguish NOT_STARTED from CLAIMED/RUNNING/AGENT_EXITED/PUBLISHING, `PUSHED_UNREVIEWED`, FAILED and `NEEDS_RECONCILIATION`. Timeout is not proof no side effects occurred. If consumed or state uncertain, **do not replay** same Dispatch; reconcile ledger, real host action and Git side effects. A necessary safe rerun uses new identity and source binding within SAME logical task, only after observed no-replay and rights checks. Never reset dirty worktree, rewrite accepted status or rerun broker/LIVE effects.

## Completion / stop
Produce the concrete deliverable and actual proof with DONE/REWORK/BLOCKED or a precisely named lower execution state. Do not mark completed because a prompt, Dispatch, tool invocation or plan exists. CHAT owns the end-to-end result.

## Shared operating and Bridge applicability
Apply shared `../../shared/operating_rules.md`. A routine reversible independent native task needs no Bridge Dispatch, manual R0–R7 artifact or immutable prompt publication. When and only when the actual execution is Bridge-controlled, follow `../../shared/bridge_e2e_v041.md` and the **installed** runtime contract, not an assumed current version. All source/receipt/test evidence must be observed, not invented. Old consumed attempts remain immutable and non-replayable. Complete outcomes in the SAME logical task; do not create administrative micro-WPs.
