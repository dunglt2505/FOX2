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
