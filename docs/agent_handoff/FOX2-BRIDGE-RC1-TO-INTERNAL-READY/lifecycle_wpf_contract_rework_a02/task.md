# FOX2 - Lifecycle/WPF Contract Rework A02

Task ID: `FOX2-BRIDGE-RC1-LIFECYCLE-WPF-CONTRACT-REWORK-A02`
Whole-WP: `FOX2-BRIDGE-RC1-TO-INTERNAL-READY`
Stage: BUILD
Actor candidate: CODEX
Model: `gpt-6.1-sol`
Thinking: `high`
Execution path: `MANUAL_LOCAL`
Permission profile: `FULL_ACCESS`
Max Agent attempts for this fresh assignment: 1

## Purpose

Continue the same bounded lifecycle/WPF contract rework from the immutable recovery snapshot produced after CODEX Attempt 001 was consumed and stopped by usage quota.

This is a fresh assignment identity. It is NOT a replay of:

`FOX2-DISPATCH-BRIDGE-RC1-LIFECYCLE-WPF-CONTRACT-REWORK-A01-CODEX-001`

Attempt 001 remains immutable:

- state: `EXITED_CONSUMED`;
- result delivery: `NEEDS_RECONCILIATION`;
- replay: forbidden;
- Agent result: absent;
- CHAT acceptance: absent.

## Immutable recovery source

Recovery snapshot commit:

`1a11fa0b232a69f0c26a0b4029c331ee2a8c840f`

Recovery branch:

`work/FOX2-BRIDGE-RC1-LIFECYCLE-WPF-CONTRACT-REWORK-A01-RECOVERY-CODEX001`

Recovery parent/base:

`e7d5acf51dddcbc95324a992ad6be2773e61285f`

Recovery provenance:

`reports/FOX2-BRIDGE-RC1-TO-INTERNAL-READY/evidence/lifecycle_wpf_contract_rework/recovery_codex001_snapshot.json`

Recovery metadata states:

- `snapshot_is_agent_result=false`;
- `chat_accepted=false`;
- `result_contract_complete=false`;
- `tests=NOT_VERIFIED`;
- `k1=NOT_VERIFIED`;
- `static_checks=NOT_VERIFIED`;
- `real_host_lifecycle=NOT_RUN`;
- `g3_allowed=false`.

The recovery snapshot is salvage input only. Any PASS-like text or JSON created by Attempt 001 is provisional and must not be reused as proof unless A02 independently reruns and records the applicable check.

## Current governance/source resolution

Live readback on the Owner-approved Governance release branch resolves:

- Policy 2.0.0:
  - path `docs/governance/FOX2_POLICY_V2.0.0.md`
  - commit `96175ac4f39197794a04e695f0046fa7ef9321fe`
  - blob `2d373f374f906bf7959062050bbeae5350b0c482`
  - SHA-256 `281bcd61bb8c2fb7929ac474f218adbd004bbca6bc21e5311944a0e590723e1e`
- Project Dictionary 1.3:
  - path `docs/governance/FOX2_PROJECT_DICTIONARY_v1.3.json`
  - commit `b25f7f728de67cf8595bf24f22fcbd79ef50babc`
  - blob `6c8f30e2e6b07f2e65e45c14faab99672d036083`
  - SHA-256 `8a64771916d9e3d447f560658e20b307b5945a5d6b3820ea61cd0298636abe1d`
- Routing Index 1.4.0:
  - path `docs/governance/FOX2_AGENT_PROMPT_POLICY_V1_4_0_OWNER_OVERRIDE_ROUTING_INDEX_20261019.md`
  - commit `bcd008983b61349646a5198ff243069f81484fae`
  - blob `14d2e95e419cc67c3e0cf851cc806a96cf885b7e`
  - SHA-256 `5759b9a8d63ef165ef63c60ecc601198e39296518c5a1eb91db54555ccd07205`
