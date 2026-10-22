FOX2 — CODEX EXECUTION PROMPT — PRESENTATION LOCK CERTIFIER REWORK R3

Role: CODEX — bounded BUILD correction executor inside Bridge TEST stage
Model: gpt-6.1-sol
Thinking: medium
Project: FOX2 only
Repository: dunglt2505/FOX2
Branch: work/FOX2-BRIDGE-RC1-PRESENTATION-LOCK-CERTIFIER-REWORK-R3-20261022
Permission profile: FULL_ACCESS bounded to exact task
Max runs: 1
No model substitution
No effort substitution
No historical Dispatch replay

TASK_ROUTE_ASSESSMENT

- COMPLEXITY=MEDIUM
- ambiguity=LOW_MEDIUM
- EXECUTION_RISK=MEDIUM
- SAFETY_OVERRIDE=NO
- dependency impact=MEDIUM_HIGH
- evidence quality=HIGH
- ROUTE_RATIONALE=bounded two-file external-certifier correction with known real-host failure and deterministic negative fixtures; no architecture redesign, package mutation, or irreversible host action.

Selected route:
CODEX / gpt-6.1-sol / medium

PreExec must verify this selected route. It must not upgrade/downgrade thinking, infer complexity, or swap actor/model.

IMMUTABLE TASK

Task ID:
FOX2-BRIDGE-RC1-PRESENTATION-LOCK-CERTIFIER-REWORK-R3

Task:
- path: docs/agent_handoff/FOX2-BRIDGE-RC1-TO-INTERNAL-READY/presentation_lock_certifier_rework_r3/task.md
- commit: c5b8ccef94fc222bc2626209c74c074b827269f3
- blob: e66f8fc39add4024de3b242771d171e9b6b5bec3
- SHA-256: 4dde2215f4095f26caa00bb6c0254cfb421d3d5d21086e5c1b6769b197acec5e

SOURCE LOCK

Exact accepted Bridge product source:
085cc8302e824dbccf9cbef80422ed48894b9cb4

Current certifier:
agent_bridge/scripts/certify_user_lifecycle.py
blob 7e62103ea4876833f67794a927a2a54622a59ea5

Current focused test:
agent_bridge/tests/test_lifecycle_wpf_contract.py
blob f80e50d59b1f1bb9ec9d553e84bbe7948971cb66

CONTROLLING EVIDENCE

Master Plan reuse-first directive:
ad7d6f0b9889fe4247c29ac3d77f0b90b5f40e56

Reuse plan:
da6fd27d78380db42fce155d634044c94a661229

Skills v0.3.7 Bridge reassessment:
7cee0933ffd241deaa8e748bfeb626c56fab0cd0

Feature Status v0.3.7 correction:
55751ebb52d4b4e4eed92ad7b8966b07b31a523c

A04 result:
92394d0ae68911c98bcdaa40aaa76ed56de66881

A04 CHAT review:
a3e49a62dbd340eacd8dc8369aa303ed0e93b6f3

A04 runtime package subject remains unchanged:
f99c7add1b99bad938d977f634fd8a88e20763f5e35aaadf5cfe3072a1a327ee
from source:
085cc8302e824dbccf9cbef80422ed48894b9cb4

SUPERSEDED — DO NOT RUN / DO NOT REPLAY

R1 PreExec:
4d0ae5636ac91969c2a15416f8f0bd50d581d180

R2-High task/prompt/PreExec:
9e1551d4e8e10aff3d302034c3f0c06588eac9ca
f6da01e9729b441ca80aece34ac282dd8195b12a
da869f7171eb3e970e766ed3f8ff9100cfa316b0

Both are superseded-before-run with no receipt, no Dispatch and no Agent start.

PASS PRESERVATION

A04 accepted PASS is reusable. Do NOT:
- rebuild A04 package;
- redo package provenance/hash work;
- install/update/uninstall/reinstall Bridge;
- launch/exit WPF;
- mutate host lifecycle;
- redo singleton certification;
- touch Worker/F1;
- enable G3/G4/Canary.

R3 only corrects the external certifier and focused test.

OBJECTIVE

Fix presentation-lock certification semantics exposed by real Owner-host Python 3.13:

PermissionError: [Errno 13] Permission denied: BridgeDesktop/desktop.lock

Current implementation accepts live denial only when winerror == 32.

Implement fail-closed differential proof.

REQUIRED IMPLEMENTATION

