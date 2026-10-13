# FOX2 M1-P2-02 delivery result

Prepared for PUSHED_UNREVIEWED; successful push and exact remote SHA are reported separately. CHAT owns independent review and acceptance. No self-referencing commit SHA appears in this manifest.

## Task and authority

- Worktree: `C:\Projects\FOX2-worktrees\FOX2-M1-P2-02-CODEX`; created this run, clean at creation, CODEX-only task scope.
- Branch: `work/FOX2-M1-P2-02-store-codex`; initial local/remote HEAD `a99d50dd76af29deaf21e9a1a6a882b7e8047ca6`.
- Executable handoff: `a99d50dd76af29deaf21e9a1a6a882b7e8047ca6:docs/agent_handoff/M1/P2-02/FOX2_M1_P2_02_CODEX_EXECUTE_20261014.md`.
- Source/design lock: `e9e5749fbcebd392facfd06c96e38bf02a4b4e8c:docs/agent_handoff/M1/P2-02/FOX2_M1_P2_02_SQLITE_STORE_PREDEV_SOURCE_LOCK_20261014.md`; blob `55e8ebf6d09b02d1dc3d3b73ceb4c2c1333d348e`.
- Accepted P2-01 `4bbbdf02387727e7d3c6900f163d7b1eedc5e2b3` reused without implementation changes. Policy V1.8.5, Routing V1.2.6, Technical v0.1, P2 Plan v0.1, BRD-06 v0.5, Contract/schema and Acceptance v0.4 pinned in source_readback.json.
- Race check reused the preceding local precheck: exact branch HEAD, absent destination, no attached branch, no observable P2-02 writer/Bridge execution. Generic Agent runtime session targets remain incompletely observable; no collision observed. No package install.
- Agent: CODEX / operational; GPT-6 session identity, exact model variant/thinking/numeric quota NOT_EXPOSED. No model switch claimed; usage NOT_MEASURED.

## Delivered behavior

The stdlib SQLite repository implements the three frozen ports in store-owned files. Migration version 1, checksum `83e240072f775c894033ad458230c1041acf7651c0b9cc7e3e513fdbe1d5f468`. Ordered SQL statements execute in one transaction with schema/profile identity and checksum checks. Tampered, future or unrelated databases are refused. DELETE rollback journal, FULL synchronization, foreign keys, immutable-history triggers, series-scoped projection constraints and bounded busy timeout (default 250 ms) are explicit choices tested under close/reopen, concurrency and hard subprocess exits.

Receipt IDs/raw hashes and market IDs/fingerprints are separate. Canonical fingerprints exclude receipt/local revision, selection and rights metadata. Duplicate polls append receipt linkage without another market revision. Source revision labels remain original provenance. Per-bar batch revisions commit atomically, retain cumulative replacements and preserve RAW/ADJUSTED/source identity. The frozen singular batch CommitResult identifies the first input item and indicates whether any item promoted; receipt_records/selection_audit retain every item.

Trusted clock verification sets first_available_at; no provider/event/bar/envelope timestamp establishes availability. Trusted receipts have a bounded 0–5 second verification delay; original availability claims must be absent/current, except known duplicate availability. PIT reads use immutable promotion history and hide future-known corrections across restart. Current retained-use rights remain independent from the historical cutoff. Expiry/revocation blocks reads, polling cannot re-grant, and no unauthorized source fallback occurs.

Promotion requires explicit trusted local identity/lifecycle/calendar/context evidence and verified integer ordering; no provider ordering is inferred. Corrections require exact same-series/logical predecessor with increasing verified order; final-to-provisional cannot displace current. Newer same-series daily bars advance on verified chronology and nondecreasing evidenced order; quote events require newer market time and increasing order. Same-time events remain distinct and ambiguous. Missing evidence quarantines; invalid candidates reject; both preserve current. Multiple eligible series use Unavailable(UNKNOWN), as required by the frozen selector-free read port.

Watchlist compare-and-replace validates trusted instrument IDs, duplicates, size and version, then commits list/version/time atomically. Conflict/failure does not mutate; tests cover competing CAS writers and restart.

Paths are explicit FOX2-only roots outside Git, with legacy Data/Fox, symlink and junction rejection on each connection. Isolated-test and investor store profiles cannot mix. All tests use synthetic values and temporary DBs outside Git. No API/DSM/provider/Bridge/SFR/frontend implementation, credentials, real feed, private account information, PR, main merge, deployment or LIVE.

## Current validation

- p2_02: 97 passed in 8.37s
- p2_01_regression: 79 passed, 1 deselected in 1.96s

