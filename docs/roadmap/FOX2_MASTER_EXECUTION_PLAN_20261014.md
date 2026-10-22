# FOX2 — MASTER EXECUTION PLAN — 2026-10-14

**Status:** `ACTIVE / OWNER-DIRECTED / CONSOLIDATED EXECUTION PLAN`  
**Project:** `FOX2 ONLY`  
**Governance:** Project Dictionary v1.2 -> FOX2 Policy V1.8.9 + Routing Index V1.3.0  
**Execution contract:** PreExec Evidence Protocol v1.1 + Preflight Receipt Schema v1 + CHAT Preflight Intake v1.1 + Dictionary-resolved Dispatch Schema v3 + Git-first Protocol v12 + Result Contract v2 + CHAT Result Intake v9  
**Planning rule:** maximize delivery progress with whole-WP/batch execution; do not create Owner-facing micro-WPs for operational reconciliation, metadata cleanup, validator reruns or non-material tool/version deviations.

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
- Owner-authorized project-wide implementation mandate: `docs/governance/FOX2_PROJECT_WIDE_PREEXEC_IMPLEMENTATION_MANDATE_v1.md`; rollout is one systemic infrastructure change, not task-local micro-fixes.

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

APP-BATCH-B and BRIDGE-BATCH-B may run in parallel if writer/path checks remain disjoint.

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
NOW — SECOND EXECUTION PHASE
  ├─ APP-BATCH-B
  │    P3 + P4 -> runnable localhost M1-A
  │
  └─ BRIDGE-BATCH-B
       setup/package/installed-runtime certification
       + carry-forward current-schema certification debt
       -> INTERNAL FOX2 BRIDGE READY

THEN
  -> M1-A RELEASE INTEGRATION

THEN
  -> M1-B PROVIDER INTEGRATION (P5+P6+P7 as one milestone)

LATER
  -> M2 coverage/PIT/corporate-actions/soak
  -> M3/M4 analytics/risk/capital/exit/shadow under their own BRDs
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

### Current pre-execution facts for the two next batches

- project-wide rollout branch `work/FOX2-PREEXEC-ROLLOUT-V1` has a live PASS receipt proving Codex current execution readiness and clean dedicated worktree;
- Copilot remains `AUTH_REQUIRED`; under the project-wide alternative-route rule this is routing evidence, not a blocker when Codex is an allowed route and passes;
- the previous receipt is historical because it predates the aggregate-route semantic release; a fresh v1 receipt must be regenerated from the re-bound source before final assignment;
- APP-BATCH-B and BRIDGE-BATCH-B remain PREEXEC_HOLD and will consume the shared engine after rollout acceptance instead of keeping independent lifecycle semantics;
- no executable Dispatch for the rollout, APP-BATCH-B or BRIDGE-BATCH-B is valid until CHAT reads the fresh re-bound receipt.

`MASTER_PLAN_STATUS=ACTIVE / GOVERNANCE=PROJECT_DICTIONARY_V1.2+POLICY_V1.8.9+ROUTING_V1.3.0 / PREEXEC=V1.1 / PREFLIGHT_RECEIPT=V1 / AGENT_ROUTE_MATERIALITY=AGGREGATE / DISPATCH=V3 / PROTOCOL=V12 / APP_BATCH_A=ACCEPTED / BRIDGE_BATCH_A=OWNER_ACCEPTED_WITH_VALIDATION_WAIVER / CURRENT_PHASE=PROJECT_WIDE_PREEXEC_ROLLOUT_THEN_APP_B+BRIDGE_B / PROJECT_WIDE_PREEXEC_ROLLOUT=OWNER_AUTHORIZED / MICRO_WP_DEFAULT=NO`

## Current consolidated execution directive — 2026-10-17

This section is the current Owner-directed execution ordering and supersedes earlier scheduling text that permitted APP-BATCH-B and BRIDGE-BATCH-B to run in parallel. Historical sections remain evidence and are not deleted.

Owner-facing work is consolidated into three Whole-WPs:

```text
WP1 — FOX2-BRIDGE-RC1-TO-INTERNAL-READY
  source/trust-root freeze
  -> fresh PreExec
  -> final Agent selection
  -> RC1 implementation
  -> build/package/installed lifecycle certification
  -> independent pre-Canary audit
  -> Canary 009 exactly once
  -> restart/no-replay
  -> CHAT final intake
  -> INTERNAL_FOX2_BRIDGE_READY

WP2 — FOX2-M1-A-TO-INTERNAL-GOLIVE
  resume APP-BATCH-B only after WP1
  -> complete UI/integration/offline acceptance
  -> M1-A release integration
  -> FOX2_INTERNAL_GO_LIVE_READY

WP3 — FOX2-M1-B-MARKET-DATA-GOLIVE
  provider REST read-only
  -> market WebSocket
  -> recovery/PIT/freshness/soak
  -> FOX2_MARKET_DATA_GO_LIVE_READY
```

