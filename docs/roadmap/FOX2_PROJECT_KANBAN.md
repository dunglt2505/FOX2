# FOX2 — Project Kanban — LIVE

**Operating model:** FOX2 Agile Lite / Policy v2.1.0  
**Board:** one project board: `BACKLOG → DOING ↔ BLOCKED → DONE`  
**Evidence checked:** 2026-10-24 (Git SHA/PR/CI/Agent evidence; fresh Owner-host heartbeat UNKNOWN)  
**Status:** `NON_MAIN_PROGRESS_SYNC_CANDIDATE / MAIN_UNCHANGED_UNTIL_AUTHORIZED_MERGE`  
**Management authority:** `main:docs/governance/FOX2_PROJECTWIDE_GOVERNANCE_REGISTRY.json` @ `a7ca2b7610fa8ecd2766c67cfb19a28c32d9e5c9`  
**Rule:** Git/test/host evidence wins over stale Issue/PR prose. Prompt, PreExec, Dispatch, Agent start, or `PUSHED_UNREVIEWED` alone is never DONE.

## Live board

| Priority | ID | Outcome / goal | Status | Delivery owner | Current evidence | Acceptance / next action |
| --- | --- | --- | --- | --- | --- | --- |
| P0 | `FOX2-M1-A-APP-BATCH-B` | First usable offline-safe M1-A Website: React/Vite 4 routes, accepted backend, Watchlist, Dark/Light/responsive | **DOING / SECURITY_HTTP_ACCEPTED / BROWSER_NOT_RUN** | CHAT acceptance; CODEX VS Code for real browser tests | Verified result `work/FOX2-M1-A-APP-BATCH-B@d472031a526d04263015c7b871fde35aed740322` (code `5690afb29b662bd62a0adaea364c2c29a1146e45`); bounded CHAT_ACCEPTED Origin Guard rework; typecheck/build PASS, focused 4/4, real localhost HTTP 22/22 plus 28 Host/Origin negatives PASS; no provider fixture/live rights. | Reuse same Website worktree. Run real browser 4 routes/deep link, UI Watchlist, Dark/Light 1440/1024/390, UNKNOWN/STALE/GAP, browser console/network/polling; save actual evidence and Git SHA for CHAT Whole-WP ACCEPT/REWORK. NOT_RUN is not PASS, no R5 replay, no main merge. |
| P0 | `FOX2-BRIDGE-RC1-TO-INTERNAL-READY` | Make the internal Windows Bridge usable and recoverable with correct no-replay behavior | **DOING — restart FAILED / G3-G4 NOT_RUN** | CHAT | R5 `10326dd116ccbfa90a70db4f4c8ec27487ee4fbf` CHAT_ACCEPTED_CODE_ONLY (69/686 PASS). Pause recovery `68c648fc0abcfa787a7f40cc96669fbd1715a144` safe/paused=true. Integrated Validation 001 CONSUMED; A04 lifecycle PASS_OBSERVED (private local proof not independently read), restart FAILED (`RuntimeException`, cause UNKNOWN). G3/G4 NOT_RUN. Git Delivery PR #26 `e6b898b28a427c0492f466a2beab0f3c278ac40b`: 235 focused PASS, 774 full before final guard, 85 final guard PASS; PUSHED_UNREVIEWED, installed E2E NOT_RUN. | Preserve consumed R5/Validation001. Physical Windows G3 read-only and authorized E1-E10 → separately authorized G4 final F1 adoption → final F1 restart/singleton/no-replay. Bind installed Policy/CLI/Git rights, test verifier and writer/lease for Git Delivery host E2E. CHAT final acceptance; no Bridge READY inference. |
| P1 | `FOX2-M1-A-RELEASE-INTEGRATION` | Integrate the accepted runnable M1-A product into the intended release/main line | **BACKLOG** | CHAT | APP-BATCH-A accepted; APP-BATCH-B not yet accepted; main and APP lineages currently diverged | Start only after APP-BATCH-B CHAT acceptance and explicit protected-main/merge authority. |
| P2 | `FOX2-M1-B-PROVIDER-INTEGRATION` | Add read-only real market-data integration: REST + market WebSocket + recovery/freshness | **BACKLOG** | CHAT | Provider rights/network/entitlement evidence not current; no provider implementation milestone accepted | Begin after M1-A product acceptance and explicit provider/data-rights capability. No broker/account/order write. |
| P3 | `FOX2-M2-DATA-HARDENING` | Extend coverage, PIT/corporate-actions handling and soak/recovery quality | **BACKLOG** | CHAT | M2 not started under current M1 delivery | Start after M1-B data path is accepted. |
| Later | `FOX2-M3-M4-DOMAIN-ENGINES` | Portfolio Risk, Exit/Profit Protection, capital/discovery/analytics engines under their own released BRDs | **BACKLOG** | CHAT | Current Governance Registry releases BRD-00/06/08 for M1; BRD-03/04 engine implementation is not current released M1 scope | Research may continue; implementation waits for released BRD/acceptance/source authority. |

