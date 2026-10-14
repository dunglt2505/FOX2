# FOX2 — MASTER EXECUTION PLAN — 2026-10-14

**Status:** `ACTIVE / OWNER-DIRECTED / CONSOLIDATED EXECUTION PLAN`  
**Project:** `FOX2 ONLY`  
**Governance:** Project Dictionary v1 -> FOX2 Policy V1.8.7 + Routing Index V1.2.8  
**Execution contract:** Dictionary-resolved Dispatch Schema v3 + Git-first Protocol v10 + Result Contract v2 + CHAT Intake v9  
**Planning rule:** maximize delivery progress with whole-WP/batch execution; do not create Owner-facing micro-WPs for operational reconciliation, metadata cleanup, validator reruns or non-material tool/version deviations.

## 1. Current immutable status

### Governance / orchestration

- `FOX2_PROJECT_DICTIONARY_v1.json` is the single machine-readable identity/compatibility registry for all new/re-scoped FOX2 WPs.
- The Dictionary currently resolves Policy V1.8.7 and Routing Index V1.2.8.
- New/re-scoped execution uses Dictionary-resolved Dispatch Schema v3 and stable version-neutral dispatch paths.
- New/re-scoped task/result flow uses Git-first Protocol v10.
- Codex CLI and Copilot CLI are the primary implementation engines.
- Normal coding permission baseline is `FULL_ACCESS`.
- Git publication ownership is dispatch-owned: `delivery_owner=AGENT|BRIDGE`.
- CHAT owns source binding, routing and independent result acceptance.
- Bridge is transport/supervision and only publishes when explicitly assigned as delivery owner.
- Readiness is capability-based; exact version equality is not a hard gate by itself.

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
- Protocol v10 enforces source binding and in-flight materiality;
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

### Current pre-execution facts for the two next batches

- dedicated Batch-B task branches did not exist before this transition and must be created from the exact accepted/Owner-accepted heads;
- APP-BATCH-B requires Node/npm/Vite-capable local toolchain: current local material capability is `UNKNOWN` until direct preflight;
- latest Bridge evidence proves both Codex CLI and Copilot CLI binaries + Full Access argument compatibility, but current quota/capacity is `UNKNOWN` because observed quota is not exposed and paid execution was not run in that evidence cycle;
- no final Agent assignment or executable Dispatch v3 is valid until CHAT completes R3/R5 with current local preflight evidence.

`MASTER_PLAN_STATUS=ACTIVE / GOVERNANCE=PROJECT_DICTIONARY_V1+POLICY_V1.8.7+ROUTING_V1.2.8 / DISPATCH=V3 / PROTOCOL=V10 / APP_BATCH_A=ACCEPTED / BRIDGE_BATCH_A=OWNER_ACCEPTED_WITH_VALIDATION_WAIVER / CURRENT_PHASE=APP_BATCH_B+BRIDGE_BATCH_B_PREEXEC / MICRO_WP_DEFAULT=NO`
