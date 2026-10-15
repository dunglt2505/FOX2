# FOX2 — MASTER EXECUTION PLAN — 2026-10-14

**Status:** `ACTIVE / OWNER-DIRECTED / CONSOLIDATED EXECUTION PLAN`  
**Project:** `FOX2 ONLY`  
**Governance:** Project Dictionary v1.2 -> FOX2 Policy V1.8.9 + Routing Index V1.3.0  
**Execution contract:** PreExec Evidence Protocol v1.1 + Preflight Receipt Schema v1 + CHAT Preflight Intake v1.1 + Dictionary-resolved Dispatch Schema v3 + Git-first Protocol v12 + Result Contract v2 + CHAT Result Intake v9  
**Planning rule:** maximize delivery progress with whole-WP/batch execution; do not create Owner-facing micro-WPs for operational reconciliation, metadata cleanup, validator reruns or non-material tool/version deviations.

**Owner priority override — 2026-10-14:** complete the Bridge path before resuming Website/APP-BATCH-B execution. Shared PreExec work is treated only as Bridge-enablement infrastructure. The website dual-theme source is frozen until Bridge reaches `INTERNAL_FOX2_BRIDGE_READY`.


## 1. Current immutable status

### Governance / orchestration

- `FOX2_PROJECT_DICTIONARY_v1.json` is the single machine-readable identity/compatibility registry for all new/re-scoped FOX2 WPs.
- The Dictionary v1.2 currently resolves Policy V1.8.9 and Routing Index V1.3.0.
- New/re-scoped execution uses Dictionary-resolved Dispatch Schema v3 and stable version-neutral dispatch paths.
- New/re-scoped task/result flow uses project-wide PreExec Evidence Protocol v1.1 before Dispatch and Git-first Protocol v12 after PASS_TO_ASSIGN.
- Codex CLI and Copilot CLI are the primary implementation engines.
- Normal coding permission baseline is `FULL_ACCESS`.
- Git publication ownership is dispatch-owned: `delivery_owner=AGENT|BRIDGE`.
- CHAT owns source binding, routing, preflight intake/final assignment, and independent result acceptance.
- Bridge is transport/supervision and only publishes when explicitly assigned as delivery owner.
- Readiness is capability-based; exact version equality is not a hard gate by itself.
- Every new/re-scoped executable WP must publish/read a durable Preflight Receipt before final Agent assignment and executable Dispatch publication.
- `PASS` may close R3/R5; `BLOCKED` and safely-publishable `INFRA_FAILED` must remain durable Git evidence.
- Pre-start failure does not consume a Dispatch and is not an Agent Result.
- Owner-authorized project-wide implementation mandate: `docs/governance/FOX2_PROJECT_WIDE_PREEXEC_IMPLEMENTATION_MANDATE_v1.1.md`; rollout is one systemic infrastructure change, not task-local micro-fixes.

### Project Dictionary / identity registry

- Current canonical control branch: `work/FOX2-DISPATCH-chat`.
- Current canonical dispatch path: `docs/agent_handoff/DISPATCH/<dispatch_id>.json`.
- Current dispatch schema: `3.0`.
- Supported legacy schemas: `2.0`, `0.6`.
- Bridge/runtime consumers must load the Dictionary or a generated binding and must not hand-code competing current constants.
- Released BRD-00/06/08 semantics remain unchanged; BRD identity binding is handled by the BRD Project Dictionary Binding v1.

### Main branch

`main = 40e653f009548f4b1c3d906aba9358e2210a6ab3`.

Main remains a bootstrap/document state and is not the runnable M1-A product. Accepted application and Bridge work remains on bounded non-main branches until a later explicit integration/release boundary.

### M1-A application lane

Accepted/current upstream:

1. **P2-01 Foundation / Contract**
   - accepted remote result: `4bbbdf02387727e7d3c6900f163d7b1eedc5e2b3`;
   - offline foundation/DTO/validator/health scope accepted;
   - canonical integrated acceptance remains partial.

2. **P2-02 SQLite Store**
   - current accepted upstream used by P2-03: `f70f0237356c4f27afb0e6760b01870228ba3739`;
   - atomic/revisioned SQLite store, PIT/rights/watchlist repository offline scope delivered;
   - provider/integrated acceptance remains partial.

3. **P2-03 DSM**
   - implementation commit: `7478e09bcae1f890058fd134e79fd6f7013103c6`;
   - CHAT evidence-metadata head: `d90987afd861a41aef01059d95ca039509ede09c`;
   - CHAT verdict: `P2_03_OFFLINE_DSM_ACCEPTED`;
   - 98 P2-03 tests PASS; 175 upstream regressions PASS with 2 obsolete stage assertions deselected;
   - provider/API/UI/Production/LIVE remain NOT_RUN.

