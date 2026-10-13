# FOX2 — M1-P2-02 SQLite Versioned Store | PRE-DEV Source & Design Lock

**Date:** 2026-10-14
**WP:** `FOX2-M1-P2-02`
**Status:** `DESIGN_LOCKED_FOR_LOCAL_READBACK / CODE_ALLOWED=NO / GIT_CODE_PUSH=NO`
**Owner request:** “Do it” — freeze P2-02 identity, migration, atomicity, promotion and acceptance scope; inspect source and writer before executable code assignment.
**Execution priority:** runnable localhost M1-A, without reopening accepted P2-01 or expanding M1-B.
**Upstream P2-01:** `P2_01_OFFLINE_FOUNDATION_ACCEPTED`, remote commit `4bbbdf02387727e7d3c6900f163d7b1eedc5e2b3`, reviewed at GitHub Issue #8 comment 6150994812. Integrated acceptance remains PARTIAL.

## 1. Source authority and task base

New/re-scoped WP authority:
- FOX2 Policy **V1.8.5 RELEASED_EFFECTIVE**, Git commit `63c9c0e86ba8892f96566189def63cb8afe33cf2`, path `docs/governance/FOX2_POLICY_V1.8.5.md`, blob `5b38b6bd6776b5ef3a771ba2297f4565c2d9abed`.
- FOX2 Routing Index **V1.2.6 EFFECTIVE_DERIVATIVE**, same Git source tree, path `docs/governance/FOX2_AGENT_PROMPT_POLICY_V1_2_6_EFFECTIVE_ROUTING_INDEX_20261013.md`, blob `263966d1c5e0eb3900a73c2f1327312f2cf94ec9`.
- M1 Technical Specification **v0.1 RELEASED_EFFECTIVE**, frozen in P2-01 base `588da7b1c1a642ddfd935ff6372af83a35acaa2f`, path `docs/architecture/FOX2_M1_TECHNICAL_SPEC_v0.1.md`, blob `e4a95b97039d482085996afbfad232b789d1b236`.
- M1 Roadmap **v0.4**, path `docs/roadmap/FOX2_M1_ROADMAP_v0.4.md`, blob `ed842860259628cb1404b3a9fa7ad9e28eaa326c`.
- P2 WP Plan **v0.1 OWNER APPROVED DESIGN**, path `docs/roadmap/FOX2_M1_P2_WP_PLAN_v0.1.md`, blob `6612f7d05b4724be396214e5446eb685e58979c9`.
- BRD-06 **v0.5 RELEASED_EFFECTIVE**, path `docs/brd_mirror/FOX2-BRD-06_v0.5.md`, blob `ee912b39cd009ba89a50cb28e4a3a6e76b52b5df`; implements `FOX2-06-R04/R11/R17/R20`.
- Market Data Contract **v0.4**, `docs/data_contracts/FOX2_MARKET_DATA_CONTRACT_v0.4.md`, blob `369a893a83dd140ce423c032784941a22d4a443e`; JSON schema `docs/data_contracts/FOX2_MARKET_DATA_v0.4.schema.json`, blob `fa395662b772658d782b46718b7eb8392f6bbf76`.
- Acceptance Matrix **v0.4**, `docs/acceptance/FOX2_M1_ACCEPTANCE_v0.4.csv`, blob `0e7ff73eb58e11bba4b513f84199e96f0c0d6193`.
- Accepted P2-01 code base is exactly `4bbbdf02387727e7d3c6900f163d7b1eedc5e2b3`. In particular, preserve `backend/src/fox2/ports/store.py`, `ports/preferences.py`, `ports/outcomes.py`, `contracts/market.py`, `validation/schema.py` and `validation/semantics.py` as read-only interfaces.

These source identities were read from GitHub before source-lock publication. Their inclusion here does **not** claim that a Windows coding-host/worktree or Library was independently probed in this turn.

## 2. Bounded deliverable and file ownership

Implement only SQLite local persistence for public market observation revisions, point-in-time (PIT) store reads, migration/versioning, audited ingest, transactional current projection, deterministic crash/duplicate handling, gaps/rights registry and local watchlist preference repository.

**Proposed exclusive code allowlist (conditional, not active):**
- `backend/src/fox2/store/**` — store implementation, SQL schema and migrations, migration metadata
- `tests/p2_02/**` — isolated offline tests and sanitized fixtures

