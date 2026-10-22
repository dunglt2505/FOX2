# FOX2 Lifecycle/WPF Contract Rework A02 â€” BUILD result

## R01 â€” Identification and submission

Task `FOX2-BRIDGE-RC1-LIFECYCLE-WPF-CONTRACT-REWORK-A02`; Whole-WP `FOX2-BRIDGE-RC1-TO-INTERNAL-READY`. CODEX `gpt-6.1-sol`, high, MANUAL_LOCAL, task-scoped FULL_ACCESS. One fresh A02 Agent attempt, no retries or subagents. Started `2026-10-22T02:29:30.5759665Z`; report assembled `2026-10-22T02:38:46.542606+00:00`. Delivery state after the authorized branch push is **PUSHED_UNREVIEWED**. CHAT acceptance is not claimed.

## R02 â€” Authority, routing and start gates

Fresh Dispatch `FOX2-DISPATCH-BRIDGE-RC1-LIFECYCLE-WPF-CONTRACT-REWORK-A02-CODEX-001` is at `126e8d857e7e4964fe05a47d558215763779535f`, blob `0997c8126e24dbf973949fb14610324b49b99bdc` on `work/FOX2-DISPATCH-chat`. It grants bounded code/report writes and non-main result push, with no PR/merge/provider/broker/LIVE permission. The task-specific PreExec REV3 receipt at `4504bf95dd2baf474b30f896b23365c52fe10c9f` and CHAT PASS_TO_ASSIGN `61b75156bb4b241b88a26c0c11cb8af79f79a94b` bind this route. Policy 2.0.0, Dictionary 1.3, Routing Index 1.4.0 and Protocol v12 immutable bytes were verified independently. Source bytes and task-scoped execution authority are verified; global publication/runtime promotion is not claimed. TechSpec v0.7 REV10 remains **CANDIDATE_NO_PROMOTION**.

Required-versus-observed gates: exact branch/worktree/base and remote task head PASS; recovery ancestor PASS; task/prompt/PreExec/Dispatch hashes PASS; Dispatch schema blob `1692061941e2bef498515cd0e96b9b3046119ebb` PASS; current launcher claim/model/effort/FULL_ACCESS PASS; initial worktree clean PASS; no pre-start product drift PASS; one task Agent process PID 3496 observed PASS. Fresh PreExec authenticated capacity probe PASS and this pinned execution is active; numeric quota is not measured. Only the two bound task/prompt additions and PreExec receipt separate recovery snapshot from runtime base. Start verdict: **GO for offline BUILD only**. See `evidence/lifecycle_wpf_contract_rework/source_binding.json` for identities, R0â€“R7 provenance and observations.

## R03 â€” Immutable inputs and A01 preservation

Runtime base `4504bf95dd2baf474b30f896b23365c52fe10c9f`; original runtime base `e7d5acf51dddcbc95324a992ad6be2773e61285f`; recovery snapshot `1a11fa0b232a69f0c26a0b4029c331ee2a8c840f`. Task commit `f796306ca4e79b9ab61cd436cf69a5f28ede4faf`, task SHA-256 `7bfe425ad18f372960fb0440cd8694fb1a2a86edd7bd10cac5b105817f73d58c`. Prompt commit `56e4c1eeb9341062fdb8ec52110e4e5c44c329e2`, blob `faef3f5cf4b6d286d7a30cb4200c6b6526ed55b2`, prompt SHA-256 `a9b07516ce8f5b31ffb7b404f993407855cb1449f28be244011902630df5f201`.

A01/CODEX-001 remains EXITED_CONSUMED, exit 1, CODEX_USAGE_LIMIT, NEEDS_RECONCILIATION, no Git result, no CHAT acceptance and no replay. Its recovery provenance JSON is byte-identical. Salvage is input, never accepted evidence. Every inherited source/test hunk was reviewed; provisional evidence and A01-bound helpers were replaced with fresh A02 execution evidence. `salvage_review.json`, `k1.json`, `original_to_final_diff.json` and `salvage_to_final_diff.json` distinguish retained salvage from A02 corrections.

## R04 â€” Implemented behavior and corrections

The harness uses stable `BridgeRoot/launch.ps1` twice and validates one current-package `FOX2.Bridge.Desktop.exe` by its exact installed executable path, current package pointer and inspected UI PID. It requires paused=true, setup_complete=true and explicit current_dispatch=null. No desktop-tray health, legacy launcher-process health, Worker heartbeat or Worker start is required. Worker/F1 health is **NOT_APPLICABLE_PRE_G3**, never a health PASS.

Existing `certify_rc1_ui.ps1` supplies inspect/check/explicit exit. Inspect validates all six navigation entries and the current presentation PID; check proves Check Now disabled while paused. The harness observes the held presentation lock, rechecks safe control and exact presentation identity, invokes graceful UI exit, waits boundedly for zero presentations, observes lock release and rechecks STOPPED/paused/setup/no-current-dispatch before uninstall. No forced-exit path was added.