**Next application base:** `d90987afd861a41aef01059d95ca039509ede09c`.

### Bridge lane

`BRIDGE-DESKTOP-01-02-FIX-01` is accepted.

- result SHA: `ef9f290e73c4f4500900528656212c38acf43a4f`;
- parent/base: `ceeb2bb2db3e09c2c2ad485a82a70c4f446e8e6a`;
- ahead 1 / behind 0;
- only `agent_bridge/**` and `reports/BRIDGE-DESKTOP-01-02/**` changed;
- 134 tests PASS;
- validator PASS;
- post-launch non-zero -> `NEEDS_RECONCILIATION`;
- consumed dispatch replay blocked;
- no automatic Agent substitution.

Pre-publication metadata wording that no longer describes the final remote state is classified as non-material evidence debt. No FIX-02 is created. The systemic artifact-canonicalization fix is already absorbed into Bridge Batch A.

**Next Bridge base:** `ef9f290e73c4f4500900528656212c38acf43a4f`.

## 2. Project assessment

FOX2 is no longer at bootstrap architecture stage. The backend foundation, durable store and offline DSM core exist and have bounded CHAT acceptance. The largest product gap is now **integration into an actually usable localhost application**, not additional foundational decomposition.

The Bridge has enough proven core behavior to move from repeated corrective/hotfix work into consolidated productization. The remaining Bridge work should be completed in two batches, not by reopening Desktop-01/02 or individual telemetry/permission/artifact WPs.

The project therefore has two material critical paths:

```text
LANE A — M1-A APPLICATION
accepted P2-03
 -> APP-BATCH-A: API + WATCHLIST + BACKEND INTEGRATION
 -> APP-BATCH-B: UI + OFFLINE ACCEPTANCE
 -> M1-A RELEASE INTEGRATION
 -> RUNNABLE LOCALHOST FOX2

LANE B — BRIDGE
accepted FIX-01
 -> BRIDGE-DESKTOP-BATCH-A
 -> BRIDGE-DESKTOP-BATCH-B
 -> INTERNAL FOX2 BRIDGE READY
```

These lanes are dependency-safe for parallel execution because their primary code paths are disjoint (`backend/frontend/tests` vs `agent_bridge`) and FOX2 Policy permits up to two independent material writers.

## 3. Immediate execution phase — run two whole batches in parallel

### Lane A — `FOX2-M1-A-APP-BATCH-A` — ACCEPTED

**Result:** accepted at `3db6298e4286022e5820eb7b712c436cbade6a62` with 364 PASS / 3 superseded stage-only deselections. The next application gate is APP-BATCH-B (UI + integrated offline acceptance).

**Base:** accepted P2-03 evidence head `d90987afd861a41aef01059d95ca039509ede09c`.

**Scope:**
- wire accepted P2-01 DTO/validators + P2-02 store + P2-03 DSM;
- approved read-only market API endpoints;
- watchlist preference service/CAS behavior using existing repository ownership;
- loopback Host/Origin/content-type/security guards;
- explicit `UNKNOWN/UNAVAILABLE` behavior when provider data is not available;
- no synthetic investor prices;
- no provider transport/network construction;
- full P2-01/P2-02/P2-03 regression set adjusted only for superseded stage-boundary assertions;
- one final backend integration evidence package.

**Do not split** API routes, watchlist, integration wiring and backend negative tests into separate Owner-facing WPs.

**Candidate routing:** Copilot CLI / `NATIVE_AUTO` / Balance for clear implementation if current capacity is available; otherwise Codex CLI / pinned model / Medium. CHAT selects at dispatch from current usage/capability evidence.

**Exit:** backend M1-A API/watchlist offline integration accepted; API DTOs frozen for frontend.

### Lane B — `BRIDGE-DESKTOP-BATCH-A` — OWNER ACCEPTED WITH VALIDATION WAIVER

**Final code head:** `3013f34d7ad91d1462e44495c873a84c41297b6b`.

**Parent validated result:** `b2de4a10f259c4baf40a83372783e11fc7edd64a` with 243 PASS / 0 fail / 0 skip.

Owner explicitly waived a separate post-patch Windows rerun after CHAT corrected the Dispatch-v3 structural-conformance gap. Therefore Batch A is operationally closed and may feed Batch B, but the waived post-patch tests remain `NOT_RUN` and MUST NOT be rewritten as PASS.

