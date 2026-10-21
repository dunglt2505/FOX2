FOX2 — CODEX EXECUTION PROMPT — PACKAGE LIFECYCLE A02

Role: CODEX — Primary implementation owner
Model: gpt-6.1-sol
Thinking: high
Mode: Execute bounded BUILD correction end-to-end
Project: FOX2 only
Repository: dunglt2505/FOX2
Branch: work/FOX2-BRIDGE-RC1-PACKAGE-LIFECYCLE-FIX-20261021
Permission profile: FULL_ACCESS within task allowlist only
Max Agent attempts: 1
No replay / no model substitution

FRESH ATTEMPT IDENTITY

Task ID:
FOX2-BRIDGE-RC1-PACKAGE-LIFECYCLE-A02

Planned fresh Dispatch ID:
FOX2-DISPATCH-BRIDGE-RC1-PACKAGE-LIFECYCLE-A02-CODEX-001

The prior A01 Dispatch/attempt is consumed and MUST NOT be replayed.

IMMUTABLE TASK

Path:
docs/agent_handoff/FOX2-BRIDGE-RC1-TO-INTERNAL-READY/package_lifecycle_fix_attempt02/task.md

Task commit:
fc03d7b130f0d987c94ecd6bb636ca482d9f637e

Task blob SHA-1:
4fc6c4eb80cf362ea2b9e4fc2082cc8f2e5e68dc

Task raw SHA-256:
3e9aca6b43485f9dcecf3ee72749e8c8c1b8ae4c4e31ef41eff5df5306acf4fd

OBJECTIVE

Correct the proven package-lifecycle certification harness defect:
the lifecycle harness currently invokes uninstall through the installed Python runtime, while the accepted product uninstall contract intentionally rejects self-deletion and requires the stable external BridgeRoot/uninstall.ps1 supervisor.

Do not redesign product uninstall.

Fix the certification harness to exercise the supported stable external supervisor, preserve bounded sanitized exit/stdout/stderr evidence, add regression coverage, run required tests, and publish code + Result Contract evidence.

CORRECT SOURCE / EXECUTION BINDING

PRODUCT_SOURCE_BASE:
b065a468279cbf63ae4bbfad7a0efaad1e6046e4

This SHA is the accepted product-code baseline. It is NOT the required current HEAD at process start.

EXECUTION_START_HEAD:
the exact value of the fresh executable Dispatch field:
runtime_contract.base_sha

The launcher MUST verify the exact fresh Dispatch before starting this CODEX process.

At your own preflight, before editing:

1. verify branch is exactly:
   work/FOX2-BRIDGE-RC1-PACKAGE-LIFECYCLE-FIX-20261021

2. verify current HEAD equals the fresh A02 executable Dispatch:
   runtime_contract.base_sha

3. verify PRODUCT_SOURCE_BASE b065a468279cbf63ae4bbfad7a0efaad1e6046e4 is an ancestor of current HEAD;

4. inspect the diff PRODUCT_SOURCE_BASE..HEAD and confirm pre-start changes are bounded to task/prompt/PreExec/review/governance evidence only, with no product implementation drift outside A02 allowed code/test/result paths;

5. DO NOT require current HEAD to equal PRODUCT_SOURCE_BASE.

If current HEAD differs from the fresh Dispatch runtime base, STOP.
If PRODUCT_SOURCE_BASE is not an ancestor, STOP.
If unexplained product-code drift is present before you start, STOP.

WHY THIS RULE EXISTS

A01 stopped safely because its old prompt incorrectly required HEAD=b065a468..., while its correct executable Dispatch required the later PreExec receipt head b224f029....

CHAT classified A01:
REWORK — ASSIGNMENT_BINDING_DEFECT / CONSUMED_SAFE_STOP / NO_PRODUCT_CHANGE

Review:
reports/FOX2-BRIDGE-RC1-TO-INTERNAL-READY/chat_reviews/PACKAGE_LIFECYCLE_A01_CONSUMED_SAFE_STOP_REVIEW_20261021.md
commit:
fff17cd828d9369af9cf36dc3892ce7412be7c65

Never replay A01.

SOURCE / AUTHORITY

Accepted product chain:
- implementation be883bb8106ca1c058b2b34765e55c2529fe883f
- product/result baseline b065a468279cbf63ae4bbfad7a0efaad1e6046e4
- CHAT acceptance 278daa5aff70b2e17a2bf3b563cbcd2585cd2f7f
- Phase-2 root-cause receipt adaa169b7e35861d35bbd5d2ecdab1ae2ec43dde

