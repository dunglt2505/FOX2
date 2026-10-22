# FOX2 — Current-Package Owner-Host Lifecycle Certification A02

Task ID: `FOX2-BRIDGE-RC1-HOST-LIFECYCLE-CERT-A02`
Whole-WP: `FOX2-BRIDGE-RC1-TO-INTERNAL-READY`
Stage: TEST / REAL OWNER-HOST PACKAGE LIFECYCLE
Actor: CODEX
Model: `gpt-6.1-sol`
Thinking: `high`
Execution path: `MANUAL_LOCAL`
Permission profile: `FULL_ACCESS` only within this task
Max Agent attempts: 1

Task revision: `R2_PRE_ASSIGNMENT_WPF_HIDDEN_STATE_RECOVERY`

This revision supersedes the earlier **pre-assignment** task binding at
`d0b070e42d25a1581fee8a8731f393206ec5ef5b` for future execution only.

No executable Host Lifecycle A02 Dispatch existed and no Agent execution or host mutation had started when this revision was published.

Reason for revision: PreExec v2 observed exactly one current-package `FOX2.Bridge.Desktop.exe` and then failed because the UI Automation top-level window was unavailable. Accepted WPF source proves this can be a legitimate hidden/minimized presentation state: `ShutdownMode=OnExplicitShutdown`, close/minimize hides the window, and startup may create `MainWindow` without `Show()`. The TEST contract therefore distinguishes exact hidden/minimized presentation from unknown/wrong-process state instead of requiring a visible UI during read-only PreExec.

## Goal

Certify the **accepted A02 WPF presentation-only lifecycle contract** on the Owner physical Windows host.

Required sequence:

`exact package build -> install/update exact package -> establish safe paused state -> WPF presentation certification -> graceful WPF exit -> stable external uninstall once -> reinstall same exact package -> durable/final-state verification`.

This TEST does not perform Worker/F1 activation, G3/G4/AppLocker/service/ACL adoption or Canary.

## Immutable accepted source

Repository: `dunglt2505/FOX2`
Branch: `work/FOX2-BRIDGE-RC1-HOST-LIFECYCLE-CERT-A02-20261022`
Accepted source/result base: `085cc8302e824dbccf9cbef80422ed48894b9cb4`

Accepted A02 BUILD result:
`085cc8302e824dbccf9cbef80422ed48894b9cb4`

CHAT A02 acceptance:
`cdf9f9c919102a2337ef357f4b658dc9993f48e5`

A02 acceptance is BUILD-only. Real Owner-host lifecycle remains NOT_RUN.

Historical host lifecycle A01 result `9dd91becf47d934183baf147d0a4f03f4bf5933d` remains FAIL and its consumed Dispatch must never be replayed.

Historical lifecycle/WPF rework A01 Dispatch and A02 BUILD Dispatch are also consumed/no-replay.

## Accepted lifecycle semantics

The accepted A02 source deliberately uses a **WPF presentation-only launcher contract before G3**:

- stable entrypoint: `BridgeRoot/launch.ps1`;
- launch twice must result in exactly one current-package `FOX2.Bridge.Desktop.exe`;
- exact presentation identity is bound to current package path/pointer and UI PID;
- Bridge must be `paused=true`, `setup_complete=true`, and explicitly `current_dispatch=null`;
- Worker/F1 health is `NOT_APPLICABLE_PRE_G3`;
- no Worker/F1 start or heartbeat is required or permitted;
- existing `certify_rc1_ui.ps1` performs inspect/check/explicit exit;
- presentation lock must be held while live and released after graceful exit;
- post-exit Bridge state must be STOPPED/paused/setup-complete/no current dispatch;
- only after these checks may stable uninstall run.

Any requirement for legacy `desktop_tray.ps1`, Worker heartbeat or Worker/F1 activation is a contract violation and must STOP, not be worked around.

## Execution-start identity

Do not hard-code the future executable Dispatch sequence.

At execution:
- exact HEAD must equal fresh Dispatch `runtime_contract.base_sha`;
- accepted source `085cc830...` must be an ancestor;
- commits between accepted source and runtime base may contain only this task/prompt/PreExec/receipt evidence;
- no product/source/test drift is allowed.

## Host target and mutation boundary

Owner physical Windows host only.

Allowed real host mutation is strictly the per-user Bridge package lifecycle required for this TEST:
- bounded surface-and-graceful-close of one existing exact-current-package WPF presentation before install if necessary and provably safe;
- exact package install/update;
- setup/startup state operations required by the accepted lifecycle harness;
- WPF launch/inspect/check/graceful exit;
- stable external uninstall exactly once;
- exact same package reinstall;
- bounded recovery reinstall of the same exact package if needed after a post-mutation failure.