Carry-forward rule into Batch B final certification:

- include current code head `3013f34...`;
- exercise the canonical Dispatch-v3 schema binding/structural-conformance gates as part of the single Batch-B certification cycle;
- do not reopen Batch A as a standalone validation WP;
- if final Batch-B certification exposes a material regression from the CHAT patch, resolve it inside Batch B or the release-readiness decision, not as a historical micro-fix.

`BRIDGE_BATCH_A=OWNER_ACCEPTED_WITH_VALIDATION_WAIVER`  
`POST_PATCH_FULL_WINDOWS_RERUN=WAIVED`  
`TECHNICAL_TEST_PASS_FOR_3013F34=NOT_CLAIMED`

## 4. Second execution phase

### `FOX2-M1-A-APP-BATCH-B` — UI + offline acceptance

**CHAT UI slicing status — 2026-10-14:** Owner authorized CHAT to implement the visual/presentation slice directly inside the existing whole-WP. Current source head on `work/FOX2-M1-A-APP-BATCH-B` is `1b1a7d23c5a0a2c99afd060f5b793f162c8f6ed2`. The slice adds the React/TypeScript/Vite shell, Overview, Watchlist, Stock360, Data Sources, truthful loading/unavailable/stale/gap/provisional presentation, responsive 1440/1024/390 layout, and Owner-requested Dark/White theme selection with presentation-only local persistence under `frontend/**`. No backend/provider/business semantic code was changed. Source review is complete; frontend build/runtime/integrated acceptance remain NOT_RUN. **Owner priority now sets APP-BATCH-B to `PAUSED_AFTER_UI_SLICE` until Bridge reaches `INTERNAL_FOX2_BRIDGE_READY`.**


Start after APP-BATCH-A freezes the accepted API shape.

This one batch absorbs historical P3 + P4:

- React/TypeScript/Vite localhost UI;
- Overview, Watchlist, Stock360 and Data Source Diagnostics;
- browser talks only to FOX2 backend;
- explicit unavailable/unknown/source/freshness/gap display;
- responsive 1440/1024/390;
- no fake trend/zero substitution;
- frontend + backend integrated offline tests;
- localhost startup/restart/navigation/security evidence;
- acceptance-matrix attribution for M1-A only;
- one independent acceptance checkpoint at the end.

This is the first target where FOX2 should be considered **runnable locally as an M1-A product**, even with real provider data still disabled/unavailable.

### `BRIDGE-DESKTOP-BATCH-B` — setup/package/real certification

Start from Owner-accepted Bridge Batch A head `3013f34d7ad91d1462e44495c873a84c41297b6b`.

Batch A's post-patch Windows rerun was explicitly waived by Owner. Batch B therefore carries one bounded certification debt: its final certification must exercise the current Dispatch-v3 schema binding/structural-conformance behavior together with the normal Batch-B installed-runtime/E2E gates. This is not a separate Batch-A rerun.

Scope:
- first-run setup;
- installed per-user runtime;
- installer/update/uninstall;
- sanitized diagnostics/support bundle;
- one real eligible FOX2 WP through the installed Bridge;
- exact selected Agent/model/permission;
- result delivery + CHAT readback;
- usage snapshot available for next routing;
- restart confirms no replay.

Exit: `INTERNAL FOX2 BRIDGE READY`.

Owner priority now serializes these lanes: finish `BRIDGE-DESKTOP-BATCH-B` first, then resume APP-BATCH-B build/test/integration. The frozen website source remains `1b1a7d23c5a0a2c99afd060f5b793f162c8f6ed2` until Bridge is accepted.

## 4A. Bridge closure state — current live evidence 2026-10-15

Owner priority remains **Bridge first**.

Current Bridge Batch B remote head:
`501822a33ef08c7365154913bbc677544856eee5`.

### Dispatch 008 result — consumed; code correction phase complete

Dispatch 008 is CONSUMED exactly once and MUST NOT be replayed.

008 proved the Windows self-uninstall correction and the complete disposable lifecycle:
- 29 focused tests PASS;
- 373 full Bridge tests PASS;
- deterministic package builds PASS;
- certified package SHA-256 `6d6b66b6fa8d1b986835e3bf4368a9f7a8749a37f687c79d2ed4d95d88f3d5a6`;
- contaminated-parent install/setup/update PASS;
- stable external uninstall PASS with versions empty, pointer/launchers removed and durable files preserved;
- reinstall PASS;
- fresh-process 001–008 no-replay PASS;
- disposable Tray/Worker restart + diagnostics PASS.

