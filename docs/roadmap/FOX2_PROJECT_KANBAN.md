# FOX2 — Project Kanban — LIVE

**Operating model:** FOX2 Agile Lite / Policy v2.1.0  
**Board:** one project board: `BACKLOG → DOING ↔ BLOCKED → DONE`  
**Live as of:** 2026-10-22 21:15 ICT  
**Status:** `LIVE_GIT_EVIDENCE_SYNCED`  
**Management authority:** `main:docs/governance/FOX2_PROJECTWIDE_GOVERNANCE_REGISTRY.json` @ `a7ca2b7610fa8ecd2766c67cfb19a28c32d9e5c9`  
**Rule:** Git/test/host evidence wins over stale Issue/PR prose. Prompt, PreExec, Dispatch, Agent start, or `PUSHED_UNREVIEWED` alone is never DONE.

## Live board

| Priority | ID | Outcome / goal | Status | Delivery owner | Current evidence | Acceptance / next action |
| --- | --- | --- | --- | --- | --- | --- |
| P0 | `FOX2-M1-A-APP-BATCH-B` | Deliver the first runnable localhost FOX2 M1-A product: React/Vite UI + accepted backend integration + offline acceptance | **DOING** | CHAT | Branch `work/FOX2-M1-A-APP-BATCH-B@51a97bfa7420efa0a0e0ea9a1f35f77d2e823613`; frontend source exists and is 20 commits ahead of accepted APP-BATCH-A; no `tests/app_batch_b/**`, result report, or evidence manifest observed | Build/typecheck; implement focused UI/integration tests; run localhost/offline acceptance; CHAT review actual result. Keep frozen backend/API unless a reproducible backend defect is proven. |
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

- **APP:** continue APP-BATCH-B directly under Agile Lite: build/typecheck, focused UI/API integration tests, localhost/offline acceptance, then CHAT result acceptance. No new Bridge/PreExec ceremony for ordinary reversible native DEV.
- **Bridge:** consume the already-published R5 execution exactly once; preserve no-replay; then CHAT review and one integrated internal validation.
- **Project:** do not create new governance or micro-WPs unless a real scope/authority/risk boundary appears.

`PROJECT_HEALTH=YELLOW_GREEN / PRODUCT=DOING / BRIDGE=DOING / PROJECT_BLOCKED=NO / WIP=2 / NEXT=APP_BATCH_B_PRODUCT_CLOSURE_PARALLEL_R5_BRIDGE`