Forbidden:
- force-killing WPF as a normal path;
- Worker/F1 start;
- AppLocker/AppIDSvc;
- FOX2F1Authority service;
- ProgramData authority ACL;
- reboot;
- G3/G4;
- Canary;
- main/PR/merge;
- provider/broker/LIVE.

## Pre-mutation gates

Before package build or host mutation:

1. exact branch/worktree/source/task/prompt binding;
2. clean worktree and one task-scoped writer;
3. PowerShell 7, Python, Git, CODEX, dotnet and current pinned route available;
4. existing compatible isolated build Python available;
5. no tool/dependency installation;
6. fresh PreExec PASS for this exact A02 task;
7. historical consumed Dispatch identities remain no-replay;
8. current Bridge installed state captured read-only;
9. current WPF presentation processes captured read-only;
10. worker state captured read-only;
11. durable root/path identities captured read-only;
12. no G3/G4/Canary task active;
13. no unsafe process/state condition that would make package mutation ambiguous.

If exactly one current-package WPF presentation remains from a previous failed certification, read-only PreExec may classify it as either:
- `VISIBLE_INSPECTABLE_EXACT_CURRENT`; or
- `HIDDEN_OR_MINIMIZED_EXACT_CURRENT`.

The hidden/minimized classification is allowed only when process count is exactly one, executable path exactly matches the current-package Desktop executable, Bridge control state is paused/setup-complete/no-current-dispatch, and Worker/legacy tray processes are absent.

A hidden/minimized exact-current presentation is **not** closed during PreExec. The future fresh executable Dispatch may surface that same singleton exactly once via stable `BridgeRoot/launch.ps1`, require process count remains one and PID/path remain unchanged, then require UI inspect to bind the same PID before a single graceful exit.

If path/PID identity is unknown, launch creates more than one presentation, UI remains unavailable after bounded surfacing, or graceful exit fails, STOP before package install/update. No force kill.

Missing material capability or unsafe host state => STOP before mutation.

## Package-build gate

Build exact current package from accepted source using:

`agent_bridge/scripts/build_user_package.py`

Requirements:
- use clean accepted task branch;
- use already-existing isolated build Python only;
- package path must be outside `BridgeRoot` and survive uninstall;
- compute package SHA-256;
- verify manifest and payload/source/wheel hashes;
- require `manifest.source_git_commit == 085cc8302e824dbccf9cbef80422ed48894b9cb4`;
- verify dictionary/source provenance;
- verify package before first install;
- record bounded build environment identity and package evidence;
- package binary must not be committed.

No package mutation before this gate passes.

## Pre-state snapshot

Before first install/update capture bounded/sanitized evidence of:
- installed/not-installed state;
- current package SHA/source SHA if installed;
- exact WPF presentation count/path/PID if any;
- Worker state if readable;
- paused/setup/current-dispatch state if readable;
- startup preference;
- current pointer;
- durable config hash;
- database identity/hash and SQLite quick-check if safely available;
- manual consumption hash if present;
- stable `uninstall.ps1` presence/hash;
- owned version identities;
- Task Scheduler presence/status;
- exact package SHA/source to be installed.

Do not commit secrets, raw config, DB contents, raw prompts, private local paths or unnecessary logs.

## Real lifecycle sequence

### L0 — optional stale exact-current WPF reconciliation and cleanup

Only if PreExec observes exactly one WPF presentation and execution re-verifies it is the exact current package.

If the presentation is already visible/inspectable:
- require UI inspect PID equals the observed process PID.

If the presentation is exact-current but hidden/minimized:
- invoke stable `BridgeRoot/launch.ps1` exactly once to signal the existing singleton show-event;
- do not start Worker/F1;
- wait boundedly for the UI window;
- require WPF process count remains exactly one;
- require the same PID and exact executable path remain;
- require UI inspect PID equals that same process PID.

After either visible path is established:
- recheck paused/setup-complete/current_dispatch=null;
- invoke explicit graceful `exit` exactly once;
- wait boundedly for zero presentations;
- require presentation lock release;
- record cleanup as preparation, not lifecycle PASS.

If surfacing creates a second presentation, process/PID/path drifts, UI remains unavailable, safe control drifts, or graceful exit fails, STOP before install/update. No force kill and no fallback Worker/tray launch.

### L1 — install/update accepted package

Use:

`agent_bridge/scripts/install_user.ps1`

with exact package and SHA-256.

Requirements:
- no elevation/system-wide install;
- exact integrity verification;
- current pointer equals exact package SHA after success;
- installed receipt binds accepted source;
- no Worker/F1 start.

