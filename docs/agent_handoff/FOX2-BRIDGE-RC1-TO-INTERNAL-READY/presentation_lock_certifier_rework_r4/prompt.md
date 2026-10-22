FOX2 — CODEX EXECUTION PROMPT — PRESENTATION LOCK CERTIFIER REWORK R4

Role: CODEX — bounded BUILD correction executor inside Bridge TEST stage
Model: gpt-6.1-sol
Thinking: medium
Project: FOX2 only
Repository: dunglt2505/FOX2
Branch: work/FOX2-BRIDGE-RC1-PRESENTATION-LOCK-CERTIFIER-REWORK-R4-20261022
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
- ROUTE_RATIONALE=bounded two-file external-certifier correction with known real-host failure and deterministic negative fixtures; no architecture redesign, package mutation or irreversible host action.

Selected route:
CODEX / gpt-6.1-sol / medium

IMMUTABLE TASK

Task ID:
FOX2-BRIDGE-RC1-PRESENTATION-LOCK-CERTIFIER-REWORK-R4

Task:
- path: docs/agent_handoff/FOX2-BRIDGE-RC1-TO-INTERNAL-READY/presentation_lock_certifier_rework_r4/task.md
- commit: 6b6cc697ca35b35ade1ccdf363782a1f912a8936
- blob: 90e6c18192cb594f408c9fd99b23da772e37c87f
- SHA-256: 54c2075c0cce6faa90c4f23292ebe43f90e28c356089f4cbbe1e245b9a257456

SOURCE LOCK

Exact accepted Bridge product source:
085cc8302e824dbccf9cbef80422ed48894b9cb4

Current certifier:
agent_bridge/scripts/certify_user_lifecycle.py
blob 7e62103ea4876833f67794a927a2a54622a59ea5

Current focused test:
agent_bridge/tests/test_lifecycle_wpf_contract.py
blob f80e50d59b1f1bb9ec9d553e84bbe7948971cb66

RECOVERY / NO-REPLAY

R3 A01 Dispatch:
FOX2-DISPATCH-BRIDGE-RC1-PRESENTATION-LOCK-CERTIFIER-REWORK-R3-CODEX-001

Final recovery:
3c32743e9b9cdcb7eb799094ee7bdefdaeb9aa71

Verdict:
CONSUMED_NO_RESULT / NO_REPLAY

Do not replay, relaunch, rebind or recover R3 A01.

R4 is a fresh attempt identity under the same Whole-WP.

PASS PRESERVATION

Reuse unaffected evidence:
- accepted current Bridge BUILD source;
- A04 package/provenance/install/safe-state/singleton PASS;
- R3 route assessment rationale;
- R3 schema-valid PreExec v4 host evidence as historical same-session capability evidence;
- reuse-first Master Plan and A04/A05 reuse plan.

Do not:
- rebuild A04 package;
- redo A04 provenance/hash work;
- install/update/uninstall/reinstall Bridge;
- launch/exit WPF for real host lifecycle;
- mutate Bridge host lifecycle;
- redo historical singleton proof;
- touch Worker/F1;
- open A05/G3/G4/Canary.

OBJECTIVE

Correct the external presentation-lock certification semantics exposed by the Owner-host Python 3.13 failure:

PermissionError: [Errno 13] Permission denied: BridgeDesktop/desktop.lock

Implement fail-closed differential proof without changing WPF product behavior.

REQUIRED IMPLEMENTATION

1. Bounded exception classification:
- record only exception class, errno, winerror and classification;
- explicit winerror=32 accepted;
- PermissionError errno=EACCES/13 accepted only under differential ownership proof;
- unrelated OSError fails closed;
- do not emit uncontrolled private path text.

2. Fresh full-certification path:
- pre-live existing lock must be read/write openable; absence allowed;
- pre-live denial => FAIL;
- preserve exact presentation/singleton/current-package checks;
- live lock must exist and be denied;
- winerror=32 accepted;
- errno=13 accepted only with pre-live accessibility + exact live identity;
- UI inspect/check;
- graceful exit;
- zero WPF;
- same lock becomes read/write openable;
- existing lifecycle tail remains.

3. A04 continuation mode for A05:
- explicit testable continuation mode/API/flag;
- one exact-current WPF live => do not relaunch merely to repeat singleton evidence;
- verify PID/path/current package;
- require lock exists and live open denied;
- winerror=32 accepted;
- errno=13 provisional until post-exit same-lock openability proves release;
- UI inspect/check;
- graceful exit;
- zero WPF;
- same lock openable;
- then continue lifecycle tail.
- zero WPF => one launch only;
- >1 or wrong WPF => fail closed.

4. Lock integrity:
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
- full path errno=13/no-winerror + differential proof PASS;
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

VALIDATION

Use existing compatible Windows environment only.
Do not install or upgrade tools.

Run:
python -m pytest -q agent_bridge/tests/test_lifecycle_wpf_contract.py

python -m pytest -q agent_bridge/tests

git diff --check

Also prove:
- exact changed-path allowlist;
- secret/privacy scan;
- K1 classification every material hunk:
  REQUESTED / NECESSARY_DEPENDENCY / JUSTIFIED_GENERATED / UNEXPLAINED
- require UNEXPLAINED=0.

RESULT PATHS

Code/test:
- agent_bridge/scripts/certify_user_lifecycle.py
- agent_bridge/tests/test_lifecycle_wpf_contract.py

Result:
- reports/FOX2-BRIDGE-RC1-TO-INTERNAL-READY/report.md
- reports/FOX2-BRIDGE-RC1-TO-INTERNAL-READY/evidence_manifest.json
- reports/FOX2-BRIDGE-RC1-TO-INTERNAL-READY/evidence/presentation_lock_certifier_rework_r4/**

Commit/push actual code/tests/result/evidence to the authorized non-main R4 branch.
Return observed remote result SHA outside committed report.
Result remains PUSHED_UNREVIEWED until CHAT result review.

STOP

STOP before edit if:
- task/prompt/Dispatch binding differs;
- selected route differs from CODEX / gpt-6.1-sol / medium;
- worktree dirty/wrong;
- competing task writer exists;
- source blobs differ;
- third product/test path required;
- WPF product behavior must change;
- package build/install/host lifecycle action required;
- tool installation/elevation required;
- focused/full regression materially fails;
- A05/G3/G4/Canary/main/merge/provider/broker/LIVE would be touched.

Historical R3 A01 is consumed/no-result/no-replay.
Historical PASS stays reusable.
Historical FAIL/NOT_RUN stays factual.
