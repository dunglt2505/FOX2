# FOX2 Attempt03 â€” BLOCKED engineering result

Attempt: FOX2-BRIDGE-MANUAL-LOCAL-ADMISSION-DEV-20261019-NATIVE-OFFLINE-ATTEMPT-03.
Whole-WP: FOX2-BRIDGE-RC1-TO-INTERNAL-READY. Same infrastructure WP; no micro-WP.

Engineering stopped before implementation under pinned prompt sections 3 and 6: the legacy restart lifecycle and durable shared identity authority are unproven. No production or test source was modified. MANUAL_LOCAL remains unimplemented and unaccepted. This result is for independent CHAT review, with no release/adoption permission.

The admitted start is 3167d8502588dd106f9a4cea8ef931e9148040ff on the exact CODE branch. Initial worktree was clean, origin matched dunglt2505/FOX2, and fresh ls-remote matched start HEAD. Task, prompt, design and receipt object hashes match their bindings. Handoff remote head is 26c112885a22752b47878b6b05bb61d65cae8631; its separately published admission was read. Source bindings and hashes are recorded in diff_trace.json. Supplied HOST_ATTESTATION is the bounded launch/mutex evidence; no independent model/effort/quota telemetry is claimed. This invocation is consumed; no replay or additional coding invocation was performed.

## Concrete safety findings

- desktop.py initialize_runtime (lines 30â€“64) snapshots only when the current DB is absent, temporarily holds the legacy lock, and imports only the current-root manual marker. Existing current databases ignore later legacy consumed identities and both valid/corrupt legacy markers.
- ledger.py claim_dispatch (lines 388â€“440) uses BEGIN IMMEDIATE and duplicate checks in one database. Its control checks do not cover another database. Direct ledger callers bypass startup-only reconciliation.
- e2e_runner.py run_once (around line 829) correctly requests honor_controls=True before checkpoint/adapter work, but receives the same one-database claim decision.
- Two sequential fresh fixture processes reproduced the hard case: current initialized from legacy, claimed under its current root lock, then exited; a freshly started legacy process acquired its own lock and claimed the SAME identity. Both claim calls returned true with process exit code 0. This is a safety FAIL, not a successful no-replay test. Exact inline probe source, process outputs and time are in test_summary.json.

A current-root durable fence alone cannot change what an already frozen legacy executable does after restart. A double lock only excludes cooperating processes while held. No evidence in the admitted bundle identifies and durably retires every legacy launcher/executable/root alias or establishes a protocol jointly understood by both versions. The host coding mutex is not that runtime identity authority. Offline fixture claims of retirement would not supply that missing evidence.

## Exact K1 dependency and next action

ledger.py claim_dispatch requires a sound shared authority, and desktop.py initialize_runtime requires both-root reconciliation plus evidence of retirement. Both are allowed dependencies, but their correctness depends on a contract for the legacy lifecycle. startup.py set_start_with_windows and installation.py setup call initialize_runtime; process_lock.py releases its OS lock at process exit. These files were inspected read-only. They do not provide a durable retirement proof; editing process_lock.py alone would not change the frozen legacy binary.

CHAT/host must bind verifiable legacy executable/startup/supervisor/root identities and durable retirement evidence, or specify an authority actually honored by both versions. Any necessary edit outside the ten-path scope needs a separate exact K1 binding. No new path expansion is assumed. A future task must distinguish strict UNKNOWN/BLOCKED denial from positive VERIFIED admission, cover direct claims and crash/restart, and be separately admitted as a new attempt. Full MANUAL_LOCAL acceptance remains blocked.

## Tests and evidence

Fresh focused suite: 210 PASS, 34 FAIL, exit 1 (244 collected). The six historical negative cases failed for the expected missing cross-root enforcement. The other 28 failures were in test_preexec.py; a diagnostic reproduced GIT_OPERATION_FAILED because git show returned exit 128 and Filename too long for the nested Windows fixture path. A follow-up module run uses process-local core.longpaths=true, without modifying any Git config file. That rerun passed all 65 tests with exit 0 in 102.64 seconds, confirming the path-length diagnosis for the baseline PreExec failures. Its exact outcome is recorded in test_summary.json and the manifest. Original failures remain preserved.

The initial command failed at collection (exit 4) because the package was not installed; the corrected command set PYTHONPATH to agent_bridge/src. This setup failure is preserved separately. PYTHONDONTWRITEBYTECODE=1 and -p no:cacheprovider were used. Existing fixtures fake paid adapter capability probes; synthetic tests use disposable roots/local bare remotes. No real Agent integration, provider, installed ledger, Worker or protected Dispatch test was performed.

Historical six identities/meanings and source blob 7b2a2c48e6bf4225d849dc7a7a32126652b0c3be remain unchanged. New simultaneous dual-root concurrency, migration crash windows, exhaustive marker-missing/corrupt combinations, and positive provably fenced MANUAL_LOCAL acceptance are NOT_RUN after engineering STOP; existing focused regressions do not substitute for those missing acceptance cases. No historical PASS count is reused.

Only four result files are added. diff_trace.json classifies their material contents as JUSTIFIED_GENERATED, with exact consumers, tests and risks. The manifest follows Result Schema v2; evidence hashes bind the report, test summary and trace. Its own changed-path hash is null to avoid self-reference. The source_manifest_sha256 field binds diff_trace.json, which contains immutable source object bindings. Fixture credential strings in traceback text are redacted explicitly; raw-output hashes are retained for provenance.

## Delivery and protected state

Submit only on the exact non-main CODE branch, fast-forward, for CHAT review. The observed remote result SHA is returned outside these files after push/readback. Committed delivery metadata is an Agent assertion to be independently checked, not CHAT acceptance. No main, merge, install, Worker resume, provider, broker or LIVE action. No previous attempt worktree, marker, receipt, report history or PreExec file was edited. Canary009 HOLD, COMPAT001 PUBLISHED_HOLD and original Bridge bootstrap BLOCKED are preserved as task restrictions, not independently re-attested installed status.