**Proposed Result Contract v2 allowlist (conditional):**
- `reports/FOX2-M1-P2-02/report.md`
- `reports/FOX2-M1-P2-02/evidence_manifest.json`
- `reports/FOX2-M1-P2-02/evidence/**`

All other paths are read-only. In particular **no modification** to P2-01 DTOs/ports/validators, `backend/pyproject.toml`, API routes, `frontend/**`, `agent_bridge/**`, `source_freshness/**`, `docs/**`, `.github/**`, the official Acceptance CSV or Market Data Contract. Stop for CHAT scope review if an existing frozen port proves incompatible rather than quietly altering it. Preserve accepted P2-01 code unchanged.

Never import or write legacy FOX store (`D:\Data\Fox` or another legacy path). Application store root must be explicit, FOX2-only, outside Git; tests use temporary isolated DB files. No network or provider client.

## 3. Frozen identities and idempotency

**Receipt/audit identity is NOT market identity.**
- An ingest receipt uses unique `IngestAudit.audit_id`, `received_at` (trusted local receipt UTC), `raw_sha256`, append/attempt status, sanitized reason and candidate linkage. Repeat receipt id with different raw hash is a conflict, never an overwrite.
- Market series key for a BARS item includes: `capability=BARS / source_id / origin_provider / instrument_id / venue / board_id / timeframe / price_basis / adjustment_version (where adjusted)`. A logical bar identity adds `start_at` with the verified time/calendar mapping. Distinct RAW, ADJUSTED, UNKNOWN basis or adjustment series **must not** silently join.
- Quote/INDEX observations use capability-scoped identity and immutable observation IDs; never derive tick uniqueness from timestamp alone. Source/provider revision remains provenance, not locally fabricated source revision.
- Store-owned immutable `record_id` and increasing **local** revision are separate from provider `source_revision`. Derive a canonical **market-content fingerprint** from normalized market value/finality/provenance fields; exclude polling receipt id/timestamp and process-generated envelope time from equivalence. Store original immutable payload and source metadata sufficient for exact reconstruction/traceability.
- Identical repeated polling of an unchanged market-content fingerprint may append an ingest audit/receipt, but **must not append another market revision or increase the current revision**.
- A changed provisional update or provable correction appends an immutable local revision; never mutate or erase previous versions. Cumulative volume/turnover updates **replace** cumulative values, never add them as increments.
- A BARS payload containing multiple items is decomposed into independently keyed bar revisions and committed consistently in a single bounded ingest transaction; unknown or ambiguous identity must be rejected or quarantined, not merged across series.

## 4. First availability and PIT semantics

- `event_at`, `as_of`, `received_at`, `first_available_at` and `bar.start_at` have distinct roles. `event_at`, `bar.start_at` or `generated_at` NEVER establish local availability.
- On a **new** observation/correction, set persisted `first_available_at` from trusted actual **local first receipt/verification** evidence captured at ingestion; never copy a past provider timestamp or accept user-supplied historical `first_available_at` as proof. Use an injectable trusted clock in tests; reject impossible future/backdated availability claims and preserve the actual local first-seen timestamp.
- Duplicate receipts never reset earliest availability of an identical immutable revision. Correction receives its own new first-availability instant.
- A PIT read at `at_or_before=T` may return only a revision with true persisted `first_available_at <= T`; later-observed corrections are invisible to earlier cutoffs. Preserve old revision and unmodified earlier projection across restart.
- Current-time rights/retained-use must be checked separately from the historical PIT cutoff. A past valid snapshot does not authorize read after rights expiry or revocation.
- The current P2-01 `StoreReadPort.get_observation(instrument_id, capability, at_or_before)` has **no source/basis selector**. It must not choose arbitrarily among multiple allowed series: return explicit `Unavailable(UNKNOWN)` until P2-03 defines an unambiguous selection context. Do not silently change the frozen port.

## 5. Deterministic promotion and state machine

A current projection key is **series-scoped**, never global per display symbol. Transactional candidate path:

`RECEIVED -> SHAPE/SEMANTIC_CHECK -> IDENTIFIED -> INSERT_REVISION_OR_DEDUP -> PROMOTE_OR_RETAIN -> AUDIT_COMMIT`