### BLOCKED

**None at project level.** APP R5 native route and Bridge host G3/G4 have scoped unresolved prerequisites; the two Whole-WPs remain DOING.

A task is placed in BLOCKED only when an active outcome has a real prerequisite that prevents progress. Historical blocked preflights, old provider-rights gaps, stale Issue text, or an unrun future task do not make the whole project BLOCKED.

## Accepted capability baseline

| Capability | Evidence | Board state |
| --- | --- | --- |
| M1 backend foundation / contracts | accepted P2-01 lineage | **DONE** |
| SQLite versioned store / persistence | accepted P2-02 lineage | **DONE** |
| Offline DSM / source-selection core | `work/FOX2-M1-P2-03-dsm-codex@d90987afd861a41aef01059d95ca039509ede09c`; focused and upstream regression evidence preserved | **DONE** |
| M1-A backend API + watchlist integration | `work/FOX2-M1-A-APP-BATCH-A-codex@3db6298e4286022e5820eb7b712c436cbade6a62`; 364 PASS / 3 superseded stage-only deselections | **DONE** |
| Agile Lite project-management reform | Policy 2.1.0 + Routing 1.5.0 + Protocol 13 effective for new/re-scoped human management on main | **DONE** |
| React/Vite presentation source + loopback HTTP integration | `work/FOX2-M1-A-APP-BATCH-B@d472031a526d04263015c7b871fde35aed740322`; code `5690afb29b662bd62a0adaea364c2c29a1146e45`; build/typecheck PASS, 4/4 focused PASS, 22/22 real HTTP PASS; browser/UI acceptance NOT_RUN | **TEST_EVIDENCED_SCOPED / PRODUCT_NOT_ACCEPTED** |
| Bridge R5 certifier correction | remote `10326dd116ccbfa90a70db4f4c8ec27487ee4fbf`; 69 focused and 686 full PASS; CHAT code/result review 2026-10-23 | **DONE — bounded BUILD correction only** |
| Bridge Git Delivery source/fixtures | PR #26 @ `e6b898b28a427c0492f466a2beab0f3c278ac40b`; 235 focused PASS, 774 full before final guard, 85 final guard PASS; installed CODEX/Copilot E2E NOT_RUN | **PUSHED_UNREVIEWED / TEST_EVIDENCED_SCOPED** |

## Bridge completion plan — one logical task

**Task:** `FOX2-BRIDGE-RC1-TO-INTERNAL-READY`  
**Goal:** `INTERNAL_FOX2_BRIDGE_READY`  
**Board status:** **DOING**  
**Rule:** R5, former A05, G3/G4, local trial and restart/no-replay are internal checks of this one task, not separate Agile tasks.

### Promotion and status

`OUTCOME_DEFINED=YES; DEPENDENCIES_KNOWN=YES; SOURCE_READY_ENOUGH=YES` for management planning; `ACCEPTANCE_ACTIONABLE=YES; NEXT_SAFE_ACTION_KNOWN=YES`.
**Decision:** `READY_FOR_BOARD=YES / PROMOTE_TO_DOING` (retain existing DOING). **Stage:** TEST. **Product release:** NOT_ATTESTED.

### Definition of Done — four observable outcomes

| Outcome | Observed baseline | Remaining acceptance |
| --- | --- | --- |
| Exact identity / safe install | A04 accepted package build, exact pointer/install/safe state, stable singleton observations reusable | Fresh host/installed state and exact accepted R5 certifier invocation identity |
| WPF presentation lifecycle | R5 offline correction accepted: 69 focused PASS, 686 full PASS | Real WPF singleton, live lock proof, UI inspect/check, graceful exit, zero WPF and same lock OPENABLE |
| Durable lifecycle recovery | A04 logical state, SQLite quick_check and consumption baseline reusable; A04 stopped before uninstall | One stable external uninstall, postconditions, durable-state preservation, reinstall same A04 package SHA `f99c7add1b99bad938d977f634fd8a88e20763f5e35aaadf5cfe3072a1a327ee`, safe final state |
| Usable internal restart/no-replay | Existing no-replay/ledger behavior and offline tests reusable | One internal local trial, stop/restart, singleton/Worker-F1 applicability and no consumed Dispatch replay on Owner host |