Anti-fragmentation rule: PreExec, implementation, reconciliation, build/test, independent audit, Canary and final intake are internal stages of their Whole-WP, not new Owner-facing micro-WPs unless a material scope or authority boundary changes.

Current scheduling:
- WP1 = ACTIVE.
- APP-BATCH-B = PAUSED / WAIT_BRIDGE_READY.
- Canary 009 = PRESERVE / UNCONSUMED until WP1 pre-Canary readiness.
- main/merge/deploy/provider/broker/LIVE authority = NO.
- historical Controller 009–013 and historical final closure are not replayable execution authority for RC1.
- fresh RC1 PreExec must bind the exact publication head containing the current RC1 task + current source-set manifest + this directive.

`CURRENT_OWNER_PRIORITY=BRIDGE_FIRST / CURRENT_WHOLE_WP=FOX2-BRIDGE-RC1-TO-INTERNAL-READY / APP_BATCH_B=PAUSED / CANARY_009=PRESERVE_UNCONSUMED / MICRO_WP_DEFAULT=NO / NEXT=FRESH_PREEXEC_ON_EXACT_SOURCE_FREEZE_HEAD / MERGE=NO / LIVE=NO`

## Bridge Host Lifecycle reuse-first directive — 2026-10-22

This section is the current Owner-directed execution rule for the Host Lifecycle portion of WP1 and supersedes any earlier Host Lifecycle wording that would repeat already accepted A04 prerequisites. Historical A01–A04 attempts remain immutable evidence and are not rewritten.

### Controlling principles

- Whole-WP remains `FOX2-BRIDGE-RC1-TO-INTERNAL-READY`; this directive does not create a new Owner-facing micro-WP.
- A04 is CLOSED as `CHAT_REWORK / FAIL`, consumed and no-replay.
- Host Lifecycle acceptance may be composite when all evidence refers to the same runtime subject and each required gate row is independently covered.
- Historical PASS may be reused only when the underlying runtime subject and relevant implementation bytes remain unchanged.
- Historical FAIL / NOT_RUN remain FAIL / NOT_RUN until a later fresh attempt covers those exact missing rows.
- Fresh execution must never rerun passed mutation solely to reproduce evidence.
- G3/G4/Canary remain locked until composite Host Lifecycle acceptance.

### Fixed A04 runtime subject

The runtime subject preserved from A04 is:

- package SHA-256: `f99c7add1b99bad938d977f634fd8a88e20763f5e35aaadf5cfe3072a1a327ee`;
- package source commit: `085cc8302e824dbccf9cbef80422ed48894b9cb4`;
- source inventory SHA-256: `6d76f99ce9fcc62bbcf9f2450a45bc920c28b2fd70828353c0a8fea096c5de73`;
- A04 package archive: `C:\Projects\FOX2-artifacts\host_lifecycle_cert_a04\FOX2-Bridge-085cc830-A04.zip`.

The A04 CHAT result review is:
`a3e49a62dbd340eacd8dc8369aa303ed0e93b6f3`.

The detailed reuse decision is:
`reports/FOX2-BRIDGE-RC1-TO-INTERNAL-READY/chat_reviews/HOST_LIFECYCLE_A04_A05_REUSE_PLAN_20261022.md`
published at commit
`da6fd27d78380db42fce155d634044c94a661229`.

### A04 accepted prerequisites — REUSE, do not rerun

A04 materially established and CHAT accepted as truthful prerequisite evidence:

1. runtime authorization/source/task/Dispatch integrity;
2. split orchestration/package-source worktree provenance;
3. accepted builder provenance probe;
4. exact package build once;
5. exact package SHA/source/source-inventory identity;
6. 59 source-file, 40 wheel-module and 255 payload hash checks;
7. stale exact-current WPF bounded cleanup;
8. per-user install/update exact package;
9. exact installed pointer and receipt;
10. STOPPED / paused / setup_complete / current_dispatch=null;
11. Worker/legacy absent;
12. launch-twice reached one exact-current WPF singleton;
13. package/current/source identity preserved after first failure;
14. SQLite quick_check and logical durable-state preservation at A04 failure checkpoint.

These rows remain accepted prerequisites while the fixed A04 runtime subject above remains unchanged.

### A04 uncovered rows — must be completed, not inferred

A04 first failed at presentation-lock certification with
`PermissionError(errno=13)`.

