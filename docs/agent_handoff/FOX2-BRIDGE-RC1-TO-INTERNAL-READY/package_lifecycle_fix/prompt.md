FOX2 — CODEX EXECUTION PROMPT

Role: CODEX — Primary implementation owner
Model: gpt-6.1-sol
Thinking: high
Mode: Execute bounded BUILD correction end-to-end
Project: FOX2 only
Repository: dunglt2505/FOX2
Branch: work/FOX2-BRIDGE-RC1-PACKAGE-LIFECYCLE-FIX-20261021
Exact starting base: b065a468279cbf63ae4bbfad7a0efaad1e6046e4
Permission profile: FULL_ACCESS within task allowlist only
Max Agent attempts: 1
No replay / no model substitution

IMMUTABLE TASK
Path:
docs/agent_handoff/FOX2-BRIDGE-RC1-TO-INTERNAL-READY/package_lifecycle_fix/task.md

Task commit:
31caeb95ceb6d50644722527252f714a4406ab97

Task blob SHA-1:
4fa3356f3d6a362a8af8cbc7340288a13a451835

Task raw SHA-256:
c2270f33db37b39f6296abeac86dd3e572309258918bab5d878454895a034811

OBJECTIVE

Correct the proven package-lifecycle certification harness defect:
the harness currently invokes uninstall through the installed Python runtime, while the accepted product uninstall contract intentionally rejects self-deletion and requires the stable external BridgeRoot/uninstall.ps1 supervisor.

Do not redesign uninstall. Fix the certification harness to exercise the supported stable supervisor, preserve bounded sanitized exit/stdout/stderr evidence, add regression coverage, run required tests, and publish code + Result Contract evidence.

SOURCE / AUTHORITY

Use the exact source set and root-cause evidence bound in task.md.

Accepted immediate source:
- same-host implementation be883bb8106ca1c058b2b34765e55c2529fe883f
- same-host result/evidence b065a468279cbf63ae4bbfad7a0efaad1e6046e4
- CHAT acceptance 278daa5aff70b2e17a2bf3b563cbcd2585cd2f7f
- Phase-2 root-cause receipt adaa169b7e35861d35bbd5d2ecdab1ae2ec43dde

Governance:
- Registry/source release head d34da1e3b4918a902646621b487ca8ad3e05b0e0
- Policy 2.0.0 @ 96175ac4f39197794a04e695f0046fa7ef9321fe
- Dictionary 1.3 @ b25f7f728de67cf8595bf24f22fcbd79ef50babc
- Routing 1.4.0 @ bcd008983b61349646a5198ff243069f81484fae
- Git-first Protocol 12 @ f2a8bc8e6ce0785a800d78a3c384f205fdc5a6fa

TASK RULES

1. Verify exact branch, base SHA, immutable task bytes, clean worktree, one writer and current route before editing.
2. Read the actual current files before changing anything:
   - agent_bridge/scripts/certify_user_lifecycle.py
   - agent_bridge/src/fox2_agent_bridge/installation.py
   - agent_bridge/src/fox2_agent_bridge/__main__.py
   - relevant installation/package tests.
3. Keep installation.py / __main__.py unchanged unless a focused test proves the accepted product contract itself is defective. If that happens, STOP and report; do not expand scope silently.
4. Replace lifecycle certification's installed-interpreter uninstall call with synchronous PowerShell 7 execution of the stable external BridgeRoot/uninstall.ps1.
5. Capture bounded sanitized uninstall evidence:
   - entrypoint identity/kind
   - exit code
   - stdout
   - stderr
   - post-uninstall current pointer/version absence
   - durable config/data checks
6. On non-zero uninstall: preserve bounded sanitized failure evidence and stop immediately. No retry, alternate entrypoint or hidden recovery.
7. Preserve historical Batch-B UNINSTALL_PATH=FAIL unchanged.
8. Do not perform a real install/update/uninstall/reinstall on the Owner host in this coding task.
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

Classify every material hunk as:
REQUESTED / NECESSARY_DEPENDENCY / JUSTIFIED_GENERATED / UNEXPLAINED.
Required UNEXPLAINED=0. No drive-by refactor.

GIT DELIVERY

After tests:
1. commit permitted code/tests;
2. create/update the required report.md and evidence_manifest.json plus bounded evidence/package_lifecycle_fix/**;
3. commit result/evidence;
4. push only this authorized non-main branch;
5. independently read the remote branch head;
6. report the observed remote result SHA outside committed report.

Do not claim CHAT acceptance. Final status after a successful push is PUSHED_UNREVIEWED.

STOP

STOP without further edits or retry if:
- source/task/prompt binding mismatches;
- branch/base drift exists before execution;
- unrelated WIP or competing task writer exists;
- the change requires paths outside task allowlist;
- the accepted product uninstall contract is itself shown defective;
- real host install/uninstall mutation is required;
- model/effort/permission differs;
- auth/quota/capacity fails after attempt consumption;
- protected operations are required;
- tests cannot pass without scope expansion.

Return a truthful result with any FAIL/NOT_RUN preserved.
