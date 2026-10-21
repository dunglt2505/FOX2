FOX2 — CODEX EXECUTION PROMPT — LIFECYCLE/WPF CONTRACT REWORK A01

Role: CODEX — Primary source rework owner
Model: gpt-6.1-sol
Thinking: high
Mode: BUILD correction only
Project: FOX2 only
Repository: dunglt2505/FOX2
Branch: work/FOX2-BRIDGE-RC1-LIFECYCLE-WPF-CONTRACT-REWORK-20261022
Permission profile: FULL_ACCESS only within this task
Max Agent attempts: 1
No replay / no model substitution

TASK ID

FOX2-BRIDGE-RC1-LIFECYCLE-WPF-CONTRACT-REWORK-A01

IMMUTABLE TASK

Path:
docs/agent_handoff/FOX2-BRIDGE-RC1-TO-INTERNAL-READY/lifecycle_wpf_contract_rework/task.md

Task commit:
aabe81fad8a465ea12a763fd4cccc54670dd707f

Task blob SHA-1:
e6503c2a817450f270ab674ce1cd723019961dce

Task raw SHA-256:
50bf03fc9fdb149dd7b4d0a3edf4bd2acbc26ec0000f39208b17b9d2f7bc2b01

SOURCE / FAILURE BINDING

Branch base / failed host-cert result:
9dd91becf47d934183baf147d0a4f03f4bf5933d

Unchanged accepted product source under that result:
2faa33f9ab4d06bcc51c8fd1d2c7040fc06a29cb

CHAT_REWORK receipt:
1f3a07ea76485cb1b175d90a4303d9997b66e047

Do not replay:
FOX2-DISPATCH-BRIDGE-RC1-HOST-LIFECYCLE-CERT-A01-CODEX-001

EXECUTION START

At actual CODEX start:
- current HEAD must equal the fresh executable Dispatch runtime_contract.base_sha;
- 9dd91becf47d934183baf147d0a4f03f4bf5933d must be an ancestor;
- product changes after 9dd91bec... before Agent start are forbidden;
- only this task/prompt/PreExec/Dispatch binding evidence may precede the implementation start;
- no competing material writer may exist.

Do not hard-code a future Dispatch sequence in source or evidence.

OBJECTIVE

Correct the stale Phase-2 user lifecycle certification seam that expects legacy desktop_tray.ps1 + Worker heartbeat even though the accepted current runtime intentionally separates WPF presentation from protected Worker/F1 execution.

Preserve current architecture. Do not make the WPF launcher start the Worker.

AUTHORITATIVE IMPLEMENTATION CONTRACT

Treat the following as controlling for this bounded rework:

1. agent_bridge/src/fox2_agent_bridge/launcher.py is presentation-only.
2. launcher.launch() remains worker_started=False.
3. agent_bridge/tests/test_rc1_launcher.py explicitly states:
   "Launcher creates presentation only; Worker/Agent require the F1 service."
4. F1 service/adoption belongs to later G3/G4.
5. Phase-2 must not start Worker/F1 manually or infer F1 health.
6. WPF singleton/presentation lock in App.xaml.cs remains unchanged.
7. Existing agent_bridge/scripts/certify_rc1_ui.ps1 is the installed UI automation seam.
8. Stable installed launch path is BridgeRoot/launch.ps1.
9. Stable uninstall path is BridgeRoot/uninstall.ps1.

Bridge TechSpec v0.7 REV10 remains CANDIDATE_NO_PROMOTION and does not override this accepted implementation contract.

IMPLEMENTATION REQUIREMENTS

Modify the minimum source/test surface.

A. Remove stale legacy-tray assumptions from certify_user_lifecycle.py:
- no desktop_tray.ps1 process-count requirement;
- no pwsh tray identity requirement;
- no Worker heartbeat requirement caused by WPF launch;
- no direct "python -m fox2_agent_bridge worker" singleton test in pre-G3 lifecycle;
- no Worker/F1 PASS claim.

B. Launch current installed Desktop through BridgeRoot/launch.ps1.
- launch twice;
- prove exactly one FOX2.Bridge.Desktop.exe presentation;
- prove the observed presentation belongs to the current exact package;
- prove control remains paused/setup_complete/no current dispatch;
- record Worker/F1 as NOT_APPLICABLE_PRE_G3 or equivalent.

C. Reuse certify_rc1_ui.ps1.
- inspect current WPF navigation;
- check must prove Check Now is disabled while paused;
- exit must trigger explicit graceful WPF presentation exit before uninstall.
Do not duplicate UIAutomation implementation.

D. Before uninstall:
- WPF presentation must be observed live;
- perform explicit UI exit;
- wait boundedly for WPF presentation count zero;
- verify presentation lock released;
- verify Bridge control remains safe;
- do not force-kill WPF.

