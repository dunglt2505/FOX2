# FOX2-BRIDGE-DESKTOP-01 — final Codex evidence

Date: 2026-10-14
Disposition: DELIVERY_READY — implementation and local validation complete; Bridge owns final verification, commit, push, and remote readback. No task commit or push was performed.

## Binding and authority

- Repository: dunglt2505/FOX2
- Branch: work/FOX2-BRIDGE-DESKTOP-01-worker-codex
- Base and final local HEAD: 308edc7bdabbc541216a97318590d2394acc9096
- Worktree: C:\Projects\FOX2-worktrees\FOX2-BRIDGE-DESKTOP-01-CODEX
- Initial local branch, HEAD, worktree, and index matched the dispatch and were clean.
- REV2 was treated as self-contained. Off-branch provenance blobs were not accessed; no docs-branch fetch, remote source verification, or competing-process discovery was performed.
- No installation, root/product/governance edits, main mutation, task staging, task commit, or task push.

## Sandbox baseline compatibility

The inherited Python installation resolved Bridge imports to a different worktree. Test conftest now places this task's source first. Synthetic adapter/E2E worktrees use a unique task-local temporary tree, with the configured root adjusted only inside the pytest fixture. Actual adapter containment and worktree-marker validation remain active.

Pytest's mode=0700 temp/cache directories were inaccessible to the Windows sandbox identity. The test-local tmp_path fixture uses ordinary inherited directory permissions, closes its Bridge log handlers, collects unreferenced SQLite connections, and removes its own tree, including read-only Git objects. Test-local pytest.ini disables the nonessential persistent cache; no test was skipped or xfailed.

The local poller fixture publishes Git objects and bare refs directly. A test-only local GitTransport subclass queries a bare ref and copies immutable objects to the Bridge store; production discovery, ancestry, blob identity, anomaly handling, cursor transactions, and ledger operations remain under test. The production HTTPS GitTransport is unchanged. A focused command-boundary test separately verifies the exact production fetch refspec, expected-SHA check, and observed-SHA pin.

Mandatory pre-Worker gate: `python -m pytest agent_bridge/tests -q` — **99 passed**, one cache warning, 51.57s. Worker coding began only after this passed.

## Worker implementation

BackgroundWorker is composed from BridgeApp, DispatchPoller, BridgeOps, BridgeE2ERunner, SQLiteLedger, and the accepted ProcessLock. Startup still acquires the existing runtime lock, initializes/refuses ledger schema, and reconciles interrupted rows before polling.

Each iteration probes the configured control branch through the existing Git transport. A healthy unchanged SHA with a completed processing checkpoint performs no full fetch, candidate/blob scan, or Agent invocation. Changed SHA uses the existing exact control-ref fetch and durable discovery transaction. Opt-in selection and execution remain in BridgeOps/E2E; the Worker passes the fetched immutable SHA so that selection and execution do not repeat remote queries/fetches.

All eligible discoveries drain before the processed checkpoint advances. Selection no longer silently omits older candidates behind the former 500-row selection limit. The existing Core's CODEX auto_execute eligibility policy is preserved; no second transport/governance engine was introduced.

## Durable state, pause, recovery, and timing

Schema stays at version 3. One namespaced metadata row stores pause, last observed SHA, processed SHA, bounded failure count/delay, control sequences, and latest poll status. Partial updates and control increments use SQLite transactions so controls cannot overwrite polling checkpoints. Existing dispatch/execution rows and future-schema refusal are preserved. Offline probe errors retain the last successful SHA observation.

The discovery cursor and candidate rows commit atomically through the existing poller. The Worker processed SHA commits only after selection drains. On restart, a discovery cursor ahead of the processed SHA causes reconciliation of durable pending candidates, even if the remote SHA is unchanged. This is an intentional recovery case; a completed idle checkpoint has zero fetch/selection/Agent activity.

Claims and terminal states remain the replay authority. Startup terminalizes interrupted RUNNING rows through existing recovery. INTERRUPTED, PUSHED_UNREVIEWED, and DELIVERY_RECOVERY_REQUIRED rows are excluded from new selection. Successful Agent delivery contexts remain under accepted Hotfix recovery; delivery recovery is never automatically turned into a new Agent run.

Pause/stop checks are inside the claim transaction as well as before selection/execution. A pause arriving during preflight therefore prevents a new claim. Already claimed tasks finish through their existing route. Resume retries pending selection and skips all previously claimed/terminal rows. Transient blob-read errors retain the processed checkpoint for retry.

Healthy cadence uses the existing 30-second default. Failed Git contact uses 30, 60, 120, 300 seconds, capped at 300 and preserved across restart. A successful ref contact resets healthy cadence, including contact followed by a fetch/history failure. Tests inject clock and wake primitives; no real 30/60/120/300-second waits occur.

