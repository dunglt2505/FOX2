# FOX2 — Lifecycle/WPF Contract Rework A01

Task ID: `FOX2-BRIDGE-RC1-LIFECYCLE-WPF-CONTRACT-REWORK-A01`
Whole-WP: `FOX2-BRIDGE-RC1-TO-INTERNAL-READY`
Stage: BUILD
Actor: CODEX
Model: `gpt-6.1-sol`
Thinking: `high`
Execution path: `MANUAL_LOCAL`
Permission profile: `FULL_ACCESS`
Max Agent attempts: 1

## Goal

Correct the stale Phase-2 user-lifecycle certification harness so it matches the already-accepted current WPF/F1 runtime architecture, without changing that architecture.

The real Owner-host lifecycle A01 at result `9dd91becf47d934183baf147d0a4f03f4bf5933d` truthfully failed before uninstall because `certify_user_lifecycle.py` still requires a legacy `desktop_tray.ps1` process plus Worker heartbeat.

The current accepted runtime intentionally does not work that way.

## Immutable source / evidence

Branch base:
`9dd91becf47d934183baf147d0a4f03f4bf5933d`

Product source carried by that result:
`2faa33f9ab4d06bcc51c8fd1d2c7040fc06a29cb`

A01 CHAT review:
`1f3a07ea76485cb1b175d90a4303d9997b66e047`

A01 result:
`9dd91becf47d934183baf147d0a4f03f4bf5933d`

Historical accepted Desktop evidence:
- FIX-01 accepted result `ef9f290e73c4f4500900528656212c38acf43a4f`;
- Batch-A Owner accepted code head `3013f34d7ad91d1462e44495c873a84c41297b6b`;
- Batch-B final technical closure evidence at the accepted source lineage.

## Authoritative implementation contract for this rework

The Bridge Technical Spec v0.7 REV10 remains `CANDIDATE_NO_PROMOTION`; do not promote it or use it to override accepted implementation evidence.

For this rework, preserve the accepted current runtime contract proven by source/tests and historical CHAT/Owner acceptance:

1. `agent_bridge/src/fox2_agent_bridge/launcher.py` is presentation-only.
2. `launcher.launch()` must continue to return `worker_started=False`.
3. `agent_bridge/tests/test_rc1_launcher.py` states: “Launcher creates presentation only; Worker/Agent require the F1 service.”
4. F1 service/adoption is G3/G4 responsibility; Phase-2 package lifecycle must not manually start or simulate the protected Worker.
5. WPF `FOX2.Bridge.Desktop.exe` has its own singleton/presentation lock.
6. Existing `agent_bridge/scripts/certify_rc1_ui.ps1` is the supported installed-UI automation seam for `inspect / close / exit / check / artifact`.
7. Stable installed launcher is `BridgeRoot/launch.ps1`.
8. Stable uninstall is `BridgeRoot/uninstall.ps1`, external to version directories.

Do not “fix” the failing lifecycle by making Desktop presentation own/start the Worker.

## Required source correction

Update `agent_bridge/scripts/certify_user_lifecycle.py` so its pre-uninstall lifecycle stage follows the current architecture.

Required behavior:

### 1. Remove legacy-tray/Worker false assumptions

The harness must not:
- require a `pwsh.exe` process containing `desktop_tray.ps1`;
- require Worker heartbeat merely because WPF presentation launched;
- run installed `python -m fox2_agent_bridge worker` to prove a pre-G3 singleton;
- infer Phase-2 PASS from Worker/F1 runtime health.

### 2. Use stable installed WPF launch path

Launch the installed Desktop through:

`BridgeRoot/launch.ps1`

not directly through a version-local legacy tray path.

Launch twice and prove current WPF singleton semantics:
- exactly one `FOX2.Bridge.Desktop.exe` presentation remains;
- the observed presentation belongs to the exact current installed package;
- current Bridge control state remains safe for Phase-2: paused=true, setup_complete=true, no current dispatch;
- no Worker/F1 health claim is made.

### 3. Reuse existing installed UI automation seam

Use the existing:

`agent_bridge/scripts/certify_rc1_ui.ps1`

Do not duplicate UIAutomation logic in a new product module.

At minimum:
- `inspect` proves expected current WPF navigation surface;
- `check` proves Check Now is disabled while paused;
- `exit` is used for explicit graceful WPF presentation exit before uninstall.

### 4. Presentation lifecycle before uninstall

The harness must explicitly prove:
- live WPF presentation exists after launch;
- stable package lifecycle does not proceed to uninstall while WPF remains live;
- explicit UI `exit` causes WPF presentation count to reach zero within a bounded timeout;
- control state remains STOPPED/paused as applicable;
- presentation lock is released before uninstall.

Do not force-kill the WPF process in this Phase-2 harness.

### 5. Worker/F1 boundary