1. Bounded exception classification
- record only exception class, errno, winerror and classification;
- explicit winerror=32 remains accepted;
- PermissionError errno=EACCES/13 may be accepted only when differential ownership proof exists;
- unrelated OSError remains failure;
- do not emit uncontrolled private path text.

2. Fresh full-certification path
- pre-live existing lock must be read/write openable; absence permitted;
- pre-live access denied => FAIL;
- exact presentation + existing singleton/current-package checks remain;
- live lock must exist and be denied;
- winerror=32 accepted;
- errno=13 accepted only with pre-live accessibility + exact live identity;
- UI inspect/check;
- graceful exit;
- zero WPF;
- same lock must become read/write openable;
- existing lifecycle tail remains.

3. A04 continuation mode for future A05
- expose explicit testable continuation mode/API/flag;
- if one exact-current WPF is live, do not relaunch merely to repeat singleton evidence;
- verify exact PID/path/current package;
- require live lock exists and live open is denied;
- winerror=32 accepted;
- errno=13 is provisional transient-live evidence;
- UI inspect/check;
- graceful exit;
- zero WPF;
- same lock read/write open must succeed;
- only then finalize provisional errno=13 as PRESENTATION_LOCK_HELD;
- continue lifecycle tail.
- if zero WPF exists, allow one launch only to establish live state;
- >1 WPF or wrong WPF => fail closed.

4. Lock integrity
- never truncate/write/modify lock bytes.

ALLOWED CODE/TEST PATHS — EXACTLY TWO

1. agent_bridge/scripts/certify_user_lifecycle.py
2. agent_bridge/tests/test_lifecycle_wpf_contract.py

No third product/test path.
No WPF C# source.
No drive-by refactor.

REQUIRED TEST COVERAGE

At minimum:
- full path winerror=32 PASS;
- full path errno=13/no-winerror + valid differential proof PASS;
- pre-live access denied FAIL;
- continuation existing exact WPF + errno=13 + post-exit openable PASS;
- continuation existing exact WPF + errno=13 + post-exit denied FAIL;
- continuation zero-WPF performs one launch only;
- live lock unexpectedly openable FAIL;
- live lock missing FAIL;
- unrelated OSError FAIL;
- lock bytes unchanged;
- duplicate/wrong-path/PID/current-pointer/UI/safe-state negatives preserved;
- Worker/F1 remains NOT_APPLICABLE_PRE_G3;
- no Worker/F1/tray fallback.

Do not weaken existing negative fixtures.

VALIDATION

Use existing compatible Windows environment only. Do not install or upgrade tools.

Run:
python -m pytest -q agent_bridge/tests/test_lifecycle_wpf_contract.py

python -m pytest -q agent_bridge/tests

git diff --check

Also prove:
- exact changed-path allowlist;
- secret/privacy scan;
- K1 classification for every material hunk:
  REQUESTED / NECESSARY_DEPENDENCY / JUSTIFIED_GENERATED / UNEXPLAINED
- require UNEXPLAINED=0.

RESULT PATHS

Code/test:
- agent_bridge/scripts/certify_user_lifecycle.py
- agent_bridge/tests/test_lifecycle_wpf_contract.py

Result:
- reports/FOX2-BRIDGE-RC1-TO-INTERNAL-READY/report.md
- reports/FOX2-BRIDGE-RC1-TO-INTERNAL-READY/evidence_manifest.json
- reports/FOX2-BRIDGE-RC1-TO-INTERNAL-READY/evidence/presentation_lock_certifier_rework_r3/**

Commit/push actual code/tests/result/evidence to the authorized non-main R3 branch.

Return observed remote result SHA outside the committed report.

Result remains PUSHED_UNREVIEWED until CHAT result review.

PERMISSIONS / STOP

Allowed:
- code edits only in the two exact code/test paths;
- result/evidence write/push only in exact result paths;
- Git push only to authorized R3 non-main branch.

Not allowed:
- package build;
- Bridge install/update/uninstall/reinstall;
- WPF host mutation;
- Worker/F1;
- G3/G4/Canary;
- PR/merge/main;
- provider/broker/LIVE.

STOP if:
- task/prompt/source/Dispatch binding differs;
- selected route differs from CODEX / gpt-6.1-sol / medium;
- worktree dirty/wrong;
- competing task writer exists;
- source blobs differ;
- third product/test path is required;
- WPF product behavior must change;
- package/host lifecycle action is required;
- tool installation/elevation is required;
- required focused/full regression materially fails.

Historical PASS stays reusable.
Historical FAIL/NOT_RUN stays factual.