- Git-first Task/Result Protocol v12:
  - path `docs/agent_handoff/FOX2_GIT_FIRST_TASK_RESULT_PROTOCOL_v12.md`
  - commit `f2a8bc8e6ce0785a800d78a3c384f205fdc5a6fa`
  - blob `d34a022f2bda39a167a404c8530e57b30f337cb9`

Bridge Technical Spec v0.7 REV10 remains `CANDIDATE_NO_PROMOTION`.

These governance sources do not grant merge, provider, broker, Canary or LIVE permission.

## A02 branch

Fresh A02 branch:

`work/FOX2-BRIDGE-RC1-LIFECYCLE-WPF-CONTRACT-REWORK-A02-20261022`

The branch was created from exact recovery snapshot `1a11fa0b232a69f0c26a0b4029c331ee2a8c840f`.

The product/test/evidence bytes from that snapshot are the starting salvage state. A02 must preserve ancestry to the snapshot and must not silently reconstruct Attempt 001 from local WIP.

## Goal

Finish, correct where necessary, independently verify, and deliver the lifecycle/WPF contract rework so Phase-2 lifecycle certification matches the accepted presentation-only WPF architecture without moving Worker/F1 ownership into the presentation lifecycle.

Do not redo already-salvaged implementation merely for cosmetic reasons. Review every salvaged hunk, keep it only if correct, and change only what is necessary to satisfy this task and tests.

## Required semantics

The final source must:

1. Remove legacy `desktop_tray.ps1` / tray-process / Worker-heartbeat assumptions from Phase-2 lifecycle certification.
2. Launch installed WPF through stable `BridgeRoot/launch.ps1`.
3. Prove launch twice leaves exactly one `FOX2.Bridge.Desktop.exe` presentation belonging to the exact installed package.
4. Require paused=true, setup_complete=true and no current dispatch; make no Worker/F1 health PASS claim.
5. Record Worker/F1 health as `NOT_APPLICABLE_PRE_G3` or equivalent.
6. Reuse existing `agent_bridge/scripts/certify_rc1_ui.ps1` for `inspect`, `check`, and explicit graceful `exit`.
7. Prove live presentation lock while WPF is running, explicit graceful exit, zero presentation processes after bounded wait, and lock release before uninstall.
8. Preserve accepted A03 stable external uninstall semantics and durable-state preservation.
9. Preserve presentation-only launcher/F1 ownership architecture byte-identically on forbidden production paths.
10. Perform no real Owner-host install/update/uninstall/reinstall/WPF launch/Worker/F1/G3/G4/Canary mutation during this BUILD task.

## Salvaged files requiring review

Snapshot changed product/test files:

- `agent_bridge/scripts/certify_user_lifecycle.py`
- `agent_bridge/tests/test_rc1_package.py`
- `agent_bridge/tests/test_lifecycle_wpf_contract.py`

Snapshot also contains provisional evidence helpers/artifacts under:

`reports/FOX2-BRIDGE-RC1-TO-INTERNAL-READY/evidence/lifecycle_wpf_contract_rework/**`

The following recovery provenance file is immutable and MUST NOT be changed:

`reports/FOX2-BRIDGE-RC1-TO-INTERNAL-READY/evidence/lifecycle_wpf_contract_rework/recovery_codex001_snapshot.json`

Any other provisional evidence file may be regenerated/replaced only by real A02 checks.

## Allowed code paths

Only:

- `agent_bridge/scripts/certify_user_lifecycle.py`
- `agent_bridge/tests/test_rc1_package.py`
- `agent_bridge/tests/test_rc1_launcher.py`
- `agent_bridge/tests/test_lifecycle_wpf_contract.py`

No other product/source path is authorized.

## Forbidden source changes

Do not modify:

- `agent_bridge/src/fox2_agent_bridge/launcher.py`
- `agent_bridge/src/fox2_agent_bridge/f1_service.py`
- `agent_bridge/src/fox2_agent_bridge/installation.py`
- `agent_bridge/scripts/certify_rc1_ui.ps1`
- `agent_bridge/desktop_app/**`
- G3/AppLocker/service/ACL source
- unrelated application/backend/frontend code