The following remain FAIL/NOT_RUN and must be covered by continuation evidence:

- live presentation-lock classification;
- UI inspect/check after lock proof;
- graceful exit;
- zero WPF + lock release;
- post-exit safe state;
- stable external uninstall exactly once;
- uninstall postconditions;
- durable preservation across uninstall;
- same exact A04 package reinstall;
- final installed safe state.

### External certifier correction — R2

`agent_bridge/scripts/certify_user_lifecycle.py` is an external certification harness and is not part of the installed runtime package payload. A correction limited to this harness and its focused regression test does not itself create a new runtime package subject.

R2 correction scope is exactly:

- `agent_bridge/scripts/certify_user_lifecycle.py`;
- `agent_bridge/tests/test_lifecycle_wpf_contract.py`.

Required semantics:

- explicit `winerror=32` sharing violation remains accepted;
- actual Windows/Python `PermissionError(errno=EACCES/13, winerror absent/None)` may be accepted only under differential proof;
- persistent ACL/access denial remains fail-closed;
- lock missing while live, lock unexpectedly openable while live, and lock inaccessible after exit remain FAIL;
- lock bytes are never modified by the proof;
- negative singleton/UI/safe-state cases remain preserved;
- no WPF C# product change unless a separate material scope change is authorized.

The previously published unrun R1 PreExec
`4d0ae5636ac91969c2a15416f8f0bd50d581d180`
is `SUPERSEDED_BEFORE_RUN`; receipt absent, coding Dispatch absent, Agent not started. It MUST NOT be run.

### A05 continuation-only rule

After CHAT accepts R2 certifier correction, A05 is a fresh attempt identity because A04 Dispatch is consumed, but it is not a full lifecycle rerun.

A05 PreExec performs only read-only validity checks:

- installed package remains `f99c7add…`;
- installed receipt source remains `085cc830…`;
- A04 archive exists and hashes to `f99c7add…`;
- safe control remains STOPPED/paused/setup_complete/current_dispatch=null;
- Worker/legacy remain absent;
- any live WPF is exact-current and count is 0 or 1;
- corrected certifier source/tests have CHAT acceptance;
- A04 consumed/no-replay identity remains preserved.

If the A04 archive is present and hash-valid:
- package rebuild is forbidden as unnecessary repetition;
- pre-lifecycle install/update is forbidden as unnecessary repetition.

If one exact-current WPF remains live from A04:
- reuse it;
- do not relaunch merely to repeat singleton evidence;
- corrected proof is `live exact WPF -> live lock denied -> UI check -> graceful exit -> WPF=0 -> same lock openable`.

If zero WPF exists:
- one launch of the already-installed exact package is allowed only to re-establish the missing live state;
- historical A04 launch-twice singleton evidence remains accepted.

After corrected presentation proof, A05 must execute only the previously unrun lifecycle tail:

`fresh durable baseline -> stable uninstall exactly once -> uninstall postconditions -> preservation compare -> reinstall SAME exact A04 package -> final safe-state verification`.

### Composite Host Lifecycle exit gate

Host Lifecycle is ACCEPTED only when the union of:

`A04 accepted prerequisite evidence + CHAT-accepted R2 certifier evidence + A05 continuation evidence`

contains no required FAIL/NOT_RUN rows.

A04 remains historical `CLOSED_REWORK / FAIL`; A05 does not rewrite it.

After composite Host Lifecycle ACCEPTED:

`G3 physical gate -> G4 installed adoption -> fresh independent current-source pre-Canary audit -> Canary 009 exactly once -> restart/no-replay -> CHAT final intake -> INTERNAL_FOX2_BRIDGE_READY`.

### Current WP1 execution order

```text
WP1 ACTIVE
  A04 CLOSED_REWORK / no replay
  -> R2 external-certifier correction (2 files only)
  -> CHAT_ACCEPT corrected certifier
  -> A05 continuation-only on SAME A04 package
  -> CHAT composite Host Lifecycle acceptance
  -> G3/G4
  -> independent pre-Canary audit
  -> Canary 009 exactly once
  -> restart/no-replay
  -> CHAT final intake
  -> INTERNAL_FOX2_BRIDGE_READY
```

`BRIDGE_HOST_LIFECYCLE_STRATEGY=REUSE_FIRST / A04=CLOSED_REWORK_NO_REPLAY / R1_PREEXEC_4D0AE563=SUPERSEDED_UNRUN / R2=CERTIFIER_ONLY / A05=CONTINUATION_ONLY / A05_REBUILD=NO_IF_ARCHIVE_VALID / A05_PREINSTALL=NO / G3=LOCKED_UNTIL_COMPOSITE_ACCEPT`