### Real per-user recovery — materially successful, certification incomplete

Only after disposable lifecycle PASS, 008 inspected and reconciled the real Bridge.

Accepted real recovery facts:
- historical partial versions were ownership-validated before removal;
- durable config/data/logs/reports and ledger values were preserved;
- certified package installed successfully;
- repeated setup PASS and remains PAUSED;
- fresh installed processes reject Dispatches 001–008;
- exact SID-qualified startup task was registered successfully;
- worker final state is STOPPED / PAUSED;
- startup task is owned, Limited, Interactive and IgnoreNew.

008 stopped at `REAL_STARTUP_TASK_OWNERSHIP` because its harness compared the executable string case-sensitively:
`C:\Program Files\PowerShell\7\pwsh.EXE`
versus Task Scheduler:
`C:\Program Files\PowerShell\7\pwsh.exe`.

Read-only diagnosis proves both resolve to the same Windows executable, and every other task ownership field matches. This is a certification-harness comparison error, not evidence of a production Bridge defect.

No further real Tray launch occurred after the stop, so these gates remain incomplete:
- real INSTALLED_TRAY_WORKER;
- real STARTUP_SINGLE_INSTANCE completion;
- final real diagnostics;
- real Tray/Worker RESTART_NO_REPLAY;
- installed-runtime Dictionary / Dispatch-v3 / v2 / v0.6 certification;
- EXACT_AGENT_CONFIGURATION / FULL_ACCESS application evidence;
- REAL_ELIGIBLE_FOX2_DISPATCH;
- RESULT_REMOTE_READBACK;
- USAGE_SNAPSHOT.

### Observer-corrected Controller 011 — ready and unconsumed

CHAT corrected the certification harness without touching production Bridge code.

Pinned process observer:
- commit `928e8279ac6ca45d9421d5fa3773dd44943008ef`;
- path `docs/agent_handoff/RECOVERY/FOX2-BRIDGE-CERT-PROCESS-OBSERVER-011.ps1`;
- blob `000dc032777cec198f59ddb7d6af049a9d23f1fc`;
- raw UTF-8 SHA-256 `75325a05b79cc97e20811d724bde9f0642376b2b359de68d5d6439b5f97d5792`.

Observer semantics:
- targets are supplied via environment, so target literals do not appear in the observer process command line;
- observer PID is excluded explicitly;
- Tray requires exact expected pwsh executable plus exact installed `desktop_tray.ps1`;
- Worker requires exact installed Python plus `-m fox2_agent_bridge worker`;
- observer emits structured JSON and performs no runtime mutation.

Controller 011:
- Dispatch `FOX2-DISPATCH-BRIDGE-DESKTOP-BATCH-B-CODEX-011`;
- Dispatch control commit `4eae4eec694acb70e472e0e14d23861cee9c214c`;
- prompt commit `ebb841afd47a1f41dcb03a4f5c7a114e203cdb1a`;
- prompt blob `e1e892f30ab36c77ff7b9e7305a68d91dbc7b554`;
- prompt SHA-256 `2ad27316f2d049baf4dec12161d186adaef6f428ac02f36dbb6dd6a6f61a197d`;
- source head `92bd9c82385f05893d9379c00f964760e9fe06dc`;
- certified product source remains `501822a33ef08c7365154913bbc677544856eee5`;
- route `CODEX / gpt-6.1-sol / High / FULL_ACCESS`;
- writable repository scope only `reports/BRIDGE-DESKTOP-BATCH-B/evidence/final011/**`;
- no `agent_bridge/**` or product source mutation authorized.

Controller 011 launcher performs a **pre-claim observer smoke test** while Bridge is expected STOPPED / PAUSED. Controller 011 is not consumed unless the pinned observer first proves:
- tray_count=0;
- worker_count=0;
- no self-match.

Existing Worker canary remains unchanged:
`FOX2-BRIDGE-FINAL-CANARY-009-CODEX-001`

Canary branch remains:
`work/FOX2-BRIDGE-FINAL-CANARY-009@501822a33ef08c7365154913bbc677544856eee5`.

Canary remains UNCLAIMED / UNEXECUTED and no canary result exists.

Fail-closed launcher:
`docs/agent_handoff/RECOVERY/RUN_FOX2_BRIDGE_FINAL_CERTIFICATION_011.ps1`

Launcher control head:
`07a9d53c2e94facb680631475581d692b67e70f5`.

### Controller 010 intake — consumed, stopped on certification observer self-match

