# FOX2 — Current-Package Owner-Host Lifecycle Certification A01

Task ID: `FOX2-BRIDGE-RC1-HOST-LIFECYCLE-CERT-A01`
Whole-WP: `FOX2-BRIDGE-RC1-TO-INTERNAL-READY`
Stage: TEST / REAL OWNER-HOST PACKAGE LIFECYCLE
Actor: CODEX
Model: `gpt-6.1-sol`
Thinking: `high`
Execution path: `MANUAL_LOCAL`
Permission profile: `FULL_ACCESS` only within this task
Max Agent attempts: 1

## Goal

Certify the **current accepted package source** on the Owner physical Windows host after CHAT accepted the A03 lifecycle-harness correction.

This task performs real host lifecycle operations required for Phase 2 only:

`exact package build → install/update exact package → verify paused installed state → corrected lifecycle certification → stable external uninstall → reinstall exact same package → durable-state verification`.

This task does **not** perform G3/AppLocker/service/ACL adoption.

## Immutable accepted source

Repository: `dunglt2505/FOX2`
Branch: `work/FOX2-BRIDGE-RC1-HOST-LIFECYCLE-CERT-20261021`
Accepted source/result base: `2faa33f9ab4d06bcc51c8fd1d2c7040fc06a29cb`

Accepted implementation:
`fab3642b818415428ae3f67965430e3ea0b11401`

CHAT A03 acceptance receipt:
`37691b71b64de03091de9908014da2256c1d2901`

A03 acceptance is BUILD-only. Real Owner-host lifecycle remains NOT_RUN until this task.

Historical Batch-B `UNINSTALL_PATH=FAIL` remains factual and must not be rewritten.

## Execution-start identity

Do not hard-code the executable start HEAD to the source base.

At real execution:
- exact current HEAD must equal the fresh executable Dispatch `runtime_contract.base_sha`;
- accepted source base `2faa33f9...` must be an ancestor;
- commits after the accepted source base before execution may contain only this task/prompt/PreExec evidence;
- no product-code drift is allowed.

The future Dispatch sequence number is not hard-coded here.

## Host target

Owner physical Windows 11 Pro host only.

No VM target.

This task may mutate only the per-user Bridge package/runtime lifecycle required below.

## Pre-mutation gates

Before any package build or host mutation:

1. exact branch/worktree/source binding;
2. clean worktree and one task-scoped writer;
3. PowerShell 7, Python, Git, CODEX and current route available;
4. no A01/A02/A03 replay;
5. no G3/G4/Canary task active;
6. no Bridge install/worker/tray process that would make package mutation unsafe;
7. current Bridge installation state captured read-only;
8. current durable root paths captured read-only;
9. an existing isolated build Python satisfying `build_user_package.py` requirements is available;
10. `dotnet` required by the deterministic Desktop package build is available;
11. no tool installation or host setup is permitted to satisfy missing capability;
12. fresh PreExec PASS exists for this exact task before executable Dispatch issue.

Missing material capability => STOP before mutation.

## Package-build gate

Build the exact current package from the accepted source using:

`agent_bridge/scripts/build_user_package.py`

Requirements:
- build from the clean accepted task branch;
- use an already-existing isolated build Python;
- do not install/update tools or dependencies on the Owner host;
- use a package path outside `BridgeRoot` that survives uninstall;
- compute package SHA-256;
- verify package manifest;
- require `manifest.source_git_commit == 2faa33f9ab4d06bcc51c8fd1d2c7040fc06a29cb`;
- verify package dictionary/source provenance;
- verify package before first install;
- record exact package path, package SHA-256 and manifest evidence.

No host package mutation may occur before this package gate passes.

## Pre-state snapshot

Before first install/update capture bounded/sanitized evidence of:
- whether Bridge is installed;
- current package SHA/source SHA if installed;
- current worker state if readable;
- paused/setup state if readable;
- startup preference if readable;
- current pointer SHA;
- durable config hash;
- durable database file identity/hash if safely readable;
- manual consumption file hash if present;
- stable `uninstall.ps1` presence/hash if present;
- owned version directory identities;
- Task Scheduler presence/status for the current user;
- exact accepted package SHA to be installed.

Do not copy secrets, raw configuration, prompts, logs or database contents into Git.

## Real lifecycle sequence

### L1 — install/update current accepted package

Use the supported per-user installer:

`agent_bridge/scripts/install_user.ps1`

with exact package path and SHA-256.

Requirements:
- no elevation;
- no system-wide install;
- no service/AppLocker/ACL mutation;
- exact package integrity verification;
- after install/update, current pointer must equal the accepted package SHA;
- installed receipt/manifest must bind to accepted source;
- run/setup the installed Bridge only as needed to obtain the required paused test state.

### L2 — establish safe paused state