The existing process lock rejects another Bridge/Worker profile owner. An additional in-process guard prevents two watch loops on the same started BridgeApp. Graceful stop releases the native wake handle and then the normal app context releases the runtime lock.

## CLI controls and local wake

Commands: `worker-start`, `worker-pause`, `worker-resume`, `worker-check-now`, `worker-status`, `worker-stop`. All accept the existing `--config`; start also accepts `--timeout`. Start is a foreground long-running watch loop; no scheduling/installer/service is included.

Controls operate against an already initialized supported ledger without acquiring the runtime writer lock or starting another poller. A per-user/profile Windows auto-reset named event wakes the watch loop promptly. Persistent sequence changes cover requests around wait boundaries. Stop affects the active watch generation; a later explicit start may run again.

Status reports persisted Worker state, not a claim of current process liveness. Controls against an uninitialized/future-schema ledger fail closed; initial ledger creation/migration remains under normal startup lock ownership.

## Final validation

| Check | Result |
| --- | --- |
| `python -m pytest agent_bridge/tests/test_worker.py -q` | 26 passed, 13.38s |
| `python -m pytest agent_bridge/tests -q` | 125 passed, 45.57s |
| `python -m pytest agent_bridge/tests/test_delivery_hotfix.py -q` | 22 passed, 4.78s |
| Syntax/import check | All 19 source modules parsed and imported |
| Schema migration | NOT_REQUIRED; version 3 retained, existing ledger regressions pass |
| `git diff --check` | PASS, exit 0 |
| Changed-file scope | PASS for enumerated source/test/report artifacts |
| Obvious-secret scan | PASS, no matches in deliverable files |
| Inbound-listener static scan | PASS; Worker uses kernel event, not sockets/server APIs |

Full command outputs are in evidence/test_results.json. Detailed scope, import/listener scan, and enumeration warnings are in evidence/checks.json.

## Acceptance D01–D21

| ID | Assertion | Verdict | Evidence |
| --- | --- | --- | --- |
| D01 | Deterministic state and controls | PASS | test_worker_controls_cli_operate_while_runtime_lock_held; test_worker_state_preserves_existing_rows_and_future_schema_refusal |
| D02 | Unchanged SHA: zero full fetch | PASS | test_idle_unchanged_zero_fetch_scan_and_agent |
| D03 | Unchanged SHA: zero Agent call | PASS | test_idle_unchanged_zero_fetch_scan_and_agent |
| D04 | Changed SHA: exact fetch/discovery | PASS | test_changed_exact_fetch_then_execute_once_and_terminal_resume; test_production_git_fetch_is_exact_control_ref_and_pinned |
| D05 | Changed SHA without opt-in: no Agent | PASS | test_changed_without_opt_in_never_executes |
| D06 | Eligible dispatch executes once | PASS | test_changed_exact_fetch_then_execute_once_and_terminal_resume; test_worker_reuses_real_e2e_hotfix_route |
| D07 | Healthy cadence deterministic | PASS | test_fake_clock_healthy_wait_check_now_and_graceful_stop |
| D08 | 30/60/120/300 capped backoff | PASS | test_backoff_capped_persisted_and_contact_resets |
| D09 | Successful Git contact resets cadence | PASS | test_backoff_capped_persisted_and_contact_resets |
| D10 | Check-now wakes promptly | PASS | test_fake_clock_healthy_wait_check_now_and_graceful_stop; test_windows_local_wake_cross_handle_no_listener |
| D11 | Pause blocks new claim/launch | PASS | test_control_inside_claim_transaction_blocks_launch; test_pause_persists_and_resume_discovers_pending_without_fetch |
| D12 | Resume does not replay terminal dispatch | PASS | test_changed_exact_fetch_then_execute_once_and_terminal_resume; test_pause_does_not_abandon_already_claimed_task |
| D13 | Required durable state survives restart | PASS | test_pause_persists_and_resume_discovers_pending_without_fetch; test_backoff_capped_persisted_and_contact_resets; test_successful_ref_observation_survives_offline_contact |
| D14 | Stopped Worker finds later publication | PASS | test_task_published_while_stopped_discovered_on_restart |
| D15 | Pre-Agent interruption reconciles safely | PASS | test_restart_reconciliation_never_relaunches_claimed_dispatch[INTERRUPTED]; existing runtime-ledger recovery regression |
| D16 | Delivery recovery never relaunches Agent | PASS | test_restart_reconciliation_never_relaunches_claimed_dispatch[DELIVERY_RECOVERY_REQUIRED]; Hotfix recovery regressions |
| D17 | One Worker per profile | PASS | test_second_worker_profile_cannot_start; test_two_workers_in_same_runtime_cannot_run; existing second-process lock regression |
| D18 | Cursor crashes lose no valid dispatch | PASS | test_cursor_discovery_transaction_failure_is_retryable; test_crash_after_discovery_cursor_commit_loses_no_dispatch; test_crash_after_execution_before_processed_checkpoint_never_replays; test_transient_blob_read_failure_cannot_checkpoint_away_valid_dispatch; existing transaction rollback regression |
| D19 | No inbound Internet listener/server | PASS | worker imports/static listener scan; test_windows_local_wake_cross_handle_no_listener |
| D20 | Full Bridge suite passes in sandbox | PASS | python -m pytest agent_bridge/tests -q: 125 passed |
| D21 | No main/merge/Production/provider/broker/LIVE authority | PASS | Local HEAD/branch unchanged; changed-file scope check; no task Git delivery or remote source verification |