Controller 010 is CONSUMED and MUST NOT be replayed.

Bridge task remote head after bounded stop evidence:
`92bd9c82385f05893d9379c00f964760e9fe06dc`

010 immutable/controller bindings all PASS:
- Controller 010 prompt raw SHA-256 PASS;
- canary prompt raw SHA-256 PASS;
- Dictionary/Policy/task bindings PASS;
- report-only lineage from certified product source PASS;
- canary branch still exact `501822a...`;
- canary remains UNCLAIMED / UNEXECUTED.

010 stopped in Phase 0 on:
`CERTIFICATION_HARNESS_PROCESS_OBSERVER_SELF_MATCH`.

Read-only diagnosis proves the process observer matched its own PowerShell query process:
- observed executable: `C:\Program Files\PowerShell\7\pwsh.EXE`;
- observer query contains the literal Tray path in its own command line;
- `is_observer_query=true`;
- `real_matches=[]`;
- actual Tray processes observed: 0;
- actual Worker processes observed: 0.

Therefore this is a **certification harness observer defect**, not a Bridge/product/runtime failure.

Safety outcome:
- runtime_mutated=false;
- product_source_mutated=false;
- intake remains PAUSED;
- Worker remains STOPPED;
- canary claimed=false;
- canary executed=false;
- canary branch remains `501822a...`;
- canary result remains absent.

Task-branch delta from `3e8f47a...` to `92bd9c...` contains only `reports/BRIDGE-DESKTOP-BATCH-B/evidence/final010/**`.

Next controller must correct only the certification process-observer implementation outside production source, then continue final certification using the same still-unclaimed Worker canary. No production code correction and no new canary identity are indicated by current evidence.

### Replacement Controller 010 — ready and unconsumed

Controller 010 has been published as the one replacement certification controller after the metadata-only 009 stop.

Dispatch:
`FOX2-DISPATCH-BRIDGE-DESKTOP-BATCH-B-CODEX-010`

Controller source head:
`3e8f47a28bc66a78442059f0b0d1d3ccd4663a06`

Certified product source remains:
`501822a33ef08c7365154913bbc677544856eee5`

The source difference `501822a..3e8f47a` is report-only under `reports/BRIDGE-DESKTOP-BATCH-B/evidence/final009/**`; no production source changed.

Controller prompt:
- commit `d161710832de15e1acd6f75cc99ab15b48885a1d`;
- blob `ced663bbbfb4f2a5e4695747ee8c3de51a9a8b47`;
- raw UTF-8 SHA-256 `c7c44dc400017b057debbfa1c9c74475faa6218405750ee2924b6d0abe35383e`.

Controller route:
`CODEX / gpt-6.1-sol / High / FULL_ACCESS`.

Controller writable repository scope:
`reports/BRIDGE-DESKTOP-BATCH-B/evidence/final010/**`.

No `agent_bridge/**` or product source mutation is authorized.

The existing Worker canary is reused without a new identity:
`FOX2-BRIDGE-FINAL-CANARY-009-CODEX-001`.

Its prompt SHA-256 was independently revalidated:
`dd9f45c5ac5f62bc8c65c53fe629a15d67381fe794e18956347fd1e9999ba3e0`.

Canary branch remains:
`work/FOX2-BRIDGE-FINAL-CANARY-009@501822a33ef08c7365154913bbc677544856eee5`.

Canary remains UNCLAIMED / UNEXECUTED and no canary result exists.

Fail-closed launcher:
`docs/agent_handoff/RECOVERY/RUN_FOX2_BRIDGE_FINAL_CERTIFICATION_010.ps1`

Launcher control head:
`0908e8c73b02099384d633a1dc2a17ca217af221`.

The launcher validates raw Git blob SHA-256 using Python hashlib before creating the Controller-010 claim, preventing recurrence of the Controller-009 metadata error.

### Dispatch 009 intake — consumed, stopped before runtime mutation

Dispatch 009 was claimed once and is CONSUMED. It MUST NOT be replayed.

Remote result head:
`3e8f47a28bc66a78442059f0b0d1d3ccd4663a06`

009 stopped in Phase 0 on:
`CONTROLLER_PROMPT_SHA256_BINDING_MISMATCH`.

