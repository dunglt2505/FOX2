# FOX2 — Current-Package Owner-Host Lifecycle Certification A04

Task ID: `FOX2-BRIDGE-RC1-HOST-LIFECYCLE-CERT-A04`
Whole-WP: `FOX2-BRIDGE-RC1-TO-INTERNAL-READY`
Stage: TEST / REAL OWNER-HOST PACKAGE LIFECYCLE
Actor: CODEX
Model: `gpt-6.1-sol`
Thinking: `high`
Execution path: `MANUAL_LOCAL`
Permission profile: `FULL_ACCESS` only within this task
Max Agent attempts: 1

Retry class: `FRESH_ATTEMPT_AFTER_A03_PROVENANCE_REWORK`

Historical A03 Dispatch:
`FOX2-DISPATCH-BRIDGE-RC1-HOST-LIFECYCLE-CERT-A03-CODEX-001`

is permanently consumed and MUST NOT be replayed.

A03 result:
`883ea51a429baf6749fa3fd412cc9ebb044f6efc`

CHAT A03 review:
`eced60bc22e7294bf49b367791c122ad91a97f43`

A03 truth:
- result delivery/evidence accepted as truthful;
- lifecycle certification NOT_RUN;
- no package build;
- no host lifecycle mutation;
- blocker: builder provenance follows the worktree HEAD, while the A03 orchestration worktree HEAD necessarily included task/prompt/PreExec/receipt commits after the accepted product source.

A04 corrects that contradiction by separating the **orchestration worktree** from the **package-source worktree**. It does not change product/source/test code.

## Goal

Certify the accepted WPF presentation-only lifecycle on the Owner physical Windows host.

Required sequence:

`exact accepted-source package build -> install/update exact package -> safe paused state -> WPF presentation certification -> graceful WPF exit -> stable external uninstall exactly once -> reinstall same exact package -> durable/final-state verification`.

This TEST does not perform Worker/F1 activation, G3/G4/AppLocker/service/ACL adoption or Canary.

## Immutable accepted product source

Repository: `dunglt2505/FOX2`

Accepted BUILD result:
`085cc8302e824dbccf9cbef80422ed48894b9cb4`

CHAT BUILD acceptance:
`cdf9f9c919102a2337ef357f4b658dc9993f48e5`

The accepted product source is unchanged from A03.

## A04 orchestration branch/worktree

Branch:
`work/FOX2-BRIDGE-RC1-HOST-LIFECYCLE-CERT-A04-20261022`

Owner-host orchestration worktree:
`C:\Projects\FOX2-worktrees\FOX2-BRIDGE-RC1-HOST-LIFECYCLE-CERT-A04-20261022`

This worktree contains the fresh A04 task/prompt/PreExec/receipt/result history and is where CODEX executes.

It MUST have no `agent_bridge` product/source/test drift from the accepted BUILD result.

The package MUST NOT be built from this orchestration worktree because its HEAD includes post-source governance/handoff commits.

## Dedicated accepted-source package worktree

Exact Owner-host path:
`C:\Projects\FOX2-worktrees\FOX2-BRIDGE-RC1-PACKAGE-SOURCE-085CC830-A04`

This MUST be a dedicated Git worktree of the same repository with:

- detached HEAD;
- `HEAD == 085cc8302e824dbccf9cbef80422ed48894b9cb4`;
- clean tracked/untracked state before package build;
- no task/prompt/PreExec/report commits;
- no branch checkout;
- no source modifications;
- no manifest rewrite;
- no environment/ref override that changes reported provenance;
- no product/source/test commit.

The unchanged builder used for packaging MUST be:

`C:\Projects\FOX2-worktrees\FOX2-BRIDGE-RC1-PACKAGE-SOURCE-085CC830-A04\agent_bridge\scripts\build_user_package.py`

Accepted builder blob:
`2417212e5677a2061e3957544a99e2ba80f46f4d`

Before package build, CODEX MUST invoke the accepted builder's `source_git_commit()` read-only from this package-source worktree and require:

`085cc8302e824dbccf9cbef80422ed48894b9cb4`

Only then may the package be built.

The package build may create only ordinary ignored/transient build outputs in this dedicated package-source worktree and temporary/output directories; no tracked source modifications are allowed.

## Package output

Package output MUST be outside:
- `BridgeRoot`;
- the orchestration worktree;
- the package-source worktree.

It must survive stable uninstall/reinstall.

No package binary or build artifact is committed to Git.

## Runtime authorization envelope

Future A04 PASS_TO_ASSIGN and Dispatch commit SHAs are unknown at task/prompt publication time.

At actual CODEX start, the verified Owner-visible PowerShell launcher MUST inject:

- `FOX2_DISPATCH_ID`
- `FOX2_DISPATCH_COMMIT`
- `FOX2_RUNTIME_BASE`
- `FOX2_ACCEPTED_SOURCE`
- `FOX2_PASS_TO_ASSIGN_COMMIT`
- `FOX2_PASS_TO_ASSIGN_PATH`
- `FOX2_PREEXEC_RECEIPT_COMMIT`
- `FOX2_CONTROL_BRANCH`
- `FOX2_STATUS_BRANCH`
- `FOX2_PACKAGE_SOURCE_WORKTREE`
- `FOX2_OWNER_LAUNCHER_VERIFIED`

Expected fixed values:
- Dispatch ID: `FOX2-DISPATCH-BRIDGE-RC1-HOST-LIFECYCLE-CERT-A04-CODEX-001`
- accepted source: `085cc8302e824dbccf9cbef80422ed48894b9cb4`
- control branch: `work/FOX2-DISPATCH-chat`
- status branch: `work/FOX2-BRIDGE-F1-G1-INTEGRATED-DESIGN-20261021`
- PASS_TO_ASSIGN path: `reports/FOX2-BRIDGE-RC1-TO-INTERNAL-READY/chat_reviews/HOST_LIFECYCLE_CERT_A04_PASS_TO_ASSIGN_20261022.md`
- package-source worktree: `C:\Projects\FOX2-worktrees\FOX2-BRIDGE-RC1-PACKAGE-SOURCE-085CC830-A04`
- `FOX2_OWNER_LAUNCHER_VERIFIED=TRUE`
- `FOX2_PREEXEC_RECEIPT_COMMIT == FOX2_RUNTIME_BASE`

Before package build or host mutation, CODEX MUST independently fetch/read the supplied immutable Git refs and verify the task/prompt/source/PreExec/PASS_TO_ASSIGN/Dispatch bindings.

Environment variables transport evidence only; Git remains authoritative.

## Accepted WPF lifecycle semantics

Before G3:
- WPF is presentation-only;
- stable entrypoint is `BridgeRoot/launch.ps1`;
- launch twice => exactly one current-package `FOX2.Bridge.Desktop.exe`;
- exact presentation identity must agree with current package path/pointer and UI PID;
- `paused=true`;
- `setup_complete=true`;
- explicit `current_dispatch=null`;
- Worker/F1 health = `NOT_APPLICABLE_PRE_G3`;
- no Worker/F1 start or heartbeat;
- `certify_rc1_ui.ps1` is the inspect/check/explicit-exit seam;
- presentation lock held while live and released after graceful exit;
- post-exit state STOPPED/paused/setup/no-current-dispatch;
- only then stable uninstall may run.

Legacy `desktop_tray.ps1`, Worker heartbeat or Worker/F1 activation must not be used to make a check pass.

## Pre-mutation gates

Before package build or host mutation verify:

1. exact A04 orchestration branch/worktree/task/prompt/PreExec/runtime envelope;
2. orchestration worktree clean and no `agent_bridge` drift;
3. package-source worktree exact detached accepted source and clean;
4. accepted builder blob exact;
5. accepted builder `source_git_commit()` returns exact accepted source from package-source worktree;
6. one task-scoped CODEX writer;
7. PowerShell 7, Git, Python, CODEX, dotnet and pinned route available;
8. existing compatible isolated build Python only; no installs;
9. fresh A04 PreExec PASS;
10. historical consumed Dispatch identities preserved/no-replay;
11. current Bridge state/WPF/Worker/durable identities captured read-only;
12. no G3/G4/Canary;
13. no unsafe host condition.

## Existing hidden/minimized WPF

If exactly one exact-current presentation exists and is hidden/minimized, the executable TEST may:

- reverify exact current package/path/PID;
- require paused/setup/current_dispatch=null and Worker/legacy absent;
- invoke stable `BridgeRoot/launch.ps1` exactly once only to signal the existing singleton;
- require WPF count remains one;
- require same PID/path;
- require UI inspect binds that PID;
- recheck safe state;
- invoke explicit graceful UI exit once;
- require zero WPF presentations and presentation-lock release.

STOP before install if any identity drifts, a second WPF appears, UI remains unavailable, safe state drifts or graceful exit fails.

No force kill and no Worker/F1 fallback.

## Package build gate

Use ONLY the builder in the detached accepted-source package worktree.

Use only the already-existing compatible isolated build Python.

Before build:
- builder blob must equal `2417212e5677a2061e3957544a99e2ba80f46f4d`;
- builder raw source must be from accepted source;
- `source_git_commit()` must return exact accepted source;
- package-source worktree must be clean.

Build exactly once.

After build:
- compute package SHA-256;
- verify manifest;
- require `manifest.source_git_commit == 085cc8302e824dbccf9cbef80422ed48894b9cb4`;
- verify source/payload/wheel-module hashes;
- verify dictionary/source provenance;
- package path outside BridgeRoot/worktrees;
- record bounded build Python and dotnet identities.

No manifest rewrite or provenance override.

If package provenance differs, STOP before host mutation.

## Pre-state snapshot

