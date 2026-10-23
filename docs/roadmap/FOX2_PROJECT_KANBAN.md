# FOX2 — Project Kanban — LIVE

**Operating model:** FOX2 Agile Lite / Policy v2.1.0  
**Board:** one project board: `BACKLOG → DOING ↔ BLOCKED → DONE`  
**Live as of:** 2026-10-22 21:15 ICT (main baseline); Website candidate refreshed 2026-10-23  
**Status:** `OWNER_APPROVED_WEBSITE_UPDATE_PUBLISHED_NON_MAIN / MAIN_BOARD_NOT_YET_CHANGED`  
**Management authority:** `main:docs/governance/FOX2_PROJECTWIDE_GOVERNANCE_REGISTRY.json` @ `a7ca2b7610fa8ecd2766c67cfb19a28c32d9e5c9`  
**Rule:** Git/test/host evidence wins over stale Issue/PR prose. Prompt, PreExec, Dispatch, Agent start, or `PUSHED_UNREVIEWED` alone is never DONE.

## Live board

| Priority | ID | Outcome / goal | Status | Delivery owner | Current evidence | Acceptance / next action |
| --- | --- | --- | --- | --- | --- | --- |
| P0 | `FOX2-M1-A-APP-BATCH-B` | First usable offline-safe localhost M1-A Website: React/Vite Dark/Light, four pages, accepted backend, truthful states and watchlist | **DOING** (native Codex route HOLD) | CHAT; CODEX only verified host-dependent coding | Product `work/FOX2-M1-A-APP-BATCH-B@ee4784e9fbf055979dea540242ce74f2b79736cc`; 25 commits since accepted Batch A, implementation present; focused helper tests 4/4 isolated PASS only; no real frontend build/browser/API integration PASS. R3/R4 consumed and host-blocked; R5 assignment `e5807980...` had PowerShell alias error before claim (local marker NOT_VERIFIED) | Reconcile R5 marker/worktree (do not replay consumed run); run actual npm typecheck/build/focused tests and localhost/backend/browser offline acceptance; publish Git code/evidence and CHAT review ACCEPT/REWORK/HOLD. M1-B/provider/WS not in offline DoD. |
| P0 | `FOX2-BRIDGE-RC1-TO-INTERNAL-READY` | Make the internal Windows Bridge usable and recoverable with correct no-replay behavior | **DOING** | CHAT | Current R5 branch `work/FOX2-BRIDGE-RC1-PRESENTATION-LOCK-CERTIFIER-REWORK-R5-20261022@59ba8b50136ac5bcee7cf2d2edbf65e360812b78`; R5 PreExec PASS; immutable owner launcher published on control branch `42cac745d4611003b304db2af27b433a5bce0455`; R5 result not observed | Execute R5 once on Owner host; CHAT accepts/reworks same logical task. After R5 acceptance, run one integrated Bridge internal validation rather than separate Owner-facing A05/G3/G4/audit/canary micro-tasks. |
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
| Bridge R5 correction | PreExec PASS, execution/result still pending | **DOING** |


## Website product closure — Owner-approved Agile Lite update (2026-10-23)

**READY_FOR_BOARD=YES / DECISION=KEEP_DOING / ID=`FOX2-M1-A-APP-BATCH-B`.** Five checks: outcome = offline usable localhost UI; dependencies = accepted APP-BATCH-A and frozen API; sources = BRD-00/06/08 v0.5, Technical Spec v0.1, acceptance v0.4; acceptance = real checkout build + offline routes/API/watchlist/security/browser; next action = reconcile R5 preclaim failure and run first real checkout product tests. No new Website Whole-WP or micro-WP.

| Execution step | Owner | Exit / evidence | Current |
| --- | --- | --- | --- |
| A. Product readiness | CHAT direct | Actual Git/source/task/marker and exact remaining gaps | IN_PROGRESS |
| B. Build and causal fix | CODEX when native host verified; otherwise CHAT direct within available capabilities | Install/typecheck/build/focused tests; edits only to frontend and APP tests | NOT_VERIFIED |
| C. Offline M1-A acceptance | Verified localhost/browser host; CHAT review | 4 routes/reload, watchlist CAS/validation/persistence, truthful unavailable/stale data, Dark/Light 1440/1024/390, API/security negatives and no provider calls | NOT_RUN |
| D. Delivery and closure | Authorized Git publisher → CHAT | Non-main result SHA, diff, actual test/evidence, verdict ACCEPT/REWORK/HOLD | GIT_DELIVERY_PENDING |