- Only valid and evidenced quality/rights/mapping candidates can be eligible for promotion; isolated-test fixtures remain in separate test stores and can never leak into investor mode.
- For **different bar starts in the same series**, a verified chronologically newer eligible bar can advance the pointer. Out-of-order older bars are retained as history, not promoted merely because they arrived later.
- For **the same logical bar**, a positively verified advance from provisional to eligible final, or a correction with explicitly verified ordering/lineage, may promote to a new revision. A claimed closed flag, local arrival time or lexicographic `source_revision` alone is NOT conclusive provider/exchange finality or correction precedence.
- If finality, revision ordering, rights, mapping, quality or calendar validation is absent/ambiguous, append a safe quarantined/auditable candidate **without promoting** and mark partial/unknown/gap reasons. Preserve previous valid current pointer.
- Where evidence cannot prove deterministic precedence, **do not break ties by received_at, record_id, SHA, alphabetical source ID or arbitrary writer order**. Keep current unchanged and record `AMBIGUOUS_ORDER`.
- No time/basis/source crossover promotion. An invalid/synthetic-for-investor/entitlement-blocked candidate can never displace a valid projection.
- Valid current projection is either absent or points to an existing immutable observation/revision of the exact same series; foreign key and transactional constraints prohibit orphans.

These promotion conditions are local offline invariants, **not** certification of DNSE provider ordering/finality.

## 6. Transaction, migration and concurrency lock

- SQLite schema includes `instruments`, `observations`, `bar_revisions`, `current_projection`, `gaps`, `selection_audit`, `rights_registry`, `watchlist_preferences` and migration/version tracking. Specific internal columns/indexes are the implementing Agent's responsibility as long as invariants, FK/check/unique rules and tests below hold.
- Migrations must be versioned, ordered, idempotent, transactional and checksummed, refusing incompatible future schema and inconsistent migration history. Reopen after interrupted migration must be safe; no destructive migration or repair of non-FOX2 data.
- All observation/revision/current/audit mutation of one ingest is **one atomic write transaction** (`BEGIN IMMEDIATE` or equivalent), with foreign keys on, bounded busy timeout and explicit rollback on any validation/SQL/disk failure. Never commit an orphan pointer or half an ingest.
- One ingest writer owns writes; API/DSM readers use separate connections and consistent snapshots. No network await while holding a write transaction; no process-global mutable `last_metadata`/current result on concurrent requests. Concurrent writers either serialize safely within bounded wait or return a typed unavailable/busy outcome without corruption.
- SQLite WAL may be used where safe; select a durability configuration whose crash/restart behavior is actually tested. No blanket infinite retry, uncontrolled background threads or silent transaction retries.
- Store-level `rights_registry` must preserve evidence and expiry; read using `LOCAL_STORE`/retained-use blocked or expired returns `Unavailable(RIGHTS_BLOCKED)` rather than stale cached payload. DSM owns final use-context/source selection at P2-03; this store may only enforce stricter safe boundaries.
- P2-02 owns the `watchlist_preferences` DB migration **and** `PreferenceRepositoryPort.replace_if_version` repository atomic compare-and-replace: expected_version, verified IDs (via a trusted, locally provided instrument registry), version increment, new item list and `updated_at` commit in one transaction. Duplicate, unknown, >100, or stale version must not mutate data. P2-04 owns HTTP status mapping/UI service; no HTTP routes in P2-02.

## 7. Frozen negative acceptance matrix (offline subset only)

The following **nine existing IDs** are verified present in `FOX2_M1_ACCEPTANCE_v0.4.csv`; do not invent or rename IDs or mark full canonical/provider scenarios PASS:

| ID | Required P2-02 sub-evidence |
|---|---|
| `FOX2-06-T10` | duplicate/out-of-order/correction/revision lineage, separate RAW/ADJUSTED identities |
| `FOX2-06-T11` | PIT cutoff excludes future-known correction; never backdate first availability |
| `FOX2-06-T12` | local immutable revision/current/audit survives close/reopen without restamping |
| `FOX2-06-T17` | atomic ingest rollback at injected stages; no cross-request mutable metadata |
| `FOX2-06-T21` | provisional/cumulative replacement, final/correction lineage, no double count |
| `FOX2-06-T23` | restart and rights expiry/revocation prevent unauthorized retained-use cache read |
| `FOX2-N1-T05` | RAW/ADJUSTED never concatenate or cross-promote |
| `FOX2-N1-T06` | fetch/correction observed today cannot appear before first local availability |
| `FOX2-N1-T07` | revoke/expire rights blocks cached result, not replaced by unauthorized fallback |

