# FOX2-BRIDGE-DESKTOP-BATCH-B — Whole-WP Task / RC1 Rebind

**Status:** SOURCE_READY_RC1_REBIND / PREEXEC_HOLD  
**Project phase:** Bridge final productization before INTERNAL_FOX2_BRIDGE_READY  
**Governance:** Project Dictionary v1.2 -> Policy V1.8.9 -> Routing Index V1.3.0  
**Protocol:** PreExec Evidence v1.1 + Receipt Schema v1 + CHAT Preflight Intake v1.1 + Dispatch Schema v3 + Git-first Protocol v12  
**Final implementation Agent assignment:** PENDING fresh current-source R3/R5 receipt + CHAT Intake  
**Execution path:** MANUAL_LOCAL candidate for RC1 implementation; installed Bridge is the certification target  
**Delivery owner:** AGENT candidate  
**CODE_ALLOWED_FOR_EXECUTION:** HOLD until fresh PreExec PASS + CHAT PASS_TO_ASSIGN

## 1. Source binding

Historical accepted/corrected Bridge facts:

- Owner-accepted Batch-A code head: `3013f34d7ad91d1462e44495c873a84c41297b6b`.
- Parent validated Batch-A result: `b2de4a10f259c4baf40a83372783e11fc7edd64a` with 243 PASS / 0 fail / 0 skip.
- Control-store product correction implementation: `0be8a52b9622bf70dcb21fd2d35ddf913b17a635`.
- Accepted correction evidence/task head before RC1 planning: `d129f9195adab04f158942f5a8638c63d0f3d0e6`.
- Focused correction tests: 40 PASS.
- Full Bridge correction regression: 380 PASS.
- Installed-runtime certification after that correction: NOT_RUN.
- Canary 009 after that correction: NOT_RUN.
- Historical `final_closure/final_certification.json`: INVALID / SUPERSEDED; never use it to grant readiness.

RC1 planning baseline is Git-readable under:

`reports/BRIDGE-DESKTOP-BATCH-B/evidence/rc1_plan/**`

Current RC1 planning manifest before this task rebind:

`4b48116583e3488bf0b81215fa94a84c8cb9f9c7:reports/BRIDGE-DESKTOP-BATCH-B/evidence/rc1_plan/BRIDGE_RC1_GIT_MANIFEST.json`

Normative RC1 planning artifacts:

- `BRIDGE_RC1_RELEASE_PLAN.md`
- `BRIDGE_RC1_ACCEPTANCE.json`
- `BRIDGE_RC1_ROUTING_INTAKE.md`
- `BRIDGE_RC1_DESKTOP_IMPLEMENTATION_SPEC.md`
- `BRIDGE_RC1_GIT_MANIFEST.json`

Current Project Dictionary: v1.2 / `docs/governance/FOX2_PROJECT_DICTIONARY_v1.json`.

The previous PreExec receipt under:

`reports/BRIDGE-DESKTOP-BATCH-B/preexec/local_preflight.json`

binds source `ac41a7e0b543e79e470bed46b1aeb0101ba77405` and is HISTORICAL/STALE for RC1. It MUST NOT authorize RC1 implementation.

## 2. Owner priority and project ordering

Owner priority is now serial:

```text
BRIDGE RC1 source-ready
 -> fresh PreExec
 -> RC1 implementation
 -> installed certification
 -> independent pre-Canary audit
 -> Canary 009 exactly once
 -> restart/no-replay
 -> CHAT final intake
 -> INTERNAL_FOX2_BRIDGE_READY
 -> resume FOX2-M1-A-APP-BATCH-B
```

APP-BATCH-B remains paused. Do not create a competing frontend/product writer while Bridge RC1 is active.

## 3. Whole-WP RC1 objective

Produce the final internally usable installed per-user FOX2 Bridge RC1 and certify the exact product shape that will be used after acceptance.

RC1 product shape:

```text
corrected Python Bridge core
+ native .NET 8 WPF Desktop App
+ local Artifact Vault
+ stable launcher/startup integration
+ installed package/update/uninstall lifecycle
```

Implement/test together, without fragmenting into Owner-facing micro-WPs:

