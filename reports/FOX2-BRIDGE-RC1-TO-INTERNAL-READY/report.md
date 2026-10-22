# FOX2 A04 owner-host lifecycle certification — FAIL / REWORK_REQUIRED

## R01 — Identification and submission

FOX2 / FOX2-BRIDGE-RC1-TO-INTERNAL-READY / FOX2-BRIDGE-RC1-HOST-LIFECYCLE-CERT-A04. TEST on the Owner Windows host, CODEX gpt-6.1-sol / high / MANUAL_LOCAL / FULL_ACCESS. One Agent attempt, no substitution or replay. Started 2026-10-22T06:11:53Z; report UTC 2026-10-22T06:22:34.815393+00:00. Submission: READY_FOR_CHAT_REVIEW; delivery: PUSHED_UNREVIEWED after actual publication. **The lifecycle result is FAIL, not PASS.**

## R02 — Authority, routing and grants

Owner instruction, fetched A04 Dispatch `533712e930a5cf937fa9401add0a89baa4994615`, CHAT PASS_TO_ASSIGN `fa8bfb6ee4e8fd6c3649d4ddd36243c07c43b23a` and PreExec/runtime base `6d1d2a70f2d1cc47e44f70a0ba6cd07cd3985713` independently verified. All envelope, source, route, PreExec, one-writer and permissions gates passed (E_GATE/E_GOV/E_BASELINE). Current A04 CODEX PID 11960 matches the consumed launcher claim; no second task writer observed. Controlling permissions: code_allowed=false, git_code_push=false; report write/push=true. Legacy decision_receipt.code_allowed=YES is schema compatibility only, as explicitly bounded by the Dispatch. Policy 2.0.0 scoped human operating authority is distinct from installed machine adoption. No wider release or trading authority.

## R03 — Immutable source and package provenance

Task commit `8fdc2f7181e7f3e9a7f56ea72472fe3d2d2cea43`, task blob `50d77f3039d2a8f9ce40105457da8e18b639289d`, task SHA-256 `397e179c63666ce611e2c03cfb988ccbd9290a72b9643014fe1ff0588bfb7aa8`. Prompt commit `43abc5a8a988d93e3ccdd09b72f14fa4feae4d24`; SHA-256 `5ed59d6fe681ffdd15cc2e41cf88ac2a478717499f7d1b8e7812259be44ca5ef`.

Accepted product source `085cc8302e824dbccf9cbef80422ed48894b9cb4`; CHAT BUILD acceptance `cdf9f9c919102a2337ef357f4b658dc9993f48e5`. Clean orchestration worktree had no product drift. Package used the separate detached `WORKTREES/FOX2-BRIDGE-RC1-PACKAGE-SOURCE-085CC830-A04`, exact accepted HEAD, same repository, clean before/after build. Builder blob `2417212e5677a2061e3957544a99e2ba80f46f4d`, raw bytes exact; read-only source_git_commit() pre-probe returned the accepted commit. No source/environment/manifest override.

One build, exit 0. Package `ARTIFACTS/host_lifecycle_cert_a04/FOX2-Bridge-085cc830-A04.zip`, outside BridgeRoot and both Git worktrees, survives uninstall; not committed. SHA-256 `f99c7add1b99bad938d977f634fd8a88e20763f5e35aaadf5cfe3072a1a327ee`. Manifest source_git_commit is exactly accepted source; source inventory hash `6d76f99ce9fcc62bbcf9f2450a45bc920c28b2fd70828353c0a8fea096c5de73`. All 59 source-file, 40 wheel-module and 255 payload hashes passed. Package intentionally retains generated machine Dictionary 1.2 / `7fc3532890f4a60a4abc7bf3b08dc06fe6af6ee000176ac464bfe3aacda2ecd7` from accepted product bytes; human governance Dictionary 1.3 is separately resolved. Existing isolated Python 3.13 / setuptools 84.0.0 / wheel 0.48.0 / dotnet 8.0.426 used; no host build-tool installation.

Historical A03 Dispatch remains consumed; A03 result `883ea51a429baf6749fa3fd412cc9ebb044f6efc` and CHAT review `eced60bc22e7294bf49b367791c122ad91a97f43` remain untouched. No historical PASS substitutes for this execution.

## R04 — Completed and first failure

Fresh A04 baseline captured before lifecycle mutation and again before first install. One stable launch signal surfaced stale exact-current PID 10608 with unchanged path/count=1. UI inspection bound the same PID, six screens were inspectable, one explicit exit completed, process count became zero and the presentation lock released. No force kill.

