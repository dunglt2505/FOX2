# FOX2 Current-Package Owner-Host Lifecycle A01 — FAIL

## R01 — Result and submission

Task `FOX2-BRIDGE-RC1-HOST-LIFECYCLE-CERT-A01`; Whole-WP `FOX2-BRIDGE-RC1-TO-INTERNAL-READY`.
Dispatch `FOX2-DISPATCH-BRIDGE-RC1-HOST-LIFECYCLE-CERT-A01-CODEX-001`. One CODEX `gpt-6.1-sol`, high, MANUAL_LOCAL, task-scoped FULL_ACCESS attempt; no model substitution or Agent replay.
Host execution UTC: 2026-10-21T16:47:20.863447+00:00 to 2026-10-21T16:48:37.133912+00:00.
Result: **FAIL / REWORK_REQUIRED**. Submission: READY_FOR_CHAT_REVIEW; delivery PUSHED_UNREVIEWED after authorized branch publication. CHAT acceptance is not claimed.

The supported installer updated the exact accepted package successfully. The single lifecycle invocation then exited 1 with **RuntimeError: installed tray/worker did not become healthy**, at `certify_user_lifecycle.py:133`, before uninstall. Stable uninstall attempts: **0**; reinstall: **NOT_RUN**; recovery attempts: **0**. No lifecycle or uninstall retry occurred.

## R02 — Authority and routing

Owner task plus exact fresh Dispatch authorize bounded Phase-2 per-user TEST only. Task-specific PreExec v5 PASS blob `08056cb73333934a148cef2b4f1f3da11f6b9b3e`, CHAT PASS_TO_ASSIGN `185f4cdcdfb6a7487f8bbc0f256c304fb1d9f263`, and A03 BUILD-only acceptance `37691b71b64de03091de9908014da2256c1d2901` are source-bound. Policy 2.0.0 applies as task-scoped Owner authority. R0–R7/assignment PASS are inherited from the exact Dispatch and PreExec, with route, writer and host checks observed again here. Product/source/test writes remain disabled despite the legacy Dispatch decision field.

## R03 — Immutable bindings and package

Starting HEAD `208de84f39dcf783bd4ee9053c0288cda9aa0024` matched the live remote task branch and Dispatch runtime base before build. Accepted source `2faa33f9ab4d06bcc51c8fd1d2c7040fc06a29cb` is an ancestor; all eight pre-start changed paths are task/prompt/PreExec evidence, with no product drift. Exact Dispatch commit `8cac3d2798c4e3906ceac351676d32ada761056e`, blob `353ca16452d5d717ca023872a54c2eeb2f3c310b` was fetched and matched to launcher environment bindings. Task commit `d95f08ceed2f5a25ad288b9630ffc87b698f329c` and prompt commit `250c8ab15bdfd8339e6332dc105a559dbd5b3151` pass raw SHA-256 readback. See source_binding.json for all locked identities.

Package alias: `BUILD_ROOT/accepted-package.zip`, outside BridgeRoot and retained for this task. SHA-256: `52007843327db63acb0c7908f06ba33378404686f03b6f81d07178de4c2f16d4`; size 64529059 bytes. Manifest source_git_commit is exactly `2faa33f9ab4d06bcc51c8fd1d2c7040fc06a29cb`. Build used the already-existing isolated Python 3.13.15 / setuptools 84.0.0 / wheel 0.48.0 / build 1.6.1 environment and dotnet 8.0.426. No tools or dependencies were installed to satisfy capability. The unmodified builder downloaded pinned wheel payloads and built the self-contained package.

The temporary clean checkout carries the accepted commit while the execution worktree retains its Dispatch base. All 59 source inventory and 40 wheel module entries, all payload hashes, sorted fixed-time ZIP entries and declared deterministic build flags were checked. No second build was performed. Machine dictionary 1.2 (`7fc3532890f4a60a4abc7bf3b08dc06fe6af6ee000176ac464bfe3aacda2ecd7`) and Dispatch routing dictionary 1.3 are independently pinned; global machine adoption is not claimed.

Two preparation corrections are preserved in package_verification.json: the temporary clone already had the task branch, so an initial branch-creation command refused before build; an evidence-only assertion initially conflated the two dictionary layers. Both were resolved before install without changing product code or rebuilding the package.