1. preserve corrected Bridge transport/control-store/replay semantics;
2. implement WPF Desktop App under `agent_bridge/desktop_app/**`;
3. enforce Worker/UI two-process separation;
4. enforce Desktop App single-instance per interactive user;
5. preserve Worker single-instance per Bridge profile;
6. implement fixed Desktop control/status client only;
7. integrate Dashboard, Activity, Agents, Diagnostics, Artifacts, Settings;
8. integrate Tray as secondary UI surface;
9. implement local Artifact Vault v1 with `LOCAL_SAVED` only;
10. integrate Desktop App into deterministic package/install/update/uninstall;
11. use one stable launcher to start Worker and Desktop App independently;
12. preserve Start-with-Windows current-user/limited/interactive behavior;
13. preserve CLI controls/diagnostics when Desktop App is unavailable;
14. run current Dispatch-v3 + legacy compatibility certification debt;
15. prove one real installed safe poll against the corrected control-store path;
16. complete pre-Canary independent audit;
17. execute immutable Canary 009 exactly once only after pre-Canary readiness;
18. prove restart/no replay;
19. publish exact bounded evidence and result for CHAT final intake.

## 4. Mandatory architecture boundary

Final topology:

```text
stable launcher
  +--> Python Bridge Worker
  +--> FOX2 Bridge Desktop App (.NET 8 / WPF / MVVM)
```

Mandatory invariants:

- Desktop App crash/close MUST NOT terminate the Worker.
- Desktop App MUST NOT own Git polling.
- Desktop App MUST NOT claim dispatches.
- Desktop App MUST NOT invoke Codex/Copilot directly.
- Desktop App MUST NOT read/write Bridge SQLite directly.
- Desktop App MUST NOT select routing/model/reasoning/permission.
- Desktop App MUST NOT grant merge/deploy/provider/broker/LIVE authority.
- Desktop App may use only fixed Bridge control/status/diagnostics commands defined in RC1 spec.
- No visible PowerShell console is required for normal use.
- CLI diagnostics/control remain available when GUI is unavailable.

## 5. Artifact Vault boundary

Local root:

`%LOCALAPPDATA%\FOX2\BridgeDesktop\Artifacts`

RC1 Artifact Vault must:

- accept explicit local file selection only;
- compute SHA-256 before copy;
- use content-addressed local storage;
- verify SHA-256 after copy;
- atomically update its local index;
- sanitize file names;
- enforce a bounded file size;
- expose only `LOCAL_SAVED` as implemented state.

Canonical semantics:

```text
LOCAL_SAVED != GIT_SYNCED != RELEASED
```

RC1 MUST NOT auto-run Git for artifacts, mark artifacts RELEASED, mutate Bridge ledger, or grant execution/release authority.

## 6. Writable scope

Allowed code:

- `agent_bridge/**`

Allowed reports:

- `reports/BRIDGE-DESKTOP-BATCH-B/**`

Everything else READ-ONLY for implementation Agent.

No application/backend/frontend/provider/broker code may be changed.

## 7. Required acceptance — pre-Canary

All of the following must be PASS before Canary 009 may be claimed:

- `SOURCE_FREEZE=PASS`
- `FRESH_PREEXEC=PASS`
- `DESKTOP_APP_BUILD=PASS`
- `DESKTOP_APP_CONTRACT_TESTS=PASS`
- `DESKTOP_APP_SINGLE_INSTANCE=PASS`
- `WORKER_UI_PROCESS_SEPARATION=PASS`
- `FIRST_RUN_SETUP=PASS`
- `PER_USER_INSTALL=PASS`
- `INSTALLER_PACKAGE=PASS`
- `UPDATE_PATH=PASS`
- `UNINSTALL_PATH=PASS`
- `START_WITH_WINDOWS=PASS`
- `STARTUP_SINGLE_INSTANCE=PASS`
- `PAUSE_RESUME=PASS`
- `CHECK_NOW=PASS`
- `OPEN_LOGS=PASS`
- `SUPPORT_BUNDLE=PASS`
- `ARTIFACT_LOCAL_SAVE=PASS`
- `ARTIFACT_SHA256_VERIFY=PASS`
- `ARTIFACT_ATOMIC_INDEX=PASS`
- `LOCAL_SAVED_NOT_GIT_SYNCED=PASS`
- `PROJECT_DICTIONARY_BINDING=PASS`
- `DISPATCH_V3_SCHEMA_BINDING=PASS`
- `DISPATCH_V3_STRUCTURAL_CONFORMANCE=PASS`
- `DISPATCH_V3_RUNTIME_COMPATIBILITY=PASS`
- `V2_COMPATIBILITY=PASS`
- `V06_COMPATIBILITY=PASS`
- `REAL_INSTALLED_POLL=PASS`
- `CONTROL_STORE_PATH=PASS`
- `FULL_BRIDGE_TESTS=PASS`
- `CHANGED_PATH_ALLOWLIST=PASS`
- `SECRET_SCAN=PASS`
- `GIT_DIFF_CHECK=PASS`
- `PRECANARY_INDEPENDENT_AUDIT=PASS`