Three A02 proof gaps were corrected: absent current_dispatch no longer passes as null; only WinError 32 sharing violation proves a live FileShare.None lock, while access-denied/other errors fail; process queries fail on PowerShell errors and must return an explicit array, so null cannot falsely prove exit. Negative fixtures also cover process-query failure/timeout, PID changes and unsafe state changes before/after exit. Correct salvaged behavior was retained.

## R05 â€” A03 preservation and changed-path ownership

Only the allowed lifecycle harness and two test files contain material source/test changes. `test_rc1_launcher.py` was rerun unchanged. A03 `certify_uninstall` and `_uninstall_output` ASTs match the original runtime base. Stable external PowerShell 7 at `BridgeRoot/uninstall.ps1`, synchronous single attempt, installed-Python exclusion, sanitized bounded output, nonzero/timeout/start/postcondition stop-once behavior and checkpoint-before-reinstall semantics remain intact.

Configuration/database/manual-consumption checks and historical Batch-B consumed identities 001â€“004 remain intact. Successful reinstall uses the same package/SHA, verifies the current package, and rechecks the safe stopped/paused state. No historical consumed identity was replayed or rewritten. The protected launcher/F1/installation/UI/WPF source files retain original Git blobs and raw bytes from a same-base checkout. All other agent_bridge paths remain unchanged.

The complete changed-path inventory and raw SHA-256 values are in `evidence_manifest.json`; the manifest's own hash is null to avoid self-reference. No unrelated WIP was present or introduced. Test artifacts are isolated in a detached short fixture worktree, with no second material writer.

## R06 â€” Executed validation and environment

Focused lifecycle/WPF + launcher + package + installation: **103 passed in 3.34s**. Full `agent_bridge/tests`: **653 passed in 236.02s (0:03:56)**. Real command lines, cwd, environment, UTC times, exit codes and unabridged logs are retained in `*_run.json` and associated `.log` files.

The short detached A02 test worktree at `C:/Projects/FOX2/.git/wpf-a02-test` starts from the exact runtime base and has byte-for-byte copies of the final allowed source/test files; all tracked agent_bridge files were compared before each run. This follows the established short-worktree test approach for Windows MAX_PATH. No test was edited or skipped to hide environment behavior. The focused and full runs passed without a core.longpaths override. No repository/global Git configuration, test or host setting changed.

An initial generated-evidence formatting check found CRLF trailing-whitespace diagnostics; its output is retained in diff_check_initial.log. A02-generated text was normalized to LF and writers now request LF explicitly; the immutable recovery provenance bytes were preserved. A later staged check flagged the literal blank context lines in unified-diff evidence; exact Git stdout is now stored in JSON, with that failed validation output preserved in static_validation_history.json. Syntax/compile checks, static parsing of the generated PowerShell query (without executing it), changed-path allowlist, forbidden production-file byte identity, immutable recovery provenance, A03 AST identity, git diff --check, bounded secret scan and K1 **UNEXPLAINED=0** all pass. K1 classifies material hunks against both original runtime base and salvage as REQUESTED or NECESSARY_DEPENDENCY; regenerated evidence is JUSTIFIED_GENERATED. Result Contract v2 schema and evidence/changed-file hash readback are verified by `verify_result.py --manifest-only`.

## R07 â€” Requirements and evidence

All Dispatch-required offline checks are mapped individually in the manifest. Singleton/current identity/safe state/UI/lock/exit tests use intercepted process boundaries; launcher tests retain worker_started=False. Stable-uninstall success and nonzero/timeout/start/postcondition stop-once cases are rerun, along with durable-state assertions. No prior A01 PASS substitutes for an A02 result. Historical host lifecycle FAIL remains unchanged in Git history.

Evidence includes source binding, test snapshot byte hashes, actual pytest receipts/logs, salvage review, both source diffs, hunk classifications, static checks and Result Contract validation output. The manifest binds every evidence item with raw SHA-256. Observed remote result SHA is returned outside this committed report.

## R08 â€” Scope, risks and next owner

Real installed-host lifecycle: **NOT_RUN**. No actual package install/update/uninstall/reinstall, installed WPF launch, Task Scheduler change, Bridge durable data/config/database change, Worker/F1 start, AppLocker/AppIDSvc/service/ACL change, reboot, G3/G4/Canary, main/PR/merge or provider/broker/LIVE action occurred during A02 BUILD. Tests exercise temporary offline fixtures.

Fixture validation does not certify Owner-host lifecycle, F1 adoption, G3/G4 or operational readiness. Usage totals are NOT_MEASURED; attempts=1, retries=0. CHAT must independently review this immutable pushed BUILD result. Any future real host certification needs its own authorized binding and material PreExec. No CHAT acceptance or feature-stage promotion is claimed here.
