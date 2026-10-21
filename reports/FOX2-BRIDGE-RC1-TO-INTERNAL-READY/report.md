# FOX2 G2 Integrated F1 Build A01 — Agent result

## R01 — Identification and disposition

Project/WP/task/change: FOX2 / FOX2-BRIDGE-RC1-TO-INTERNAL-READY / FOX2-BRIDGE-RC1-G2-A01 / G2-F1-INTEGRATED-A01.
CODEX `gpt-6.1-sol`, reasoning `high`, MANUAL_LOCAL, FULL_ACCESS technical sandbox. Active turn context observed at 2026-10-21T03:31:22.526Z; host: Windows-11-10.0.26300-SP0. One implementation attempt, no Dispatch/Agent retry or model substitution. Usage NOT_MEASURED.

Disposition at report assembly: LOCAL_ONLY, with G2 source/build checks completed for independent CHAT review after actual push. No self-acceptance. F1 Owner-host runtime remains DENY; G3/G4 enforcement is NOT_RUN_G3. This result does not establish INTERNAL_FOX2_BRIDGE_READY.

## R02 — Authority and PreExec

The full immutable task was read before implementation. The exact G2 PreExec at `preexec/g2_preflight.json` was PASS at 2026-10-21T03:27:17.603284+00:00, with pinned CODEX/model/high/FULL_ACCESS, this non-main worktree, NONE_OBSERVED writer competition, and all three dispatch/start flags false. Active session metadata independently confirmed the model, high effort, danger-full-access and approval=never. Other active thread metadata used the project-chat workspace; no competing G2 material writer was observed.

Scoped Owner G2 hold-lift and accepted G1 design are controlling. Policy 2.0.0, Dictionary 1.3, Routing 1.4.0 and Protocol 12 bytes were checked against the task's pinned commits/blobs. Bridge machine Dictionary 1.2 compatibility remains only the separately published scoped receipt. BRD-09/TechSpec remain globally candidate; neither is promoted to EFFECTIVE. Scope and routing checks are PASS for this task only. No STOP condition was bypassed.

## R03 — Exact immutable inputs and SHAs

- Start SHA: `94c936b1d93bbfcee5818db24dd75bd9bb32733f`.
- Task publication: `653e49fc0d0f15981bf230995925c89d6994723d`; blob `7f0b82e56f7bfa001e40bb176bb26b0ef918c609`.
- Task base/Owner scoped grant: `fe926ad24d89231e5cf80f0f48ea44eb36887834`.
- PreExec source head: `ca684b09b3eaea7fa2ce7fc7983f890384202296`; task bytes equal publication bytes; this source is an ancestor of the start SHA.
- Final implementation SHA: `66e8f0a8b3a93140b5f908628b55ac965e15b96e`. The final result/report commit containing this document cannot self-reference its own SHA; its observed remote SHA is supplied outside the committed report after push.
- Source/authority distinctions and full path/commit/blob/SHA-256 observations: `evidence/g2/source_readback.json`.

## R04 — Implemented behavior and limits

Implemented a LocalSystem/SCM-only Windows authority boundary, explicit-DACL local named pipe, OS-derived caller identity/token/session/PID, fixed protected global store, boot epoch fencing, durable claim and one-use spawn intent, service-owned suspended CreateProcessAsUser/Job creation and guarded resumption, lease/revoke/clock/policy/service/source/package checks, and idempotent informational outcomes. Revocation durably tombstones the sealed adoption-plan digest, so restart/rollback cannot reactivate an unchanged plan. No client bearer launch token or caller-side installed spawn fallback exists.

Launcher starts only presentation; ledger retains installed direct-claim denial and now closes installed alternate-database and pre-spawn bypasses. Installed/configured E2E delegates before local creation/claim/adapters; Ops/Desktop/App use that runner. Installed smoke requires a staged service task. Existing offline reconciliation and F0 primitives remain in use. Runtime/SCM configuration drift or missing bindings deny; failed revocation storage still closes jobs.

