# FOX2 Bridge RC1 — Release Plan

**State:** CHAT_LOCKED_PLANNING_BASELINE / NON_EXECUTABLE  
**Project:** FOX2  
**Planning source head:** `d129f9195adab04f158942f5a8638c63d0f3d0e6`  
**Control head:** `113faf3e49e3fc53004e7e889184c6f26505f302`  
**Canary 009 head:** `501822a33ef08c7365154913bbc677544856eee5`  
**Governance:** Project Dictionary v1.2 -> Policy v1.8.9 -> Routing v1.3.0 -> PreExec v1.1 -> Dispatch v3 -> Git-first Protocol v12

## 1. Release decision

RC1 includes the corrected Bridge core plus the native FOX2 Bridge Desktop App and local Artifact Vault. The next installed certification SHALL certify this final product shape once; do not certify the old PowerShell Tray as the final product and then recertify after replacing it.

```text
fixed Bridge core
 + WPF Desktop App
 + local Artifact Vault
 + stable launcher/startup integration
 -> FOX2 Bridge RC1
 -> fresh PreExec
 -> build/package/install/update/uninstall certification
 -> pre-Canary audit
 -> Canary 009 exactly once
 -> restart/no-replay
 -> CHAT final intake
 -> INTERNAL_FOX2_BRIDGE_READY
```

Canary 009 remains immutable and unconsumed until every pre-Canary RC1 gate is PASS.

## 2. Architecture lock

Final runtime topology:

```text
Windows user logon / explicit launch
            |
            v
Stable Bridge launcher
    |                     |
    |                     +--> FOX2 Bridge Desktop App (.NET 8 / WPF / MVVM)
    |                              |
    |                              +--> fixed local control/status contract only
    |
    +--> Python Bridge Worker
             |
             +--> durable ledger / replay guard
             +--> Git mailbox transport
             +--> dispatch validation
             +--> exact Codex/Copilot adapter selected by dispatch
```

Mandatory invariants:

1. Worker and Desktop App are separate processes.
2. Closing or crashing the Desktop App MUST NOT stop the Worker.
3. Desktop App MUST NOT own Git polling, dispatch claiming, Agent execution, routing, ledger mutation, merge/deploy/provider/broker/LIVE authority.
4. Desktop App may call only fixed Bridge controls and diagnostics already owned by the Bridge runtime.
5. Desktop App is single-instance per interactive Windows user.
6. Worker remains single-instance per Bridge profile.
7. CLI diagnostics/control remain usable when Desktop App is unavailable.
8. No visible PowerShell console is required for normal use.
9. Start-with-Windows remains current-user / limited / interactive; never SYSTEM by default.

## 3. Desktop App v1 requirements

Technology baseline:
- .NET 8;
- WPF;
- MVVM;
- native Windows;
- no Electron;
- no WebView execution dependency;
- no third-party UI framework required for RC1.

Required screens:
- Dashboard;
- Activity;
- Agents;
- Diagnostics;
- Artifacts;
- Settings.

Required UX:
- selected dark navy / FOX Orange visual baseline;
- Dashboard-first;
- Tray is secondary entry/control surface;
- left-click Tray opens Dashboard;
- X hides the window to Tray;
- `Exit after current task` requests graceful Worker exit;
- PAUSED is neutral, not error;
- DEGRADED/ERROR are actionable;
- no fabricated progress, usage, capacity, model, permission, or quota value;
- unknown/non-exposed values remain explicit.

## 4. Fixed Desktop control boundary

Allowed Desktop-to-Bridge calls:
- `control status`
- `control pause`
- `control resume`
- `control check-now`
- `control request-exit`
- `control open-logs`
- `control set-start-with-windows --enabled true|false`
- `diagnostics --output <path>`

Forbidden in Desktop App:
- `poll-once`
- `run-next`
- `e2e-once`
- direct Git commands;
- direct SQLite access;
- direct Codex/Copilot invocation;
- arbitrary shell command execution;
- model/reasoning/permission override.

## 5. Artifact Vault v1

Root:
`%LOCALAPPDATA%\FOX2\BridgeDesktop\Artifacts`

Required behavior:
- explicit user-selected file intake only;
- compute SHA-256 before copy;
- content-addressed local storage;
- verify copied SHA-256;
- atomic index update;
- sanitized file name;
- local size bound;
- local summary/open-vault controls.

Canonical states:

```text
LOCAL_SAVED != GIT_SYNCED != RELEASED
```

RC1 implements `LOCAL_SAVED` only. Automatic Git sync/release is not part of RC1 and MUST NOT be inferred.

## 6. Packaging and launcher requirements

The final RC1 package SHALL:
- preserve the existing verified per-user Python runtime/package model;
- include/publish the WPF Desktop App in a deterministic bounded package path;
- have one stable launcher that starts Worker and Desktop App without a visible console;
- tolerate Desktop App absence/failure without corrupting Worker state;
- update Desktop App transactionally with the Bridge package;
- uninstall application binaries while preserving intended durable config/data/logs/reports/artifacts according to the final uninstall contract;
- preserve project repositories/worktrees.

## 7. Historical evidence disposition

The historical `final_closure/final_certification.json` is INVALID/SUPERSEDED as readiness evidence because it claimed closure without a real Canary result. It MUST NOT be used to grant `INTERNAL_FOX2_BRIDGE_READY`.

Accepted product correction:
- implementation commit: `0be8a52b9622bf70dcb21fd2d35ddf913b17a635`;
- task/evidence head: `d129f9195adab04f158942f5a8638c63d0f3d0e6`;
- focused tests: 40 PASS;
- full Bridge tests: 380 PASS;
- installed certification after this correction: NOT_RUN;
- Canary 009: NOT_RUN.

The current historical PreExec receipt binds `ac41a7e0b543e79e470bed46b1aeb0101ba77405` and is stale for RC1 execution.

## 8. Release ordering

```text
A. RC1 source integration
B. source freeze
C. fresh PreExec on exact frozen source
D. Windows build/test/package
E. install/update/uninstall/startup/diagnostics certification
F. real safe poll proving control-store fix in installed runtime
G. independent pre-Canary release-readiness audit
H. Canary 009 exactly once
I. restart/no-replay
J. CHAT immutable remote intake
K. INTERNAL_FOX2_BRIDGE_READY
L. resume APP-BATCH-B
```

## 9. No-go rules

STOP before Canary if any of these is not PASS:
- source/worktree ownership;
- Desktop App build;
- Worker/UI process separation;
- single-instance semantics;
- deterministic package;
- install/update/uninstall;
- startup;
- control-store real poll;
- current/legacy dispatch compatibility;
- secret scan;
- changed-path allowlist;
- diff check;
- release-readiness audit;
- exact Canary identity/readiness.

No routing result grants PR/main/merge/deploy/provider/broker/LIVE authority.

## 10. Milestone markers

Pre-Canary:
`FOX2_BRIDGE_RC1_PRECANARY_READY`

Post-Canary/restart/readback:
`INTERNAL_FOX2_BRIDGE_READY`

Project internal go-live after APP-BATCH-B + M1-A release integration:
`FOX2_INTERNAL_GO_LIVE_READY`

This planning baseline is non-executable. A new executable source freeze requires a fresh Dictionary-resolved PreExec receipt and CHAT intake.
