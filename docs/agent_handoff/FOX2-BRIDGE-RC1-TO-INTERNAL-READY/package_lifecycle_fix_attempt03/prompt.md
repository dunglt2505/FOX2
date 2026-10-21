FOX2 — CODEX EXECUTION PROMPT — PACKAGE LIFECYCLE A03

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

ATTEMPT IDENTITY

Task ID:
FOX2-BRIDGE-RC1-PACKAGE-LIFECYCLE-A03

Do not assume or hard-code a Dispatch sequence number.

The Owner launcher must supply and remote-verify one exact fresh executable Dispatch before this process starts. Treat that verified Dispatch as the only executable assignment identity.

A01 is consumed and MUST NOT be replayed.
Both published A02 Dispatches are NOT_EXECUTABLE and MUST NOT be used.

IMMUTABLE TASK

Path:
docs/agent_handoff/FOX2-BRIDGE-RC1-TO-INTERNAL-READY/package_lifecycle_fix_attempt03/task.md

Task commit:
ac12501e1b3c94a0e75b72adc7dc78743d18e660

Task blob SHA-1:
264c1bb54e985d8cd3a73df21072b04271b79d6c

Task raw SHA-256:
b6bbe42d781939a1b05b1dd2aa3fd985677d970b783ab8c2a30b11e9ada85c7e

OBJECTIVE

Correct the proven package-lifecycle certification harness defect.

The lifecycle harness currently invokes uninstall through the installed Python runtime. The accepted product contract intentionally rejects installed-interpreter self-deletion and requires the stable external BridgeRoot/uninstall.ps1 supervisor.

Do not redesign product uninstall.

Fix the certification harness to exercise the stable external supervisor, preserve bounded sanitized exit/stdout/stderr evidence, add focused regression coverage, run required tests, and publish code + Result Contract evidence.

SOURCE / EXECUTION BINDING

PRODUCT_SOURCE_BASE:
b065a468279cbf63ae4bbfad7a0efaad1e6046e4

This is the accepted product-code baseline. It is NOT the required current HEAD at process start.

EXECUTION_START_HEAD:
the exact runtime_contract.base_sha from the fresh executable Dispatch that the launcher remote-verified immediately before starting this process.

At your own preflight, before editing:

1. verify branch exactly:
   work/FOX2-BRIDGE-RC1-PACKAGE-LIFECYCLE-FIX-20261021

2. verify current HEAD equals the executable Dispatch runtime_contract.base_sha already verified by the launcher;

3. verify PRODUCT_SOURCE_BASE b065a468279cbf63ae4bbfad7a0efaad1e6046e4 is an ancestor of current HEAD;

4. inspect PRODUCT_SOURCE_BASE..HEAD and confirm all pre-start changes are bounded handoff, PreExec, review or receipt evidence, with no unexplained agent_bridge product-code drift;

5. verify clean worktree and one writer;

6. never require HEAD == PRODUCT_SOURCE_BASE;

7. never execute A01 or either A02 Dispatch.

If any binding is ambiguous, STOP before editing.

SOURCE / AUTHORITY

Accepted product chain:
- implementation be883bb8106ca1c058b2b34765e55c2529fe883f
- product/result baseline b065a468279cbf63ae4bbfad7a0efaad1e6046e4
- CHAT acceptance 278daa5aff70b2e17a2bf3b563cbcd2585cd2f7f
- Phase-2 root-cause receipt adaa169b7e35861d35bbd5d2ecdab1ae2ec43dde

Prior attempt reviews:
- A01 consumed safe-stop: fff17cd828d9369af9cf36dc3892ce7412be7c65
- A02 Dispatch001 schema rejection: 824406f8a5cd9bdccb412f2006b806b059c7308b
- A02 Dispatch002 prompt-binding rejection: 9f7cf7500d0124729c7eb6c3a758d918b6a727fa

Governance:
- Registry/source release head d34da1e3b4918a902646621b487ca8ad3e05b0e0
- Policy 2.0.0 @ 96175ac4f39197794a04e695f0046fa7ef9321fe
- Dictionary 1.3 @ b25f7f728de67cf8595bf24f22fcbd79ef50babc
- Routing 1.4.0 @ bcd008983b61349646a5198ff243069f81484fae
- Git-first Protocol 12 @ f2a8bc8e6ce0785a800d78a3c384f205fdc5a6fa

TASK RULES

1. Read current:
   - agent_bridge/scripts/certify_user_lifecycle.py
   - agent_bridge/src/fox2_agent_bridge/installation.py
   - agent_bridge/src/fox2_agent_bridge/__main__.py
   - relevant installation/package tests.

2. Keep installation.py and __main__.py unchanged unless a focused test proves the accepted product contract itself defective. If so, STOP and report.

3. Replace lifecycle certification installed-interpreter uninstall with synchronous PowerShell 7 execution of stable external BridgeRoot/uninstall.ps1.

4. Do not use installed versions/<sha>/runtime/Scripts/python.exe for uninstall.

5. Capture bounded sanitized uninstall evidence:
   - stable external supervisor identity/kind;
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

7. Preserve historical Batch-B UNINSTALL_PATH=FAIL.

8. Do not perform real install/update/uninstall/reinstall on Owner host.

9. No AppLocker, AppIDSvc, Windows service, ProgramData ACL, reboot, G3/G4, Canary, main/PR/merge, provider/broker/LIVE.

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

Must satisfy task.md. At minimum:
- focused lifecycle/uninstall regressions PASS;
- installation/package regressions PASS;
- full agent_bridge/tests PASS;
- static syntax / PowerShell parse as applicable PASS;
- changed-path allowlist PASS;
- git diff --check PASS;
- bounded secret scan PASS;
- K1 UNEXPLAINED=0;
- Result Contract v2 PASS;
- real host lifecycle remains NOT_RUN.

K1

Classify every material implementation hunk:
REQUESTED / NECESSARY_DEPENDENCY / JUSTIFIED_GENERATED / UNEXPLAINED.

Required:
UNEXPLAINED=0

No drive-by refactor.

GIT DELIVERY

After tests:
1. commit only permitted code/tests;
2. create/update report.md, evidence_manifest.json and bounded evidence/package_lifecycle_fix/**;
3. commit result/evidence;
4. push only authorized non-main task branch;
5. independently read remote branch head;
6. return observed remote result SHA outside committed report.

Do not claim CHAT acceptance.
Successful push remains PUSHED_UNREVIEWED.

STOP

STOP without edits or retry if:
- fresh A03 task/prompt/PreExec/executable Dispatch binding mismatches;
- current branch wrong;
- current HEAD differs from verified executable Dispatch runtime base;
- product source baseline is not an ancestor;
- unexplained pre-start agent_bridge code drift exists;
- unrelated WIP or competing writer exists;
- change requires paths outside allowlist;
- accepted product uninstall contract is shown defective;
- real host lifecycle mutation is required;
- model/effort/permission differs;
- auth/quota/capacity fails after attempt consumption;
- protected operations are required;
- tests cannot pass without scope expansion.

Return truthful FAIL/NOT_RUN boundaries.
