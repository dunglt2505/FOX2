FOX2 — CODEX EXECUTION PROMPT — PRESENTATION LOCK CERTIFICATION REWORK A01

Role: CODEX — bounded BUILD correction executor
Model: gpt-6.1-sol
Thinking: high
Project: FOX2 only
Repository: dunglt2505/FOX2
Branch: work/FOX2-BRIDGE-RC1-PRESENTATION-LOCK-CERT-REWORK-A01-20261022
Permission profile: FULL_ACCESS bounded to this task
Max runs: 1
No model substitution
No replay of any historical Host Lifecycle Dispatch

TASK

Task ID:
FOX2-BRIDGE-RC1-PRESENTATION-LOCK-CERT-REWORK-A01

Immutable task:
- path: docs/agent_handoff/FOX2-BRIDGE-RC1-TO-INTERNAL-READY/presentation_lock_cert_rework_a01/task.md
- commit: ce72a539cbdc53a100a9c8b78d2bffe29726c15d
- blob: 8c54daf0b25f5322c92d1207831c7f5fac172e2a
- SHA-256: 05b8e571f1ba6557fb3898c14a9e23abf412f479adafa9e5f1bfd625a9e46b6f

SOURCE LOCK

Base / accepted BUILD source:
085cc8302e824dbccf9cbef80422ed48894b9cb4

CHAT prior BUILD acceptance:
cdf9f9c919102a2337ef357f4b658dc9993f48e5

A04 truthful result:
92394d0ae68911c98bcdaa40aaa76ed56de66881

CHAT A04 review:
a3e49a62dbd340eacd8dc8369aa303ed0e93b6f3

A04 Dispatch is permanently consumed and no-replay.

CURRENT CODE IDENTITIES

agent_bridge/scripts/certify_user_lifecycle.py
blob 7e62103ea4876833f67794a927a2a54622a59ea5

agent_bridge/tests/test_lifecycle_wpf_contract.py
blob f80e50d59b1f1bb9ec9d553e84bbe7948971cb66

OBJECTIVE

Correct only the Windows presentation-lock certification semantics exposed by A04.

The real Owner-host failure was:

PermissionError: [Errno 13] Permission denied: BridgeDesktop/desktop.lock

at certify_user_lifecycle.py line 157.

The WPF implementation itself uses FileAccess.ReadWrite + FileShare.None and is NOT in code scope.

Do not "fix" this by accepting every PermissionError.

Implement fail-closed differential proof:

1. Before presentation launch:
   - if desktop.lock exists, prove it is read/write openable;
   - if absent, absence is permitted;
   - pre-live access denial is a hard failure.

2. Preserve existing launch-twice exact singleton/current-package checks.

3. While exact WPF is live:
   - require lock exists;
   - probe same read/write open;
   - explicit sharing violation winerror=32 remains accepted;
   - PermissionError errno=EACCES/13 may be accepted as live held-lock only because pre-live access was not denied and exact live WPF identity has already been established;
   - unrelated OSError remains failure;
   - record bounded exception classification (type, errno, winerror), never private raw path content.

4. Preserve UI inspect/check, safe control, exact PID/path.

5. After explicit graceful exit + zero WPF:
   - require lock read/write open succeeds;
   - then mark lock release PASS.

6. Probe must not truncate/write/modify lock bytes.

ALLOWED CODE/TEST PATHS

Only:
- agent_bridge/scripts/certify_user_lifecycle.py
- agent_bridge/tests/test_lifecycle_wpf_contract.py

No WPF C# source edits.
No other product/test edits.
No drive-by refactor.

REQUIRED TEST COVERAGE

Focused test file must include cases for:

- real A04 shape: PermissionError(errno=13) with absent/None winerror under valid differential proof => PASS;
- explicit winerror=32 => PASS;
- persistent pre-live access denial => FAIL;
- live lock unexpectedly openable => FAIL;
- live lock missing => FAIL;
- lock retained/inaccessible after exit => FAIL;
- unrelated OSError => FAIL;
- lock bytes remain unchanged;
- existing duplicate/missing/wrong-path/pointer/PID/UI/safe-state negatives preserved;
- Worker/F1 remains NOT_APPLICABLE_PRE_G3 and no fallback added.

TESTS

Use the existing compatible Windows environment only. Do not install/upgrade tools.

Run:

python -m pytest -q agent_bridge/tests/test_lifecycle_wpf_contract.py

python -m pytest -q agent_bridge/tests

git diff --check

Record exact commands, exit codes and counts.

If the normal system Python is not the accepted compatible test interpreter, use the already-existing verified compatible interpreter from the FOX2 host and record its identity. Do not create a new environment.

K1

Every material code/test hunk must be classified:
REQUESTED / NECESSARY_DEPENDENCY / JUSTIFIED_GENERATED / UNEXPLAINED.

Require UNEXPLAINED=0.

RESULT WRITE SCOPE

Code/test:
- agent_bridge/scripts/certify_user_lifecycle.py
- agent_bridge/tests/test_lifecycle_wpf_contract.py

Result:
- reports/FOX2-BRIDGE-RC1-TO-INTERNAL-READY/report.md
- reports/FOX2-BRIDGE-RC1-TO-INTERNAL-READY/evidence_manifest.json
- reports/FOX2-BRIDGE-RC1-TO-INTERNAL-READY/evidence/presentation_lock_cert_rework_a01/**

Push actual code/tests/result to the authorized non-main branch.

Return observed remote result SHA outside committed report.

Result state is PUSHED_UNREVIEWED until CHAT result review.

PERMISSIONS

Code edits allowed only in the two explicit code/test paths.
Git code push allowed only on this authorized non-main branch.
Report/evidence write+push allowed.
No PR.
No merge.
No main.
No install/deploy.
No host package lifecycle.
No G3/G4/Canary.
No provider/broker/LIVE.
No force kill.
No WPF host mutation required by this BUILD task.

STOP

Stop before editing if:
- HEAD/source/task/prompt binding differs;
- worktree contains unrelated WIP;
- another task-scoped writer is active;
- task requires any third product/test path;
- evidence indicates the WPF implementation itself must change;
- existing tools/capability are unavailable;
- source lineage has drifted.

Stop after tests with truthful FAIL/REWORK if:
- focused or full regression fails materially;
- negative cases are weakened;
- source/test scope exceeds allowlist;
- K1 UNEXPLAINED != 0.

No consumed Dispatch may be replayed.