**R5 result:** `work/FOX2-BRIDGE-RC1-PRESENTATION-LOCK-CERTIFIER-REWORK-R5-20261022@10326dd116ccbfa90a70db4f4c8ec27487ee4fbf` — bounded code/result **CHAT_ACCEPTED 2026-10-23**; it is **not** proof the installed package carries the corrected certifier and does not certify host lifecycle.

**Execution boundary:** R5 Dispatch **CONSUMED_NO_REPLAY**; **do not rerun its Owner launcher**. This management update is not an executable grant. Current host state, machine-pinned source/validator, installed R5 adoption, worktree/one-writer, permissions and any route-specific PreExec must be verified for **one new integrated validation attempt** before host mutation. Stop on mismatch; do not fabricate PASS.

Run one integrated validation of missing/current host facts (former A05/G3/G4/local trial/restart) with actual installed runtime and appropriate bounded evidence. Reuse accepted A04 package/provenance and unchanged PASS; no automatic rebuild, replay, administrative micro-WP, WORK audit or Canary. Protect host/service/F1/irreversible operations with specific actual authority.

**CHAT final acceptance:** inspect Git-pushed result SHA and actual safe host outcome, then `DONE / INTERNAL_FOX2_BRIDGE_READY`, `REWORK` in this same task for the first causal defect, or `BLOCKED` for a real failed prerequisite. Host lifecycle, uninstall/reinstall and internal restart are currently **NOT_VERIFIED**, not PASS.

### Current next action

`CHAT_R5_REVIEW_DONE → HOST_AND_INSTALLED_CONTRACT_RECONCILIATION → NEW_AUTHORIZED_INTEGRATED_VALIDATION_ONCE → REMOTE_GIT_RESULT_READBACK → CHAT_FINAL_ACCEPTANCE`

### Evidence and dependency reconciliation — 2026-10-23 20:03 ICT

The earlier four-outcome host plan below its original R5 baseline is **historical** where superseded by actual Validation 001 and later Owner-approved physical-host G3 direction. Validation 001 emitted A04 lifecycle PASS_OBSERVED, then failed at restart and was CONSUMED/NO_REPLAY. Its private lifecycle JSON was not independently reviewed; no final F1 restart PASS exists. The A04 restart-only continuation is **deferred** unless read-only diagnosis establishes a real need. Current critical acceptance order is **G3 physical Windows host capability/enforcement E1-E10 and restore → separately authorized G4 final F1 adoption → final installed F1 restart/singleton/no-replay → CHAT final result acceptance**. The actual installed Git Delivery verifier, recovery ref, credentials, writer lease and normal/interrupted CODEX/Copilot E2E remain unverified. PR #26 is a source/test candidate, not internal-ready acceptance. Owner-host heartbeat remains UNKNOWN.

Website PR #27 remains a separate unmerged closure-plan candidate; R3/R4 consumed and R5 preclaim alias error are historical. Later native VS Code Extension work published actual APP code/test result `5690afb29b662bd62a0adaea364c2c29a1146e45` and receipt HEAD `d472031a526d04263015c7b871fde35aed740322` with verified remote readback. The Origin guard defect was reproduced and corrected; frontend build/typecheck/4 focused and 22 real HTTP checks passed on isolated loopback fixtures. Browser rendering/responsive/STALE-GAP/polling checks remain NOT_RUN and product CHAT acceptance PENDING. Do not replay consumed attempts or claim a canonical M1 PASS (105/105 NOT_RUN).

**Sync boundary:** this Board is a non-main progress candidate. Main, Registry, historical Master Plans, immutable Dispatch and installed runtime are unchanged until separately authorized operations.

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
  -> R5 correction CHAT_ACCEPTED
  -> new authorized integrated Bridge host validation
  -> INTERNAL_FOX2_BRIDGE_READY
