# FOX2 — Project Kanban — LIVE

**Operating model:** FOX2 Agile Lite / Policy v2.1.0  
**Board:** one project board: `BACKLOG → DOING ↔ BLOCKED → DONE`  
**Live as of:** 2026-10-23 (PR #26 exact agent_bridge code tree full Windows CI 778 PASS; installed Bridge host E2E HOLD)
**Status:** `LIVE_GIT_EVIDENCE_SYNCED`  
**Management authority:** `main:docs/governance/FOX2_PROJECTWIDE_GOVERNANCE_REGISTRY.json` @ `a7ca2b7610fa8ecd2766c67cfb19a28c32d9e5c9`  
**Rule:** Git/test/host evidence wins over stale Issue/PR prose. Prompt, PreExec, Dispatch, Agent start, or `PUSHED_UNREVIEWED` alone is never DONE.

## Live board

| Priority | ID | Outcome / goal | Status | Delivery owner | Current evidence | Acceptance / next action |
| --- | --- | --- | --- | --- | --- | --- |
| P0 | `FOX2-M1-A-APP-BATCH-B` | Deliver the first runnable localhost FOX2 M1-A product: React/Vite UI + accepted backend integration + offline acceptance | **DOING** | CHAT | Branch `work/FOX2-M1-A-APP-BATCH-B@51a97bfa7420efa0a0e0ea9a1f35f77d2e823613`; frontend source exists and is 20 commits ahead of accepted APP-BATCH-A; no `tests/app_batch_b/**`, result report, or evidence manifest observed | Build/typecheck; implement focused UI/integration tests; run localhost/offline acceptance; CHAT review actual result. Keep frozen backend/API unless a reproducible backend defect is proven. |
| P0 | `FOX2-BRIDGE-RC1-TO-INTERNAL-READY` | Internal Windows Bridge safe, usable and recoverable | **DOING** | CHAT (review/integration); WORK/CODEX result published | G2/R5 already accepted; A04 integrated attempt001 CONSUMED/NO_REPLAY. Existing baseline Windows CI on `b11bf27` SUCCESS, Git Delivery 757 PASS prior. **PR #26** Draft source `e6b898b28a427c0492f466a2beab0f3c278ac40b`, exact agent_bridge tree `922db7077737f47d03537f475ffbc70520dec37a`, CHAT **ACCEPT CODE/OFFLINE-SCOPED** via PR review #5626116011; Independent Windows CI #39930138365 checked exact PR26 agent_bridge tree 922db707 and **778 full tests + 34 package tests PASS** on verifier-only branch fef9f3e (F0 DENY, not host install). WORK native 774 pre-final + 85 final scoped tests remain historical. Trusted required-test gate and WIP scope/UUID/quiescence/writer lease present as fail-closed code, not installed runtime proof. G3 physical enforcement/G4 NOT_RUN, Bridge internal-ready NOT_ATTESTED | **Runtime HOLD:** installed Policy/Dictionary/CLI and ledger/source readback, Git rights, trusted test verifier, authorized recovery ref, child process quiescence and exclusive writer proof unavailable; installed CODEX/Copilot normal/interrupted E2E NOT_RUN. Next safe action read-only host reconciliation then actual supervisor bindings and NEW permitted non-main test attempts; no main merge, no replay or LIVE. |
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

**Owner decision 2026-10-23 — G3 uses Owner's PHYSICAL Windows computer.** Only relevant Windows capabilities/permission and existing service/policy state are preconditions; no extra hardware-form-factor admission. Current G3 task, PreExec and read-only capability source at `9f2d10822fb1a3926b8bda6d992a795880160927`. Earlier BLOCKED G3 receipt remains historical. G2/R5 accepted and A04 lifecycle PASS_OBSERVED are preserved; integrated attempt 001 remains CONSUMED, restart FAILED, unused A04 restart-only runner ON_HOLD. Before privileged changes, current host must establish Windows AppLocker/SCM/privilege, no-conflict and existing-policy restoration capability. G3/G4 host execution NOT_RUN; G4 adoption is a distinct right, no Canary/LIVE/main/provider/broker.

**G3 host result intake (Owner stdout, 2026-10-23 04:02:17Z):** `FOX2_G3_SOURCE_IDENTITY=PASS`, syntax PASS, read-only scan COMPLETE. Windows edition candidate true; AppLocker native module AVAILABLE and GP policy query PASS; no domain, F1 service or F1 authority root. AppIDSvc currently Stopped (not host capability FAIL). Administrator token absent in this non-elevated session; Group Policy policy digests equal, but actual export/restore and CSP coverage NOT_VERIFIED. Privileged G3, G4 and internal-ready remain NOT_RUN/NOT_ATTESTED. Current future PreExec source helper repaired at `fc982cbf734fa3049b2c6d29862dfb1142c8a361` (9 Git invocations); previously published G3 PreExec v3 task/script binding is historical-only. No new runtime claim consumed.

**Owner elevated G3 snapshot intake (2026-10-23 04:14:24Z):** Administrator PASS; AppLocker local and effective XML export/readback PASS, both SHA-256 `635222d6f1ee0a7561e6c04e8894e688a5d19a3ce7549294f4c821a11f807e15` matched the previous GP query; drift NONE_OBSERVED. Backup remains local only (`LOCALAPPDATA\FOX2\G3PolicySnapshots\20261023T041424Z`). `AppIDSvc=Stopped`, start mode Manual; F1 service/root absent. No policy or service mutation. Restore execution NOT_RUN and CSP coverage NOT_VERIFIED; G3 privileged tests/G4 NOT_RUN, Bridge readiness NOT_ATTESTED.

**G3 policy inventory finding — Owner stdout 2026-10-23:** Local/Effective hash matched the preserved private snapshot; each has 0 collections, 0 Allows and 0 Denies across Exe, Script, Msi, Dll and Appx. `EXE_SCRIPT_ALLOW_BASELINE_MISSING` is a hard stop for `f1_policy.policy_artifact` under accepted G2 source; this was expected fail-closed behavior. Offline candidate generation requires original-snapshot digest + explicit, host-reviewed Exe/Script path manifest and produces AuditOnly XML only. No automatic default rules, no service/policy modification. Candidate module/CLI/focused negative tests published at `8138fb6a2dc35f78fed5c2713db4ee72bb03b856`, latest failure cleanup `ee504e435b068dc7ef3d07d94705251cf12756c2`; 68/68 scoped offline candidate/G2 policy tests PASS; CHAT_ACCEPTED_OFFLINE_TOOL_ONLY. This is not host-policy validation. Accepted G2/R5/A04 evidence remains unchanged.


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

This is the Agile-Lite replacement for separate Owner-facing A05 → G3 → G4 → independent audit → Canary → restart milestones. The prepared one-shot runner covers lifecycle and presentation restart on the current host; G3 physical Windows host enforcement, G4 adoption and F1 Worker runtime remain explicitly NOT_RUN until correctly evidenced. Combined management scope is not a machine safety waiver.

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

`G2_F1_BUILD_CHAT_ACCEPT + R5_CODE_CHAT_ACCEPT + A04_LIFECYCLE_PASS_OBSERVED/ATTEMPT001_CONSUMED_RESTART_FAILED + G3_PHYSICAL_READONLY_AND_ADMIN_GP_EXPORT_PASS_SCOPED_ZERO_ALLOW_RULES → ONE_REMAINING_HOST_READONLY_INTAKE(GIT_LEDGER_INSTALLED_CLI_ALLOW_ACL_PACKAGE) → BIND_TRUSTED_TEST_VERIFIER_WRITER_AND_WIP_RECOVERY_AUTHORITY → NEW_AUTHORIZED_NON_MAIN_NORMAL_AND_INTERRUPTED_E2E → G3_RESTORABLE_POLICY_AND_E1_E10 → G4_INSTALLED_F1_ADOPTION_RESTART → ONE_CHAT_FINAL_ACCEPTANCE`

## Whole-Bridge Agile reality check — 2026-10-23

**One Whole-WP:** `FOX2-BRIDGE-RC1-TO-INTERNAL-READY`; board `DOING`, delivery `HOLD_FOR_ACTUAL_HOST_EVIDENCE`; `INTERNAL_FOX2_BRIDGE_READY=NOT_ATTESTED`. This is outcome tracking, not a new release gate or additional Agent task.

| Slice | SDLC / observed state | Acceptance boundary |
| --- | --- | --- |
| Desktop/Core F0 + R5 | BUILD/TEST code accepted. Prior A04 installed/lifecycle observed; consumed attempt001, restart trial **FAILED_IN_PROGRESS** | Old A04 package is **not** the new F1 package; do not replay or rerun accepted R5 coding |
| F1 G1/G2 | G1 design and G2 build/code CHAT-accepted, offline security tests PASS | F1 installed protection not proven |
| Bridge Git Delivery + WIP | Source PR #26 `e6b898b` CHAT_ACCEPTED **code/offline only**; exact `agent_bridge` tree `922db707` independently passed Windows **778/778 full** plus **34/34 package** tests ([run 39930138365](https://github.com/dunglt2505/FOX2/actions/runs/39930138365)). WIP separate-ref and test gate exist in code | Installed CODEX/Copilot E2E, trusted required-test verifier, Git credentials/rights, immutable recovery grant, child-tree quiescence and one-writer supervisor lease **NOT_VERIFIED** |
| Owner physical G3 host | Administrator, native AppLocker module, GP query and exported XML SHA readback PASS_SCOPED; Local/Effective GP policy **zero RuleCollections/EXE/Script Allow**, AppIDSvc Stopped/Manual, F1 service/root absent | Actual safe Allow/ACL inventory, CSP scope, policy **RESTORE_NOT_TESTED**, privileged G3 E1–E10 **NOT_RUN** |
| G4 + final runtime | Old installed A04 state only; source CI builds F0 DENY/quarantined artifact | G4 final F1 installed adoption/restart **NOT_RUN**; INTERNAL_READY **NOT_ATTESTED** |
| Canary / LIVE | OUT_OF_SCOPE_HOLD | No automatic Canary, broker/provider operation, main merge or LIVE rights |

**Smallest safe critical path (without duplicate gates):** reuse all accepted R5/G2/A04/code CI evidence. Conduct **one remaining read-only owner physical host intake**, combining the already published Git Delivery installed-source/ledger/CLI check and the G3 Allow-path/ACL/package check; do not rerun Owner's earlier AppLocker/Admin/backup probes. Resolve the actual installed Policy/Dictionary/ledger and Git writer rights before any executor use. Bind the trusted test verifier and process-tree/one-writer attestation under real supervisor control; for WIP use only a separately authorized recovery ref. Execute **new non-main authorized normal/failed Agent host attempts** without replaying attempt001, then G3 only after safe restore/coverage checks, followed by G4 installed F1 and restart. CHAT gives **one** final product verdict. PR #25 design remains Candidate; PR #26 code remains Draft/non-main. Neither is runtime or release authority.

**Agile operating correction:** stop parallel CHAT/WORK writers in overlapping `agent_bridge/**`; no more generic source-version cleanup, repeated full CI or separate audit by default. Rework only demonstrable regression(s). Preserve historical FAIL/BLOCKED/NOT_RUN and do not promote them by analogy from offline tests.

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
  -> G2 F1 accepted + A04 lifecycle PASS observed / restart FAILED
  -> G3 physical Windows host checks, G4 F1 adoption still NOT_RUN
  -> INTERNAL_FOX2_BRIDGE_READY
```

The two top streams are independent enough to progress in parallel while writable paths remain disjoint.

## Next safe actions

- **APP:** continue APP-BATCH-B directly under Agile Lite: build/typecheck, focused UI/API integration tests, localhost/offline acceptance, then CHAT result acceptance. No new Bridge/PreExec ceremony for ordinary reversible native DEV.
- **Bridge Git Delivery — PR #26:** [CHAT reviewed](https://github.com/dunglt2505/FOX2/pull/26) source `e6b898b28a427c0492f466a2beab0f3c278ac40b` on draft non-main PR; source/subtree and report remote-readback verified, code + offline test evidence **ACCEPT_SCOPED**, **HOST_E2E/FINAL_DOD HOLD**. 778/778 full Windows Bridge tests plus 34/34 package tests independently PASS on the exact PR26 agent_bridge Git tree via [CI #39930138365](https://github.com/dunglt2505/FOX2/actions/runs/39930138365); verifier commit fef9f3e changes only workflow and Owner-host-intake docs, not code tree. This is source-only TEST, not installed runtime or PR26-root-SHA CI. Previous accepted `b11bf27` Windows CI run `39925879798` remains independent unchanged evidence. WIP host published ref requires independent supervisor/source/permissions/quiescence proof; current source is fail-closed. Next: installed-host read-only Git/ledger/policy/CLI/writer inventory, then bind trusted test verifier/recovery permission/single-writer and run NEW authorized non-main CODEX/Copilot normal/interrupted trials. A04 attempt001 remains consumed; G3 AppLocker Allow baseline and G4 remain NOT_RUN. No main merge, Canary or LIVE.
- **Project:** do not create new governance or micro-WPs unless a real scope/authority/risk boundary appears.

`PROJECT_HEALTH=YELLOW_GREEN / PRODUCT=DOING / BRIDGE=DOING / PROJECT_BLOCKED=NO / WIP=2 / NEXT=APP_BATCH_B_PRODUCT_CLOSURE_PARALLEL_BRIDGE_INTERNAL_VALIDATION`
