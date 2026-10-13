# FOX2 — CODEX EXECUTION HANDOFF — M1-P2-02 SQLITE VERSIONED STORE

**Date:** 2026-10-14  
**WP:** `FOX2-M1-P2-02`  
**Status:** `EXECUTABLE / DEV_AUTHORIZED_TASK_BOUND / STOP_AT_PUSHED_UNREVIEWED`  
**Owner direction:** proceed after the P2-02 local READ-ONLY precheck returned `PRECHECK=PASS`.  
**Priority:** make FOX2 runnable locally; no broad re-audit and no repeat P1/P2-01.

## 0. CHAT routing / grant

Routing result:

- R0: PASS — P2-01 accepted; reuse exact upstream result.
- R1: P2-02 implementation.
- R2: Policy V1.8.5 / Routing Index V1.2.6; offline M1-A only.
- R3: CODEX usable; model/thinking/quota may remain `NOT_EXPOSED`; numeric quota invisibility alone is not a blocker.
- R4: CODEX selected for transaction/revision/concurrency complexity. COPILOT remains on disjoint Bridge scope and must not write P2-02.
- R5: precheck reports target local worktree absent and safe to create; no material writer collision observed. Recheck only immediate race-sensitive facts before mutation.
- R6: immutable P2-02 source/design lock readback PASS.
- R7: one whole-WP bounded execution; stop only on material blocker or final delivery.

After the immediate local race check below passes, this handoff activates exactly:

```text
CODE_ALLOWED=YES_FOR_FOX2_M1_P2_02_ONLY
GIT_CODE_PUSH=YES_OWN_TASK_BRANCH_ONLY
GIT_REPORT_WRITE=YES_TASK_RESULT_ONLY
GIT_REPORT_PUSH=YES_TASK_BRANCH_ONLY
PR_CREATE=NO
MERGE_ALLOWED=NO
DNSE_PRODUCTION=NO
BROKER_WRITE=NO
LIVE=NO
```

No additional Owner confirmation is required for unchanged internal P2-02 implementation/test checkpoints.

## 1. Immutable source lock

Repository:

`dunglt2505/FOX2`

Task branch:

`work/FOX2-M1-P2-02-store-codex`

Accepted upstream P2-01:

`4bbbdf02387727e7d3c6900f163d7b1eedc5e2b3`

P2-02 PRE-DEV source/design lock:

`e9e5749fbcebd392facfd06c96e38bf02a4b4e8c:docs/agent_handoff/M1/P2-02/FOX2_M1_P2_02_SQLITE_STORE_PREDEV_SOURCE_LOCK_20261014.md`

Source-lock blob:

`55e8ebf6d09b02d1dc3d3b73ceb4c2c1333d348e`

Read that source-lock document completely. It is normative for identity, PIT, revision, promotion, transaction, migration, rights, watchlist CAS and negative-test semantics.

Current released governance:
- FOX2 Policy V1.8.5 RELEASED_EFFECTIVE
- FOX2 Routing Index V1.2.6 EFFECTIVE_DERIVATIVE
- M1 Technical Spec v0.1
- P2 WP Plan v0.1
- BRD-06 v0.5
- Market Data Contract/schema v0.4
- Acceptance Matrix v0.4

Do not re-open or rewrite these sources.

## 2. Local worktree

Preferred path:

`C:\Projects\FOX2-worktrees\FOX2-M1-P2-02-CODEX`

The previous precheck observed this path as `ABSENT_SAFE_TO_CREATE`.

Immediately before creation:
1. fetch/read the task branch;
2. confirm it is not attached to another worktree;
3. confirm the destination still does not contain WIP;
4. confirm no active P2-02 writer/Bridge execution has appeared;
5. confirm remote branch HEAD equals the immutable executable handoff commit supplied by CHAT/Issue #12.

If all pass, create/attach exactly this worktree to exactly this task branch.

Do not reuse the P2-01 worktree. Do not reset, clean, stash, rebase or mutate another worktree.

## 3. Exclusive write scope

Allowed implementation:

- `backend/src/fox2/store/**`
- `tests/p2_02/**`

Allowed result delivery:

- `reports/FOX2-M1-P2-02/report.md`
- `reports/FOX2-M1-P2-02/evidence_manifest.json`
- `reports/FOX2-M1-P2-02/evidence/**`

Everything else is READ-ONLY.

Especially do not edit:
- `backend/src/fox2/ports/**`
- `backend/src/fox2/contracts/**`
- `backend/src/fox2/validation/**`
- `backend/pyproject.toml`
- API, DSM, provider, frontend
- Bridge or SFR
- governance/docs
- `.github/**`
- official BRD/Contract/Acceptance files.

Use Python stdlib `sqlite3`; do not add a package solely for SQLite.

If a frozen P2-01 interface is genuinely insufficient, STOP with `BLOCKED_INTERFACE_CONFLICT`; do not silently modify it.