Per-user install_user.ps1 updated to the exact package, exit 0. Installed receipt/source/pointer were exact; state STOPPED / paused=true / setup_complete=true / current_dispatch=null; Worker/legacy absent. Lifecycle certification ran exactly once from the external existing build Python. Setup and limited interactive user-logon scheduler checks passed. Both stable launches and the singleton wait completed, then certification failed at `agent_bridge/scripts/certify_user_lifecycle.py:157`, opening the live desktop.lock with `Path.open('r+b')`:

`PermissionError: [Errno 13] Permission denied: BridgeDesktop/desktop.lock`

The accepted handler re-raises OSError unless `winerror == 32`. The traceback and source establish that this condition did not accept the real exception; the actual winerror value was not logged. A Python/Windows exception-shape mismatch is the bounded diagnosis, not a completed product fix. The live held-lock proof did not pass. First failure preserved in E_FIRST_FAILURE and E_LIFE. No source edit, lifecycle rerun, uninstall attempt or reinstall occurred. No recovery reinstall was needed because the exact installed package remained usable.

At the mandated failure stop, current WPF PID 8144 remains live at the exact package path. Its UI inspect/check, explicit exit, zero-WPF/lock release, post-exit state, diagnostics, stable uninstall and same-package reinstall were **NOT_RUN**. The successful stale cleanup does not certify these current-package steps.

## R05 — Changed paths and ownership

Only `reports/FOX2-BRIDGE-RC1-TO-INTERNAL-READY/report.md`, `reports/FOX2-BRIDGE-RC1-TO-INTERNAL-READY/evidence_manifest.json`, and `reports/FOX2-BRIDGE-RC1-TO-INTERNAL-READY/evidence/host_lifecycle_cert_a04/**` changed. The manifest inventories every path/hash; its self-hash is null to avoid recursion. Source/test/handoff/PreExec/history remain untouched. K1 classifies all report/manifest hunks REQUESTED and bounded execution/snapshot/helper evidence JUSTIFIED_GENERATED; UNEXPLAINED=0. Evidence helper scripts are reviewable execution records; the gate helper is a sanitized copy replacing its absolute user-profile CODEX path with LOCALAPPDATA. Raw config/DB/prompts/package binaries are excluded.

## R06 — Executed verification and host state

E_GATE/E_PACKAGE: remote authorization, no drift, detached-source provenance, accepted builder and package integrity PASS. E_CLEANUP: one-shot stale singleton surface and graceful exit PASS. E_INSTALL/E_INSTALLED: exact per-user update and safe state PASS. E_LIFE_ATTEMPT/E_FIRST_FAILURE: real lifecycle FAIL before uninstall. E_STATIC/E_DIFF/E_K1/E_CONTRACT: scope, evidence syntax, privacy/secret scan, diff check, K1 and Result Contract v2 checks. No accepted product-code suite was rerun; this TEST used the real Owner-host lifecycle and stopped on its first failure.

E_FINAL/E_PRESERVATION: exact package/source remains installed; STOPPED/paused/setup/null, Worker/legacy count=0; current WPF count=1, PID 8144. Startup preference remains true, scheduler Limited/Interactive/IgnoreNew and stable-launch action matches baseline. Config SHA-256 `b39bdc088a6ef3f7b59c48ab9692706adcec7905eb5a263c7baceb17fb9076f7` and manual-consumption SHA-256 `c758c3707b45289466d80635e5b7e7a386bb7823c33bed9ba2b7f1950a9a236c` are unchanged from fresh A04 pre-mutation state. DB file identity, all consumed dispatch identities and all pre-install logical table row hashes are unchanged; SQLite quick_check=ok. DB physical SHA changed from `723321b63c849306f580d8bc78b4f678c39d60631472ab856a5e5a27ab80cb20` to `6add09ff2570dfe84a17aba283da278173c1c276bd0d19087ecf63cd458b5929`. Installed status/setup initializes sticky claim_authority using INSERT OR REPLACE, so byte hash changes while logical row hashes remain identical. Physical byte preservation is not claimed. Across-uninstall/reinstall durability is NOT_RUN.

## R07 — A04 acceptance matrix