## BRD mapping

| BRD | Desktop acceptance / disposition |
| --- | --- |
| T23 | D02 / D04 / D19 — remote SHA probe, exact fetch/discovery, outbound-only transport |
| T24 | D02 / D03 / D10 — idle avoids full fetch and Agent; local wake |
| T25 | D03 — unchanged completed checkpoint has zero Agent launch |
| T26 | D08 / D09 — capped backoff and successful-contact reset |
| T27 | D19 — no inbound Internet listener |
| T28 | D14 — stopped-worker publication found on restart |
| T29 | NOT_IMPLEMENTED — future push-hint only, explicitly outside this WP |

## Restart, idle, and no-listener proof

Restart tests exercise publication while stopped, pre-Agent claimed interruption, terminal/delivery recovery exclusions, crash after discovery commit, crash after successful execution before processed checkpoint, failed discovery persistence, and interrupted blob reads. Single-use claims and durable checkpoints prove safe recovery without lost valid pending dispatches or Agent replay. The real E2E route integration test invokes the accepted Hotfix method with a supplied fetched SHA and forbids redundant remote contact.

The idle test snapshots transport counters after initial processing, executes three unchanged iterations, and asserts only query count rises; fetch, discovery scan, blob read, and Agent count remain unchanged. Multi-dispatch drain also verifies the next unchanged iteration is idle.

Worker imports and listener-pattern inspection find no socket/listen/bind/server API. Local wake integration uses two real Windows event handles with zero-time waits. Remote access remains the existing outbound Git boundary. No Internet listener, relay, webhook, or cloud service was added. Live network/process inspection was not used.

## Changed implementation/test paths

- `agent_bridge/src/fox2_agent_bridge/__main__.py`
- `agent_bridge/src/fox2_agent_bridge/app.py`
- `agent_bridge/src/fox2_agent_bridge/e2e_runner.py`
- `agent_bridge/src/fox2_agent_bridge/ledger.py`
- `agent_bridge/src/fox2_agent_bridge/ops_runner.py`
- `agent_bridge/src/fox2_agent_bridge/worker.py`
- `agent_bridge/tests/conftest.py`
- `agent_bridge/tests/pytest.ini`
- `agent_bridge/tests/test_codex_adapter.py`
- `agent_bridge/tests/test_copilot_adapter.py`
- `agent_bridge/tests/test_dispatch_poller.py`
- `agent_bridge/tests/test_worker.py`

Final evidence is confined to reports/FOX2-BRIDGE-DESKTOP-01/report.md, evidence_manifest.json, and evidence/**. The manifest records source and evidence hashes.

## NOT_RUN, limitations, and open delivery gates

- NOT_RUN: real GitHub connectivity, live Agent execution, real Git delivery, remote HEAD readback, or desktop deployment. Tests use local Git/fake mailboxes and bounded mocked Agent/delivery boundaries. Bridge owns commit/push and final remote verification.
- NOT_IMPLEMENTED: Tray, Start-with-Windows, scheduler, installer, onboarding GUI, webhook/cloud relay, remote desktop, multi-user service, and T29 push hints.
- Recovery remains fail-closed: interrupted claimed tasks are terminalized, not automatically relaunched; DELIVERY_RECOVERY_REQUIRED requires the accepted explicit recover-delivery flow.
- Inaccessible generated pytest directories remain from early failing baseline attempts. Accessible fixture artifacts were removed, and final runs clean up their own trees. The directories and Git enumeration warnings are listed in evidence/checks.json; their contents could not be inspected by this sandbox. Bridge should clean/verify these generated directories before delivery and exclude them from staging.
- Automatic approval review rejected the attempted ACL-reset/recursive cleanup action with “blocked by policy”; no further reason was supplied. No ACL reset was performed. A narrower cleanup removed accessible artifacts.
- Scope and secret verdicts apply to enumerated deliverable source/tests/reports; inaccessible generated directories are an explicit inspection/cleanup limitation.
- No local task staging/commit/push occurred. Final local HEAD and branch remain the authorized base and task branch.