Executed commands and UTC/environment are in the manifest and JUnit/log evidence. Delivery runner: `python -B reports/FOX2-M1-P2-02/evidence/verify_delivery.py`. P2-02 command: `python -B -m pytest tests/p2_02 -p no:cacheprovider -q --tb=short --junitxml=reports/FOX2-M1-P2-02/evidence/p2_02.xml`. P2-01 command: `python -B -m pytest tests/p2_01 -k "not test_domain_dependency_boundary" -p no:cacheprovider -q --tb=short --junitxml=reports/FOX2-M1-P2-02/evidence/p2_01_regression.xml`.

One frozen P2-01 test asserts the store directory does not yet exist. Its expected P2-01-stage assertion fails at P2-02 and remains untouched; the relevant 79-test regression subset excludes it. P2-02 `test_domain_dependency_boundary_for_p2_02_stage` repeats its full domain import rules and provider/DSM exclusion while permitting the now-authorized store. Fresh-process network/import denial also passes. This exclusion does not claim the unchanged complete P2-01 suite passes at P2-02.

Failure history is explicit in quality.json: initial frozen DTO assignment/fixture serialization mistakes, same-batch ordering, contextual missing evidence and the obsolete stage assertion were resolved inside this scope. Required current suites pass. Temporary default-shell startup failure was resolved using installed explicit PowerShell; no platform security refusal occurred.

Integrity/FK/migration/syntax/allowlist/obvious-secret checks PASS. Network/provider/broker construction and socket/DNS attempts measured as zero in test denial regions. Git readback/push are the only authorized remote operations. All preexisting tracked files, including P2-01 code/tests and pyproject, are unchanged. Final staged whitespace/scope/secret/hash checks run before commit.

## Acceptance mapping

| ID | Status | Executed evidence |
| --- | --- | --- |
| FOX2-06-T10 | PASS offline subcase / PARTIAL canonical | test_poll_idempotency_receipt_identity_and_restart; test_correction_lineage_pit_replacement_and_exact_history; test_out_of_order_and_same_time_events_do_not_choose_arrival; test_series_isolation_and_ambiguous_read |
| FOX2-06-T11 | PASS offline subcase / PARTIAL canonical | test_correction_lineage_pit_replacement_and_exact_history; test_backdated_or_future_availability_rejected; test_trusted_receipt_processing_lag_does_not_backdate_verification |
| FOX2-06-T12 | PASS offline subcase / PARTIAL canonical | test_migration_reopen_and_integrity; test_committed_ingest_survives_process_restart; test_process_crash_rolls_back_hot_journal |
| FOX2-06-T17 | PASS offline subcase / PARTIAL canonical | test_each_ingest_stage_failure_rolls_back; test_reader_snapshot_is_old_until_writer_commits; test_second_bar_failure_rolls_back_entire_batch |
| FOX2-06-T21 | PASS offline subcase / PARTIAL canonical | test_correction_lineage_pit_replacement_and_exact_history; test_provisional_to_final_requires_lineage; test_ambiguous_finality_or_order_quarantines |
| FOX2-06-T23 | PASS offline subcase / PARTIAL canonical | test_rights_expiry_revocation_restart_and_no_fallback; test_changed_rights_are_not_a_market_revision |
| FOX2-N1-T05 | PASS offline subcase / PARTIAL canonical | test_series_isolation_and_ambiguous_read; test_cross_series_predecessor_rejected_atomically; test_unknown_basis_quarantine_not_merged |
| FOX2-N1-T06 | PASS offline subcase / PARTIAL canonical | test_backdated_receipt_and_clock_regression_rejected; test_correction_lineage_pit_replacement_and_exact_history |
| FOX2-N1-T07 | PASS offline subcase / PARTIAL canonical | test_rights_expiry_revocation_restart_and_no_fallback; test_blocked_candidate_cannot_displace_verified_projection |

All nine official IDs remain PARTIAL for full canonical scenarios; only listed offline subcases PASS. The schema has no PARTIAL acceptance enum, so manifest entries conservatively use NOT_RUN for the remaining canonical integrated obligations, with the local PASS reason/evidence.

## Limits and remaining gates

Trusted registry/clock/evidence are local injected dependencies, not provider certification. No source-selection adapter, rights re-grant workflow or application wiring is delivered. SQLITE FULL/DELETE durability is tested through forced process exit/reopen; physical power loss, real disk exhaustion and real provider timing/finality are NOT_RUN. Disk failures are injected deterministically. Rights and observations share a consistent transaction snapshot; later requests observe committed revocation.

CHAT immutable-SHA review and acceptance remain open. Integrated provider/store/DSM/API/frontend behavior, real licensing/LIVE, broker/account operations and deployment are NOT_RUN/outside scope. Commit command: `git commit -m "feat(p2-02): add atomic SQLite versioned store and offline evidence"`. Push: `git push origin HEAD:refs/heads/work/FOX2-M1-P2-02-store-codex`; readback: `git ls-remote origin refs/heads/work/FOX2-M1-P2-02-store-codex`. STOP after successful verified PUSHED_UNREVIEWED.