### L2 — establish safe paused state

Require:
- `paused=true`;
- `setup_complete=true`;
- explicit `current_dispatch=null`;
- no competing Worker/tray/other stale presentation that violates the accepted WPF lifecycle contract.

Do not start Worker/F1 to manufacture health.

### L3 — run accepted current lifecycle certification

Run:

`agent_bridge/scripts/certify_user_lifecycle.py`

using exact package/SHA and evidence path outside installed versions.

Accepted harness must exercise:
- setup/startup checks;
- `BridgeRoot/launch.ps1` twice;
- exactly one current-package WPF presentation;
- six UI navigation screens;
- paused Check Now disabled;
- held presentation lock;
- safe-control recheck;
- explicit graceful UI exit;
- zero presentation processes;
- lock release;
- STOPPED/paused/setup-complete/no-current-dispatch state;
- diagnostics;
- stable external `BridgeRoot/uninstall.ps1`;
- uninstall postconditions;
- durable state preservation;
- exact package reinstall;
- reinstalled setup/final safe state;
- historical consumed identity preservation.

Worker/F1 health remains `NOT_APPLICABLE_PRE_G3`.

Stable uninstall may be attempted exactly once.

### L4 — final installed state

On PASS:
- exact accepted package installed;
- current pointer exact;
- installed receipt binds source `085cc830...`;
- config/data/manual-consumption preserved;
- setup complete;
- paused safe state;
- no active dispatch;
- no WPF presentation left unintentionally;
- startup state explicitly recorded;
- historical consumed identities unchanged;
- no G3/G4 positive authority activated.

## Failure and recovery

Once host mutation begins:
- preserve first observed failure;
- do not rerun lifecycle certification;
- do not retry stable uninstall;
- do not replay Dispatch.

If failure leaves Bridge unavailable, bounded recovery may reinstall the **same exact accepted package** once if necessary to restore a usable per-user installation.

Recovery success does not convert lifecycle FAIL/BLOCKED into PASS.

If source/code change appears necessary, return REWORK_REQUIRED; no code changes in this TEST task.

## Allowed repository writes

No product/script/test edits.

Only:
- `reports/FOX2-BRIDGE-RC1-TO-INTERNAL-READY/report.md`
- `reports/FOX2-BRIDGE-RC1-TO-INTERNAL-READY/evidence_manifest.json`
- `reports/FOX2-BRIDGE-RC1-TO-INTERNAL-READY/evidence/host_lifecycle_cert_a02/**`

Temporary package/build/test outputs are not committed.

## Required acceptance evidence

1. accepted source/result = `085cc830...`;
2. package source_git_commit exactly `085cc830...`;
3. package SHA-256/manifest/payload verification before mutation;
4. bounded pre-state snapshot;
5. any pre-install WPF cleanup proves exact-current identity; hidden/minimized state may be surfaced once through stable launch with same singleton PID before graceful exit;
6. install/update exact package PASS;
7. current pointer/installed receipt exact;
8. safe paused/setup/no-current-dispatch state;
9. WPF launch twice -> one exact presentation;
10. UI inspect/check PASS;
11. live presentation lock held;
12. safe-control/presentation identity unchanged before exit;
13. explicit graceful WPF exit PASS;
14. presentation count zero + lock released;
15. post-exit STOPPED/paused/setup/no-current-dispatch PASS;
16. stable external uninstall attempted exactly once;
17. uninstall exit 0;
18. current pointer and owned versions absent immediately after uninstall;
19. durable config/database/manual-consumption preserved;
20. exact same package reinstall PASS;
21. final current pointer/source exact;
22. final setup/paused safe state PASS;
23. historical consumed identities preserved;
24. no old Dispatch replay;
25. no Worker/F1/G3/G4/AppLocker/service/ACL mutation;
26. report/evidence-only changed-path allowlist PASS;
27. secret scan PASS;
28. `git diff --check` PASS;
29. K1 `UNEXPLAINED=0`;
30. Result Contract v2 PASS;
31. remote result pushed and read back.

## Result states

Truthful result must be one of:
- PASS
- FAIL
- BLOCKED
- NEEDS_RECONCILIATION

Never convert recovery success or partial progress into lifecycle PASS.

## Result delivery

Agent must push only authorized report/evidence paths and return the observed remote result SHA outside committed report.

Final submission remains `PUSHED_UNREVIEWED` until CHAT applies `fox2-result-review`.

## STOP

STOP before mutation on source/task/prompt/PreExec/Dispatch drift, missing capability, dirty worktree, competing writer, package provenance failure or unsafe host state.

After mutation begins, preserve first failure and use only the bounded same-package recovery rule. Never blindly retry.