Deterministic AppLocker artifact support enforces EXE/Script/MSI/DLL collections, uses exact hashes/SID scopes, closes copied legacy fixtures without path trust, includes service/system extensions, and distinguishes raw versus AppLocker hashes. Unsupported Python-source rules fail: interpreter identity must be fenced. Packaging includes F1 modules and read-only inventory support with DENY_PENDING_G3_G4. No new product dependency was introduced.

Details, protected-plan contract, explicit 60-second lease bound, interpreter constraints, operational limits and primary API references are in `evidence/g2/implementation_notes.md`. The actual full offline user-package build is NOT_RUN: no provisioned isolated setuptools/build/wheel environment was present. Package/source contract tests and static checks ran; no release package was fabricated. A real non-elevated Windows desktop build ran separately.

## R05 — Changed paths and K1

Every material hunk is classified in `evidence/g2/k1.json`; UNEXPLAINED=0. New source/test files are entirely REQUESTED. Fixture-name shortening is NECESSARY_DEPENDENCY for this exact long Windows path. Result receipts are JUSTIFIED_GENERATED. No governance/BRD/TechSpec or unrelated engine edit occurred.

| Path | K1 classification |
|---|---|
| `agent_bridge/scripts/build_user_package.py` | REQUESTED |
| `agent_bridge/scripts/f1_inventory.ps1` | REQUESTED |
| `agent_bridge/scripts/f1_policy_artifact.py` | REQUESTED |
| `agent_bridge/src/fox2_agent_bridge/app.py` | REQUESTED |
| `agent_bridge/src/fox2_agent_bridge/desktop.py` | REQUESTED |
| `agent_bridge/src/fox2_agent_bridge/e2e_runner.py` | REQUESTED |
| `agent_bridge/src/fox2_agent_bridge/f1_authority.py` | REQUESTED |
| `agent_bridge/src/fox2_agent_bridge/f1_broker_store.py` | REQUESTED |
| `agent_bridge/src/fox2_agent_bridge/f1_client.py` | REQUESTED |
| `agent_bridge/src/fox2_agent_bridge/f1_policy.py` | REQUESTED |
| `agent_bridge/src/fox2_agent_bridge/f1_protocol.py` | REQUESTED |
| `agent_bridge/src/fox2_agent_bridge/f1_service.py` | REQUESTED |
| `agent_bridge/src/fox2_agent_bridge/f1_windows.py` | REQUESTED |
| `agent_bridge/src/fox2_agent_bridge/installation.py` | REQUESTED |
| `agent_bridge/src/fox2_agent_bridge/launcher.py` | REQUESTED |
| `agent_bridge/src/fox2_agent_bridge/ledger.py` | REQUESTED |
| `agent_bridge/src/fox2_agent_bridge/startup.py` | REQUESTED |
| `agent_bridge/tests/test_f1_authority.py` | REQUESTED |
| `agent_bridge/tests/test_f1_consumers.py` | REQUESTED |
| `agent_bridge/tests/test_f1_host_fence.py` | REQUESTED |
| `agent_bridge/tests/test_f1_policy.py` | REQUESTED |
| `agent_bridge/tests/test_f1_windows.py` | REQUESTED |
| `agent_bridge/tests/test_installation.py` | NECESSARY_DEPENDENCY |
| `agent_bridge/tests/test_rc1_launcher.py` | REQUESTED |
| `reports/FOX2-BRIDGE-RC1-TO-INTERNAL-READY/evidence/g2/capture_command_inventory.py` | NECESSARY_DEPENDENCY |
| `reports/FOX2-BRIDGE-RC1-TO-INTERNAL-READY/evidence/g2/command_inventory.json` | JUSTIFIED_GENERATED |
| `reports/FOX2-BRIDGE-RC1-TO-INTERNAL-READY/evidence/g2/delivery_checks.json` | JUSTIFIED_GENERATED |
| `reports/FOX2-BRIDGE-RC1-TO-INTERNAL-READY/evidence/g2/desktop-build-01.json` | JUSTIFIED_GENERATED |
| `reports/FOX2-BRIDGE-RC1-TO-INTERNAL-READY/evidence/g2/desktop-build-02.json` | JUSTIFIED_GENERATED |
| `reports/FOX2-BRIDGE-RC1-TO-INTERNAL-READY/evidence/g2/focused-01.json` | JUSTIFIED_GENERATED |
| `reports/FOX2-BRIDGE-RC1-TO-INTERNAL-READY/evidence/g2/focused-02.json` | JUSTIFIED_GENERATED |
| `reports/FOX2-BRIDGE-RC1-TO-INTERNAL-READY/evidence/g2/focused-03.json` | JUSTIFIED_GENERATED |
| `reports/FOX2-BRIDGE-RC1-TO-INTERNAL-READY/evidence/g2/focused-04.json` | JUSTIFIED_GENERATED |
| `reports/FOX2-BRIDGE-RC1-TO-INTERNAL-READY/evidence/g2/full-01.json` | JUSTIFIED_GENERATED |
| `reports/FOX2-BRIDGE-RC1-TO-INTERNAL-READY/evidence/g2/full-02.json` | JUSTIFIED_GENERATED |
| `reports/FOX2-BRIDGE-RC1-TO-INTERNAL-READY/evidence/g2/full-03.json` | JUSTIFIED_GENERATED |
| `reports/FOX2-BRIDGE-RC1-TO-INTERNAL-READY/evidence/g2/implementation_notes.md` | NECESSARY_DEPENDENCY |
| `reports/FOX2-BRIDGE-RC1-TO-INTERNAL-READY/evidence/g2/k1.json` | JUSTIFIED_GENERATED |
| `reports/FOX2-BRIDGE-RC1-TO-INTERNAL-READY/evidence/g2/preexec_diagnostic.json` | JUSTIFIED_GENERATED |
| `reports/FOX2-BRIDGE-RC1-TO-INTERNAL-READY/evidence/g2/prepare_result.py` | NECESSARY_DEPENDENCY |
| `reports/FOX2-BRIDGE-RC1-TO-INTERNAL-READY/evidence/g2/regression-01.json` | JUSTIFIED_GENERATED |
| `reports/FOX2-BRIDGE-RC1-TO-INTERNAL-READY/evidence/g2/regression-02.json` | JUSTIFIED_GENERATED |
| `reports/FOX2-BRIDGE-RC1-TO-INTERNAL-READY/evidence/g2/regression-03.json` | JUSTIFIED_GENERATED |
| `reports/FOX2-BRIDGE-RC1-TO-INTERNAL-READY/evidence/g2/regression-04.json` | JUSTIFIED_GENERATED |
| `reports/FOX2-BRIDGE-RC1-TO-INTERNAL-READY/evidence/g2/regression-05.json` | JUSTIFIED_GENERATED |
| `reports/FOX2-BRIDGE-RC1-TO-INTERNAL-READY/evidence/g2/regression-06.json` | JUSTIFIED_GENERATED |
| `reports/FOX2-BRIDGE-RC1-TO-INTERNAL-READY/evidence/g2/result_preparation_diagnostic.json` | JUSTIFIED_GENERATED |
| `reports/FOX2-BRIDGE-RC1-TO-INTERNAL-READY/evidence/g2/run_checks.py` | NECESSARY_DEPENDENCY |
| `reports/FOX2-BRIDGE-RC1-TO-INTERNAL-READY/evidence/g2/source_readback.json` | JUSTIFIED_GENERATED |
| `reports/FOX2-BRIDGE-RC1-TO-INTERNAL-READY/evidence/g2/source_readback.py` | NECESSARY_DEPENDENCY |
| `reports/FOX2-BRIDGE-RC1-TO-INTERNAL-READY/evidence/g2/static-01.json` | JUSTIFIED_GENERATED |
| `reports/FOX2-BRIDGE-RC1-TO-INTERNAL-READY/evidence/g2/static-02.json` | JUSTIFIED_GENERATED |
| `reports/FOX2-BRIDGE-RC1-TO-INTERNAL-READY/evidence/g2/static-03.json` | JUSTIFIED_GENERATED |
| `reports/FOX2-BRIDGE-RC1-TO-INTERNAL-READY/evidence/g2/static_checks.py` | NECESSARY_DEPENDENCY |
| `reports/FOX2-BRIDGE-RC1-TO-INTERNAL-READY/evidence/g2/validate_result.py` | NECESSARY_DEPENDENCY |
| `reports/FOX2-BRIDGE-RC1-TO-INTERNAL-READY/evidence/g2/windows-01.json` | JUSTIFIED_GENERATED |
| `reports/FOX2-BRIDGE-RC1-TO-INTERNAL-READY/evidence/g2/windows-02.json` | JUSTIFIED_GENERATED |
| `reports/FOX2-BRIDGE-RC1-TO-INTERNAL-READY/evidence_manifest.json` | JUSTIFIED_GENERATED |
| `reports/FOX2-BRIDGE-RC1-TO-INTERNAL-READY/report.md` | REQUESTED |

