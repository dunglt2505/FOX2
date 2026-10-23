# FOX2 — Project Kanban — LIVE

**Operating model:** FOX2 Agile Lite / Policy v2.1.0  
**Board:** one project board: `BACKLOG → DOING ↔ BLOCKED → DONE`  
**Live as of:** 2026-10-23 (main Bridge baseline preserved; Website result review updated on non-main candidate)  
**Status:** `WEBSITE_RESULT_REVIEW_SYNCED_NON_MAIN / MAIN_BOARD_NOT_YET_UPDATED`  
**Management authority:** `main:docs/governance/FOX2_PROJECTWIDE_GOVERNANCE_REGISTRY.json` @ `a7ca2b7610fa8ecd2766c67cfb19a28c32d9e5c9`  
**Rule:** Git/test/host evidence wins over stale Issue/PR prose. Prompt, PreExec, Dispatch, Agent start, or `PUSHED_UNREVIEWED` alone is never DONE.

## Live board

| Priority | ID | Outcome / goal | Status | Delivery owner | Current evidence | Acceptance / next action |
| --- | --- | --- | --- | --- | --- | --- |
| P0 | `FOX2-M1-A-APP-BATCH-B` | Deliver offline-safe localhost M1-A Website: four React/Vite routes, accepted backend, truthful market states, Watchlist, Dark/Light responsive | **DOING — bounded security/HTTP ACCEPTED; browser pending** | CHAT owns acceptance; CODEX VS Code owns remaining host/browser verification | `work/FOX2-M1-A-APP-BATCH-B@d472031a526d04263015c7b871fde35aed740322` (code `5690afb29b662bd62a0adaea364c2c29a1146e45`); CHAT reviewed Vite Origin Guard: foreign-Origin PUT 403, no ASGI receipt/state change; real localhost HTTP 22/22 PASS incl. 28 header cases, typecheck/build PASS, focused 4/4, test-only SQLite ISOLATED_TEST; Git remote readback VERIFIED | Browser UI/Watchlist interactions, theme, 1440/1024/390, console/network/polling, STALE/GAP UI remain NOT_RUN; run real browser checks and publish incremental evidence on same task branch; CHAT final Whole-WP acceptance after review. |
| P0 | `FOX2-BRIDGE-RC1-TO-INTERNAL-READY` | Make the internal Windows Bridge usable and recoverable with correct no-replay behavior | **DOING** | CHAT | R5 remote result `work/FOX2-BRIDGE-RC1-PRESENTATION-LOCK-CERTIFIER-REWORK-R5-20261022@10326dd116ccbfa90a70db4f4c8ec27487ee4fbf` read back and CHAT accepted (69 focused / 686 full PASS); A04 package/host baseline reusable; real host continuation NOT_VERIFIED. R5 consumed/no-replay | Reconcile actual host/installed R5 certifier and current machine authority; one NEW authorized integrated host-validation attempt; CHAT final result acceptance. Never rerun R5 launcher. |
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
| React/Vite presentation + Vite Origin Guard / localhost API | `work/FOX2-M1-A-APP-BATCH-B@d472031a526d04263015c7b871fde35aed740322`; bounded CHAT review: 22/22 HTTP, 28 header negatives, 4/4 focused, typecheck/build PASS | **BUILD_SECURITY_HTTP_ACCEPTED / BROWSER_NOT_RUN / WHOLE_WP_DOING** |
| Bridge R5 certifier correction | remote `10326dd116ccbfa90a70db4f4c8ec27487ee4fbf`; 69 focused and 686 full PASS; CHAT code/result review 2026-10-23 | **DONE — bounded BUILD correction only** |

## Website M1-A closure — verified Git result and residual browser test (2026-10-23)

**Scope:** Existing Whole-WP `FOX2-M1-A-APP-BATCH-B`; no new WP or Dispatch; no merge/main. **READY_FOR_BOARD=YES / DECISION=KEEP_DOING.**

- **DONE (bounded):** CODE_CHANGE on frontend Vite Origin Guard, HTTP 22/22 PASS including foreign-Origin 403/no forwarded request/no SQLite mutation and 28 header cases, typecheck/build and focused 4/4 PASS, evidence/manifest/readback verified at product branch `d472031a526d04263015c7b871fde35aed740322`. CHAT ACCEPT applies only to Origin Guard/security + recorded HTTP/build subset, not the Website product.
- **NOT_RUN:** Real browser navigation/rendering at four routes, UI Watchlist workflows, Dark/Light at 1440/1024/390, STALE/GAP presentation and browser console/network/polling evidence. HTTP HTML route entry is not browser acceptance. M1-A product remains **DOING / NOT_ACCEPTED**, with no provider/WS/LIVE permission inferred.
- **NEXT_SAFE_ACTION:** Reuse the current single-writer Website worktree in VS Code, run actual local Chromium/Edge/Playwright browser acceptance if executable capability exists, save screenshots/console/network/result mapping within `reports/FOX2-M1-A-APP-BATCH-B/evidence/**` and scoped test code if needed, Git push/readback new full SHA, then CHAT review and Board update. If browser automation unavailable, report `BROWSER_NOT_RUN` with exact host blocker instead of forging PASS.
- **OWNER workspace preference:** One persistent FOX2 VS Code workspace; reuse existing Website worktree rather than create attempt-specific checkout. Do not consolidate/delete the Website worktree while its active evidence/result is unreviewed. Cleanup remains a separate safe inventory activity, not a browser gate.
- **Document publication:** this status is recorded on existing non-main PR branch `work/FOX2-AGILE-WEBSITE-CLOSURE-20261023`; protected `main` retains its current authoritative Board until authorized integration. The Bridge status above is synchronized from the newer main baseline, not overwritten by older candidate text.

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

- **APP:** preserve accepted Origin Guard/HTTP/typecheck/build/focused evidence at `d472031a526d04263015c7b871fde35aed740322`; execute only pending real browser UI/theme/responsive/network acceptance, push scoped results and request CHAT final Whole-WP review. No new Bridge/PreExec ceremony.
- **Bridge:** R5 result already reviewed; **do not rerun R5**. Reconcile installed host, current machine contract and rights; prepare one new authorized integrated host validation and final Git/CHAT acceptance.
- **Project:** do not create new governance or micro-WPs unless a real scope/authority/risk boundary appears.

`PROJECT_HEALTH=YELLOW_GREEN / WEBSITE_SECURITY_HTTP=CHAT_ACCEPTED / WEBSITE_BROWSER=NOT_RUN / WEBSITE_WP=DOING / BRIDGE=DOING / PROJECT_BLOCKED=NO / WIP=2 / NEXT=WEBSITE_BROWSER_ACCEPTANCE_PARALLEL_BRIDGE_INTEGRATED_HOST_VALIDATION`