Pre-Canary marker:

`FOX2_BRIDGE_RC1_PRECANARY_READY`

## 8. Canary 009 — immutable certification identity

Do not create a replacement Canary.

Immutable identity:

- dispatch id: `FOX2-BRIDGE-FINAL-CANARY-009-CODEX-001`
- branch: `work/FOX2-BRIDGE-FINAL-CANARY-009`
- current preserved head: `501822a33ef08c7365154913bbc677544856eee5`
- execution path: BRIDGE_DIRECT_CODEX_CLI
- max runs: 1
- production code write scope: none
- exact prompt/Agent/permission tuple remains immutable.

Canary may run only after all pre-Canary gates PASS and CHAT confirms the pre-Canary marker.

Post-start uncertainty is `NEEDS_RECONCILIATION`. Never blind replay.

## 9. Final acceptance after Canary

Required final gates:

- `CANARY_009_EXACTLY_ONCE=PASS`
- `EXACT_AGENT_CONFIGURATION=PASS`
- `FULL_ACCESS_PERMISSION=PASS`
- `RESULT_REMOTE_READBACK=PASS`
- `USAGE_SNAPSHOT=PASS_OR_NOT_EXPOSED_WITH_EXECUTION_PROOF`
- `RESTART_NO_REPLAY=PASS`
- `CHAT_FINAL_REMOTE_INTAKE=PASS`

Exit target:

`INTERNAL_FOX2_BRIDGE_READY`

This exit grants no PR/main/merge/deploy/provider/broker/LIVE authority.

## 10. Material PreExec gates

Before final implementation Agent assignment:

1. exact current branch/source head = PASS;
2. exact worktree ownership = PASS;
3. no competing `agent_bridge/**` writer = PASS;
4. .NET 8 / Windows WPF build capability = PASS;
5. Python/PowerShell/Git/install prerequisites = PASS;
6. at least one CHAT-allowed Agent route demonstrates current execution readiness with required permission profile;
7. receipt is durable/pushed/read back under project-wide PreExec v1.1;
8. implementation Agent has not started and executable Dispatch is not already consumed.

Until then:

`CODE_ALLOWED_FOR_EXECUTION=HOLD`

## 11. Routing candidates — no final executable assignment yet

CHAT owns source binding, routing, acceptance and release decisions.

Implementation candidates after fresh PreExec:

- **CODEX CLI / PINNED / gpt-6.1-sol / Medium / FULL_ACCESS**  
  Preferred candidate for this whole RC1 integration because launcher/process lifecycle, installer/update/uninstall, recovery and replay boundaries are materially coupled. Escalate to High only if concurrency/recovery debugging becomes material.

- **COPILOT CLI / NATIVE_AUTO / Balance / FULL_ACCESS**  
  Valid alternative only if fresh PreExec proves current auth/capacity and CHAT determines it can safely own the whole bounded RC1 implementation. Do not create an overlapping WPF-only writer inside `agent_bridge/**`.

- **WORK**  
  Not implementation owner by default. Required independent pre-Canary release-readiness audit after implementation/installed gates PASS.

No implementation Agent is finally assigned while R3/R5 remain unresolved.

## 12. Git authority after executable dispatch

Candidate delivery owner = AGENT, exact non-main task branch only.

No PR/main/merge/deploy/provider/broker/LIVE authority.

## 13. STOP conditions

STOP for:

- source/base/branch mismatch;
- stale/missing fresh PreExec receipt;
- wrong worktree;
- overlapping `agent_bridge/**` writer;
- missing .NET/WPF packaging capability;
- no eligible Agent route;
- Desktop App boundary violation;
- Worker lifecycle/replay regression;
- required test/security failure;
- secret/private exposure;
- out-of-scope write;
- push/readback failure.

## 14. Delivery

Expected:

- RC1 code under `agent_bridge/**`;
- `reports/BRIDGE-DESKTOP-BATCH-B/report.md`;
- `reports/BRIDGE-DESKTOP-BATCH-B/evidence_manifest.json`;
- RC1 evidence under `reports/BRIDGE-DESKTOP-BATCH-B/evidence/**`.

Final implementation result remains PUSHED_UNREVIEWED until CHAT intake.