If a forbidden path change is necessary, STOP and report the incompatibility.

## Allowed result paths

- `reports/FOX2-BRIDGE-RC1-TO-INTERNAL-READY/report.md`
- `reports/FOX2-BRIDGE-RC1-TO-INTERNAL-READY/evidence_manifest.json`
- `reports/FOX2-BRIDGE-RC1-TO-INTERNAL-READY/evidence/lifecycle_wpf_contract_rework/**`

Preserve the A01 recovery provenance JSON byte-identically.

## Host mutation boundary

Offline BUILD/rework only.

Do not:

- install/update/uninstall/reinstall a real Owner-host package;
- launch the real installed WPF Desktop;
- mutate Task Scheduler;
- mutate Bridge durable host data;
- start Worker/F1;
- touch AppLocker/AppIDSvc/service/ACL;
- reboot;
- run G3/G4/Canary;
- merge or write main;
- access provider/broker/LIVE.

## Required verification

A02 must independently run and preserve real output for at least:

1. focused WPF lifecycle tests;
2. no legacy desktop-tray health dependency;
3. launch twice -> one WPF presentation fixture;
4. exact-current-package presentation identity fixture;
5. paused/setup/no-current-dispatch fixture;
6. UI inspect/check/exit invocation fixture;
7. graceful WPF exit before uninstall fixture;
8. no Worker start / heartbeat requirement;
9. Worker/F1 health explicitly not applicable pre-G3;
10. no F1/G3 mutation;
11. stable uninstall success;
12. uninstall nonzero/timeout/start/postcondition stop-once regressions;
13. `test_rc1_launcher.py`;
14. installation/package tests;
15. full `agent_bridge/tests`;
16. Python syntax/static checks;
17. changed-path allowlist;
18. forbidden-file byte identity;
19. `git diff --check`;
20. bounded secret scan;
21. K1 with `UNEXPLAINED=0`;
22. Result Contract v2 schema plus evidence hash readback.

Historical environment-specific MAX_PATH behavior, if encountered, must be recorded truthfully and may use only the established process-only workaround. Do not change repository/global Git configuration or tests to hide it.

## K1

Every material source/test hunk must map to one of:

- REQUESTED
- NECESSARY_DEPENDENCY
- JUSTIFIED_GENERATED

No drive-by refactor. `UNEXPLAINED=0` is required.

## Result delivery

Push only to the authorized fresh A02 non-main branch.

Deliver:

- final code/test changes within allowed paths;
- `reports/FOX2-BRIDGE-RC1-TO-INTERNAL-READY/report.md`;
- `reports/FOX2-BRIDGE-RC1-TO-INTERNAL-READY/evidence_manifest.json`;
- real A02 evidence under the allowed lifecycle evidence directory.

Return the observed remote result SHA outside the committed report.

Final Agent state is `PUSHED_UNREVIEWED` until CHAT independently performs result review.

## Execution gate

This task/prompt may be published before execution readiness.

Do NOT execute A02 until a fresh route-specific PreExec proves current capability, authentication, quota/capacity, clean dedicated A02 worktree, one writer, exact task/prompt bytes and source/snapshot binding, followed by a fresh Dispatch A02.

Known current blocker at task preparation time: CODEX Attempt 001 ended because the account hit its usage limit. No quota PASS may be inferred from the old successful start.

## STOP

STOP on:

- any attempt to replay Dispatch A01/CODEX-001;
- recovery snapshot ancestry mismatch;
- task/prompt/source/branch drift;
- current quota/capacity not ready;
- competing writer or dirty unrelated worktree;
- forbidden path change needed;
- real host lifecycle mutation needed;
- Worker/F1 start required before G3;
- unrelated code change;
- missing real test/evidence output;
- Result Contract delivery failure;
- main/PR/merge/provider/broker/LIVE;
- G3/G4/Canary action.
