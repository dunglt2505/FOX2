# FOX2 — Presentation Lock Certifier Rework R2

Task ID: `FOX2-BRIDGE-RC1-PRESENTATION-LOCK-CERTIFIER-REWORK-R2`
Whole-WP: `FOX2-BRIDGE-RC1-TO-INTERNAL-READY`
Feature: `FOX2-BRIDGE-RC1`
Stage: BUILD
Actor: CODEX
Model: `gpt-6.1-sol`
Thinking: `high`
Execution: Windows / PowerShell 7+ / CODEX CLI
Permission profile: FULL_ACCESS bounded to this task
Max Agent attempts: 1

## Owner objective

Implement the reuse-first Bridge lifecycle strategy recorded in the current Master Plan. Correct only the external presentation-lock certification harness and its focused regression tests so A05 can continue from A04 without rebuilding/reinstalling work that already passed.

## Current controlling plan

Master Plan:
- path: `docs/roadmap/FOX2_MASTER_EXECUTION_PLAN_20261014.md`
- commit: `ad7d6f0b9889fe4247c29ac3d77f0b90b5f40e56`
- blob: `6068b0e664d43afc87468e52785806dafc70b59f`
- directive: `Bridge Host Lifecycle reuse-first directive — 2026-10-22`

Detailed reuse plan:
- path: `reports/FOX2-BRIDGE-RC1-TO-INTERNAL-READY/chat_reviews/HOST_LIFECYCLE_A04_A05_REUSE_PLAN_20261022.md`
- commit: `da6fd27d78380db42fce155d634044c94a661229`
- blob: `65f5a8359c18588be61ca42122acd894a8a80d99`

## Historical truth / no replay

A04:
- Dispatch: `FOX2-DISPATCH-BRIDGE-RC1-HOST-LIFECYCLE-CERT-A04-CODEX-001`
- result: `92394d0ae68911c98bcdaa40aaa76ed56de66881`
- CHAT review: `a3e49a62dbd340eacd8dc8369aa303ed0e93b6f3`
- state: `CLOSED_CHAT_REWORK / CONSUMED / NO_REPLAY`

A04 package/runtime subject:
- package SHA-256: `f99c7add1b99bad938d977f634fd8a88e20763f5e35aaadf5cfe3072a1a327ee`
- runtime source commit: `085cc8302e824dbcc51c8fd1d2c7040fc06a29cb`
- corrected exact runtime source commit (authoritative spelling): `085cc8302e824dbccf9cbef80422ed48894b9cb4`
- source inventory SHA-256: `6d76f99ce9fcc62bbcf9f2450a45bc920c28b2fd70828353c0a8fea096c5de73`
- archive: `C:\Projects\FOX2-artifacts\host_lifecycle_cert_a04\FOX2-Bridge-085cc830-A04.zip`

The shorter/incorrect source spelling above is historical text only; this task binds exclusively to exact source:
`085cc8302e824dbccf9cbef80422ed48894b9cb4`.

R1 certifier rework:
- branch: `work/FOX2-BRIDGE-RC1-PRESENTATION-LOCK-CERT-REWORK-A01-20261022`
- PreExec publication: `4d0ae5636ac91969c2a15416f8f0bd50d581d180`
- state: `SUPERSEDED_BEFORE_RUN`
- receipt: ABSENT
- coding Dispatch: ABSENT
- Agent started: FALSE
- instruction: DO NOT RUN

R1 is not replayed or rebound.

## Immutable code base

Base / accepted runtime source:
`085cc8302e824dbccf9cbef80422ed48894b9cb4`

CHAT accepted BUILD:
`cdf9f9c919102a2337ef357f4b658dc9993f48e5`

Current certifier:
- path: `agent_bridge/scripts/certify_user_lifecycle.py`
- blob: `7e62103ea4876833f67794a927a2a54622a59ea5`

Current focused regression test:
- path: `agent_bridge/tests/test_lifecycle_wpf_contract.py`
- blob: `f80e50d59b1f1bb9ec9d553e84bbe7948971cb66`

## Key architectural fact

`certify_user_lifecycle.py` is an EXTERNAL certification harness. It is not part of the installed runtime package payload produced by `build_user_package.py`.

Therefore this task MUST NOT:
- rebuild the A04 package;
- install/update the Bridge;
- mutate the current host lifecycle;
- create a new runtime package subject;
- edit WPF product code.

The correction produces a new certifier/test source commit only.

## A04 first failure

Actual Owner-host failure:

`PermissionError: [Errno 13] Permission denied: BridgeDesktop/desktop.lock`

at the live presentation-lock probe in:
`agent_bridge/scripts/certify_user_lifecycle.py`.

Current harness accepts live lock denial only when:
`getattr(error, "winerror", None) == 32`.

The real Python 3.13 exception shape had errno 13 and no usable accepted winerror value.

## Required correction semantics

Implement fail-closed differential lock proof without weakening security.

### Shared classifier

Introduce a bounded helper/classifier that records only:
- exception class;
- errno;
- winerror;
- classification.

Do not record raw private paths or exception text if it may include them.

Accepted live-denial forms:
1. explicit Windows sharing violation `winerror == 32`;
2. `PermissionError` with `errno == errno.EACCES (13)` only when differential proof context establishes exact live presentation ownership.

