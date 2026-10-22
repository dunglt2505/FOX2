# FOX2 — Presentation Lock Certifier Rework R4

Task ID: `FOX2-BRIDGE-RC1-PRESENTATION-LOCK-CERTIFIER-REWORK-R4`
Whole-WP: `FOX2-BRIDGE-RC1-TO-INTERNAL-READY`
Feature: `FOX2-BRIDGE-RC1`
Whole feature stage: TEST
Residual task stage: BUILD correction inside TEST
Actor: CODEX
Model: `gpt-6.1-sol`
Thinking: `medium`
Execution: Windows / PowerShell 7+ / CODEX CLI
Permission profile: FULL_ACCESS bounded to this task
Max Agent attempts: 1

## TASK_ROUTE_ASSESSMENT — FOX2 Skills v0.3.7

Residual task:
correct the external presentation-lock certification harness and focused regression tests only.

- `COMPLEXITY=MEDIUM`
- ambiguity: `LOW_MEDIUM`
- `EXECUTION_RISK=MEDIUM`
- `SAFETY_OVERRIDE=NO`
- dependency impact: `MEDIUM_HIGH`
- evidence quality: `HIGH`
- route rationale: known real-host failure, exact two-file scope, deterministic negative fixtures, no architecture redesign, no package build/install/uninstall/reinstall and no irreversible host mutation.

Selected route:
- Role: CODEX bounded BUILD correction executor
- Model: `gpt-6.1-sol`
- Thinking: `medium`
- Scope: exact two code/test files plus governed R4 result/evidence
- STOP: third product/test path, WPF product change, package/host mutation, A05/G3/G4/Canary, main/merge/provider/broker/LIVE

## Recovery lineage

R3 coding attempt A01:
- Dispatch: `FOX2-DISPATCH-BRIDGE-RC1-PRESENTATION-LOCK-CERTIFIER-REWORK-R3-CODEX-001`
- Dispatch commit: `097c57a779d1fca58d08aed80e2af4a0646b7ea8`
- runtime base: `7fcdfd19e0d9177b4d85e39fd249b5e65ccc0d49`
- final recovery: `3c32743e9b9cdcb7eb799094ee7bdefdaeb9aa71`
- verdict: `CONSUMED_NO_RESULT / NO_REPLAY`
- local result bytes: NONE
- remote result bytes: NONE
- active writer: NONE

R3 A01 MUST NOT be replayed or rebound.

## Reusable evidence

Preserve as reusable unless directly invalidated:
- accepted Bridge product source: `085cc8302e824dbccf9cbef80422ed48894b9cb4`
- CHAT BUILD acceptance: `cdf9f9c919102a2337ef357f4b658dc9993f48e5`
- A04 reusable package/provenance/install/safe-state/singleton PASS
- R3 route assessment rationale
- R3 schema-valid PreExec v4 host evidence as historical same-session capability evidence
- Master Plan reuse-first directive: `ad7d6f0b9889fe4247c29ac3d77f0b90b5f40e56`
- A04/A05 reuse plan: `da6fd27d78380db42fce155d634044c94a661229`
- Skills v0.3.7 Bridge reassessment: `7cee0933ffd241deaa8e748bfeb626c56fab0cd0`

Mandatory new-attempt PreExec rechecks only:
- exact R4 task/prompt/source binding;
- one-writer;
- current existing Python test runner capability;
- current CODEX auth/version/gpt-6.1-sol Medium capacity;
- current push permission;
- no fresh R4 Dispatch already exists.

Do not repeat A04 package/host PASS gates.

## Immutable product base

Accepted Bridge product source:
`085cc8302e824dbccf9cbef80422ed48894b9cb4`

Current certifier:
- path: `agent_bridge/scripts/certify_user_lifecycle.py`
- blob: `7e62103ea4876833f67794a927a2a54622a59ea5`

Current focused test:
- path: `agent_bridge/tests/test_lifecycle_wpf_contract.py`
- blob: `f80e50d59b1f1bb9ec9d553e84bbe7948971cb66`

R4 branch starts from that accepted source and contains no product/test edits before Agent execution.

## Root cause to correct

A04 real-host failure:

`PermissionError: [Errno 13] Permission denied: BridgeDesktop/desktop.lock`

The external certifier only accepted live denial when:
`getattr(error, "winerror", None) == 32`.

Owner-host Python 3.13 surfaced `errno=13` without an accepted `winerror=32` shape.

## Required implementation semantics

### 1. Bounded exception classifier

Record only:
- exception class;
- errno;
- winerror;
- classification.

Accepted live-denial shapes:
- explicit `winerror == 32`;
- `PermissionError(errno.EACCES/13)` only under differential ownership proof.

