# FOX2 Bridge — Full Git Delivery implementation plan (Agile Lite)

**Date:** 2026-10-23  |  **Status:** DESIGN_CANDIDATE / DEV_NOT_STARTED / HOST_E2E_NOT_RUN
**Existing logical task:** `FOX2-BRIDGE-RC1-TO-INTERNAL-READY`; no new project WP, no independent management board.
**Documents:** BRD-09 REV4 (R32–R43 / T30–T43) and Bridge Tech Spec v0.7 REV11 (§28).

## Outcome
CHAT handoff → exact Agent coding/test → **Bridge Git Publisher by default** → remote result SHA → CHAT acceptance. Git publication must not consume Agent tokens. Failures, quota exhaustion and restarts can preserve explicitly authorized safe WIP without declaring DONE.

## Implementation slices within the same Bridge task

| Slice | Real work | Acceptance / evidence |
|---|---|---|
| **A. Baseline and host reconciliation** | CHAT checks actual installed Bridge vs R5 source, pending immutable run, writer/permissions, current Schema v3 and recovery-ref authorization; reuse accepted evidence | Known source/host; no guessed admission; in-flight R5 untouched |
| **B. Normal Bridge Git delivery** | Generator explicitly sets BRIDGE; maintain AGENT opt-in; independent Git publisher for both CODEX/Copilot, pre-push checks, remote SHA readback | T30–T34,T42; success plus negative test/path branches |
| **C. Failure/WIP publisher** | Supervisor captures exit/quota/timeout/child state, safe recovery ref, WIP artifact/provenance; durable ledger, restart/idempotent publish | T35–T40,T43; no replay, no unsafe WIP |
| **D. CHAT handback & integrated validation** | Return publisher/ref/SHA/test status, review/rework, installed Windows host canary normal and failed run | T34,T41,T43; CHAT verdict from actual Git |

## Execution boundaries

- **Route:** CHAT selects CODEX/Copilot and proportional Model/Thinking only after actual host capability check; existing valid in-flight R5 Dispatch cannot be changed or replayed.
- **Development:** one authorized non-main writer, exact allowlisted `agent_bridge/**` and targeted tests, focused Build→Test→Deliver. Do not start a parallel Bridge writer while R5/RC1 worktree is active.
- **Technical safeguards:** real Schema/normalizer, dictionary/Policy machine pins, material PreExec/receipts, one-shot ledger, isolated worktree, permission and remote branch checks; no synthetic PASS.
- **Publisher:** reuse existing Git subprocess path or verified `pwsh` 7 host invocation, not an Agent tail command. Do not create a second competing git-push worker.
- **Failure:** preserve safe WIP only with explicit permitted recovery ref; no force/main/merge/broker/LIVE; blocked state otherwise.

## Definition of Done

1. New task generator writes explicit `delivery_owner=BRIDGE`; AGENT option works without double push; old Dispatch unaffected.
2. Agent Git disabled: CODEX and Copilot each deliver through Bridge-owned Git, full remote SHA verified.
3. Normal success is `PUSHED_UNREVIEWED` until CHAT approves diff/tests; negative/failed code never gets success status.
4. Quota/nonzero/timeout/host-failure recovery publishes WIP only with proven stopped writer, valid path, no secrets and authorized recovery branch; otherwise holds safely.
5. Crash at commit/push/readback reconciles exactly once, does not rerun consumed Agent attempt or create duplicate commits.
6. Results include actual SHA, publisher, change paths, test status and next action; protected-branch and redaction negative tests pass.
7. Focused unit/integration regressions plus real Windows-host normal and interrupted-run scenarios pass; CHAT records acceptance on same logical task.

**Current next safe action:** preserve and resolve in-flight R5, then compare actual installed code/host with §28. Begin bounded implementation only when permission/worktree/writer are available. Current project Board DOING for Bridge is not evidence that this enhancement has been coded.

**STOP:** active/uncertain Agent writer, no recovery branch permission, out-of-scope/secret, moved remote, consumed Dispatch attempted replay, unavailable installed Bridge capability. Existing accepted PASS preserved.
