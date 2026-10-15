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

Owner priority remains **Bridge first**. The project-wide PreExec implementation is no longer the critical path: its implementation evidence reports 340 Bridge tests PASS, 60 shared-PreExec cases in the final suite and all mapped rollout acceptance items PASS. Bridge Batch B has subsequently produced a current Schema-v1 PASS receipt and executed Dispatches 001–006.

Current Bridge Batch B remote head:
`ce7a8253926b7489c79311e26d7dc75ba8c81fc6`.

Current control branch head:
`2441d1b66c64acf655ed1cfe39fea69344df042e`.

### Completed/proven inside Batch B

- current Dictionary v1.2 / Policy V1.8.9 / Routing V1.3.0 / Dispatch-v3 bindings reached executable Dispatch;
- Bridge preflight PASS with Codex `gpt-6.1-sol` / Medium / FULL_ACCESS and clean worktree/no competing writer;
- package construction is deterministic: two Core006 package builds produced identical SHA-256 `6e96ee19ea103e7bd606a63abf071d00de6fa3c6cd1663b8d9d921b01d70b3a9`;
- earlier installed lifecycle evidence proved first-run setup, per-user install, update, startup/single-instance, Tray/Worker and sanitized diagnostics before the uninstall stop;
- Dispatch 004 corrected and focused-tested the Tray heartbeat/shutdown defect;
- Dispatch 005 safely reconciled the damaged installed runtime without replay or further mutation;
- Dispatch 006 proved launch/source/worktree/Agent/package readiness in a disposable profile and did not touch the damaged real user runtime;
- Dispatches 001–006 are CONSUMED and MUST NOT be replayed.

### Current material blocker

Dispatch 006 stopped at `PER_USER_INSTALL` in a completely disposable user profile. Follow-up one-shot diagnostics localized the failure to `INSTALLED_MODULE_PROOF`, and Owner's non-dispatch A/B proof on the exact Core006 package CONFIRMED inherited Python-environment contamination: with inherited `PYTHONPATH=<Bridge source>`, pip exits 0 but the installed `python -I` cannot import `fox2_agent_bridge`; with `PYTHONPATH` removed, the same exact wheel installs/imports successfully. The wheel contains the Bridge package and the package SHA matches. Root cause is therefore `INSTALL_SUBPROCESS_ENVIRONMENT_CONTAMINATION`, not malformed wheel/package format.

A non-dispatch, one-shot isolated diagnostic already exists on the control branch:

`docs/agent_handoff/RECOVERY/FOX2-BRIDGE-CORE-INSTALL-ONE-SHOT-DIAG-20261015.py`.

It:
- reuses the exact Core006 package hash;
- creates a new disposable profile;
- never reads/writes the damaged real Bridge root;
- does not execute/replay any Dispatch;
- does not invoke uninstall;
- reports the failing stage plus sanitized error classification.

### Bridge closure plan — no micro-WP loop

```text
A. ROOT CAUSE CONFIRMED
   -> exact package/wheel good
   -> inherited PYTHONPATH contamination reproduces failure
   -> clean environment passes
   -> no Dispatch consumed by A/B proof

B. ONE ROOT-CAUSE CORRECTION — DISPATCH 007
   -> sanitize installer subprocess environment centrally
   -> strip PYTHONPATH/PYTHONHOME while preserving required ordinary env
   -> same Bridge Batch B
   -> agent_bridge/** + Batch-B reports only
   -> CODEX gpt-6.1-sol / High / FULL_ACCESS
   -> single-use, retry lineage from consumed 006

C. ISOLATED CORE LIFECYCLE PASS
   package -> install -> setup -> update
   -> uninstall -> reinstall
   -> startup/single-instance -> diagnostics
   -> durable data/consumption preserved

D. REAL PER-USER RUNTIME RECOVERY
   only after isolated lifecycle PASS
   -> reconcile owned damaged runtime safely
   -> install exact certified package
   -> no blind delete/replay

E. FINAL BRIDGE CERTIFICATION — ONE CYCLE
   -> all 24 Batch-B gates
   -> Dictionary / Dispatch-v3 structural + runtime
   -> v2 / v0.6 compatibility
   -> real eligible FOX2 dispatch/result
   -> exact Agent configuration
   -> result remote readback
   -> usage snapshot
   -> restart/no-replay
   -> full Bridge suite
   -> allowlist / secret scan / git diff
   -> INTERNAL_FOX2_BRIDGE_READY
```