Remote evidence proves:
- controller prompt Git blob SHA-1 exactly matches the bound blob: `fb0822e6ab27e9721eaaf6bdcbf3566d1904329b`;
- the pinned commit and current control branch expose the exact same prompt blob;
- independent `git show` / `git cat-file` bytes are identical;
- no CRLF mutation occurred;
- actual prompt SHA-256 observed by the controller is `7e83a5c6ee9440c17d0d50fb729813408f241a2fba7d791bce4140bc4981c000`;
- Dispatch 009 carried incorrect expected SHA-256 `66c8ceee35b657d68bca1a2bdfacaf2f6c1ba9e3556504f62f156663503e2b7c`.

Therefore this is a **CHAT control-artifact metadata generation error**, not Bridge/product drift.

Safety outcome:
- runtime_mutated=false;
- product_source_mutated=false;
- intake remains PAUSED;
- worker remains STOPPED;
- real canary remains UNCLAIMED/UNEXECUTED;
- canary branch remains exactly `501822a33ef08c7365154913bbc677544856eee5`;
- canary result file does not exist;
- 001–008 consumption remains preserved.

The Bridge task branch advanced from `501822a...` to `3e8f47a...` only by new `reports/BRIDGE-DESKTOP-BATCH-B/evidence/final009/**` stop evidence; there is no production source change.

Next controller must be a new single-use certification controller with corrected immutable prompt SHA-256 binding. It may reuse the still-unclaimed immutable Worker canary 009 and its unchanged canary branch/base; no new production code fix or new canary identity is required by current evidence.

### Current phase — FINAL CERTIFICATION ONLY

Final certification artifacts are now bound and published.

Controller:
- Dispatch `FOX2-DISPATCH-BRIDGE-DESKTOP-BATCH-B-CODEX-009`;
- control commit `72290d52585c3c6e09030c1c7a840583e61af637`;
- route `CODEX / gpt-6.1-sol / High / FULL_ACCESS`;
- execution path `MANUAL_LOCAL`;
- writable repository scope only `reports/BRIDGE-DESKTOP-BATCH-B/evidence/final009/**`;
- no `agent_bridge/**` mutation authorized.

Current-schema runtime fixture:
- `docs/agent_handoff/DISPATCH/FOX2-DISPATCH-BRIDGE-FINAL-CERT-V3-009.json`;
- exact bundle commit `cd2a1bd0d2a4e851a79c17f538f70734277d5ad5`;
- schema v3 / execution_path=BRIDGE;
- intentionally non-auto-executable because v3 schema does not permit legacy `runtime_contract.auto_execute`.

Real installed Worker canary:
- `FOX2-BRIDGE-FINAL-CANARY-009-CODEX-001`;
- supported legacy schema v0.6;
- exact bundle commit `cd2a1bd0d2a4e851a79c17f538f70734277d5ad5`;
- `runtime_contract.auto_execute=true`;
- `CODEX / PINNED / gpt-6.1-sol / Medium / FULL_ACCESS`;
- `delivery_owner=BRIDGE`;
- canary branch `work/FOX2-BRIDGE-FINAL-CANARY-009` frozen at `501822a33ef08c7365154913bbc677544856eee5`;
- only `reports/BRIDGE-DESKTOP-BATCH-B/evidence/final009/canary/**` may change.

This separation is deliberate: installed v3 compatibility is proven through schema/normalizer/common validation, while the existing Worker auto-discovery path is certified through its supported legacy auto-execute contract. Do not add non-schema fields to v3 merely to make it resemble legacy Worker discovery.


No additional production code fix is authorized or indicated by current evidence.

Next work must be a single certification-only lane that:
1. validates the existing startup task with Windows path-equivalence semantics, without rewriting production code;
2. starts the real installed Tray/Worker while intake remains PAUSED and proves single-instance/heartbeat/graceful exit/restart/no-replay;
3. exports final sanitized real diagnostics;
4. proves installed-runtime Dictionary/Dispatch-v3/v2/v0.6 compatibility;
5. applies one pre-authorized immutable eligible FOX2 canary through the installed Bridge;
6. proves exact Agent configuration / Full Access application;
7. proves result publication + exact remote readback;
8. records usage snapshot or normative NOT_EXPOSED_WITH_EXECUTION_PROOF;
9. closes every remaining acceptance gate in one final evidence namespace.

Only if every required gate PASSes may CHAT accept:
`INTERNAL_FOX2_BRIDGE_READY`.

Website/APP-BATCH-B remains frozen until that exit.

## 5. Genuine milestone boundary — M1-A release integration

After APP-BATCH-B independent acceptance, create one explicit integration/release decision.

This is a genuine boundary because it may authorize integration/merge into the release/main line. It is not implied by coding acceptance.

Required:
- exact accepted application heads;
- full regression and offline acceptance receipt;
- diff/ancestry review;
- no provider/broker/LIVE rights;
- explicit merge/release authority.

