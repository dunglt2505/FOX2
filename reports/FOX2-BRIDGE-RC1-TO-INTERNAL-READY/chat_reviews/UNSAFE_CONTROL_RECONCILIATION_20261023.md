# FOX2 Bridge Unsafe control reconciliation — 2026-10-23
Feature: FOX2-BRIDGE-RC1. Whole-WP: FOX2-BRIDGE-RC1-TO-INTERNAL-READY.
Stage TEST; status BLOCKED_FOR_VALIDATOR_RESTART; internal_ready NOT_ATTESTED.

## Verdict and direct host evidence
Stable read-only snapshots observed state=STOPPED (string), paused=false (boolean),
setup_complete=true (boolean), current_dispatch=null (present).
Only paused fails the original Safe predicate. Current state corroborates the
reported failure; the exact field values at the historical failure instant were
not recorded and cannot be reconstructed from the combined STOP alone.
No control command, pause/resume, worker, validator, claim creation, uninstall,
reinstall, G3/G4, provider/broker or LIVE operation was executed in this diagnosis.
The exact internal validation claim and attempt_001 output directory were
independently absent at inspection. This supports NOT_CONSUMED for the reported
invocation together with source ordering; it is not permission to replay R5.

Archive SHA-256 was recomputed:
f99c7add1b99bad938d977f634fd8a88e20763f5e35aaadf5cfe3072a1a327ee.
Installed pointer and receipt bind this package. Pointer source inventory matches
6d76f99ce9fcc62bbcf9f2450a45bc920c28b2fd70828353c0a8fea096c5de73.
Installed desktop.py, ledger.py, __main__.py, config.py SHA-256 match receipt
wheel_source_modules. Config points at the default canonical root and database.
The A04 lifecycle_raw evidence preserves FAILED_BEFORE_UNINSTALL and setup.paused=true.
The later paused=false observation does not establish who or what changed pause,
nor when. Historical A04 safe-state PASS is not evidence of present paused state.

## Immutable source contract and separately proven runner defect
Runner base f551e3790aa93b2a43b710e4756630d95f2472b3, blob
dc972923242cc52c6a40a1a68b8fdd4e9f1b2ac2, calls Installed; Safe before NoWorker,
claim checks, claim CreateNew, and lifecycle mutation. The reported STOP therefore
precedes those later operations in that invocation.
External R5 result 10326dd116ccbfa90a70db4f4c8ec27487ee4fbf and code-only CHAT_ACCEPT
1ef5506d592cc7da9c93e61d86a158c12b9b27b3 are retained. R5 exit=1/no-replay unchanged.

A04 __main__.py control routes to desktop.control -> initialize_runtime ->
SQLiteLedger.initialize, which performs WAL/schema/claim_authority writes and
manual-consumption import. Thus the runner's preconsume comment calling these
checks read-only is false. This is a separate inspection-side-effect bug, not
the reason paused=false should be accepted. No initializations were called here.

The focused patch replaces only Safe's installed control CLI with stdlib-only
reading of config/database/WAL bytes, querying a private temporary copy, explicitly
closing its SQLite connection and deleting it, then requiring unchanged source
bytes and integrity. Source SQLite and sidecars are never opened by SQLite.
No Bridge import, initialization, state repair or authority write is performed.
Only whitelisted field summaries and failed field names are emitted.
All original safety requirements remain; missing fields and non-boolean flags
fail closed. Unknown/racing/unreadable/redirected state fails closed.
Temporary diagnostic copies are local transient files, not zero-disk-write probes.

## Validation
12 regression cases PASS: safe state; actual paused=false; unsafe state; invalid
boolean types; non-null dispatch (redacted); all four missing fields; active-WAL
snapshot with source DB/WAL/SHM byte equality; redirected config DENY.
PowerShell runner and diagnostic parser errors: 0.
The same reader independently diagnosed current host failed=["paused"].
Sandbox TEMP initially rejected test-copy creation; tests were rerun with an
explicit writable fixture TEMP parent. That first infrastructure failure is not
a test PASS. This is not an integrated lifecycle test.
Full validator was NOT_RUN. Installed files were not patched.

