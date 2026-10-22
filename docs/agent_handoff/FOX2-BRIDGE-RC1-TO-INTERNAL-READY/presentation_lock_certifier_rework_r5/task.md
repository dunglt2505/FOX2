# FOX2 — Presentation Lock Certifier Rework R5

Task ID: `FOX2-BRIDGE-RC1-PRESENTATION-LOCK-CERTIFIER-REWORK-R5`
Whole-WP: `FOX2-BRIDGE-RC1-TO-INTERNAL-READY`
Feature: `FOX2-BRIDGE-RC1`
Whole feature stage: TEST
Residual task stage: BUILD correction inside TEST
Actor: CODEX
Model: `gpt-6.1-sol`
Thinking: `medium`
Permission profile: FULL_ACCESS bounded to this task
Max Agent attempts: 1

## TASK_ROUTE_ASSESSMENT

- `COMPLEXITY=EASY`
- ambiguity: `LOW`
- `EXECUTION_RISK=MEDIUM`
- `SAFETY_OVERRIDE=NO`
- dependency impact: `MEDIUM`
- evidence quality: `HIGH`
- `ROUTE_RATIONALE`: one known boolean-proof defect plus two mandatory negative fixtures; no architecture redesign, no package or host mutation. Medium thinking is retained because this code gates fail-closed host certification semantics.

Selected route:
`CODEX / gpt-6.1-sol / medium`

## Accepted product lineage versus salvage input

Accepted Bridge product source remains:

`085cc8302e824dbccf9cbef80422ed48894b9cb4`

R4 pushed result:

`d997756b5f4cfaa7e442dfc5d929093782b7a90f`

is **UNACCEPTED SALVAGE INPUT ONLY**, because CHAT review:

`07ce66987345859f978c06fbb4abbdeeaa0ff04c`

issued:

`CHAT_REWORK`.

R4 Dispatch is consumed/no-replay:
`FOX2-DISPATCH-BRIDGE-RC1-PRESENTATION-LOCK-CERTIFIER-REWORK-R4-CODEX-001`

Do not replay R4.

## FIRST_FAILURE

R4 correctly records:
- pre-live accessible lock → `OPENABLE`;
- no pre-live lock → `ABSENT`;
- live errno13/no-winerror → `ACCESS_DENIED_REQUIRES_DIFFERENTIAL`.

But the live-decision condition accepts errno13 when merely:

`'pre_live' in probes`

rather than requiring:

`pre_live.classification == OPENABLE`.

Therefore `ABSENT + live errno13` may be incorrectly accepted.

## Required correction

In `agent_bridge/scripts/certify_user_lifecycle.py`:

1. Explicit winerror 32 / `SHARING_VIOLATION` remains accepted.
2. errno13/no-winerror in a fresh or zero-WPF launch path is accepted only when the pre-live probe classification was exactly `OPENABLE`.
3. pre-live `ABSENT` + live errno13/no-winerror MUST fail closed.
4. existing-live continuation remains distinct:
   - one exact-current WPF at entry;
   - errno13 may remain provisional;
   - final acceptance only after graceful exit, zero WPF and same-lock post-exit `OPENABLE`.
5. Preserve same-file device/inode proof and lock bytes.
6. Preserve all existing unrelated negative behavior and lifecycle tail.

## Required tests

Modify only:
`agent_bridge/tests/test_lifecycle_wpf_contract.py`

Add/retain explicit coverage:

- fresh + pre-live ABSENT + live winerror32 → PASS;
- fresh + pre-live ABSENT + live errno13/no-winerror → FAIL;
- continuation zero-WPF + pre-live ABSENT + live errno13/no-winerror → FAIL;
- existing-live continuation + errno13 + post-exit openable → PASS;
- existing-live continuation + errno13 + post-exit denied → FAIL;
- pre-live OPENABLE + errno13 fresh/zero-WPF → PASS;
- unrelated OSError → FAIL;
- winerror5 → FAIL;
- lock bytes unchanged;
- no Worker/F1/tray fallback.

Do not weaken current fixtures.

## Allowed code/test paths

Exactly:
- `agent_bridge/scripts/certify_user_lifecycle.py`
- `agent_bridge/tests/test_lifecycle_wpf_contract.py`

Result/evidence:
- `reports/FOX2-BRIDGE-RC1-TO-INTERNAL-READY/report.md`
- `reports/FOX2-BRIDGE-RC1-TO-INTERNAL-READY/evidence_manifest.json`
- `reports/FOX2-BRIDGE-RC1-TO-INTERNAL-READY/evidence/presentation_lock_certifier_rework_r5/**`

No third product/test file.

## Validation

Use existing compatible Windows environment only; no install/upgrade.

Required:

`python -m pytest -q agent_bridge/tests/test_lifecycle_wpf_contract.py`

`python -m pytest -q agent_bridge/tests`

`git diff --check`

Also:
- exact changed-path allowlist relative to R5 runtime base;
- secret/privacy scan;
- K1 every material hunk;
- `UNEXPLAINED=0`;
- Result Contract v2 schema/hash checks.

## Evidence provenance requirement

R5 report/source-binding MUST explicitly bind the actual fresh R5 Dispatch identity and R5 PreExec receipt.

Do not repeat R4 wording that no fresh Dispatch existed merely because the control-branch file was not present in the task worktree.

## Reusable PASS

Reuse unaffected evidence:
- accepted Bridge source lineage;
- A04 package/provenance/install/safe-state/singleton PASS;
- R4 route/source/allowlist/no-host-mutation evidence where inputs are unchanged;
- R4 66 focused / 683 full test evidence as historical input only, not acceptance of R4 source.

New R5 final source must rerun focused and full suites because code/test bytes change.

## Result contract

Commit/push actual allowed changes plus R5 report/manifest/evidence.
Return observed remote result SHA outside committed report.
Result remains `PUSHED_UNREVIEWED` until CHAT review.

## STOP

STOP if:
- R5 task/prompt/Dispatch binding differs;
- route differs from CODEX / gpt-6.1-sol / medium;
- salvage base differs from `d997756b5f4cfaa7e442dfc5d929093782b7a90f`;
- third product/test file required;
- WPF product code must change;
- package build/install/host lifecycle required;
- tool install/elevation required;
- A05/G3/G4/Canary/main/merge/provider/broker/LIVE would be touched.

R4 remains CHAT_REWORK and no-replay.