Unrelated OSError forms remain fail-closed.
Do not emit uncontrolled private path text.

### 2. Fresh full-certification path

1. Pre-live:
   - if `desktop.lock` exists, same user must be able to open read/write;
   - absence allowed;
   - pre-live denial FAIL.
2. Launch exact installed presentation and preserve existing singleton/current-package checks.
3. While live:
   - lock must exist;
   - same read/write open must be denied;
   - `winerror=32` accepted;
   - `errno=13` accepted only with pre-live accessibility + exact live identity.
4. UI inspect/check.
5. Graceful exit.
6. Zero WPF.
7. Same lock becomes read/write openable.
8. Existing lifecycle tail remains.

### 3. A04 continuation mode for future A05

Expose a testable continuation mode/API/flag.

If one exact-current WPF is already live:
- do not relaunch merely to repeat historical singleton evidence;
- verify exact PID/path/current package;
- require lock exists;
- live open must be denied;
- `winerror=32` accepted;
- `errno=13` is provisional live denial evidence;
- run UI inspect/check;
- graceful exit;
- require zero WPF;
- require same lock read/write open succeeds;
- only post-exit openability finalizes provisional errno-13 as `PRESENTATION_LOCK_HELD`;
- continue lifecycle tail.

If zero WPF exists:
- allow one launch only to establish live state;
- do not require launch-twice.

If >1 WPF or wrong WPF exists:
- fail closed.

### 4. Lock integrity

Probe must never truncate/write/change lock bytes.

## Required tests

Update only:
`agent_bridge/tests/test_lifecycle_wpf_contract.py`

Required coverage:
1. full path explicit `winerror=32` PASS;
2. full path `errno=13`, no usable winerror, valid differential proof PASS;
3. pre-live access denied FAIL;
4. continuation live exact WPF + errno=13 + post-exit openable PASS;
5. continuation live exact WPF + errno=13 + post-exit denied FAIL;
6. continuation zero-WPF uses one launch only;
7. live lock unexpectedly openable FAIL;
8. live lock missing FAIL;
9. unrelated OSError FAIL;
10. lock bytes unchanged;
11. duplicate/wrong-path/PID/current-pointer/UI/safe-state negatives remain;
12. Worker/F1 remains `NOT_APPLICABLE_PRE_G3`;
13. no Worker/F1/tray fallback introduced.

Do not weaken existing negative fixtures.

## Allowed paths

Code/test exactly:
- `agent_bridge/scripts/certify_user_lifecycle.py`
- `agent_bridge/tests/test_lifecycle_wpf_contract.py`

Result/evidence:
- `reports/FOX2-BRIDGE-RC1-TO-INTERNAL-READY/report.md`
- `reports/FOX2-BRIDGE-RC1-TO-INTERNAL-READY/evidence_manifest.json`
- `reports/FOX2-BRIDGE-RC1-TO-INTERNAL-READY/evidence/presentation_lock_certifier_rework_r4/**`

No third product/test file.
No WPF C# source.

## Validation

Use existing compatible Windows environment only. No install/upgrade.

Required:
- focused:
  `python -m pytest -q agent_bridge/tests/test_lifecycle_wpf_contract.py`
- full affected suite:
  `python -m pytest -q agent_bridge/tests`
- `git diff --check`
- changed-path allowlist
- secret/privacy scan
- K1 classification every material hunk:
  `REQUESTED / NECESSARY_DEPENDENCY / JUSTIFIED_GENERATED / UNEXPLAINED`
- require `UNEXPLAINED=0`

No real Host Lifecycle in R4.

## Result contract

Commit/push actual allowed code/test changes plus:
- `reports/FOX2-BRIDGE-RC1-TO-INTERNAL-READY/report.md`
- `reports/FOX2-BRIDGE-RC1-TO-INTERNAL-READY/evidence_manifest.json`
- bounded evidence under `evidence/presentation_lock_certifier_rework_r4/**`

Return observed remote result SHA outside the committed report.

Result remains `PUSHED_UNREVIEWED` until CHAT applies `fox2-result-review`.

## STOP

STOP before edit if:
- R4 task/prompt/Dispatch binding differs;
- selected route differs from `CODEX / gpt-6.1-sol / medium`;
- worktree dirty/wrong;
- competing task writer exists;
- source blobs differ;
- third product/test path required;
- WPF product behavior must change;
- package build/install/host lifecycle action required;
- tool installation/elevation required;
- A05/G3/G4/Canary/main/merge/provider/broker/LIVE would be touched.

Historical R3 A01 remains consumed/no-result/no-replay.
Historical PASS remains reusable.
Historical FAIL/NOT_RUN remains factual.
