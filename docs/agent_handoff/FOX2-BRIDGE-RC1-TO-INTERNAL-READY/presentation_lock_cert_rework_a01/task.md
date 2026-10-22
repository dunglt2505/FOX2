# FOX2 — Presentation Lock Certification Rework A01

Task ID: `FOX2-BRIDGE-RC1-PRESENTATION-LOCK-CERT-REWORK-A01`
Whole-WP: `FOX2-BRIDGE-RC1-TO-INTERNAL-READY`
Feature: `FOX2-BRIDGE-RC1`
Stage: BUILD
Actor: CODEX
Model: `gpt-6.1-sol`
Thinking: `high`
Execution: Windows / PowerShell 7+ / CODEX CLI
Permission profile: FULL_ACCESS bounded to this task
Max Agent attempts: 1

## Trigger / historical truth

Host Lifecycle A04 result:
`92394d0ae68911c98bcdaa40aaa76ed56de66881`

CHAT A04 review:
`a3e49a62dbd340eacd8dc8369aa303ed0e93b6f3`

A04 is permanently consumed and MUST NOT be replayed.

A04 materially proved:
- exact accepted-source package build PASS;
- package provenance/hashes PASS;
- exact per-user install/update PASS;
- safe STOPPED / paused / setup_complete / current_dispatch=null PASS;
- stale-WPF bounded cleanup PASS;
- launch-twice exact singleton reached;
- Worker/legacy absent;
- no G3/G4/Canary.

The real lifecycle then FAILED at the live presentation-lock probe:

`PermissionError: [Errno 13] Permission denied: BridgeDesktop/desktop.lock`

from:
`agent_bridge/scripts/certify_user_lifecycle.py:157`.

Stable uninstall and reinstall were NOT_RUN.

## Immutable source base

Repository:
`dunglt2505/FOX2`

Base / last accepted BUILD source:
`085cc8302e824dbccf9cbef80422ed48894b9cb4`

CHAT accepted BUILD receipt:
`cdf9f9c919102a2337ef357f4b658dc9993f48e5`

Current lifecycle script:
- path: `agent_bridge/scripts/certify_user_lifecycle.py`
- blob: `7e62103ea4876833f67794a927a2a54622a59ea5`

Current focused regression test:
- path: `agent_bridge/tests/test_lifecycle_wpf_contract.py`
- blob: `f80e50d59b1f1bb9ec9d553e84bbe7948971cb66`

No other product/source/test file is in scope.

## Root cause

The WPF presentation opens:

`%LOCALAPPDATA%\FOX2\BridgeDesktop\desktop.lock`

with .NET `FileAccess.ReadWrite, FileShare.None` for the presentation lifetime.

The Python lifecycle certification currently accepts a denied live lock-open only when:
`getattr(error, 'winerror', None) == 32`.

The existing offline fixture synthesizes:
- real-held case as `PermissionError` with `winerror=32`;
- access-denied case as `PermissionError` with `winerror=5`.

Owner-host Python 3.13 surfaced the actual live-held probe as:
`PermissionError(errno=13)`
without a usable accepted `winerror == 32` classification.

The certification harness therefore lacks the real Windows/Python exception shape. This is a certification compatibility defect; A04 does NOT prove the WPF singleton itself is broken.

## Required correction semantics

Do NOT accept every `PermissionError` as held-lock proof.

Implement a fail-closed **differential presentation-lock proof**:

1. Before launching the presentation:
   - if `desktop.lock` exists, prove it is read/write openable by the current user;
   - if absent, absence is permitted;
   - any pre-live access denial must FAIL before launch.

2. Launch the accepted WPF twice and retain existing exact singleton PID/path/current-package checks.

3. While exact WPF is live:
   - require `desktop.lock` exists;
   - attempt the same read/write open without modifying bytes;
   - explicit sharing-violation `winerror=32` remains accepted;
   - real `PermissionError(errno=EACCES/13)` may be classified as held only when the pre-live proof was not access-denied and the exact live presentation identity is already established;
   - bounded evidence should record exception class / errno / winerror, not private path content;
   - any other OSError shape remains fail-closed.