## Skills and source limitations
REQUIRED/APPLIED: execution-recovery, route-preflight, source-contracts, delivery.
APPLIED: publication-sync for this authorized non-main correction and readback.
NOT_APPLICABLE: prompt-builder/routing assignment/handoff; direct native bounded
repair, no Agent assignment or Dispatch. Result acceptance for new lifecycle:
NOT_APPLICABLE, no new lifecycle result exists.
The v0.5.3 README/current operating_rules replace the retired global routing
matrix with the three-layer standalone methods; these files were read.
The governance source-resolution path from older context returned 404 at the R5
review commit; no human/machine governance rebind, new authority, or broader
policy-effectiveness attestation is made. Diagnostic scope derives directly
from current Owner instruction and verified package/consumer bytes.

## Next safe action
Owner can run the supplied redacted diagnostic only. Keep validator on HOLD.
Reconcile why pause was disabled and ensure no Worker/F1/legacy writer exists
before any separately scoped pause/restoration decision and fresh preconsume
checks. Neither this patch nor absence of a claim authorizes automatic rerun.
A04 lifecycle remains FAIL/REWORK, R5 accepted code-only, G3/G4 NOT_RUN.
GOAL_MET: diagnosis and source correction; host validation goal remains unmet.

## Recovery completion — 2026-10-23, recorded 02:03:26 UTC
Owner explicitly instructed CHAT to continue after the concrete proposal to restore
pause through standard A04 control, verify, and stop before the validator.
The previously unreadable process was independently identified by Owner output as
codex-windows-sandbox-service.exe / CodexSandboxService.OpenAI.Codex, session 0.
The executed recovery freshly resolved this exclusion by exact process name AND
service PID; it did not whitelist unknown processes by session number or codex prefix.

A non-elevated host command directly executed the prepared restoration script.
Before mutation it verified: no Bridge/F1/legacy process, no task Bridge CODEX
writer, no WPF process, no internal claim/output, exact archive hash, current
pointer package/source inventory, all 40 installed Python modules against the
verified A04 wheel, and a stable current Safe snapshot failing only paused.
It invoked the installed A04 standard control pause command with captured,
non-disclosed raw stdout/stderr, then independently read a stable SQLite/WAL copy.

Observed PAUSE_RESTORED; Safe=true; state=STOPPED, paused=true,
setup_complete=true, present current_dispatch=null. Configuration and
manual_consumption bytes remained unchanged. Claim/output remained absent.
The standard pause command initializes the live ledger as previously documented;
this step is explicitly an authorized mutation, not a read-only operation.
No assertion of whole-database row equality is made.

PowerShell parser: 0 errors. Actual host restoration command exit: 0.
Validator NOT_RUN; lifecycle/uninstall/reinstall NOT_RUN; G3/G4/provider/broker/LIVE
NOT_RUN. No installed source patch, package rebuild, Dispatch or claim was created.
The new runner's source fix remains non-main and was not installed or executed.

CHAT verdict: DONE / CHAT_ACCEPTED for Unsafe-control diagnosis, source correction,
and pause restoration only. Whole-WP remains IN_PROGRESS / TEST and
INTERNAL_FOX2_BRIDGE_READY=NOT_ATTESTED.
REQUIRED/APPLIED: recovery, preflight, source-contracts, delivery; publication-sync
and result-acceptance applied for evidence publication and scoped intake.
Prompt-builder/Agent routing remain NOT_APPLICABLE; no delegation or new assignment.
Next safe action: fresh scoped preconsume and review of patched validator for the
separate integrated host validation; this recovery stops before that validator.
Do not replay consumed R5 or infer future admission from this point-in-time Safe.

Evidence: reports/FOX2-BRIDGE-RC1-TO-INTERNAL-READY/evidence/internal_validation/pause_recovery_20261023.json
Executed script: docs/agent_handoff/FOX2-BRIDGE-RC1-TO-INTERNAL-READY/internal_validation/restore_pause.ps1