Do not merge partial P2 branches one by one merely to make main appear current.

## 6. M1-B provider integration — one milestone, internal sub-blocks

Only after M1-A runnable-local acceptance and provider rights/network gates are verified.

Treat historical P5/P6/P7 as one Owner-facing milestone:

`FOX2-M1-B-PROVIDER-INTEGRATION`

Internal technical blocks:
1. DNSE REST historical/read capability;
2. market-only WebSocket capability;
3. disconnect/restart/overflow/recovery/PIT/freshness end-to-end certification.

Keep separate capability/rights gates internally because REST and WebSocket entitlements differ, but do not create repeated Owner approvals when the already-bound milestone authority is unchanged.

No account/order/broker-write/LIVE authority is implied.

## 7. Source Freshness / SFR consolidation

Do not run `SFR-010 -> SFR-050` as a third parallel product program.

For current delivery:
- CHAT resolves the Project Dictionary first and binds the newest applicable released Policy/Technical/source at new/re-scoped handoff creation;
- Dispatch Schema v3 binds exact Dictionary/Policy/source/task identities;
- Protocol v12 enforces pre-exec-to-dispatch-to-result lifecycle, alternative-route materiality, source binding and in-flight materiality;
- Bridge uses the Project-Dictionary-generated compatibility binding for task-material runtime/source attestation.

Standalone release-hook/Library-CAS hardening is deferred until it is materially required for automated release publishing. Reopen it as one consolidated hardening milestone only if current CHAT + Git provenance is insufficient.

Issue #11 therefore remains historical/design backlog, not a blocker for M1-A or Bridge Batch A.

## 8. WORK usage

WORK is not a routine checkpoint.

Use WORK only at:
- final M1-A offline acceptance if an independent audit materially improves confidence;
- Bridge Batch A/B release-readiness where concurrency/recovery/security evidence warrants independent review;
- provider-rights / WebSocket / recovery acceptance before M1-B release.

Do not insert WORK between normal implementation sub-blocks.

## 9. Project-wide STOP conditions

STOP only on material conditions:
- source/task/branch mismatch;
- overlapping writer on same writable path;
- unauthorized scope expansion;
- required test failure that affects task correctness;
- secret/private/licensed-data exposure;
- missing required capability;
- permission-profile mismatch;
- actual exhausted quota/capacity that prevents execution;
- provider/broker/LIVE access without explicit authority;
- remote publication/readback failure.

Do not STOP solely for:
- non-material version mismatch;
- missing numeric quota telemetry while Agent can execute;
- staging/index cleanup;
- stale local metadata;
- evidence wording that does not alter correctness and can be handled by the consolidated artifact pipeline.

## 10. Execution ordering summary

```text
NOW — FINALIZE BRIDGE

  COMPLETED
    Dispatch 007
      -> installer environment isolation fixed
      -> 22 focused PASS / 367 full PASS

    Dispatch 008
      -> Windows self-uninstall fixed
      -> 29 focused PASS / 373 full PASS
      -> complete disposable lifecycle PASS
      -> real owned recovery materially complete
      -> certified package installed
      -> setup PAUSED / worker STOPPED
      -> startup task registered/owned

  READY NOW
    Dispatch 009 FINAL CERTIFICATION ONLY
      -> Windows path-equivalent startup ownership
      -> real Tray/Worker + single-instance
      -> graceful exit/restart/no-replay
      -> final diagnostics
      -> installed v3 / v2 / v0.6 compatibility
      -> exactly one real Worker canary
      -> Codex gpt-6.1-sol / Medium / FULL_ACCESS
      -> Bridge-owned result publication
      -> exact remote readback
      -> usage snapshot or NOT_EXPOSED_WITH_EXECUTION_PROOF
      -> CHAT final intake
      -> INTERNAL_FOX2_BRIDGE_READY

THEN — RESUME WEBSITE
    frozen APP-BATCH-B dual-theme source
    1b1a7d23c5a0a2c99afd060f5b793f162c8f6ed2
      ↓
    build/typecheck/API integration/tests/runtime acceptance
      ↓
    runnable localhost M1-A

THEN
  -> M1-A RELEASE INTEGRATION
  -> M1-B PROVIDER INTEGRATION

LATER
  -> M2 / M3 / M4
```

### Project-wide PreExec protocol release / incident disposition — 2026-10-14