`ops_runner.py` and `f1_reconcile.py` were inspected and reused unchanged: Ops calls the gated runner; reconciliation keeps WAL/SHM/missing-root/overlap HOLD behavior. `install_user.ps1` has no service/policy activation path added.

## R06 — Commands actually run

Final checks: 61 passed in 2.47s; 200 passed in 13.14s; 557 passed in 208.24s (0:03:28); 3 passed in 0.51s.
Required final order: focused → affected regression → full supported suite → static/package contract → native Windows tests → Windows build. Exact bounded commands, UTC start/end, exit codes and output tails are in each JSON receipt. Every earlier failed run remains recorded; no historical CI substituted for new source tests.

| Receipt | Exit | Result | Summary |
|---|---:|---|---|
| `desktop-build-01.json` | 0 | PASS | Time Elapsed 00:00:04.56 |
| `desktop-build-02.json` | 0 | PASS | Time Elapsed 00:00:00.97 |
| `focused-01.json` | 0 | PASS | 48 passed in 2.10s |
| `focused-02.json` | 0 | PASS | 51 passed in 2.04s |
| `focused-03.json` | 0 | PASS | 60 passed in 2.38s |
| `focused-04.json` | 0 | PASS | 61 passed in 2.47s |
| `full-01.json` | 1 | FAIL | 26 failed, 518 passed in 181.63s (0:03:01) |
| `full-02.json` | 0 | PASS | 556 passed in 217.79s (0:03:37) |
| `full-03.json` | 0 | PASS | 557 passed in 208.24s (0:03:28) |
| `regression-01.json` | 1 | FAIL | 7 failed, 193 passed in 13.72s |
| `regression-02.json` | 1 | FAIL | 1 failed, 199 passed in 13.85s |
| `regression-03.json` | 0 | PASS | 200 passed in 14.06s |
| `regression-04.json` | 0 | PASS | 200 passed in 15.51s |
| `regression-05.json` | 0 | PASS | 200 passed in 14.16s |
| `regression-06.json` | 0 | PASS | 200 passed in 13.14s |
| `static-01.json` | 0 | PASS | {"syntax": "PASS", "allowlist": "PASS", "diff_check": "PASS", "powershell_scripts_parsed": 2, "wheel_source_contract_modules": 40, "actual_offline_package_build": "NOT_RUN_NO_ISOLATED_BUILD_ENV", "effective_policy_mutation": false, "service_install_start": false} |
| `static-02.json` | 0 | PASS | {"syntax": "PASS", "allowlist": "PASS", "diff_check": "PASS", "powershell_scripts_parsed": 2, "wheel_source_contract_modules": 40, "actual_offline_package_build": "NOT_RUN_NO_ISOLATED_BUILD_ENV", "effective_policy_mutation": false, "service_install_start": false} |
| `static-03.json` | 0 | PASS | {"syntax": "PASS", "allowlist": "PASS", "diff_check": "PASS", "powershell_scripts_parsed": 2, "wheel_source_contract_modules": 40, "actual_offline_package_build": "NOT_RUN_NO_ISOLATED_BUILD_ENV", "effective_policy_mutation": false, "service_install_start": false} |
| `windows-01.json` | 0 | PASS | 3 passed in 0.50s |
| `windows-02.json` | 0 | PASS | 3 passed in 0.51s |

