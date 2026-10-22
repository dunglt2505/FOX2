---
name: fox2-execution-recovery
description: Safely inspect and recover partial or unknown FOX2 workflow and Agent execution.
---

# fox2-execution-recovery

## Agile Lite project policy precedence

Policy v2.1.0 / `../shared/operating_rules.md` governs ordinary project work. Apply source publication, audit, immutable task and PreExec machinery only to actually selected governed release/Bridge/high-risk transport. For routine native DEV use one task, real deliverable and appropriate tests; preserve relevant professional checks, historical source locks, real permissions and no-replay.

## Activate when
Timeout, missed receipt, failed transfer, interrupted worker or uncertain completion.

## Work to perform
Inspect durable ledger/receipts, identity, last writer, source lock, remote result and whether side effects occurred. Distinguish enqueue from delivered/ACK, heartbeat from completion, unknown from failure. Repro on synthetic fixture; NEVER blind retry/replay consumed Dispatch or broker orders.

## Completion / stop
Known state with source/receipt evidence, safe next action, or explicit STOP / OWNER decision.


Completion is governed by the **Execution Contract v0.3.6** below; apply conditional obligations only when triggered, report bounded HOLD otherwise.

## Execution Contract v0.3.6 — observable completion
- **TRIGGER:** Interrupted/timeout/missing result, ambiguous dispatch delivery or possible duplicate side effects.
- **PRECONDITIONS:** Original immutable task/Dispatch identity, available ledger, host/receipt/Git history and current writer/attempt status.
- **REQUIRED_ACTIONS:** Reconcile enqueue/ACK/start/effects/result independently; check no-replay before selecting a new safe action; never blind retry.
- **REQUIRED_EVIDENCE:** Immutable attempt/source, ledger/receipts, Git remote results and side-effect evidence or explicit UNKNOWN.
- **DELIVERABLES:** Reconciliation verdict (`RECOVERED`/`NEEDS_RECONCILIATION`/`STOP`) with observed last writer, unknowns and safe next action.
- **VALIDATION:** Compare task/result identities and delivery timeline; a timeout alone proves neither no execution nor failure.
- **FAILURE_STATE:** `NEEDS_RECONCILIATION` / `NO_REPLAY_STOP` for consumed, unknown or conflicting state.
- **COMPLETION_GATE:** Exactly one defensible recovered/unknown verdict and lawful next action, without replay or fake completion.
## Git-first reconciliation
Reconcile immutable task/prompt/Dispatch SHA with the claimed start, host ledger, Git result branch/commit, report/evidence manifest and CHAT review receipt. An Agent terminal success without Git push is `DELIVERY_BLOCKED`, not accepted. Unknown start/delivery/timeout is `NEEDS_RECONCILIATION`; inspect recorded effects and writer before deciding a **new authorized attempt**, never replay a consumed Dispatch. CHAT handles Git/source evidence directly; host verifies Windows lock state; WORK only for genuine independent safety audit.


## v0.3.7 — Domain-specific bounded recovery
Identify `FIRST_FAILURE`, affected gate DAG, side effects, immutable PASS and downstream NOT_RUN. Separate delivery-only from code/host/security issues. Classify each PASS for reuse on matching source/input/environment and gate freshness; use one safe discriminating probe, not replay of any consumed attempt. New execution only if authorized and really necessary.


## v0.3.7 — Project-wide focused correction and PASS preservation
FOX2 all stages: earliest causal divergence. Accepted PASS is REUSE_VERIFIED by default; no blanket recheck. Retest only changed fact→affected gate or mandatory gates. CONSUMED Attempt cannot replay; accepted PASS evidence from it is reusable. NOT_RUN/UNKNOWN remain scoped.