## R04 — Completed and remaining scope

Exact build, package verification, durable pre-state, supported real install/update, exact installed receipt and safe paused pre-certification state completed. The real lifecycle failed at its first healthy tray/worker condition. Stable external uninstall, uninstall postconditions, diagnostics stage, single-instance stage and same-package reinstall were not reached. Across-uninstall durability remains NOT_RUN. No recovery was needed because the exact package remains installed.

## R05 — Changed paths and ownership

Only report.md, evidence_manifest.json and evidence/host_lifecycle_cert/** changed. The initial worktree was clean; one task CODEX writer PID 18272 was observed, with no G3/G4/Canary writer or subagent. Exact path/hash inventory is in the manifest; K1 classifies all paths in k1.json. Package binaries, temporary source checkout, config/database contents, raw prompts and raw local logs are excluded from Git.

## R06 — Observed tests

Build/provenance, install, pointer/receipt and paused pre-state PASS. Corrected real-host lifecycle FAIL, exit 1. Bounded source inspection shows the harness expects a legacy pwsh desktop_tray.ps1 process and a PAUSED Worker heartbeat. The accepted launcher starts WPF presentation only and returns worker_started=False. This is an observed contract mismatch requiring a separately authorized source task; no code fix or alternative Worker launch was attempted here.

## R07 — Required acceptance matrix

| Required check | Result | Evidence |
|---|---|---|
| EXACT_ACCEPTED_SOURCE_PACKAGE_BUILD_PROVENANCE | PASS | E_PACKAGE_VERIFICATION |
| PACKAGE_SHA256_AND_MANIFEST_VERIFIED_BEFORE_HOST_MUTATION | PASS | E_PACKAGE_VERIFICATION, E_PACKAGE_MANIFEST |
| PRE_STATE_DURABLE_HASH_SNAPSHOT | PASS | E_PRE_STATE, E_PRE_INSTALL_STATE |
| REAL_INSTALL_OR_UPDATE_EXACT_PACKAGE_PASS | PASS | E_EXECUTION, E_POST_INSTALL_STATE |
| CURRENT_POINTER_AND_INSTALLED_RECEIPT_BIND_EXACT_PACKAGE_SOURCE | PASS | E_POST_INSTALL_STATE |
| SAFE_PAUSED_STATE_BEFORE_CERTIFICATION | PASS | E_POST_INSTALL_STATE |
| CORRECTED_LIFECYCLE_CERTIFICATION_RUN_ON_OWNER_HOST | FAIL | E_EXECUTION, E_FAILURE_ANALYSIS |
| STABLE_EXTERNAL_UNINSTALL_EXERCISED_EXACTLY_ONCE | NOT_RUN | E_EXECUTION |
| UNINSTALL_EXIT_ZERO | NOT_RUN | E_EXECUTION |
| POST_UNINSTALL_CURRENT_POINTER_AND_OWNED_VERSIONS_ABSENT | NOT_RUN | E_FINAL_STATE |
| DURABLE_CONFIG_DATABASE_MANUAL_CONSUMPTION_PRESERVED | NOT_RUN | E_FAILURE_ANALYSIS, E_FINAL_STATE |
| SAME_EXACT_PACKAGE_REINSTALL_PASS | NOT_RUN | E_EXECUTION, E_FINAL_STATE |
| FINAL_CURRENT_POINTER_EXACT | PASS | E_FINAL_STATE |
| FINAL_SETUP_AND_HEALTH_PASS | FAIL | E_FINAL_STATE, E_FAILURE_ANALYSIS |
| CONSUMED_IDENTITIES_PRESERVED | PASS | E_FAILURE_ANALYSIS, E_FINAL_STATE |
| NO_OLD_DISPATCH_REPLAY | PASS | E_SOURCE_BINDING, E_EXECUTION |
| NO_G3_G4_APPLOCKER_SERVICE_ACL_MUTATION | PASS | E_FAILURE_ANALYSIS, E_PACKAGE_MANIFEST |
| CHANGED_PATH_ALLOWLIST_REPORT_EVIDENCE_ONLY | PASS | E_STATIC_CHECKS, E_VERIFY_RESULT, E_K1 |
| SECRET_SCAN | PASS | E_STATIC_CHECKS, E_VERIFY_RESULT, E_K1 |
| GIT_DIFF_CHECK | PASS | E_STATIC_CHECKS, E_VERIFY_RESULT, E_K1 |
| K1_UNEXPLAINED_ZERO | PASS | E_STATIC_CHECKS, E_VERIFY_RESULT, E_K1 |
| RESULT_CONTRACT_V2_REPORT_AND_EVIDENCE_MANIFEST | PASS | E_STATIC_CHECKS, E_VERIFY_RESULT, E_K1 |

## R08 — Bounded evidence and final host state

Final current pointer is `52007843327db63acb0c7908f06ba33378404686f03b6f81d07178de4c2f16d4`, with installed source `2faa33f9ab4d06bcc51c8fd1d2c7040fc06a29cb` and installed receipt SHA-256 `4075f48dc0718b7574a0764e5392fb31ca8ddc9a8896f7cd9747d7c2a67339c4`. Both the new and previous owned version remain; uninstall was not attempted. Worker is STOPPED, paused=true, setup_complete=true, no active dispatch; startup=true and the Limited/Interactive per-user scheduled task is Ready.

Config hash `b39bdc088a6ef3f7b59c48ab9692706adcec7905eb5a263c7baceb17fb9076f7`, database hash `70d387ed9ee57e950a4509b392af19966496cec770f7872e52925528e5b8d884` and manual-consumption hash `c758c3707b45289466d80635e5b7e7a386bb7823c33bed9ba2b7f1950a9a236c` are unchanged from pre-state. SQLite quick_check=ok; all 28 dispatch identity/state records and four historical consumed identities are unchanged.

One WPF Desktop process created by this run remains open. The observer's active_runtime_processes field counts worker/legacy PowerShell tray/launcher, not WPF presentation; failure_analysis.json records that limitation and the separate presentation observation. The CLI request-exit in the harness cleanup did not close the WPF presentation. No forced termination, additional runtime launch or further host mutation was attempted after failure.

The harness writes lifecycle checkpoints at uninstall and completion, so this earlier failure produced no raw lifecycle JSON. execution.json preserves sanitized process exit/stderr and the original RuntimeError separately from the orchestration assertion. Evidence IDs, relative paths and SHA-256 values are in evidence_manifest.json. No raw configuration or database content is included.

## R09 — Git delivery

Repository dunglt2505/FOX2, branch work/FOX2-BRIDGE-RC1-HOST-LIFECYCLE-CERT-20261021. Report/evidence only; no PR/main/merge. Local HEAD before result submission: `208de84f39dcf783bd4ee9053c0288cda9aa0024`. Push is followed by independent remote branch-head readback. The observed containing commit SHA is returned outside this report. Final delivery state is PUSHED_UNREVIEWED, pending CHAT intake.

## R10 — Risks and boundaries

Lifecycle certification remains FAIL; uninstall/reinstall and final healthy runtime remain unverified. Startup remains enabled and one presentation process remains open; worker stays stopped and paused. REWORK_REQUIRED must be handled through a fresh source/task/PreExec/Dispatch with no replay of this consumed attempt. Historical A03 BUILD evidence remains at `2faa33f9ab4d06bcc51c8fd1d2c7040fc06a29cb` and the separate acceptance receipt; historical Batch-B UNINSTALL_PATH=FAIL remains factual and unchanged.

No AppLocker, AppIDSvc, FOX2F1Authority service, ProgramData authority ACL, reboot, G3/G4, Canary, provider/broker/LIVE mutation was invoked. Package F1 activation remains DENY_PENDING_G3_G4. Bounded changed-text secret/private-path scan, allowlist and diff checks pass; K1 UNEXPLAINED=0. Result Contract v2 and evidence hashes/references are validated by verify_result.py.

## R11 — Attempts and usage

Agent attempts=1, Agent retries=0; package builds=1, install/update attempts=1, lifecycle invocations=1, stable uninstall attempts=0, reinstall attempts=0, recovery attempts=0. Token/credit usage NOT_MEASURED. Preparation/evidence corrections are not Agent or lifecycle retries.

## R12 — CHAT decision requested

Review the immutable pushed FAIL result and arrange separately authorized rework of current-package certification/launcher compatibility. Do not accept Phase 2 TEST, replay this Dispatch or progress to G3/G4/Canary from this result.