| Acceptance | Status | Evidence IDs | Observation / remaining work |
|---|---|---|---|
| A01_RUNTIME_ENVELOPE_REMOTE | PASS | E_GATE | All envelope, immutable Dispatch/PASS_TO_ASSIGN/receipt bytes, fetched ancestry, remote runtime HEAD, permissions and route bindings passed. |
| A02_ORCHESTRATION_NO_DRIFT | PASS | E_GATE, E_STATIC | Initially clean; no agent_bridge product/source/test drift; only authorized evidence and report writes. |
| A03_DETACHED_PACKAGE_SOURCE | PASS | E_GATE, E_PACKAGE | Same repository, exact path, detached accepted HEAD; tracked/untracked clean before and after build. |
| A04_EXACT_BUILDER_PREPROBE | PASS | E_GATE, E_BUILD | Builder blob/raw bytes exact; source_git_commit() returned accepted source before one build. |
| A05_PACKAGE_BUILT_ONCE | PASS | E_BUILD, E_BUILD_LOG | One builder invocation, exit 0, existing isolated Python and dotnet; package outside BridgeRoot/worktrees. |
| A06_PACKAGE_SOURCE_HASHES | PASS | E_PACKAGE | Exact source commit; 59 source files, 40 wheel modules, 255 payload hashes, dictionary and accepted package verifier PASS. |
| A07_FRESH_A04_BASELINE | PASS | E_BASELINE, E_PREINSTALL | Fresh bounded current/receipt, control, WPF, Worker, startup, config/DB/consumption/uninstall hashes, scheduler, versions and consumed identities; SQLite quick_check ok. |
| A08_STALE_WPF_CLEANUP | PASS | E_CLEANUP | One stable show signal; PID 10608/path/count unchanged; inspect same PID; one explicit exit; zero WPF and released lock. |
| A09_EXACT_INSTALL_UPDATE | PASS | E_INSTALL, E_INSTALL_LOG, E_INSTALLED | Per-user install_user.ps1 exact package/SHA exit 0; pointer/source receipt exact. |
| A10_SAFE_PAUSED_SETUP_NULL | PASS | E_INSTALLED | STOPPED, paused=true, setup_complete=true, explicit current_dispatch=null; Worker/legacy absent. |
| A11_TWO_LAUNCH_SINGLETON | PASS | E_FIRST_FAILURE, E_LIFE_ATTEMPT, E_FINAL | Trace reached the lock probe after both synchronous stable launches and exact-presentation wait; failure snapshot independently confirms one exact-current PID 8144. No full presentation PASS is claimed. |
| A12_CURRENT_UI_INSPECT_CHECK | NOT_RUN | E_LIFE, E_FIRST_FAILURE | Current-package UI inspect/check follows the failed lock proof and was not reached. Stale-package cleanup inspection is separate. |
| A13_LIVE_PRESENTATION_LOCK | FAIL | E_FIRST_FAILURE, E_LIFE | First failure: PermissionError errno 13 opening desktop.lock; handler re-raises winerror !=32. Live lock-held proof not accepted; actual winerror value not logged. |
| A14_CURRENT_GRACEFUL_EXIT | NOT_RUN | E_LIFE, E_FIRST_FAILURE, E_PRESERVATION | Current-package explicit exit follows the failed lock proof and was not reached. |
| A15_CURRENT_ZERO_WPF_LOCK_RELEASE | NOT_RUN | E_LIFE, E_FIRST_FAILURE, E_PRESERVATION | Current presentation remains live at first-failure stop. Stale cleanup zero/lock release must not substitute. |
| A16_POST_EXIT_SAFE_STATE | NOT_RUN | E_LIFE, E_FIRST_FAILURE, E_PRESERVATION | Current-package post-exit stage was not reached; safe paused state independently observed after failure. |
| A17_STABLE_UNINSTALL_ONCE | NOT_RUN | E_LIFE, E_FIRST_FAILURE, E_PRESERVATION | Stable uninstall attempts=0; failure occurred before uninstall. No retry. |
| A18_UNINSTALL_EXIT_ZERO | NOT_RUN | E_LIFE, E_FIRST_FAILURE, E_PRESERVATION | Uninstall not invoked; no exit code exists. |
| A19_IMMEDIATE_UNINSTALL_POSTCONDITIONS | NOT_RUN | E_LIFE, E_FIRST_FAILURE, E_PRESERVATION | Uninstall not invoked; no postcondition claim. |
| A20_DURABLE_UNINSTALL_REINSTALL_PRESERVATION | NOT_RUN | E_LIFE, E_FIRST_FAILURE, E_PRESERVATION | Across-uninstall/reinstall preservation NOT_RUN. Current preservation independently passes from fresh A04 baseline. |
| A21_SAME_PACKAGE_REINSTALL | NOT_RUN | E_LIFE, E_FIRST_FAILURE, E_PRESERVATION | Reinstall attempts=0; no recovery reinstall required. |
| A22_FINAL_CERTIFIED_STATE | NOT_RUN | E_LIFE, E_FIRST_FAILURE, E_PRESERVATION | Full successful-lifecycle final state NOT_RUN. Exact installed pointer/source and STOPPED/paused/setup/null observed after failure; one WPF remains. |
| A23_CONSUMED_IDENTITIES_PRESERVED | PASS | E_PRESERVATION, E_BASELINE, E_FINAL | All fresh-baseline DB dispatch identities and manual-consumption hash unchanged; logical DB table hashes all match pre-install baseline. |
| A24_NO_REPLAY | PASS | E_GATE, E_BASELINE, E_LIFE_ATTEMPT, E_PRESERVATION | One running consumed A04 launcher claim, one Agent/lifecycle attempt, zero reruns; historical Dispatches not replayed or rebound. |
| A25_NO_FORBIDDEN_MUTATION | PASS | E_STATIC, E_LIFE, E_PRESERVATION | No Worker/F1, legacy tray, G3/G4/Canary, AppLocker/AppIDSvc, service/ACL, reboot, provider/broker/LIVE, PR/main/merge action invoked. Worker/F1 health NOT_APPLICABLE_PRE_G3. |
| A26_RESULT_PATH_ALLOWLIST | PASS | E_STATIC, E_K1 | All changed paths restricted to report.md, evidence_manifest.json and evidence/host_lifecycle_cert_a04/**. |
| A27_SECRET_PRIVACY_SCAN | PASS | E_STATIC | Credential/private-path scan and evidence inventory review; no raw config, DB, prompts, package binaries or private account data committed. |
| A28_GIT_DIFF_CHECK | PASS | E_DIFF, E_STATIC | git diff --check against runtime base passes. |
| A29_K1_UNEXPLAINED_ZERO | PASS | E_K1 | Every report/manifest hunk REQUESTED; execution/evidence/helper files JUSTIFIED_GENERATED; UNEXPLAINED=0. |
| A30_RESULT_CONTRACT_V2 | PASS | E_CONTRACT | Dictionary-resolved v2 schema, formats, evidence references/hashes and full changed-path inventory validated. |
| A31_REMOTE_RESULT_PUBLICATION | NOT_RUN |  | Transport readback is recorded after the first push; final observed remote SHA is returned outside the committed report. |

The manifest additionally maps every controlling Dispatch required_test to these gates. Worker/F1 health remains NOT_APPLICABLE_PRE_G3. No current UI/exit/uninstall/reinstall success is inferred from code or earlier evidence.

## R08 — Evidence inventory

The companion `evidence_manifest.json` includes every evidence file's raw SHA-256, relative Git path, observation time, supporting IDs, tests and complete changed-path inventory. Key files: runtime_source_gates.json; governance_resolution.json; build_attempt.json; package_verification.json; pre_mutation.json; pre_install.json; stale_wpf_cleanup.json; install_attempt.json; installed_before_lifecycle.json; lifecycle_attempt.json; lifecycle.json; lifecycle.log; after_first_failure.json; failure_and_preservation.json; static_checks.json; k1.json; manifest_validation.log. Original lifecycle output is retained outside Git with the package; committed paths are sanitized.

## R09 — Git delivery

Repository `dunglt2505/FOX2`; branch `work/FOX2-BRIDGE-RC1-HOST-LIFECYCLE-CERT-A04-20261022`; runtime base `6d1d2a70f2d1cc47e44f70a0ba6cd07cd3985713`. Result is prepared for authorized non-main publication. Actual remote SHA is returned outside this committed report after push/readback; CHAT review remains pending. No PR/main/merge. CHAT has not accepted this failed certification result. The committed report contains no self-referential result commit SHA.

## R10 — Blocker, risks and boundaries

REWORK_REQUIRED: real held-lock error classification prevents the certifier reaching the remaining lifecycle. A separate authorized BUILD correction and CHAT intake are required before any fresh TEST Dispatch. This consumed A04 attempt cannot be rerun. Current package remains installed and paused with one exact-current WPF presentation; no post-failure cleanup mutation was performed because the first-failure STOP controls remaining execution. Stable uninstall count=0, reinstall count=0, recovery count=0. No Worker/F1, legacy tray health, G3/G4, AppLocker/AppIDSvc, FOX2F1Authority service, ProgramData ACL, reboot, Canary, provider/broker/LIVE action invoked. These are execution-scope observations, not a systemwide authority attestation.

## R11 — Resource and retry accounting

Agent attempts=1; retries=0; lifecycle attempts=1; lifecycle reruns=0; package builds=1. Stale show signals=1 and stale explicit exits=1. Current-package explicit exits=0. No model substitution or historical replay. Numeric tokens/credits/quota totals NOT_MEASURED. No extra Agent or subagent launched.

## R12 — CHAT decision request

Review this immutable FAIL result and evidence. Record REWORK_REQUIRED for the certifier's real Windows held-lock exception handling; preserve all NOT_RUN gates and consumed identities. No G3/G4/Canary/release readiness follows from the successful package/update or safe-state checks. Any later execution requires a separate approved task, material PreExec and fresh Dispatch.
