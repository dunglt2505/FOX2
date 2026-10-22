FOX2 — CODEX EXECUTION PROMPT — PRESENTATION LOCK CERTIFIER REWORK R2

Role: CODEX — bounded BUILD correction executor
Model: gpt-6.1-sol
Thinking: high
Project: FOX2 only
Repository: dunglt2505/FOX2
Branch: work/FOX2-BRIDGE-RC1-PRESENTATION-LOCK-CERTIFIER-REWORK-R2-20261022
Permission profile: FULL_ACCESS bounded to exact task
Max runs: 1
No model substitution
No historical Dispatch replay

IMMUTABLE TASK

Task ID:
FOX2-BRIDGE-RC1-PRESENTATION-LOCK-CERTIFIER-REWORK-R2

Task:
- path: docs/agent_handoff/FOX2-BRIDGE-RC1-TO-INTERNAL-READY/presentation_lock_certifier_rework_r2/task.md
- commit: 9e1551d4e8e10aff3d302034c3f0c06588eac9ca
- blob: e727eeca3d4d24332ba6a0f2afb07d7d8753c860
- SHA-256: d209ee454efeaf42b9b0001a5182ce80e8f135756bfa07745acb7b64e7425da4

SOURCE LOCK

Exact code base:
085cc8302e824dbccf9cbef80422ed48894b9cb4

Current certifier:
agent_bridge/scripts/certify_user_lifecycle.py
blob 7e62103ea4876833f67794a927a2a54622a59ea5

Current focused test:
agent_bridge/tests/test_lifecycle_wpf_contract.py
blob f80e50d59b1f1bb9ec9d553e84bbe7948971cb66

CONTROLLING PLAN

Master Plan commit:
ad7d6f0b9889fe4247c29ac3d77f0b90b5f40e56

Master Plan directive:
Bridge Host Lifecycle reuse-first directive — 2026-10-22

Reuse plan commit:
da6fd27d78380db42fce155d634044c94a661229

A04 result:
92394d0ae68911c98bcdaa40aaa76ed56de66881

A04 CHAT review:
a3e49a62dbd340eacd8dc8369aa303ed0e93b6f3

A04 package subject remains:
f99c7add1b99bad938d977f634fd8a88e20763f5e35aaadf5cfe3072a1a327ee
from source:
085cc8302e824dbccf9cbef80422ed48894b9cb4

R1 PreExec 4d0ae5636ac91969c2a15416f8f0bd50d581d180 is SUPERSEDED_BEFORE_RUN.
Do not run/reuse/rebind R1.

OBJECTIVE

Correct only the external lifecycle certification harness so future A05 can continue from A04 and reuse all still-valid A04 PASS evidence.

This task does NOT create a new runtime package source and MUST NOT:
- build the Bridge package;
- install/update/uninstall/reinstall Bridge;
- launch/exit WPF;
- mutate host lifecycle;
- touch Worker/F1;
- open G3/G4/Canary.

ALLOWED CODE/TEST PATHS — EXACTLY TWO

1. agent_bridge/scripts/certify_user_lifecycle.py
2. agent_bridge/tests/test_lifecycle_wpf_contract.py

No third product/test file.
No WPF C# source.
No drive-by refactor.

REQUIRED IMPLEMENTATION

Implement fail-closed differential presentation-lock proof.

A. Exception classification:
- retain explicit Windows sharing violation winerror=32;
- support PermissionError errno=EACCES/13 when differential ownership proof is available;
- do not accept all PermissionError;
- unrelated OSError remains failure;
- bounded evidence may record exception class, errno, winerror, classification only.

B. Fresh full-certification path:
- pre-live existing lock must be read/write openable; absent is allowed;
- launch exact WPF and preserve existing exact singleton checks;
- live lock must exist and be denied;
- errno 13 may pass only with pre-live accessibility + exact live identity;
- UI inspect/check;
- graceful exit;
- zero WPF;
- same lock must become read/write openable;
- then existing lifecycle tail continues.

C. Continuation path for A05:
- expose an explicit, testable continuation mode/API/flag;
- if one exact-current WPF is already live, do not relaunch merely to repeat A04 singleton evidence;
- verify exact PID/path/current installed package;
- require live lock denied;
- errno 13 is provisional until post-exit same-lock openability proves transient presentation-lifetime denial;
- run UI inspect/check;
- graceful exit;
- require zero WPF;
- require same lock read/write open succeeds;
- then allow lifecycle tail to continue.
- if zero WPF at continuation entry, allow one launch only to establish live state;
- more than one/wrong WPF => fail closed.

D. Lock safety:
- never truncate/write/alter lock bytes;
- prove unchanged bytes in regression fixture where applicable.

REQUIRED TESTS

Focused file must cover at least:
1. explicit winerror=32 full path PASS;
2. errno=13/no-winerror full path with valid differential proof PASS;
3. pre-live access denied FAIL;
4. continuation existing exact WPF + errno=13 + post-exit openable PASS;
5. continuation existing exact WPF + errno=13 + post-exit denied FAIL;
6. continuation zero-WPF uses only one launch;
7. live lock unexpectedly openable FAIL;
8. live lock missing FAIL;
9. unrelated OSError FAIL;
10. lock bytes unchanged;
11. duplicate/wrong-path/PID/current-pointer/UI/safe-state negatives preserved;
12. Worker/F1 remains NOT_APPLICABLE_PRE_G3;
13. no Worker/F1/tray fallback.

VALIDATION COMMANDS

Use only existing compatible Windows environment. Do not install/upgrade tools.

Run:
- python -m pytest -q agent_bridge/tests/test_lifecycle_wpf_contract.py
- python -m pytest -q agent_bridge/tests
- git diff --check

Also:
- changed-path allowlist;
- secret/privacy scan;
- K1 classifications for every material hunk:
  REQUESTED / NECESSARY_DEPENDENCY / JUSTIFIED_GENERATED / UNEXPLAINED
- require UNEXPLAINED=0.

RESULT CONTRACT

Authorized result paths:
- reports/FOX2-BRIDGE-RC1-TO-INTERNAL-READY/report.md
- reports/FOX2-BRIDGE-RC1-TO-INTERNAL-READY/evidence_manifest.json
- reports/FOX2-BRIDGE-RC1-TO-INTERNAL-READY/evidence/presentation_lock_certifier_rework_r2/**

Commit/push actual allowed code/test edits and result/evidence to the same authorized non-main branch.

Return observed remote result SHA outside committed report.

Result remains PUSHED_UNREVIEWED until CHAT result review.

STOP

STOP before editing if:
- immutable task/prompt/source/Dispatch binding differs;
- HEAD is not exact runtime base supplied by fresh Dispatch;
- worktree has unrelated WIP;
- another task-scoped writer exists;
- base blobs differ;
- correction requires any third product/test file;
- correction requires WPF product behavior change;
- host lifecycle action, package build or install is required;
- existing test environment is unavailable;
- permissions/model/reasoning differ;
- G3/G4/Canary/main/merge/provider/broker/LIVE would be touched.

STOP with truthful REWORK if required focused/full regression materially fails.

Historical A04 remains CLOSED_REWORK / FAIL.
Historical R1 remains SUPERSEDED_BEFORE_RUN.
