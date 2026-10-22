# FOX2 — Project Kanban — LIVE

**Operating model:** FOX2 Agile Lite / Policy v2.1.0  
**Board:** one project board: `BACKLOG → DOING ↔ BLOCKED → DONE`  
**Live as of:** 2026-10-22 (after R5 result acceptance)  
**Status:** `LIVE_GIT_EVIDENCE_SYNCED`  
**Management authority:** `main:docs/governance/FOX2_PROJECTWIDE_GOVERNANCE_REGISTRY.json` @ `a7ca2b7610fa8ecd2766c67cfb19a28c32d9e5c9`  
**Rule:** Git/test/host evidence wins over stale Issue/PR prose. Prompt, PreExec, Dispatch, Agent start, or `PUSHED_UNREVIEWED` alone is never DONE.

## Live board

| Priority | ID | Outcome / goal | Status | Delivery owner | Current evidence | Acceptance / next action |
| --- | --- | --- | --- | --- | --- | --- |
| P0 | `FOX2-M1-A-APP-BATCH-B` | Deliver the first runnable localhost FOX2 M1-A product: React/Vite UI + accepted backend integration + offline acceptance | **DOING** | CHAT | Branch `work/FOX2-M1-A-APP-BATCH-B@51a97bfa7420efa0a0e0ea9a1f35f77d2e823613`; frontend source exists and is 20 commits ahead of accepted APP-BATCH-A; no `tests/app_batch_b/**`, result report, or evidence manifest observed | Build/typecheck; implement focused UI/integration tests; run localhost/offline acceptance; CHAT review actual result. Keep frozen backend/API unless a reproducible backend defect is proven. |
| P0 | `FOX2-BRIDGE-RC1-TO-INTERNAL-READY` | Make the internal Windows Bridge usable and recoverable with correct no-replay behavior | **DOING** | CHAT | R5 result `work/FOX2-BRIDGE-RC1-PRESENTATION-LOCK-CERTIFIER-REWORK-R5-20261022@10326dd116ccbfa90a70db4f4c8ec27487ee4fbf`; 69 focused + 686 full PASS; 17/17 evidence SHA-256 verified; R5 code-only CHAT_ACCEPT `1ef5506d592cc7da9c93e61d86a158c12b9b27b3`; CODEX exit 1 after push; Dispatch consumed/no-replay; integrated host runner published `work/FOX2-BRIDGE-INTERNAL-VALIDATION-20261022@f551e3790aa93b2a43b710e4756630d95f2472b3` (NOT_RUN) | Next: one authorized Owner-host integrated Bridge internal validation using R5 external certifier and exact A04 package; prove WPF lock, UI, graceful exit, state preservation, uninstall/reinstall, local trial, restart and no-replay. Then CHAT final acceptance. Do not replay R5. |
| P1 | `FOX2-M1-A-RELEASE-INTEGRATION` | Integrate the accepted runnable M1-A product into the intended release/main line | **BACKLOG** | CHAT | APP-BATCH-A accepted; APP-BATCH-B not yet accepted; main and APP lineages currently diverged | Start only after APP-BATCH-B CHAT acceptance and explicit protected-main/merge authority. |
| P2 | `FOX2-M1-B-PROVIDER-INTEGRATION` | Add read-only real market-data integration: REST + market WebSocket + recovery/freshness | **BACKLOG** | CHAT | Provider rights/network/entitlement evidence not current; no provider implementation milestone accepted | Begin after M1-A product acceptance and explicit provider/data-rights capability. No broker/account/order write. |
| P3 | `FOX2-M2-DATA-HARDENING` | Extend coverage, PIT/corporate-actions handling and soak/recovery quality | **BACKLOG** | CHAT | M2 not started under current M1 delivery | Start after M1-B data path is accepted. |
| Later | `FOX2-M3-M4-DOMAIN-ENGINES` | Portfolio Risk, Exit/Profit Protection, capital/discovery/analytics engines under their own released BRDs | **BACKLOG** | CHAT | Current Governance Registry releases BRD-00/06/08 for M1; BRD-03/04 engine implementation is not current released M1 scope | Research may continue; implementation waits for released BRD/acceptance/source authority. |

### BLOCKED

**None at project level.**