4. Continue existing UI inspect/check, exact PID, safe-state and graceful-exit gates.

5. After explicit graceful exit and zero WPF:
   - require the same lock file to be read/write openable again;
   - only then is presentation-lock release PASS.

6. Never truncate/write/change lock bytes as part of the probe.

7. Preserve failures for:
   - live lock missing;
   - live lock unexpectedly openable;
   - pre-live lock inaccessible;
   - lock inaccessible after exit;
   - duplicate/missing/wrong-path/pointer-drift presentation;
   - PID drift;
   - unsafe control state;
   - UI/check/exit failures.

8. Preserve `NOT_APPLICABLE_PRE_G3`; do not add Worker/F1/tray fallback.

## Required regression tests

Update only:
`agent_bridge/tests/test_lifecycle_wpf_contract.py`

Add/adjust coverage proving at least:

- real A04 shape: `PermissionError(errno=13)` with no accepted `winerror=32` can PASS only under the differential lock proof;
- explicit `winerror=32` held-lock case remains PASS;
- persistent pre-live access denial FAILS;
- live lock free/openable FAILS;
- live lock missing FAILS;
- lock retained/inaccessible after graceful exit FAILS;
- unrelated OSError remains FAIL;
- lock bytes unchanged;
- existing singleton/UI/safe-state/Worker-F1 negative cases remain covered.

Do not weaken existing negative fixtures merely to obtain green tests.

## Allowed code paths

Only:
- `agent_bridge/scripts/certify_user_lifecycle.py`
- `agent_bridge/tests/test_lifecycle_wpf_contract.py`

Allowed result/evidence paths:
- `reports/FOX2-BRIDGE-RC1-TO-INTERNAL-READY/report.md`
- `reports/FOX2-BRIDGE-RC1-TO-INTERNAL-READY/evidence_manifest.json`
- `reports/FOX2-BRIDGE-RC1-TO-INTERNAL-READY/evidence/presentation_lock_cert_rework_a01/**`

No WPF C# source change unless task is stopped and CHAT issues a new scope. No drive-by refactor.

## Tests / validation

Required on Windows using the existing compatible environment; do not install or upgrade tools:

1. focused:
   `python -m pytest -q agent_bridge/tests/test_lifecycle_wpf_contract.py`

2. full Bridge Python regression:
   `python -m pytest -q agent_bridge/tests`

3. `git diff --check`

4. changed-path allowlist

5. K1:
   every material hunk classified as
   `REQUESTED / NECESSARY_DEPENDENCY / JUSTIFIED_GENERATED / UNEXPLAINED`;
   require `UNEXPLAINED=0`.

If a required pre-existing test failure is unrelated, preserve it truthfully; do not edit outside scope.

No host lifecycle A04/A05 execution in this BUILD task.

## Result contract

Agent must commit/push actual code/tests +:
- `reports/FOX2-BRIDGE-RC1-TO-INTERNAL-READY/report.md`
- `reports/FOX2-BRIDGE-RC1-TO-INTERNAL-READY/evidence_manifest.json`
- bounded evidence under `evidence/presentation_lock_cert_rework_a01/**`

to the authorized non-main rework branch.

Return observed remote result SHA outside the committed report.

Agent result is `PUSHED_UNREVIEWED` until CHAT applies `fox2-result-review`.

## STOP

STOP and report REWORK/BLOCKED if:
- source/task/prompt/Dispatch binding differs;
- worktree is dirty before coding;
- another writer owns the task paths;
- correction requires any path beyond the two allowed code/test files;
- correction requires WPF behavior changes rather than certification semantics;
- tests reveal a materially different root cause;
- tool installation/elevation is required;
- G3/G4/Canary/main/merge/provider/broker/LIVE would be touched;
- a consumed Dispatch would be replayed.

Historical A04 FAIL remains FAIL.
