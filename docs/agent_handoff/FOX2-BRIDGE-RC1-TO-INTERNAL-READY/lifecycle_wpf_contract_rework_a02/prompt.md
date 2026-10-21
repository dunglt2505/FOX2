FOX2 - CODEX EXECUTION PROMPT - LIFECYCLE/WPF CONTRACT REWORK A02

Role: CODEX - Primary source rework owner
Model: gpt-6.1-sol
Thinking: high
Mode: BUILD correction and verification only
Project: FOX2 only
Repository: dunglt2505/FOX2
Branch: work/FOX2-BRIDGE-RC1-LIFECYCLE-WPF-CONTRACT-REWORK-A02-20261022
Permission profile: FULL_ACCESS only within this task
Max Agent attempts for this assignment: 1

IMPORTANT ACTIVATION RULE

This prompt is published for immutable Git-first binding only.

DO NOT EXECUTE it merely because this file exists.

Execution is authorized only after CHAT publishes a fresh A02 Dispatch that binds this exact prompt and after a fresh route-specific PreExec proves current capability, authentication, quota/capacity, dedicated clean A02 worktree, one writer, and source/task/prompt identity.

Attempt A01/CODEX-001 is consumed and must never be replayed.

TASK

Task ID:
FOX2-BRIDGE-RC1-LIFECYCLE-WPF-CONTRACT-REWORK-A02

Task path:
docs/agent_handoff/FOX2-BRIDGE-RC1-TO-INTERNAL-READY/lifecycle_wpf_contract_rework_a02/task.md

Task commit:
f796306ca4e79b9ab61cd436cf69a5f28ede4faf

Task blob SHA-1:
3beb3bf2f3c2a76dcd8b10308f3670da98e70424

Task raw SHA-256:
7bfe425ad18f372960fb0440cd8694fb1a2a86edd7bd10cac5b105817f73d58c

WHOLE-WP

FOX2-BRIDGE-RC1-TO-INTERNAL-READY

IMMUTABLE SALVAGE SOURCE

Recovery snapshot:
1a11fa0b232a69f0c26a0b4029c331ee2a8c840f

Recovery parent/base:
e7d5acf51dddcbc95324a992ad6be2773e61285f

Recovery branch:
work/FOX2-BRIDGE-RC1-LIFECYCLE-WPF-CONTRACT-REWORK-A01-RECOVERY-CODEX001

Recovery provenance:
reports/FOX2-BRIDGE-RC1-TO-INTERNAL-READY/evidence/lifecycle_wpf_contract_rework/recovery_codex001_snapshot.json

The recovery provenance file is immutable and must remain byte-identical.

Attempt 001 facts are historical and non-negotiable:
- EXITED_CONSUMED
- exit code 1
- failure class CODEX_USAGE_LIMIT
- delivery NEEDS_RECONCILIATION
- no Git result
- no CHAT acceptance
- no replay

The recovery snapshot is salvage input, not an accepted result. Its provisional k1/static/source-binding artifacts are not PASS evidence for A02 unless A02 independently reruns the applicable verification and regenerates truthful evidence.

GOVERNANCE SOURCE SET

Use the Owner-approved current Governance set for new/re-scoped CHAT work:

Policy 2.0.0
- path: docs/governance/FOX2_POLICY_V2.0.0.md
- commit: 96175ac4f39197794a04e695f0046fa7ef9321fe
- blob: 2d373f374f906bf7959062050bbeae5350b0c482
- SHA-256: 281bcd61bb8c2fb7929ac474f218adbd004bbca6bc21e5311944a0e590723e1e

Project Dictionary 1.3
- path: docs/governance/FOX2_PROJECT_DICTIONARY_v1.3.json
- commit: b25f7f728de67cf8595bf24f22fcbd79ef50babc
- blob: 6c8f30e2e6b07f2e65e45c14faab99672d036083
- SHA-256: 8a64771916d9e3d447f560658e20b307b5945a5d6b3820ea61cd0298636abe1d