```

The two top streams are independent enough to progress in parallel while writable paths remain disjoint.

## Next safe actions

- **APP:** code/test Git result now delivered and read back. CHAT review bounded Origin-guard/HTTP evidence; run actual browser navigation, Dark/Light responsive 1440/1024/390, data-state and network/polling checks on an authorized host, then decide offline product acceptance. No duplicate R3/R4 or Bridge/PreExec ceremony for ordinary reversible native DEV.
- **Bridge:** R5 result already reviewed; **do not rerun R5**. Reconcile installed host, current machine contract and rights; prepare one new authorized integrated host validation and final Git/CHAT acceptance.
- **Project:** do not create new governance or micro-WPs unless a real scope/authority/risk boundary appears.

`PROJECT_HEALTH=YELLOW / APP=DOING_CODE_TEST_DELIVERED_BROWSER_PENDING / BRIDGE=DOING_G3_G4_AND_RESTART_PENDING / PROJECT_BLOCKED=NO / WIP_TARGET=2 / M1_ACCEPTANCE=0_OF_105 / BRIDGE_READY=NOT_ATTESTED / MAIN_SYNC=PENDING`

## 2026-10-24 — Skills-based project roadmap

**Authority:** main Registry for human new work: Policy v2.1.0, Routing v1.5.0, Git-first Protocol 13, BRD-00/06/08 v0.5, M1 TechSpec 0.1, Data Contract 0.4, Acceptance v0.4. Immutable Bridge machine pins remain separate. This is a non-main management candidate, not a release or mutation grant.

**WIP=2, SAME Whole-WPs:** Website APP-BATCH-B `DOING`; Bridge RC1 `TEST/DOING`; backend APP-BATCH-A, DSM, store, M1 foundation accepted. Website Origin Guard/security, HTTP and build scoped accepted, browser not run. Bridge R5 certifier bounded code accepted `10326dd116ccbfa90a70db4f4c8ec27487ee4fbf`, but installed F1 lifecycle not attested; Validation 001 `CONSUMED_NO_REPLAY` and restart `FAILED`. PR #26 `e6b898b28a427c0492f466a2beab0f3c278ac40b` is `PUSHED_UNREVIEWED` Git Delivery native source tests (235 focused, 774 full pre-final-guard, 85 final-guard PASS), not installed host E2E.

**Next sequence (no new task IDs):** 
- APP: one real Windows browser pass on existing workspace/branch for four routes/navigation/reloads, UI Watchlist, Dark/Light 1440/1024/390, truthful null/STALE/GAP, console/network, no upstream calls/polling. Use valid test-only backends, preserve accepted 22/22 HTTP/4/4 focused evidence. Git evidence readback then CHAT final offline Website verdict; failure => bounded SAME-WP rework.
- Bridge: read-only reconcile selected physical Windows installed source/Policy/ACL/AppLocker/backup, ledger/writer/host rights; separately authorized G3 E1–E10 enforcement + restoration; separately authorized G4 final F1 package adoption; real installed restart/singleton/no-replay and normal/interrupted CODEX/Copilot Git Delivery E2E; Git result/CHAT final acceptance. R5 and Validation 001 never replayed. Reuse A04 only to the scope truly evidenced.
- CHAT governance/hygiene: avoid applying historical policy versions to new human tasks; resolve PR #27 vs PR #30 overlapping Board content before any authorized integration; Skills v0.5.9 active for this CHAT plugin but draft PR #28 is not main/runtime adoption; PR #31 BRD standard, PR #25 BRD-09 remain candidates; avoid mass reformat. Maintain one persistent VS Code FOX2 workspace; read-only local Git worktree/dirty/process inventory before moving/archive any C:\Projects folder. No destructive cleanup/no third writer.
- After APP acceptance: authorized M1-A release/main integration; then M1-B provider read-only REST/WS only upon rights/net/entitlement grants; M2 hardening; finally M3/M4 domain engines only with effective BRDs and acceptance.

**Acceptance truth:** v0.4 canonical 105-case CSV historically marks all NOT_RUN; scoped Git-backed APP results do not silently rewrite it. Do not call 105/105 PASS. No main/merge/deploy/provider/broker/LIVE authority from this plan.

**STATUS:** `GOVERNANCE_HUMAN_EFFECTIVE / WEBSITE_DOING_BROWSER_PENDING / BRIDGE_TEST_IN_PROGRESS_G3_G4_NOT_RUN / RELEASE_INTEGRATION_BACKLOG / PROVIDER_BACKLOG / HOST_LIVE_STATE_NOT_VERIFIED / MAIN_NOT_UPDATED`.