**Scope:** `frontend/**`, `tests/app_batch_b/**`, `reports/FOX2-M1-A-APP-BATCH-B/**` without historical evidence rewriting. Backend accepted P2 and APP-BATCH-A PASS are preserved. Website BUILD is implemented but not accepted; TEST and usability NOT_VERIFIED; offline acceptance does not imply real provider/WS rights. R3/R4 consumed, no replay. PowerShell `GV` alias defect observed before R5 claim; R5 local claim still requires host readback, not inferred. Maintain Model/Thinking pin if completing already prepared R5; no default Bridge PreExec for independent reversible native DEV.

**Master Plan binding:** `docs/roadmap/FOX2_MASTER_EXECUTION_PLAN_20261014.md`, amendment `Owner-approved Agile Lite Website closure — 2026-10-23`. This candidate branch is not a protected-main publication; do not advertise updated `main` as EFFECTIVE before independent authorized promotion.

## Bridge completion plan — one logical task

**Task:** `FOX2-BRIDGE-RC1-TO-INTERNAL-READY`  
**Goal:** `INTERNAL_FOX2_BRIDGE_READY`  
**Board status:** **DOING**  
**Rule:** R5, former A05, G3/G4, local trial and restart/no-replay are internal checks of this one task, not separate Agile tasks.

### Definition of Done

Bridge moves to **DONE** only when all three outcome slices below are satisfied.

#### 1. Correct the certifier and accept R5

Current execution envelope remains pinned to the already-published R5 attempt.

Required outcome:

- run the immutable R5 owner launcher exactly once;
- corrected certifier must fail closed for pre-live `ABSENT + errno13/no-winerror`;
- preserve valid winerror32 and differential-proof behavior;
- focused and affected regression tests PASS;
- no unauthorized product path change;
- result is remote-read and receives `CHAT_ACCEPT`.

If R5 needs another bounded correction and Actor/Model/permissions/allowed paths are unchanged, keep the SAME logical Bridge task and use Agile Lite bounded rework; do not create an Owner-facing R6 micro-WP.

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

This is the Agile-Lite replacement for separate Owner-facing A05 → G3 → G4 → independent audit → Canary → restart milestones.

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

`OWNER_RUN_EXISTING_R5_IMMUTABLE_LAUNCHER_ONCE → CHAT_R5_RESULT_REVIEW → IF_ACCEPT THEN ONE_BRIDGE_INTERNAL_VALIDATION → FINAL_CHAT_ACCEPTANCE`

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
  -> R5 result review
  -> integrated Bridge internal validation
  -> INTERNAL_FOX2_BRIDGE_READY
```

The two top streams are independent enough to progress in parallel while writable paths remain disjoint.

## Next safe actions

- **APP:** follow 2026-10-23 Owner-approved product closure A→D: first reconcile whether R5 was claimed (PowerShell alias error occurred before claim); then run real-checkout typecheck/build/focused tests and browser/API offline acceptance, push evidence and CHAT result review. Do not generate an R6 administrative WP or weaken no-replay.
- **Bridge:** consume the already-published R5 execution exactly once; preserve no-replay; then CHAT review and one integrated internal validation.
- **Project:** do not create new governance or micro-WPs unless a real scope/authority/risk boundary appears.

`PROJECT_HEALTH=YELLOW_GREEN / PRODUCT=DOING_NOT_ACCEPTED / APP_NATIVE_ROUTE=HOLD_PRECLAIM_RECONCILE / BRIDGE=DOING / PROJECT_BLOCKED=NO / WIP=2 / NEXT=APP_BATCH_B_REAL_BUILD_TEST_PARALLEL_BRIDGE`
