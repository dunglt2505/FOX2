# FOX2 — Presentation Lock Certifier Rework R3

Task ID: `FOX2-BRIDGE-RC1-PRESENTATION-LOCK-CERTIFIER-REWORK-R3`
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
- route rationale: known real-host failure, exact two-file scope, deterministic negative fixtures, no architecture redesign, no package build/install/uninstall/reinstall, no irreversible host mutation.

R0–R7 selected route candidate:
- Role: CODEX bounded BUILD correction executor
- Engine/Model: `gpt-6.1-sol`
- Thinking: `medium`
- Scope: exact two code/test files plus governed result/evidence
- STOP: third product/test path, WPF product change, package/host mutation, G3/G4/Canary, main/merge/provider/broker/LIVE
- route verification: MUST be performed by fresh R3 PreExec; this task does not self-certify host/model/effort availability.

## Owner objective

Implement the reuse-first Bridge lifecycle strategy already recorded in the Master Plan. Correct the certifier so A05 can continue from A04 without repeating A04 work that already passed.

## Controlling plans / feature status

Master Plan:
- path: `docs/roadmap/FOX2_MASTER_EXECUTION_PLAN_20261014.md`
- commit: `ad7d6f0b9889fe4247c29ac3d77f0b90b5f40e56`
- blob: `6068b0e664d43afc87468e52785806dafc70b59f`
- controlling directive: `Bridge Host Lifecycle reuse-first directive — 2026-10-22`

Reuse plan:
- path: `reports/FOX2-BRIDGE-RC1-TO-INTERNAL-READY/chat_reviews/HOST_LIFECYCLE_A04_A05_REUSE_PLAN_20261022.md`
- commit: `da6fd27d78380db42fce155d634044c94a661229`
- blob: `65f5a8359c18588be61ca42122acd894a8a80d99`

Skills v0.3.7 reassessment:
- path: `reports/FOX2-BRIDGE-RC1-TO-INTERNAL-READY/chat_reviews/BRIDGE_FEATURE_REASSESSMENT_V037_20261022.md`
- commit: `7cee0933ffd241deaa8e748bfeb626c56fab0cd0`
- blob: `74864a7520bcaaedcb885c4581a7f679fd5d1a43`

Feature Status correction:
- commit: `55751ebb52d4b4e4eed92ad7b8966b07b31a523c`
- whole feature: `TEST / IN_PROGRESS`

## Historical truth / supersession

A04:
- Dispatch: `FOX2-DISPATCH-BRIDGE-RC1-HOST-LIFECYCLE-CERT-A04-CODEX-001`
- result: `92394d0ae68911c98bcdaa40aaa76ed56de66881`
- CHAT review: `a3e49a62dbd340eacd8dc8369aa303ed0e93b6f3`
- state: `CLOSED_CHAT_REWORK / CONSUMED / NO_REPLAY`

A04 reusable runtime subject:
- package SHA-256: `f99c7add1b99bad938d977f634fd8a88e20763f5e35aaadf5cfe3072a1a327ee`
- runtime source commit: `085cc8302e824dbccf9cbef80422ed48894b9cb4`
- source inventory SHA-256: `6d76f99ce9fcc62bbcf9f2450a45bc920c28b2fd70828353c0a8fea096c5de73`
- archive: `C:\Projects\FOX2-artifacts\host_lifecycle_cert_a04\FOX2-Bridge-085cc830-A04.zip`

R1:
- PreExec `4d0ae5636ac91969c2a15416f8f0bd50d581d180`
- `SUPERSEDED_BEFORE_RUN`
- receipt absent / Dispatch absent / Agent not started
- DO NOT RUN

R2-High:
- task `9e1551d4e8e10aff3d302034c3f0c06588eac9ca`
- prompt `f6da01e9729b441ca80aece34ac282dd8195b12a`
- PreExec `da869f7171eb3e970e766ed3f8ff9100cfa316b0`
- `SUPERSEDED_BEFORE_RUN`
- reason: v0.3.7 requires `TASK_ROUTE_ASSESSMENT` before Model/Thinking binding; R2 prematurely hard-coded High
- receipt absent / Dispatch absent / Agent not started
- DO NOT RUN

No historical task/Dispatch is replayed or rebound by R3.

## Immutable code base

Accepted Bridge product BUILD source:
`085cc8302e824dbccf9cbef80422ed48894b9cb4`

CHAT BUILD acceptance:
`cdf9f9c919102a2337ef357f4b658dc9993f48e5`

Current certifier:
- path: `agent_bridge/scripts/certify_user_lifecycle.py`
- blob: `7e62103ea4876833f67794a927a2a54622a59ea5`

Current focused test:
- path: `agent_bridge/tests/test_lifecycle_wpf_contract.py`
- blob: `f80e50d59b1f1bb9ec9d553e84bbe7948971cb66`

## PASS preservation / DO_NOT_REBUILD_OR_REPLAY

R3 is an external-certifier correction. The certifier is not part of the installed runtime package payload.

Preserve A04 accepted PASS. R3 MUST NOT:
- rebuild the A04 package;
- re-run A04 package provenance/hash work;
- install/update/uninstall/reinstall Bridge;
- launch or exit WPF;
- mutate host lifecycle;
- repeat A04 singleton certification;
- touch Worker/F1;
- open G3/G4/Canary.