A task is placed in BLOCKED only when an active outcome has a real prerequisite that prevents progress. Historical blocked preflights, old provider-rights gaps, stale Issue text, or an unrun future task do not make the whole project BLOCKED.

## Accepted capability baseline

| Capability | Evidence | Board state |
| --- | --- | --- |
| M1 backend foundation / contracts | accepted P2-01 lineage | **DONE** |
| SQLite versioned store / persistence | accepted P2-02 lineage | **DONE** |
| Offline DSM / source-selection core | `work/FOX2-M1-P2-03-dsm-codex@d90987afd861a41aef01059d95ca039509ede09c`; focused and upstream regression evidence preserved | **DONE** |
| M1-A backend API + watchlist integration | `work/FOX2-M1-A-APP-BATCH-A-codex@3db6298e4286022e5820eb7b712c436cbade6a62`; 364 PASS / 3 superseded stage-only deselections | **DONE** |
| Agile Lite project-management reform | Policy 2.1.0 + Routing 1.5.0 + Protocol 13 effective for new/re-scoped human management on main | **DONE** |
| React/Vite presentation source | present on APP-BATCH-B branch | **IMPLEMENTED_NOT_ACCEPTED** |
| Bridge R5 certifier correction | Result `10326dd1`, focused 69 + full 686 PASS, CHAT review `1ef5506d`; CODEX exit 1 after push retained | **CHAT_ACCEPTED_CODE_ONLY / HOST_NOT_RUN** |

## Bridge completion plan — one logical task

**Task:** `FOX2-BRIDGE-RC1-TO-INTERNAL-READY`  
**Goal:** `INTERNAL_FOX2_BRIDGE_READY`  
**Board status:** **DOING**  
**Rule:** R5, former A05, G3/G4, local trial and restart/no-replay are internal checks of this one task, not separate Agile tasks.

### Definition of Done

Bridge moves to **DONE** only when all three outcome slices below are satisfied.

#### 1. Correct the certifier and accept R5

R5 attempt consumed once; bounded code/test correction CHAT_ACCEPT at `1ef5506d592cc7da9c93e61d86a158c12b9b27b3`. Prior task/prompt/Dispatch/PreExec remain immutable; no replay.

Required outcome:

- immutable R5 launcher consumed exactly once; CODEX exit 1 due to usage limit after result push;
- corrected certifier must fail closed for pre-live `ABSENT + errno13/no-winerror`;
- preserve valid winerror32 and differential-proof behavior;
- focused and affected regression tests PASS;
- no unauthorized product path change;
- remote result `10326dd116ccbfa90a70db4f4c8ec27487ee4fbf` received `CHAT_ACCEPT` **for R5 code/test only**, not host lifecycle; 17/17 non-null evidence digests independently read back.

No further R5 coding attempt is required on current evidence. Any newly observed real-host defect remains within the same Bridge Whole-WP, with fresh no-replay identity only if necessary.

#### 2. Run one integrated Bridge internal validation

After R5 CHAT acceptance, execute **one Owner-host validation run** that reuses accepted A04 evidence and covers only missing/current facts.

Reuse without repetition:

- accepted package build/source/inventory provenance;
- exact A04 package SHA-256 `f99c7add1b99bad938d977f634fd8a88e20763f5e35aaadf5cfe3072a1a327ee`;
- accepted install/pointer/receipt evidence;
- STOPPED / paused / setup_complete / current_dispatch=null baseline;
- Worker/legacy absent evidence;
- historical exact-current WPF singleton evidence;
- durable SQLite quick-check / preserved logical-state evidence.

The integrated run must cover the still-material internal acceptance:

1. verify exact installed package/archive/source identity and safe starting state;
2. if one exact-current WPF is already live, reuse it; if zero, launch once; fail on duplicate/wrong WPF;
3. prove live presentation lock denial with the CHAT-accepted R5 semantics;
4. perform UI/basic interaction inspection;
5. graceful exit;
6. prove WPF count returns to zero and the same lock becomes openable;
7. capture fresh durable-state baseline;
8. perform stable external uninstall exactly once;
9. verify uninstall postconditions and durable-state preservation;
10. reinstall the **same exact A04 package** — no rebuild;
11. verify final installed safe state;
12. cover the remaining G3/G4 intent inside the same run: physical/local host viability, installed adoption and usable internal runtime behavior;
13. perform one local/internal trial followed by stop/restart;
14. verify singleton/no duplicate process, no Dispatch replay, preserved safe control state and no Worker/legacy regression.