Also mandatory **WP-local negative tests** (map to the above IDs, not new official IDs): migration checksum/future-version reject; interrupted transaction/reopen; wrong unique/foreign key; no-upsert mutable history; receipt hash conflict; multiple same-time ticks; duplicate poll idempotence; malformed candidate; ambiguous finality; source/basis crossover; writer-lock collision/busy timeout; reader/writer atomic snapshot race; failure injection before/after each write stage; rollback without orphan pointer; CAS preference conflict and restart; provider network=0; legacy FOX write forbidden; no secrets or synthetic investor fallback.

Every test receipt states environment, date, exact command, source/contract identity and hashed evidence. Mark offline subcases PASS only with actual test proof; canonical integrated/provider acceptance remains PARTIAL/NOT_RUN.

## 8. Agent comparison, reserved lane and execution STOP

**R0:** P2-01 offline result already accepted; do not re-implement. **R1:** P2-02 PRE-DEV source/design lock. **R2:** Policy V1.8.5 + current source; no provider/broker/LIVE authority. **R3:** CODEX runtime model/thinking/remaining quota and local toolchain not independently observed (`NOT_EXPOSED/UNKNOWN`); numeric hidden quota is not itself a blocker when Agent works. **R4:** CHAT owns design, source and Git review; COPILOT is capable of routine SQLite but currently occupies disjoint Bridge lane, CODEX preferred for transactional identity/correction/race complexity; WORK optional for a **specific failed/high-risk** checkpoint, not a mandatory broad audit. **R5:** Remote source and branch reservation verified separately; **local worktree, dirty/untracked/ignored WIP, writer processes, actual Git credentials remain UNKNOWN pending coding-host check**. **R6:** This immutable Git task doc must be read back at exact commit/blob before any executable prompt; P2-01 upstream commit pinned. **R7:** planned CODEX; **no executable DEV assignment before local source/ownership/rights PASS**.

- Target execution path: local Bridge -> **Codex CLI** only when Codex relay is actually proven; bounded MANUAL_LOCAL/Codex CLI is permitted fallback for this offline bootstrap task without converting the architectural target. VS Code is optional and not an execution requirement.
- Remote coding branch: `work/FOX2-M1-P2-02-store-codex`, **based on accepted P2-01 commit `4bbbdf02387727e7d3c6900f163d7b1eedc5e2b3`**; this CHAT-authored source lock document may be the sole pre-DEV doc commit on that branch. Preserve this doc; no competing Agent writes to it.
- **Proposed** exclusive CODEX local worktree: `C:\Projects\FOX2-worktrees\FOX2-M1-P2-02-CODEX`. Not established merely by Git branch creation.
- CODEX Model: current supported Codex CLI model, `NOT_EXPOSED` if hidden; Thinking: **Medium suggested**, escalate to High only if transactional/concurrency analysis actually warrants, and only if selectable/within credits. COPILOT must not write P2-02 concurrently.
- Minimum coding-host check: exact branch/current SHA, worktree path ownership + tracked/untracked/ignored WIP, no concurrent writer/lock, installed Python/pytest/SQLite, ability to use source references, test and push permissions for **only** proposed paths, actual platform permission. Reuse already accepted host evidence; test only changed facts.
- **STOP before code:** branch/worktree identity mismatch; existing unreviewed WIP; writer collision; missing essential tools or Git rights; task/spec authority drift; a required change to frozen ports/outside allowlist; actual Agent unavailable/quota exhausted; platform safety refusal. Record exact blocker rather than bypassing it.
- **After distinct task-bound DEV grant:** implement one entire P2-02 WP, run tests and negative controls, commit and push only this work branch plus approved result paths, return `PUSHED_UNREVIEWED` with exact SHA, 2-file Result Contract and CHAT readback. Do not self-merge, auto-deploy or claim M1 integrated PASS.

## 9. Scope/gate snapshot at document issue

```text
P2_01_OFFLINE_FOUNDATION=ACCEPTED
P2_02_SOURCE_DESIGN=LOCKED_FOR_PREDEV
P2_02_REMOTE_BRANCH=RESERVED_ON_P2_01_ACCEPTED_BASE
P2_02_LOCAL_WORKTREE=UNKNOWN
P2_02_LOCAL_SINGLE_WRITER=UNKNOWN
P2_02_AGENT_HOST_CREDENTIALS=UNKNOWN
CODE_ALLOWED=NO
GIT_CODE_PUSH=NO
PR_CREATE=NO
MERGE_ALLOWED=NO
DNSE_PRODUCTION=NO
BROKER_WRITE=NO
LIVE=NO
```

**This is a source/design-lock record, not proof of a Windows local precheck or DEV execution.**