Earlier installation failures were Windows MAX_PATH in fixture paths; extended-path spelling then failed PowerShell script authorization, so the fixture uses a shorter unique name in the same directory. The first full run exposed Git `show commit:path` MAX_PATH in unchanged PreExec fixtures and a missing Utility module import in the new inventory helper. Git core.longpaths is now per-test-child only; no host Git setting changed. The helper imports fixed Windows module paths. Read-only diagnostics are retained in `preexec_diagnostic.json`.

## R07 — Security/replay/concurrency acceptance

| Requirement | G2 result | Evidence |
|---|---|---|
| Service absent, AppIDSvc/policy unavailable/drift, SCM/runtime drift → DENY | PASS (source plus native absence/ACL/pipe tests) | final focused, native Windows |
| Forged caller/task/source/package/actor/nonce/epoch → DENY | PASS | focused protocol/authority |
| Same dispatch concurrency, global consumed identity | PASS: 32 concurrent requests, one service creation/consumed identity | focused authority; existing broker regressions |
| Claim/intent before creation; ambiguous spawn consumed | PASS | focused persisted-intent assertions |
| Restart/revoke/lease expiry/clock rollback; durable heartbeat floor | PASS | focused authority/store |
| Launcher/Desktop/App/Ops/E2E cannot bypass service | PASS | focused consumers; regression |
| Copied legacy/current identity and interpreter-SID artifact model | PASS (model only) | focused policy |
| WAL/SHM/missing roots/manual overlap and frozen F0 negatives | PASS | affected/full suites |
| Rollback primitive revokes and preserves consumed/tombstones | PASS (source fixture); installed rollback NOT_RUN_G3 | focused authority |
| Changed scripts/module packaging/non-activation/allowlist | PASS | static/package contract |
| Effective AppLocker/LocalSystem spawn/Owner-host installation | NOT_RUN_G3 | intentionally outside G2 |