Routing Index 1.4.0
- path: docs/governance/FOX2_AGENT_PROMPT_POLICY_V1_4_0_OWNER_OVERRIDE_ROUTING_INDEX_20261019.md
- commit: bcd008983b61349646a5198ff243069f81484fae
- blob: 14d2e95e419cc67c3e0cf851cc806a96cf885b7e
- SHA-256: 5759b9a8d63ef165ef63c60ecc601198e39296518c5a1eb91db54555ccd07205

Git-first Protocol v12
- path: docs/agent_handoff/FOX2_GIT_FIRST_TASK_RESULT_PROTOCOL_v12.md
- commit: f2a8bc8e6ce0785a800d78a3c384f205fdc5a6fa
- blob: d34a022f2bda39a167a404c8530e57b30f337cb9

Bridge Technical Spec v0.7 REV10 remains CANDIDATE_NO_PROMOTION.

OBJECTIVE

Finish and independently verify the salvaged lifecycle/WPF contract rework.

The current accepted architecture remains:
- launcher.py is presentation-only;
- launcher.launch() remains worker_started=False;
- Worker/Agent belongs to protected F1 service;
- F1 adoption is later G3/G4;
- Phase-2 lifecycle must not manually start Worker/F1;
- WPF has its own presentation singleton/lock;
- certify_rc1_ui.ps1 is the existing UI automation seam;
- stable launch is BridgeRoot/launch.ps1;
- stable uninstall is BridgeRoot/uninstall.ps1.

Do not make presentation own the Worker.

SALVAGED IMPLEMENTATION REVIEW

At start, inspect every changed hunk inherited from snapshot 1a11fa0b232a69f0c26a0b4029c331ee2a8c840f.

Keep a salvaged hunk only if it is correct and required.

Do not rewrite correct code simply because A02 is a new attempt.

Fix defects, incomplete behavior, weak fixtures, incorrect assumptions, or incomplete evidence if found.

No salvaged PASS text is authoritative by itself.

REQUIRED PRODUCT/TEST SEMANTICS

Final implementation must prove through offline fixture/testing:

1. No dependency on desktop_tray.ps1, desktop_launcher.ps1 process health, or Worker heartbeat in Phase-2 WPF presentation certification.
2. Installed Desktop launch uses BridgeRoot/launch.ps1.
3. Two launches leave exactly one FOX2.Bridge.Desktop.exe.
4. Observed presentation is from the exact current installed package.
5. Control state requires paused=true, setup_complete=true and current_dispatch=null.
6. Worker/F1 health is NOT_APPLICABLE_PRE_G3 or equivalent, never PASS.
7. Existing certify_rc1_ui.ps1 is invoked for inspect, check and explicit exit.
8. inspect validates current WPF navigation and presentation identity.
9. check proves Check Now disabled while paused.
10. exit is explicit graceful WPF presentation exit before uninstall.
11. Presentation lock is observed held while live and released after exit.
12. Presentation count reaches zero within bounded timeout.
13. Safe stopped/paused state is rechecked after exit.
14. A03 stable external uninstall semantics remain unchanged in meaning.
15. Durable config/database/manual-consumption/historical consumed identity checks remain intact.
16. No real host lifecycle mutation occurs during A02 BUILD.

ALLOWED CODE PATHS

Only:
- agent_bridge/scripts/certify_user_lifecycle.py
- agent_bridge/tests/test_rc1_package.py
- agent_bridge/tests/test_rc1_launcher.py
- agent_bridge/tests/test_lifecycle_wpf_contract.py

FORBIDDEN SOURCE PATHS