Phase-2 evidence must state Worker/F1 runtime health as:
`NOT_APPLICABLE_PRE_G3` or an equivalent explicit bounded status.

Do not convert it into PASS.

Do not start F1 service, AppLocker/AppIDSvc, privileged broker authority, service/ACL changes or G3/G4 behavior.

### 6. Preserve A03 uninstall semantics

Keep all accepted A03 properties unchanged:
- stable external `BridgeRoot/uninstall.ps1`;
- synchronous PowerShell 7 supervisor;
- installed Python never calls uninstall;
- bounded/sanitized stdout/stderr;
- exactly one stable uninstall attempt;
- nonzero/timeout/start/postcondition failure persists evidence and stops;
- no retry or alternate uninstall path;
- evidence checkpoint before reinstall;
- same exact package reinstall only after successful uninstall.

### 7. Preserve durable-state checks

Continue to verify:
- config preservation;
- database preservation;
- manual consumption preservation;
- historical Batch-B consumed identities unchanged;
- exact package reinstall;
- final paused installed state.

## Allowed code paths

Only:
- `agent_bridge/scripts/certify_user_lifecycle.py`
- `agent_bridge/tests/test_rc1_package.py`
- `agent_bridge/tests/test_rc1_launcher.py`
- at most one new focused test file under `agent_bridge/tests/` specifically for this lifecycle/WPF seam

No other product/source path is authorized.

## Explicitly forbidden source changes

Do not modify:
- `agent_bridge/src/fox2_agent_bridge/launcher.py`;
- `agent_bridge/src/fox2_agent_bridge/f1_service.py`;
- WPF production source under `agent_bridge/desktop_app/**`;
- `agent_bridge/scripts/certify_rc1_ui.ps1`;
- `agent_bridge/src/fox2_agent_bridge/installation.py`;
- AppLocker/G3/G4 source.

If the existing WPF/UI automation contract cannot support the required lifecycle without modifying one of those paths, STOP and report the exact incompatibility instead of expanding scope.

## Host mutation boundary

This is a source BUILD/rework task only.

Do not:
- build/install/update/uninstall/reinstall a real Owner-host package;
- launch the real installed WPF Desktop;
- mutate startup Task Scheduler;
- mutate Bridge durable host data;
- run G3/G4;
- touch AppLocker/AppIDSvc/service/ACL/reboot.

Use fixture/unit/integration tests only.

A fresh real host lifecycle certification will be issued only after CHAT accepts this source rework.

## Required tests

At minimum:

1. focused lifecycle/WPF regression proving no legacy `desktop_tray.ps1` health dependency;
2. launch-twice => one WPF presentation fixture;
3. exact-current-package presentation identity fixture;
4. paused/setup/no-current-dispatch pre-G3 state fixture;
5. UI inspect/check/exit command invocation fixture;
6. graceful WPF exit before uninstall fixture;
7. no Worker launch / no heartbeat requirement fixture;
8. no F1/G3 mutation fixture;
9. existing stable uninstall success regression;
10. uninstall nonzero/timeout/start/postcondition failure stop-once regressions;
11. install/package tests;
12. `test_rc1_launcher.py`;
13. full `agent_bridge/tests`;
14. Python syntax/static;
15. changed-path allowlist;
16. `git diff --check`;
17. bounded secret scan;
18. K1 `UNEXPLAINED=0`.

Historical initial MAX_PATH behavior must not be rewritten if encountered; environment-specific workaround must remain process-only and documented.

## Acceptance

CHAT can accept this BUILD rework only if:

- current presentation-only launcher/F1 ownership remains byte-identical;
- stale lifecycle legacy tray/Worker requirement is removed;
- WPF singleton/presentation identity/graceful exit is covered;
- stable uninstall/reinstall semantics remain intact;
- no real host lifecycle mutation occurred;
- required focused + full tests pass;
- no forbidden path changed;
- result contract is complete.

This acceptance will be BUILD-only.

It will not certify the real host lifecycle.

## Result delivery

Push only to the authorized non-main branch.

Required:
- code/test changes within allowed paths;
- `reports/FOX2-BRIDGE-RC1-TO-INTERNAL-READY/report.md`;
- `reports/FOX2-BRIDGE-RC1-TO-INTERNAL-READY/evidence_manifest.json`;
- `reports/FOX2-BRIDGE-RC1-TO-INTERNAL-READY/evidence/lifecycle_wpf_contract_rework/**`.

Return observed remote result SHA outside the committed report.

Final state after push is `PUSHED_UNREVIEWED` until CHAT result review.

## STOP

STOP on:
- source/task/prompt/branch drift;
- competing writer;
- missing route capability;
- need to modify forbidden architecture paths;
- need for real host lifecycle mutation;
- requirement to start Worker/F1 before G3;
- unrelated code changes;
- main/PR/merge/provider/broker/LIVE action;
- G3/G4/Canary action.

No replay of the consumed host-lifecycle A01 Dispatch.