This is the Agile-Lite replacement for separate Owner-facing A05 → G3 → G4 → independent audit → Canary → restart milestones. The prepared one-shot runner covers lifecycle and presentation restart on the current host; G3 isolated privileged host enforcement, G4 adoption and F1 Worker runtime remain explicitly NOT_RUN until correctly evidenced. Combined management scope is not a machine safety waiver.

Independent WORK audit is **not a default internal gate**. A separate external/provider/broker/LIVE boundary would require its own explicit decision and is outside this Bridge internal-ready task.

#### 3. One final CHAT acceptance

CHAT reviews the union of:

- reusable A04 accepted evidence;
- CHAT-accepted R5 correction;
- the single integrated internal-validation result.

Final verdict is one of:

- `DONE / INTERNAL_FOX2_BRIDGE_READY`;
- `REWORK` with the precise first causal defect in the SAME logical task;
- `BLOCKED` only when a real prerequisite prevents the next safe action.

### Failure / rework rule

- stop at the first material failure;
- preserve all unaffected accepted PASS;
- repair only the causal defect;
- rerun only the affected/current checks;
- never replay a consumed Dispatch;
- never rebuild/reinstall merely to reproduce already accepted evidence;
- do not create a new Board task unless the feature outcome or authority boundary materially changes.

### Current next action

`R5_CHAT_ACCEPTED_CODE_ONLY → ONE_SHOT_OWNER_HOST_LIFECYCLE_RUNNER(e52140d5,NOT_RUN) → G3_G4_INTERNAL_ASSERTIONS_ON_AUTHORIZED_TARGET → FINAL_CHAT_ACCEPTANCE → INTERNAL_FOX2_BRIDGE_READY`

## WIP policy

Current material WIP target is **2**:

1. APP-BATCH-B product closure (`frontend/**`, `tests/app_batch_b/**`).
2. Bridge RC1 internal readiness (`agent_bridge/**` / installed-host validation under its pinned machine contract).

Do not open M1-B, M2, or M3/M4 implementation while both WIP slots are occupied unless Owner explicitly reprioritizes.

## Tracker reconciliation

Open GitHub Issues/PRs are supporting history, not the live board. In particular, Issues #3, #8, #9, #10, #11 and #12 contain valid historical evidence but also stale stage/status wording that has been overtaken by later Git results. Do not use `issue=open` as equivalent to `task=DOING/BLOCKED`.

When a live task changes materially, update this board from observed Git/test/host evidence. Normal bug corrections stay in the same logical task.

## Current critical path

```text
APP-BATCH-B
  -> runnable localhost M1-A
  -> M1-A release integration
  -> M1-B provider integration
  -> M2 hardening
  -> M3/M4 domain engines

Bridge RC1
  -> R5 code/test accepted (DONE; Dispatch consumed/no-replay)
  -> integrated Bridge internal validation
  -> INTERNAL_FOX2_BRIDGE_READY
```

The two top streams are independent enough to progress in parallel while writable paths remain disjoint.

## Next safe actions

- **APP:** continue APP-BATCH-B directly under Agile Lite: build/typecheck, focused UI/API integration tests, localhost/offline acceptance, then CHAT result acceptance. No new Bridge/PreExec ceremony for ordinary reversible native DEV.
- **Bridge:** R5 code correction accepted; one-shot Owner-host lifecycle/restart runner published at `f551e3790aa93b2a43b710e4756630d95f2472b3` and not executed. Run once after host preflight, return sanitized evidence for CHAT; privileged isolated-host G3 and G4 remain NOT_RUN until actual authorized evidence exists.
- **Project:** do not create new governance or micro-WPs unless a real scope/authority/risk boundary appears.

`PROJECT_HEALTH=YELLOW_GREEN / PRODUCT=DOING / BRIDGE=DOING / PROJECT_BLOCKED=NO / WIP=2 / NEXT=APP_BATCH_B_PRODUCT_CLOSURE_PARALLEL_BRIDGE_INTERNAL_VALIDATION`