Before first install/update capture bounded/sanitized evidence:
- installed/current pointer/source receipt;
- WPF count/path/PID;
- Worker state;
- paused/setup/current_dispatch;
- startup preference;
- config SHA-256;
- database identity/hash + SQLite quick-check if safely available;
- manual-consumption SHA-256;
- stable uninstall identity/hash;
- owned versions;
- Task Scheduler state;
- historical consumed identities.

A04 uses its own fresh pre-mutation baseline. Historical DB hash differences are not automatically PASS or FAIL.

Do not commit raw config/DB contents/secrets/private paths/raw prompts.

## Lifecycle sequence

### L0 — optional stale exact-current WPF cleanup

Use the bounded singleton surface/inspect/graceful-exit contract above.

### L1 — install/update

Use:
`agent_bridge/scripts/install_user.ps1`

with exact package path and SHA-256.

Require:
- per-user only;
- no elevation/system-wide install;
- exact current pointer/package/source receipt;
- no Worker/F1 start.

### L2 — safe paused state

Require:
- paused=true;
- setup_complete=true;
- current_dispatch=null;
- no conflicting Worker/tray/presentation state.

### L3 — accepted real lifecycle

Run:
`agent_bridge/scripts/certify_user_lifecycle.py`

with exact package, package SHA-256 and bounded evidence directory outside installed versions.

It must exercise:
- setup/startup checks;
- WPF launch twice;
- singleton exact identity;
- UI inspect/check;
- six expected navigation screens;
- Check Now disabled while paused;
- held presentation lock;
- safe-state recheck;
- explicit graceful exit;
- zero WPF;
- lock release;
- post-exit safe control;
- diagnostics;
- stable external `BridgeRoot/uninstall.ps1`;
- immediate uninstall postconditions;
- durable state preservation relative to A04 pre-state;
- exact same package reinstall;
- final current pointer/source/setup/paused safe state;
- historical consumed identity preservation.

Stable uninstall attempt count must equal one on a successful lifecycle.

### L4 — final state

On PASS:
- exact accepted package installed;
- current pointer/source exact;
- config/data/manual-consumption preserved relative to A04 pre-state;
- setup complete;
- paused safe state;
- current_dispatch=null;
- no unintended WPF left;
- startup state recorded;
- historical consumed identities unchanged;
- no G3/G4 authority activated.

## Failure / recovery

Once host mutation begins:
- preserve first failure;
- never rerun lifecycle certification in this Dispatch;
- never retry stable uninstall;
- never replay Dispatch;
- never silently change package/source.

If needed after post-mutation failure, bounded recovery may reinstall the same exact package once.

Recovery success never converts FAIL/BLOCKED into PASS.

If product/source code correction is required, STOP with REWORK_REQUIRED. No product code changes are authorized in this TEST task.

## Allowed Git writes

No product/script/test edits.

Only:
- `reports/FOX2-BRIDGE-RC1-TO-INTERNAL-READY/report.md`
- `reports/FOX2-BRIDGE-RC1-TO-INTERNAL-READY/evidence_manifest.json`
- `reports/FOX2-BRIDGE-RC1-TO-INTERNAL-READY/evidence/host_lifecycle_cert_a04/**`

Temporary build/package outputs are not committed.

## Acceptance

Required truthfully:

1. runtime authorization envelope and remote Git verification PASS;
2. orchestration worktree no product drift;
3. detached package-source worktree exact accepted source PASS;
4. accepted builder exact and pre-build `source_git_commit()` PASS;
5. package built once;
6. package manifest/source/hash PASS;
7. A04 pre-state snapshot;
8. optional WPF cleanup exact identity/same PID/graceful exit if needed;
9. install/update exact package PASS;
10. safe paused/setup/no-current-dispatch;
11. launch twice one exact presentation;
12. UI inspect/check PASS;
13. presentation lock held;
14. explicit graceful exit;
15. zero WPF + lock release;
16. post-exit safe state;
17. stable external uninstall exactly once;
18. uninstall exit zero;
19. immediate uninstall postconditions;
20. durable state preserved relative to A04 pre-state;
21. same exact package reinstall PASS;
22. final pointer/source/setup/paused state PASS;
23. consumed identities preserved;
24. no replay;
25. no Worker/F1/G3/G4/AppLocker/service/ACL mutation;
26. report/evidence-only changed-path allowlist;
27. secret/privacy scan PASS;
28. git diff --check PASS;
29. K1 UNEXPLAINED=0;
30. Result Contract v2 PASS;
31. remote result push/readback.

## Result states

Truthful result:
- PASS
- FAIL
- BLOCKED
- NEEDS_RECONCILIATION

Never promote partial/recovery progress to PASS.

## STOP

STOP before mutation on any source/task/prompt/PreExec/Dispatch/PASS_TO_ASSIGN/package-source-worktree drift, missing capability, dirty worktree, provenance mismatch, competing writer or unsafe host state.

After mutation starts, preserve first failure and use only the bounded same-package recovery rule.