E. Preserve A03 stable uninstall semantics byte-for-byte in meaning:
- stable external BridgeRoot/uninstall.ps1;
- PowerShell 7;
- synchronous;
- installed Python never uninstalls itself;
- bounded/redacted stdout/stderr;
- one uninstall attempt;
- failure checkpoint before reinstall;
- no retry/alternate path;
- exact-package reinstall only after successful uninstall.

F. Preserve durable-state checks and historical consumed identities.

EXISTING REUSABLE REFERENCE

agent_bridge/scripts/certify_rc1_installed.py already demonstrates:
- BridgeRoot/launch.ps1;
- FOX2.Bridge.Desktop process counting;
- certify_rc1_ui.ps1 inspect/check/exit;
- live presentation lock behavior;
- explicit UI exit;
- stable external uninstall;
- durable preservation;
- exact-package reinstall.

Reuse the contract, not copy large duplicate logic unnecessarily.

ALLOWED CODE PATHS

Only:
- agent_bridge/scripts/certify_user_lifecycle.py
- agent_bridge/tests/test_rc1_package.py
- agent_bridge/tests/test_rc1_launcher.py
- at most one new focused test file under agent_bridge/tests/ dedicated to this WPF/lifecycle seam

REPORT/EVIDENCE:
- reports/FOX2-BRIDGE-RC1-TO-INTERNAL-READY/report.md
- reports/FOX2-BRIDGE-RC1-TO-INTERNAL-READY/evidence_manifest.json
- reports/FOX2-BRIDGE-RC1-TO-INTERNAL-READY/evidence/lifecycle_wpf_contract_rework/**

FORBIDDEN CODE PATHS

Do not modify:
- agent_bridge/src/fox2_agent_bridge/launcher.py
- agent_bridge/src/fox2_agent_bridge/f1_service.py
- agent_bridge/desktop_app/**
- agent_bridge/scripts/certify_rc1_ui.ps1
- agent_bridge/src/fox2_agent_bridge/installation.py
- G3/AppLocker/service/ACL code
- any application/backend/frontend code

If a forbidden source change appears necessary, STOP with evidence. Do not expand scope.

HOST MUTATION PROHIBITED

This task is offline BUILD correction only.

Do not:
- build/install/update/uninstall/reinstall a real Owner-host package;
- launch real installed FOX2.Bridge.Desktop.exe;
- change Task Scheduler;
- change Bridge config/data/database;
- start Worker/F1 service;
- mutate AppLocker/AppIDSvc/service/ACL;
- reboot;
- run G3/G4/Canary.

TEST REQUIREMENTS

Run and preserve real outputs for:
1. focused WPF lifecycle regression;
2. no legacy desktop_tray dependency;
3. launch twice -> one WPF presentation fixture;
4. exact current package presentation identity fixture;
5. paused/setup/no-current-dispatch fixture;
6. certify_rc1_ui inspect/check/exit invocation fixture;
7. graceful UI exit before uninstall fixture;
8. no Worker start / no heartbeat requirement fixture;
9. no F1/G3 mutation fixture;
10. stable uninstall success;
11. stable uninstall nonzero/timeout/start/postcondition failure stop-once cases;
12. agent_bridge/tests/test_rc1_launcher.py;
13. installation/package suites;
14. full agent_bridge/tests;
15. Python syntax/static;
16. changed-path allowlist;
17. git diff --check;
18. bounded secret scan;
19. K1 UNEXPLAINED=0;
20. Result Contract v2.

If full-suite Git MAX_PATH behavior recurs, preserve the initial FAIL and use only the already-established process-only core.longpaths method; do not modify repository/global Git config or tests to hide it.

K1

Every changed source/test hunk must classify as:
- REQUESTED
- NECESSARY_DEPENDENCY
- JUSTIFIED_GENERATED

No drive-by refactor. UNEXPLAINED must be 0.

PRODUCT SEMANTICS THAT MUST REMAIN UNCHANGED

- WPF presentation-only launcher.
- Worker/F1 ownership.
- F1 activation remains DENY_PENDING_G3_G4.
- first-run paused semantics.
- stable external uninstall contract.
- durable config/data/manual-consumption preservation.
- no replay of consumed Dispatches.

RESULT DELIVERY

Push actual implementation + tests + report/evidence to this authorized non-main branch.

Required:
- reports/FOX2-BRIDGE-RC1-TO-INTERNAL-READY/report.md
- reports/FOX2-BRIDGE-RC1-TO-INTERNAL-READY/evidence_manifest.json
- evidence/lifecycle_wpf_contract_rework/**

Return observed remote result SHA outside the committed report.

Do not claim CHAT acceptance.
Submission remains PUSHED_UNREVIEWED.

STOP

STOP on:
- branch/source/task/prompt/Dispatch drift;
- competing writer;
- CODEX route/model/permission mismatch;
- forbidden-path change needed;
- real host mutation needed;
- Worker/F1 start needed before G3;
- G3/G4/Canary action;
- unrelated source change;
- main/PR/merge/provider/broker/LIVE;
- Result Contract delivery failure.

The consumed host-lifecycle A01 Dispatch is historical no-replay and must not be reused.