The prior `UNINSTALL_PATH=DEFERRED_OWNER_PRIORITY` condition cannot remain deferred at final Bridge exit: `UNINSTALL_PATH=PASS` is a required Batch-B acceptance gate for `INTERNAL_FOX2_BRIDGE_READY`. The current Owner direction to finish Bridge therefore makes uninstall part of the closure certification, but only after isolated install/root-cause safety is established.

Website/APP-BATCH-B remains frozen until this exit is achieved.

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
NOW — FINISH BRIDGE

  CURRENT:
    Bridge Batch B Dispatch 006 = CONSUMED / STOPPED_NEEDS_RECONCILIATION
    blocker = isolated PER_USER_INSTALL exit 1
    exact inner cause = UNKNOWN
    real damaged runtime = quarantined from new attempts

  NEXT:
    one-shot non-dispatch isolated installer diagnostic
      ↓
    root cause classified
      ↓
    [if code defect] one bounded same-Batch-B correction Dispatch
    [if environment/harness] correct without product redesign
      ↓
    isolated full Core lifecycle PASS
      ↓
    safe real per-user runtime recovery
      ↓
    one final full Bridge certification cycle
      ↓
    INTERNAL_FOX2_BRIDGE_READY

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

### Current pre-execution facts / Bridge-first gate

- project-wide rollout branch `work/FOX2-PREEXEC-ROLLOUT-V1` currently heads at `ad58506d7e94304c0929fc9b5a6281111be7532b`;
- its latest durable receipt is logically PASS and proves Codex current execution readiness plus a clean dedicated worktree, but the receipt is bound to older source head `4bb30b3ff753368a126fa381192d9400f7682c05`; therefore it is STALE for final assignment after later source-sync commits;
- immediate next action is a fresh project-wide PreExec receipt + CHAT Intake solely to unblock Bridge;
- `BRIDGE-DESKTOP-BATCH-B` still carries stale governance references (Dictionary v1 / Policy V1.8.7 / Routing V1.2.8 / Protocol v10) and its 2026-10-14 receipt predates the current aggregate-route baseline; both task source and receipt must be rebound before executable Dispatch;
- once fresh Bridge evidence PASSes, the whole Bridge Batch B is the single active implementation lane until `INTERNAL_FOX2_BRIDGE_READY`;
- Website/APP-BATCH-B is frozen at dual-theme source head `1b1a7d23c5a0a2c99afd060f5b793f162c8f6ed2` with build/runtime/integrated acceptance NOT_RUN;
- after Bridge acceptance, resume APP-BATCH-B without redesigning the CHAT-approved Dark/White UI;
- no executable Dispatch may be issued from stale evidence, and no main/merge/deploy/provider/broker/LIVE authority is implied.

`MASTER_PLAN_STATUS=ACTIVE / GOVERNANCE=PROJECT_DICTIONARY_V1.2+POLICY_V1.8.9+ROUTING_V1.3.0 / OWNER_PRIORITY=BRIDGE_FIRST / BRIDGE_BATCH_B_HEAD=ce7a8253926b7489c79311e26d7dc75ba8c81fc6 / LAST_COMPLETED_DISPATCH=006_CONSUMED_STOPPED_NEEDS_RECONCILIATION / ROOT_CAUSE=INSTALL_SUBPROCESS_ENVIRONMENT_CONTAMINATION_CONFIRMED / NEXT_DISPATCH=007_READY / ROUTE=CODEX_GPT-6.1-SOL_HIGH_FULL_ACCESS / NEXT=ROOT_FIX_THEN_ISOLATED_FULL_LIFECYCLE_THEN_CONDITIONAL_REAL_RUNTIME_RECOVERY_THEN_FINAL_CERT / BRIDGE_TARGET=INTERNAL_FOX2_BRIDGE_READY / APP_BATCH_B=PAUSED_AFTER_UI_SLICE / APP_FROZEN_HEAD=1b1a7d23c5a0a2c99afd060f5b793f162c8f6ed2 / MERGE=NO / LIVE=NO`