## 4. Required implementation

Implement a FOX2-only SQLite store with versioned migrations and transaction-safe repositories.

Required logical persistence:
- schema/migration metadata;
- instruments;
- observations;
- bar revisions;
- current projection;
- gaps;
- selection audit;
- rights registry;
- watchlist preferences;
- ingest receipt/audit identity sufficient for deterministic idempotency and traceability.

Internal table/column/index layout is implementation-owned, provided the source-lock invariants and tests hold.

### 4A. Market identity vs receipt identity

Keep receipt/audit identity separate from market identity.

An identical repeated poll:
- may create a new ingest receipt/audit;
- MUST NOT create a new market revision;
- MUST NOT advance the current revision.

A changed provisional update or proven correction:
- appends an immutable local revision;
- never overwrites earlier revision bytes/history.

RAW / ADJUSTED / UNKNOWN basis series never silently merge or cross-promote.

Do not assume timestamp alone uniquely identifies multiple same-time events.

Do not fabricate provider `source_revision`.

### 4B. first_available_at / PIT

Persist actual local first availability using a trusted/injectable local clock/evidence path.

Never backdate availability from provider event time, bar start, generated_at or user-supplied historical value.

A correction observed later has its own later first availability.

`get_observation(..., at_or_before=T)` may return only data actually locally available by T.

Later corrections must remain invisible to earlier PIT cutoffs after close/reopen/restart.

The frozen StoreReadPort lacks source/basis selection. If multiple eligible series make the read ambiguous, return the existing explicit `Unavailable(UNKNOWN)`; do not choose arbitrarily and do not change the port.

### 4C. Promotion

Current projection is series-scoped.

Promotion may occur only when precedence/finality/correction is deterministically evidenced.

Do NOT use these as arbitrary tie-breakers:
- received_at alone;
- record_id;
- hash lexical order;
- source string alphabetical order;
- writer execution order;
- lexicographic provider revision unless its ordering semantics are explicitly proven.

Out-of-order history may be retained but must not regress current.

Ambiguous/finality-unknown candidates remain auditable/quarantined and leave the current pointer unchanged, with typed reason such as existing `AMBIGUOUS_ORDER` / unavailable outcome semantics.

No invalid, entitlement-blocked or synthetic-investor candidate may displace a valid current projection.

### 4D. Atomicity and concurrency

One ingest transaction atomically covers the applicable:
- immutable observation/revision insertion;
- current projection update/retain decision;
- ingest audit/receipt;
- associated safe metadata needed by this ingest.

On failure, all roll back and the previous valid current pointer remains.

Use foreign keys and integrity checks so a current pointer cannot become orphaned.

Use a bounded SQLite busy timeout. One intended ingest writer owns material writes; competing writer attempts must serialize safely or return a typed bounded failure without corruption.

Readers must see transaction-consistent snapshots.

Never perform provider/network await inside a DB write transaction.

No process-global mutable `last_metadata` style state.

Use WAL only if chosen deliberately and covered by restart/concurrency tests.

### 4E. Migrations

Migrations are:
- ordered;
- versioned;
- checksummed;
- idempotent where appropriate;
- transactional;
- safe after close/reopen/interrupted attempt;
- refusing unknown/incompatible future schema;
- refusing tampered migration history.

No destructive repair of legacy/non-FOX2 DBs.

All tests use temporary FOX2-owned databases outside Git.

### 4F. Rights-retained-use boundary

Persist rights evidence/expiry needed for local retained-use protection.

Expired/revoked retained-use blocks unauthorized local cached reads using existing typed unavailable semantics.

Do not make P2-02 the DSM. P2-03 owns final source/use-context selection; the store may enforce only stricter safe boundaries.

### 4G. Watchlist persistence

Implement the already-frozen `PreferenceRepositoryPort.replace_if_version(expected_version, items)` behavior without changing the port.

Atomic CAS must:
- check expected version;
- validate IDs through trusted local instrument knowledge/registry;
- reject duplicate, unknown and >100 items;
- replace the list;
- increment version;
- set updated_at;
- commit all of the above atomically.

Stale version or DB failure must not mutate list/version.

Persist across restart.

No HTTP route or UI behavior in P2-02.

## 5. Required acceptance/test evidence

Official existing IDs in scope:

- `FOX2-06-T10`
- `FOX2-06-T11`
- `FOX2-06-T12`
- `FOX2-06-T17`
- `FOX2-06-T21`
- `FOX2-06-T23`
- `FOX2-N1-T05`
- `FOX2-N1-T06`
- `FOX2-N1-T07`

These are P2-02 offline/backend sub-evidence. Do not mark integrated/provider full scenarios PASS unless actually proven at their later checkpoints.

At minimum test:

1. initial migration and reopen;
2. migration checksum tamper/future schema rejection;
3. failure injection before/after transactional stages with full rollback;
4. no orphan current pointer after failure/reopen;
5. identical poll idempotency;
6. receipt-id conflict;
7. immutable correction lineage;
8. out-of-order candidate retained without pointer regression;
9. ambiguous finality/order leaves prior current;
10. cumulative fields replace rather than double count;
11. RAW/ADJUSTED cross-series isolation;
12. PIT cutoff excludes later-known revision;
13. first availability cannot be backdated/restamped after restart;
14. rights expiry/revocation blocks retained local read;
15. writer busy/collision bounded behavior;
16. reader/writer transaction-consistent snapshot race;
17. close/reopen/restart preserving revisions/current/audit;
18. multiple same-time identities do not collapse solely by timestamp;
19. watchlist CAS success/stale conflict/invalid/unknown/duplicate/>100;
20. watchlist rollback and restart persistence;
21. no provider/network activity;
22. legacy FOX writable-store path prohibited;
23. no secrets, licensed raw feed or private account data in Git.

Use deterministic offline fixtures only.

Do not claim actual provider semantics.

## 6. Test and quality commands

Use already-installed Python/pytest/SQLite only.

Run the scoped P2-02 suite and any necessary P2-01 regression subset that is read-only and fast enough to demonstrate no interface regression.

Recommended minimum:
- `python -B -m pytest tests/p2_02 -p no:cacheprovider -q --tb=short`
- relevant `tests/p2_01` regression suite if current runtime allows it without package/network changes;
- syntax/import checks;
- `git diff --check`;
- staged-path allowlist verification;
- obvious-secret scan of changed/result files;
- DB integrity/foreign-key check and migration checksum evidence;
- explicit proof of zero provider/broker network activity for this WP.

Record exact command, versions, UTC, source commit and result.

Do not invent PASS for a test not executed.

## 7. Result Contract

Write sanitized task result only under:

`reports/FOX2-M1-P2-02/**`

Required:
- `report.md`
- `evidence_manifest.json`
- optional hashed evidence files below `evidence/**`

Result must distinguish:
- CODEX-reported local facts;
- exact test execution evidence;
- NOT_RUN integrated/provider/UI obligations;
- known limitations/remaining gates.

Before commit:
- inspect worktree/staging;
- verify every changed path is inside the exact allowlists;
- run required current tests;
- run `git diff --check`;
- confirm no secret/private/licensed raw feed exposure.

Commit only on:
`work/FOX2-M1-P2-02-store-codex`

Push only that branch.

Read back the exact remote full SHA.

Final state:
`PUSHED_UNREVIEWED`

CHAT performs independent GitHub readback and decides acceptance.

## 8. STOP conditions

STOP and preserve WIP on:
- immutable handoff/source mismatch;
- unexpected branch/worktree attachment or writer collision;
- unreviewed WIP appearing before creation;
- actual platform safety refusal;
- actual Codex unavailability/quota exhaustion;
- missing required installed tool requiring unapproved install;
- frozen port/interface conflict;
- need to modify an out-of-scope file;
- required test failure not resolvable inside scope;
- transaction/PIT/rights invariant cannot be made deterministic from frozen contract;
- secret/private/licensed feed exposure;
- push failure or remote SHA cannot be verified.

Do not bypass the blocker.

## 9. Required final return

```text
FOX2 M1-P2-02 DELIVERY RESULT

EXECUTION_STATE:
  PUSHED_UNREVIEWED
  | BLOCKED_SOURCE
  | BLOCKED_WORKTREE
  | BLOCKED_WRITER
  | BLOCKED_INTERFACE_CONFLICT
  | BLOCKED_TEST
  | BLOCKED_SCOPE
  | BLOCKED_PUSH
  | BLOCKED_OTHER

SOURCE_LOCK:
EXECUTABLE_HANDOFF:
WORKTREE:
BRANCH:
INITIAL_REMOTE_HEAD:
FINAL_LOCAL_HEAD:
REMOTE_HEAD:

MODEL:
THINKING:
QUOTA:

MIGRATION_VERSION:
SQLITE_RUNTIME:
STORE_PATH_POLICY:
NETWORK_PROVIDER_ACTIVITY:

CHANGED_CODE_PATHS:
REPORT_PATHS:
TEST_COMMANDS:
TEST_RESULTS:
P2_01_REGRESSION:
TRANSACTION_ROLLBACK:
PIT_FIRST_AVAILABILITY:
IDEMPOTENCY:
PROMOTION_RULES:
RIGHTS_RESTART:
WATCHLIST_CAS:
CONCURRENCY:
SECRET_SCAN:

ACCEPTANCE_SUBCASES:
NOT_RUN:
COMMIT:
PUSH:
RESULT_REPORT:
EVIDENCE_MANIFEST:
OPEN_GATES:
STOP_REASON:
```

No PR, main merge, deployment, DNSE Production, broker write or LIVE.