Other OSError forms remain failure.

### Fresh-from-zero mode

Preserve full lifecycle behavior for a normal fresh certification:

1. Before WPF launch:
   - if `desktop.lock` exists, prove same current user can open it read/write;
   - if absent, absence is permitted;
   - pre-live access denial is FAIL.
2. Launch exact installed presentation twice and prove exact singleton/current package.
3. While live:
   - lock must exist;
   - live open must be denied;
   - explicit winerror 32 PASS;
   - errno 13 may PASS only with pre-live accessibility + exact live identity.
4. UI inspect/check.
5. Graceful exit.
6. Zero WPF.
7. Same lock must become read/write openable.
8. Continue existing post-exit/uninstall/reinstall behavior.

### A04 continuation mode

Add an explicit continuation path suitable for A05.

Continuation entry assumptions are NOT automatically trusted; caller/A05 PreExec must prove the fixed A04 runtime subject and the certifier itself must still verify exact installed WPF identity.

If one exact-current WPF is already live:
1. DO NOT relaunch it merely to repeat A04 singleton evidence.
2. Verify exact PID/path/current package.
3. Require lock exists.
4. Probe live lock:
   - winerror 32 accepted;
   - errno 13 accepted provisionally only as transient-live denial evidence.
5. Run UI inspect/check.
6. Graceful exit.
7. Require zero WPF.
8. Require same lock becomes read/write openable.
9. Only after post-exit openability succeeds may the provisional errno-13 denial be finalized as `PRESENTATION_LOCK_HELD`.
10. Continue lifecycle tail.

If zero WPF exists at continuation entry:
- one launch is allowed to establish live presentation;
- do not require launch-twice solely to repeat historical singleton evidence;
- then apply the same live-denied -> graceful-exit -> post-exit-openable differential proof.

If more than one WPF exists or any WPF is not exact-current:
- STOP/fail closed.

### Lock bytes

The probe must never truncate/write/change lock bytes.

Tests must prove bytes unchanged where a pre-existing lock file is used.

## Required tests

Update only:
`agent_bridge/tests/test_lifecycle_wpf_contract.py`

Required focused cases:

1. fresh mode explicit `winerror=32` PASS;
2. fresh mode errno=13/no-winerror with pre-live openable and post-exit openable PASS;
3. fresh mode pre-live access denied FAIL;
4. continuation mode existing exact live WPF + errno=13 + post-exit openable PASS;
5. continuation mode existing exact live WPF + errno=13 + post-exit still denied FAIL;
6. continuation mode zero WPF permits only one launch and then differential proof;
7. live lock unexpectedly openable FAIL;
8. live lock missing FAIL;
9. unrelated OSError FAIL;
10. lock bytes unchanged;
11. duplicate/wrong-path/PID/current-pointer/UI/safe-control negative cases remain;
12. Worker/F1 remains `NOT_APPLICABLE_PRE_G3`;
13. no Worker/F1/tray fallback introduced.

Do not weaken existing negative fixtures merely to pass tests.

## Allowed code/test paths

Exactly:
- `agent_bridge/scripts/certify_user_lifecycle.py`
- `agent_bridge/tests/test_lifecycle_wpf_contract.py`

No other product/test file.

Allowed result paths:
- `reports/FOX2-BRIDGE-RC1-TO-INTERNAL-READY/report.md`
- `reports/FOX2-BRIDGE-RC1-TO-INTERNAL-READY/evidence_manifest.json`
- `reports/FOX2-BRIDGE-RC1-TO-INTERNAL-READY/evidence/presentation_lock_certifier_rework_r2/**`

## Required validation

Use existing compatible Windows test environment only. No tool installation/upgrade.

Run:
1. `python -m pytest -q agent_bridge/tests/test_lifecycle_wpf_contract.py`
2. `python -m pytest -q agent_bridge/tests`
3. `git diff --check`
4. changed-path allowlist
5. secret/privacy scan
6. K1 hunk classification:
   `REQUESTED / NECESSARY_DEPENDENCY / JUSTIFIED_GENERATED / UNEXPLAINED`
   with `UNEXPLAINED=0`.

No A05 host execution in this BUILD task.

## Result contract

Agent must commit/push:
- the two allowed code/test files as needed;
- `reports/FOX2-BRIDGE-RC1-TO-INTERNAL-READY/report.md`;
- `reports/FOX2-BRIDGE-RC1-TO-INTERNAL-READY/evidence_manifest.json`;
- bounded evidence under `evidence/presentation_lock_certifier_rework_r2/**`.

Return observed remote result SHA outside the committed report.

Result remains `PUSHED_UNREVIEWED` until CHAT applies `fox2-result-review`.

## STOP

STOP before editing if:
- source/task/prompt/Dispatch binding differs;
- branch/worktree is dirty or wrong;
- another writer owns either allowed code/test path;
- current base blobs differ;
- task requires a third product/test file;
- WPF C# behavior must change;
- host package rebuild/install/lifecycle action would be required;
- tool install/elevation is required;
- G3/G4/Canary/main/merge/provider/broker/LIVE would be touched.

Historical A04 FAIL and R1 superseded state remain immutable.