The first Batch-B local preflight incident exposed a project-wide evidence gap. It did **not** launch an implementation Agent and consumed no executable Dispatch. The incident-specific fixes are now superseded by the released FOX2-wide PreExec Evidence Protocol v1.1 / Receipt Schema v1 / CHAT Preflight Intake v1.1.

Observed:
- APP preflight: Node/npm/npx absent on the local host;
- APP and Bridge minimal Agent probes returned failure, but the original preflight did not preserve a safe failure classification;
- Bridge retained a staged preflight receipt from the failed attempt;
- the original receipt writer used platform newlines, causing `git diff --check` to flag CRLF as trailing whitespace;
- the original outer runner piped scripts through `pwsh -Command -`, so terminating errors did not reliably terminate the whole streamed session and misleading PUSHED markers could still print.

CHAT corrected the same pre-execution tooling:
- blocked preflights now publish sanitized Git receipts before returning non-zero;
- receipts are canonical UTF-8/LF;
- only stale preflight receipt state may be auto-cleaned; any other WIP remains fail-closed;
- Agent probe receipts record exit code + failure class without raw output/secrets;
- APP has an explicit Node.js LTS bootstrap;
- the recovery runner executes scripts via temporary files with `pwsh -File`, runs both lanes independently, and distinguishes BLOCKED receipt from infrastructure failure.

No product code changed. No executable Dispatch v3 has been published for either Batch-B lane.

Project-wide disposition:
- Policy V1.8.9 makes durable pre-execution evidence mandatory and defines aggregate Agent-route materiality;
- Routing V1.3.0 inserts PreExec evidence before final assignment and compares alternative Agent candidates;
- Protocol v12 separates pre-start BLOCKED/INFRA_FAILED from post-start NEEDS_RECONCILIATION and forbids silent route substitution;
- Bridge Technical v0.7 Candidate REV10 defines shared tooling behavior;
- Project Dictionary v1.2 exposes all current machine pointers and aggregate-route identifiers;
- project-wide rollout is Owner-authorized with bounded CODE_ALLOWED, but final implementation Agent remains gated by current R3/R5 evidence.

### Current pre-execution disposition / Bridge-first gate

- project-wide PreExec implementation is historical enablement, not the current Bridge blocker;
- current Bridge source has already executed Dispatches 001–008 under the current governance line;
- Dispatch 008 remote result head is `501822a33ef08c7365154913bbc677544856eee5`;
- no further production code correction is indicated by current evidence;
- final certification controller 009 and its immutable canary artifacts are published on the control branch;
- Bridge task source is intentionally kept immutable at `501822a...` until 009 completes; do not edit the task header merely to refresh wording and invalidate the certification source binding;
- Website/APP-BATCH-B remains frozen until CHAT accepts `INTERNAL_FOX2_BRIDGE_READY`;
- no main/merge/deploy/provider/broker/LIVE authority is implied.

`MASTER_PLAN_STATUS=ACTIVE / GOVERNANCE=PROJECT_DICTIONARY_V1.2+POLICY_V1.8.9+ROUTING_V1.3.0 / OWNER_PRIORITY=BRIDGE_FIRST / BRIDGE_BATCH_B_HEAD=92bd9c82385f05893d9379c00f964760e9fe06dc / LAST_COMPLETED_DISPATCH=010_CONSUMED_STOPPED_PHASE0 / CONTROLLER_010_ROOT_CAUSE=CERTIFICATION_HARNESS_PROCESS_OBSERVER_SELF_MATCH / RUNTIME_MUTATED_BY_010=NO / PRODUCT_SOURCE_MUTATED_BY_010=NO / CERTIFIED_PRODUCT_SOURCE=501822a33ef08c7365154913bbc677544856eee5 / CURRENT_PHASE=FINAL_CERTIFICATION_011_READY / CONTROLLER_011=READY_UNCONSUMED / CONTROLLER_011_CONTROL_HEAD=07a9d53c2e94facb680631475581d692b67e70f5 / PROCESS_OBSERVER_011=PINNED_SELF_EXCLUDING_PRECLAIM_GATED / REAL_WORKER_CANARY_009=READY_UNCLAIMED / CANARY_BRANCH_HEAD=501822a33ef08c7365154913bbc677544856eee5 / NEXT=RUN_CONTROLLER_011_ONCE_THEN_CHAT_FINAL_INTAKE / BRIDGE_TARGET=INTERNAL_FOX2_BRIDGE_READY / APP_BATCH_B=PAUSED_AFTER_UI_SLICE / APP_FROZEN_HEAD=1b1a7d23c5a0a2c99afd060f5b793f162c8f6ed2 / MERGE=NO / LIVE=NO`