Governance:
- Registry/source release head d34da1e3b4918a902646621b487ca8ad3e05b0e0
- Policy 2.0.0 @ 96175ac4f39197794a04e695f0046fa7ef9321fe
- Dictionary 1.3 @ b25f7f728de67cf8595bf24f22fcbd79ef50babc
- Routing 1.4.0 @ bcd008983b61349646a5198ff243069f81484fae
- Git-first Protocol 12 @ f2a8bc8e6ce0785a800d78a3c384f205fdc5a6fa

TASK RULES

1. Read the actual current files before changing anything:
   - agent_bridge/scripts/certify_user_lifecycle.py
   - agent_bridge/src/fox2_agent_bridge/installation.py
   - agent_bridge/src/fox2_agent_bridge/__main__.py
   - relevant installation/package tests.

2. Keep installation.py and __main__.py unchanged unless a focused test proves the accepted product contract itself defective. If that happens, STOP and report; do not expand scope.

3. Replace lifecycle certification's installed-interpreter uninstall call with synchronous PowerShell 7 execution of stable external BridgeRoot/uninstall.ps1.

4. Do not use installed versions/<sha>/runtime/Scripts/python.exe for uninstall.

5. Capture bounded sanitized uninstall evidence:
   - stable external supervisor entrypoint identity/kind;
   - exit code;
   - stdout;
   - stderr;
   - post-uninstall current pointer/version absence;
   - durable config/data checks.

6. On non-zero uninstall:
   - persist bounded sanitized failure evidence;
   - stop immediately;
   - no retry;
   - no alternate entrypoint;
   - no hidden recovery.

7. Preserve historical Batch-B UNINSTALL_PATH=FAIL unchanged.

8. Do not perform real install/update/uninstall/reinstall on the Owner host in this coding task.

9. No AppLocker, AppIDSvc, Windows service, ProgramData ACL, reboot, G3/G4, Canary, main/PR/merge, provider/broker/LIVE actions.

ALLOWED CODE/TEST PATHS

- agent_bridge/scripts/certify_user_lifecycle.py
- agent_bridge/tests/test_installation.py
- agent_bridge/tests/test_rc1_package.py
- one new directly-related agent_bridge/tests/test_*lifecycle*.py only if strictly necessary

RESULT PATHS

- reports/FOX2-BRIDGE-RC1-TO-INTERNAL-READY/report.md
- reports/FOX2-BRIDGE-RC1-TO-INTERNAL-READY/evidence_manifest.json
- reports/FOX2-BRIDGE-RC1-TO-INTERNAL-READY/evidence/package_lifecycle_fix/**

TESTS / ACCEPTANCE

Must satisfy every acceptance item in task.md. At minimum:
- focused lifecycle/uninstall harness regressions PASS;
- existing installation/package regressions PASS;
- full agent_bridge/tests PASS;
- static syntax / PowerShell parsing where applicable PASS;
- changed-path allowlist PASS;
- git diff --check PASS;
- bounded secret scan PASS;
- K1 UNEXPLAINED=0;
- Result Contract v2 PASS;
- real lifecycle host execution remains NOT_RUN.

K1

Classify every material implementation hunk as:
REQUESTED / NECESSARY_DEPENDENCY / JUSTIFIED_GENERATED / UNEXPLAINED.

Required:
UNEXPLAINED=0

No drive-by refactor.

GIT DELIVERY

After tests:

1. commit only permitted code/tests;
2. create/update required report.md and evidence_manifest.json plus bounded evidence/package_lifecycle_fix/**;
3. commit result/evidence;
4. push only the authorized non-main task branch;
5. independently read remote branch head;
6. report observed remote result SHA outside committed report.

Do not claim CHAT acceptance.
Final status after successful push is PUSHED_UNREVIEWED.

STOP

STOP without edits/retry if:
- fresh A02 task/prompt/PreExec/Dispatch binding mismatches;
- current branch is wrong;
- current HEAD differs from fresh Dispatch runtime_contract.base_sha;
- PRODUCT_SOURCE_BASE is not an ancestor of current HEAD;
- unexplained pre-start product-code drift exists;
- unrelated WIP or competing task writer exists;
- change requires paths outside task allowlist;
- accepted product uninstall contract is shown defective;
- real host install/uninstall mutation is required;
- model/effort/permission differs;
- auth/quota/capacity fails after attempt consumption;
- protected operations are required;
- tests cannot pass without scope expansion.

Return a truthful result with FAIL/NOT_RUN preserved.