Do not modify:
- agent_bridge/src/fox2_agent_bridge/launcher.py
- agent_bridge/src/fox2_agent_bridge/f1_service.py
- agent_bridge/src/fox2_agent_bridge/installation.py
- agent_bridge/scripts/certify_rc1_ui.ps1
- agent_bridge/desktop_app/**
- G3/AppLocker/service/ACL source
- unrelated application/backend/frontend code

If any forbidden source change is required, STOP with exact evidence.

HOST MUTATION PROHIBITED

Do not:
- install/update/uninstall/reinstall a real Owner-host package;
- launch the real installed FOX2.Bridge.Desktop.exe;
- change Task Scheduler;
- modify Bridge durable config/data/database;
- start Worker/F1;
- start or change AppLocker/AppIDSvc/service/ACL;
- reboot;
- run G3/G4/Canary;
- merge or write main;
- perform provider/broker/LIVE action.

RESULT/EVIDENCE PATHS

Allowed:
- reports/FOX2-BRIDGE-RC1-TO-INTERNAL-READY/report.md
- reports/FOX2-BRIDGE-RC1-TO-INTERNAL-READY/evidence_manifest.json
- reports/FOX2-BRIDGE-RC1-TO-INTERNAL-READY/evidence/lifecycle_wpf_contract_rework/**

MUST preserve byte-identically:
- reports/FOX2-BRIDGE-RC1-TO-INTERNAL-READY/evidence/lifecycle_wpf_contract_rework/recovery_codex001_snapshot.json

Existing provisional evidence helpers/artifacts may be corrected or regenerated only when supported by actual A02 execution.

TEST REQUIREMENTS

Run and preserve real outputs for:

1. focused lifecycle/WPF regression;
2. no legacy desktop_tray health dependency;
3. launch twice -> one WPF presentation fixture;
4. exact current package presentation identity;
5. paused/setup/no-current-dispatch;
6. certify_rc1_ui inspect/check/exit invocation;
7. graceful WPF exit before uninstall;
8. no Worker start / no heartbeat requirement;
9. Worker/F1 health NOT_APPLICABLE_PRE_G3;
10. no F1/G3 mutation;
11. stable external uninstall success;
12. uninstall nonzero/timeout/start/postcondition stop-once failures;
13. agent_bridge/tests/test_rc1_launcher.py;
14. installation/package suites;
15. full agent_bridge/tests;
16. Python syntax/static;
17. changed-path allowlist;
18. forbidden production files byte-identical to recovery parent/base as required by task;
19. git diff --check;
20. bounded secret scan;
21. K1 UNEXPLAINED=0;
22. Result Contract v2 schema validation and evidence hash readback.

If historical Git MAX_PATH behavior recurs, record the initial failure and use only the established process-only core.longpaths workaround. Do not alter repository/global Git configuration or tests to mask it.

K1

Classify every material final source/test hunk against the original runtime base and salvage source as:
- REQUESTED
- NECESSARY_DEPENDENCY
- JUSTIFIED_GENERATED

UNEXPLAINED must be 0.

Also distinguish:
- SALVAGED_UNCHANGED_FROM_A01
- A02_CORRECTION

inside evidence/report where useful, without changing the required K1 classification vocabulary.

RESULT CONTRACT

Produce and push:
- actual final implementation/tests;
- reports/FOX2-BRIDGE-RC1-TO-INTERNAL-READY/report.md;
- reports/FOX2-BRIDGE-RC1-TO-INTERNAL-READY/evidence_manifest.json;
- supporting evidence under the lifecycle evidence directory.

Result must conform to Dictionary-resolved Result Contract v2.

Return observed remote result SHA outside the committed report.

Do not claim CHAT acceptance.

PUSHED_UNREVIEWED is the maximum Agent completion state.

START GATES

At actual execution start, verify all conditions from the fresh A02 Dispatch.

At minimum:
- current branch is exact A02 branch;
- runtime base equals the fresh Dispatch base;
- recovery snapshot 1a11fa0b232a69f0c26a0b4029c331ee2a8c840f is an ancestor;
- task/prompt blobs and SHA-256 match the Dispatch;
- old Dispatch A01/CODEX-001 remains consumed/no-replay;
- no task-scoped competing writer exists;
- current CODEX authentication and quota/capacity are ready;
- dedicated A02 worktree is clean;
- no unrelated WIP;
- no product drift beyond explicitly bound A02 setup commits before Agent implementation begins.

STOP

STOP on:
- any replay of A01/CODEX-001;
- source/snapshot/task/prompt/Dispatch mismatch;
- quota/capacity/auth not ready;
- wrong worktree or branch;
- competing writer;
- unrelated WIP;
- forbidden path change required;
- real Owner-host lifecycle mutation required;
- Worker/F1 start required before G3;
- G3/G4/Canary action;
- main/PR/merge/provider/broker/LIVE;
- unrelated code changes;
- missing required real test/evidence output;
- Result Contract delivery failure.