Before lifecycle certification:
- installed runtime must be paused;
- setup complete as applicable;
- startup/tray/worker state must be consistent with the certification harness;
- no competing worker/tray remains outside expected certification behavior.

If the host cannot be brought to the required paused state without out-of-scope mutation, STOP.

### L3 — run corrected current lifecycle certification

Run:

`agent_bridge/scripts/certify_user_lifecycle.py`

using the exact package and package SHA, with a bounded evidence path outside the installed versions tree.

This script must exercise:
- setup/startup checks;
- Tray/Worker healthy behavior;
- single-instance behavior;
- graceful exit;
- diagnostics;
- stable external `BridgeRoot/uninstall.ps1`;
- uninstall postconditions;
- durable config/data/manual-consumption preservation;
- reinstall exact package;
- reinstalled setup;
- consumed-identity preservation.

Stable uninstall must be attempted exactly once.

### L4 — final installed state

After successful certification:
- exact accepted package is installed;
- current pointer equals accepted package SHA;
- config/data/manual consumption remain preserved;
- installed setup is healthy;
- worker remains paused unless the harness contract explicitly proves a different safe final state;
- startup state must be explicitly recorded;
- no old Dispatch is replayed;
- no G3/G4 positive authority is activated.

## Recovery boundary

The accepted package file must remain outside `BridgeRoot` for the entire lifecycle.

If install/update fails before switching current pointer, rely only on the installer's transactional rollback and STOP.

If uninstall or later lifecycle step fails after host mutation:
- do not rerun the lifecycle certification;
- preserve the first failure evidence;
- do not retry uninstall;
- bounded recovery may reinstall the **same exact accepted package** only if needed to restore a usable per-user Bridge installation and if that recovery action is explicitly allowed by the execution prompt/Dispatch;
- recovery must not fabricate a lifecycle PASS;
- report the original lifecycle as FAIL/BLOCKED and the recovery separately.

No recovery may touch G3/AppLocker/service/ACL/provider/broker/LIVE.

## Allowed repository writes

No product code/test edits are allowed.

Only:
- `reports/FOX2-BRIDGE-RC1-TO-INTERNAL-READY/report.md`
- `reports/FOX2-BRIDGE-RC1-TO-INTERNAL-READY/evidence_manifest.json`
- `reports/FOX2-BRIDGE-RC1-TO-INTERNAL-READY/evidence/host_lifecycle_cert/**`

Local temporary package/build outputs must not be committed.

## Required acceptance evidence

1. exact package source commit = accepted result `2faa33f9...`;
2. package SHA-256 and manifest verified before mutation;
3. pre-state snapshot recorded;
4. install/update exact package PASS;
5. current pointer/installed receipt bind exact package/source;
6. paused state established;
7. corrected stable external uninstall path exercised once;
8. uninstall exit 0;
9. current pointer absent and owned versions absent immediately after uninstall;
10. durable config/database/manual-consumption evidence preserved;
11. reinstall exact same package PASS;
12. final current pointer exact;
13. setup/final health PASS;
14. consumed identities preserved;
15. no old Dispatch replay;
16. no G3/G4/AppLocker/service/ACL mutation;
17. bounded secret scan PASS;
18. changed-path allowlist PASS;
19. `git diff --check` PASS;
20. K1 `UNEXPLAINED=0`;
21. Result Contract v2 PASS;
22. report/evidence pushed to authorized non-main branch.

## Result states

A real host lifecycle result may be:
- `PASS`
- `FAIL`
- `BLOCKED`
- `NEEDS_RECONCILIATION`

Never convert real failure or recovery success into lifecycle PASS.

## Forbidden

- product/source/test code edits;
- replay A01 or A03;
- execute either rejected A02 Dispatch;
- retry a consumed lifecycle Dispatch;
- more than one stable uninstall attempt;
- install tools or dependencies to satisfy missing capability;
- AppLocker mutation;
- AppIDSvc mutation;
- FOX2F1Authority service install/start/stop/delete;
- ProgramData authority ACL mutation;
- reboot;
- G3/G4;
- Canary009 or final Canary;
- main/PR/merge;
- provider/broker/LIVE.

## Result delivery

Agent must push:
- updated `report.md`;
- updated `evidence_manifest.json`;
- bounded `evidence/host_lifecycle_cert/**`.

Return observed remote result SHA outside the committed report.

Status after push remains `PUSHED_UNREVIEWED` until CHAT applies `fox2-result-review`.

## STOP

STOP before mutation if source/task/prompt/PreExec/Dispatch/branch binding drifts, required capability is missing, build provenance fails, worktree is dirty, competing writer exists, or host state is unsafe.

After mutation begins, preserve the first observed failure and follow only the bounded recovery rule above. Never blindly retry.