## R08 — Evidence inventory

`evidence_manifest.json` follows Result Schema v2 and contains evidence paths, raw SHA-256, command statuses and acceptance links. Evidence is bounded to `evidence/g2/`. Failure receipts contain synthetic test diagnostics and ordinary local paths, without real credentials or account tokens. Source readback is byte proof plus the supplied scoped task authority, not a global release certificate.

## R09 — Git delivery

Repository `dunglt2505/FOX2`; branch `work/FOX2-BRIDGE-F1-G2-INTEGRATED-BUILD-20261021`; exact worktree `C:\Projects\FOX2-worktrees\FOX2-BRIDGE-F1-G2-INTEGRATED-BUILD-20261021`. Code and report publication owner is AGENT. At report assembly the result is LOCAL_ONLY. After actual push and remote SHA readback the external pointer is PUSHED_UNREVIEWED. No PR, merge, main write or self-acceptance.

## R10 — Host-only gaps and boundaries

All elevated/host enforcement tests are NOT_RUN_G3: effective AppLocker deployment and full OS/dependency inventory; copied/interpreter/shell/DLL bypass closure on Windows; LocalSystem child creation with real user credentials; service crash/reboot/logoff and lifetime behavior; protected-root attack probes; installed rollback/reinstall; G4 Owner-host adoption. Source/native non-elevated tests are not enforcement certification.

Confirmed for this attempt: no AppLocker policy installed/applied; no authority service installed or started; no elevation; no scheduled-task mutation; no main/merge/deploy/provider/trading-broker/Canary/LIVE action. F1 positive Owner-host authority remains DENY. The service's protected state is independent of per-user uninstall; privileged G3 rollback must revoke authority and retain the broker store, not delete or recreate consumption.

## R11 — Attempt accounting

A01 implementation attempts=1; Dispatch retries=0. Internal test/fix/recheck cycles are recorded above and are not Agent replays. No paid Agent readiness probe, nested implementation Agent or model substitution was launched by this implementation session. Tokens/credits NOT_MEASURED.

## R12 — CHAT intake

Requested decision: independent REVIEW through fox2-result-review against the immutable remote result commit and Dictionary-bound intake v9. G2 source/build review is separate from G3/G4 host authorization. Do not self-accept, enable positive host execution, merge or run Canary from this result.