A05 later uses the same A04 runtime subject if its archive/installed identity remains valid.

## A04 first causal failure

Actual Owner-host first failure:

`PermissionError: [Errno 13] Permission denied: BridgeDesktop/desktop.lock`

at the live presentation-lock probe in:
`agent_bridge/scripts/certify_user_lifecycle.py`.

Current certifier only accepts a denied live lock-open when:
`getattr(error, "winerror", None) == 32`.

Owner-host Python 3.13 surfaced `errno=13` with no accepted `winerror=32` shape.

## Required implementation semantics

### 1. Bounded exception classifier

Record only:
- exception class;
- errno;
- winerror;
- classification.

Do not record private raw paths or uncontrolled exception text.

Accepted live-denial shapes:
- explicit `winerror == 32`;
- `PermissionError` with `errno == errno.EACCES (13)` only under differential ownership proof.

Other OSError forms remain fail-closed.

### 2. Fresh full-certification path

Preserve normal full-certification behavior:

1. Before WPF launch:
   - if `desktop.lock` exists, same current user must be able to open it read/write;
   - absence is allowed;
   - pre-live access denial FAILS.
2. Launch exact installed presentation and preserve exact singleton/current-package checks.
3. While live:
   - lock must exist;
   - same read/write open must be denied;
   - `winerror=32` is accepted;
   - `errno=13` is accepted only with pre-live accessibility + exact live identity.
4. UI inspect/check.
5. Graceful exit.
6. Zero WPF.
7. Same lock must become read/write openable.
8. Existing lifecycle tail remains available.

### 3. Explicit A04 continuation mode for future A05

Expose a testable continuation mode/API/flag.

If one exact-current WPF is already live:
1. do not relaunch merely to repeat historical singleton evidence;
2. verify exact PID/path/current package;
3. require lock exists;
4. probe live lock;
5. `winerror=32` accepted;
6. `errno=13` is provisional transient-live denial evidence;
7. run UI inspect/check;
8. graceful exit;
9. require zero WPF;
10. require same lock read/write open succeeds;
11. only post-exit openability finalizes provisional errno-13 as `PRESENTATION_LOCK_HELD`;
12. continue lifecycle tail.

If zero WPF exists at continuation entry:
- one launch is allowed to establish live state;
- do not require launch-twice merely to repeat A04 singleton evidence;
- apply same live-denied -> graceful-exit -> post-exit-openable proof.

If more than one WPF exists or a WPF is not exact-current:
- fail closed.

### 4. Lock integrity

Probe must never truncate/write/change lock bytes.

## Required regression coverage

Update only:
`agent_bridge/tests/test_lifecycle_wpf_contract.py`

Required cases:

1. full path explicit `winerror=32` PASS;
2. full path `errno=13`, no usable winerror, valid differential proof PASS;
3. pre-live access denied FAIL;
4. continuation existing exact WPF + errno=13 + post-exit openable PASS;
5. continuation existing exact WPF + errno=13 + post-exit denied FAIL;
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

Code/test — EXACTLY:
- `agent_bridge/scripts/certify_user_lifecycle.py`
- `agent_bridge/tests/test_lifecycle_wpf_contract.py`

Result/evidence:
- `reports/FOX2-BRIDGE-RC1-TO-INTERNAL-READY/report.md`
- `reports/FOX2-BRIDGE-RC1-TO-INTERNAL-READY/evidence_manifest.json`
- `reports/FOX2-BRIDGE-RC1-TO-INTERNAL-READY/evidence/presentation_lock_certifier_rework_r3/**`

No third product/test file. No WPF C# source.

## Validation

Use existing compatible Windows environment only. No install/upgrade.

Required:
1. focused:
   `python -m pytest -q agent_bridge/tests/test_lifecycle_wpf_contract.py`
2. affected full Bridge Python suite:
   `python -m pytest -q agent_bridge/tests`
3. `git diff --check`
4. changed-path allowlist
5. secret/privacy scan
6. K1 every material hunk:
   `REQUESTED / NECESSARY_DEPENDENCY / JUSTIFIED_GENERATED / UNEXPLAINED`
   with `UNEXPLAINED=0`.

No real Host Lifecycle in R3.

## Result contract

Commit/push actual allowed code/test changes plus:
- `reports/FOX2-BRIDGE-RC1-TO-INTERNAL-READY/report.md`;
- `reports/FOX2-BRIDGE-RC1-TO-INTERNAL-READY/evidence_manifest.json`;
- bounded evidence under `evidence/presentation_lock_certifier_rework_r3/**`.

Return observed remote result SHA outside committed report.

Result is `PUSHED_UNREVIEWED` until CHAT applies `fox2-result-review`.

## STOP

STOP before edit if:
- source/task/prompt/Dispatch binding differs;
- selected Model/Thinking differs from `gpt-6.1-sol / medium`;
- worktree is dirty or wrong;
- another task-scoped writer exists;
- source blobs differ;
- any third product/test path is required;
- WPF product behavior must change;
- package build/install/host lifecycle action would be required;
- tool installation/elevation is required;
- G3/G4/Canary/main/merge/provider/broker/LIVE would be touched.

Historical PASS remains reusable. Historical FAIL/NOT_RUN remains factual.
