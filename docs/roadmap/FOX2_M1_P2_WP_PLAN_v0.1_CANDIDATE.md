# FOX2 M1-A P2 — Executable Work-Package Design v0.1 (CHAT Candidate)

**STATUS:** `SPEC_PREPARED / NO_EXECUTION_ASSIGNMENT / CODE_ALLOWED=NO` · **Policy:** FOX2 V1.7.1 · **Source:** M1 BRD v0.4 git `955e74ff67e6b4ed184dc2c2dcd4260c51dc529b` · **Roadmap:** `FOX2_M1_ROADMAP_v0.4_CANDIDATE.md` · **Prepared:** 2026-10-12.

## 1. Inputs, ownership, no implicit authorizations

- BRD: FOX2-BRD-00/06/08 v0.4; Change ID `FOX2-BCC-M1-DSM-20261011-v04`.
- Market API/spec: `docs/data_contracts/FOX2_MARKET_DATA_CONTRACT_v0.4.md` + `docs/data_contracts/FOX2_MARKET_DATA_v0.4.schema.json` at frozen M1 source SHA.
- Acceptance: `docs/acceptance/FOX2_M1_ACCEPTANCE_v0.4.csv` (105 records, all NOT_RUN), plus change-to-requirement map. Apply only cases covering each WP.
- Current repo root at CHAT planning baseline includes `backend/.gitkeep`, `frontend/.gitkeep`, `tests/.gitkeep`, `fixtures/.gitkeep`, no accepted implementation. Existing user worktree and future folder contents **must be re-observed** before granting any file allowlist.
- `GIT_SOURCE_READY=YES_FOR_M1_V04_ONLY` is documentation; `CODE_ALLOWED=NO`, `GIT_CODE_PUSH=NO`, `PR_CREATE=NO`, `MERGE_ALLOWED=NO`, `DNSE_PRODUCTION=NO`, `BROKER_WRITE=NO`, `LIVE=NO` for this plan. Standing C6F.2A covers **report files only**.

## 2. Work-package breakdown and sequencing

| WP | Deliverable | Proposed implementation scope (verify exact paths again before grant) | Prerequisites | Acceptance evidence | Status |
| --- | --- | --- | --- | --- | --- |
| `FOX2-M1-P2-01` | Backend foundation, typed public market DTO/contract validation, loopback safeguards, health diagnostics, configuration | `backend/**`, WP-specific `tests/**`, only mutually owned contract/fixture paths after source freeze | P1 host readiness, locked API contract, named single writer, exact DEV grant | Offline startup + contract/schema/negative tests; provider disabled/no network; no secret exposure | `SPEC_PREPARED_NO_DEV` |
| `FOX2-M1-P2-02` | SQLite versioned observation store, immutable revisions, single writer, transaction and migration | scoped new `backend/**/store/**`, scoped `tests/**`; **must not overlap P2-01 active writer** | Accepted P2-01 interfaces + dedicated writer/worktree | atomic rollback/restart/UPSERT vs append revision/correction, no backdating, malformed input and race/one-writer negative tests | `SOURCE_PENDING_P2_01` |
| `FOX2-M1-P2-03` | DSM source selection/capability gates and source diagnostics; offline stubs only | scoped `backend/**/dsm/**`, `tests/**`, sanitized fixtures | Accepted P2-02 store API + P2-01 DTOs | provider disabled, missing rights or mapping/freshness → UNKNOWN/UNAVAILABLE; no synthetic fallback, no provider network calls, audit decisions | `SOURCE_PENDING_P2_02` |
| `FOX2-M1-P2-04` | Read-only API service wiring and local watchlist preference store + end-to-end offline negative tests | scoped `backend/**/api/**`, `tests/**`, local preference migration; no frontend changes | Accepted P2-03; contract endpoints frozen | response shapes/errors, sanitized 404/409/422/503, restart preferences, max100, origin/host loopback guards, no account/order endpoints | `SOURCE_PENDING_P2_03` |

**Ownership rule:** Table paths are **proposals**, not blanket write rights. Before each executable handoff, CHAT must bind exact pre-existing file inventory, task-specific allowlist and forbidden paths, source SHA, task branch/worktree, tests/evidence, one-writer ownership and a separately authorized `CODE_ALLOWED=YES`. No parallel writers to `backend/**` or `tests/**` without verified disjoint file paths/worktrees. No task can redefine a canonical BRD or market contract.

## 3. WP acceptance details and negative tests

### P2-01 — Foundation / API Contract

- Type-check and validate Market Data Contract v0.4 envelope `{contract_version, request_id, generated_at, data}`; keep data observation timestamps distinct from response creation timestamp.
- FastAPI loopback `127.0.0.1`, provider/network disabled by default. GET health and public diagnostics return explicit sanitized states; inaccessible input must return `UNAVAILABLE`/`UNKNOWN`, not fabricated prices.
- Reject accidental provider-secret environment echo, upstream network at offline startup, broker account or order routes, synthetic fixture imports from investor runtime.
- Evidence: pinned contract hash, command/version/log summary, passing offline unit/schema/negative tests, zero unexpected network attempt under measured offline harness, security checks of route table.
- Example case mapping **subject to exact CSV review**: `FOX2-00-T01/T02/T03/T04`, `FOX2-06-T05/T13/T14/T16/T18`. Include status per case, never blanket PASS.

### P2-02 — Transactional Store

- SQLite tables for `instruments`, `observations`, `bar_revisions`, `current_projection`, `gaps`, `selection_audit`, `rights_registry`, `watchlist_preferences`; schema version/migration. A real market observation is append-only/revisioned; no synthetic into production store.
- Transactional ingestion: either all observation/revision/current/audit commit, or none. Protect one writer. `first_available_at` is observed availability; corrections cannot rewrite history; source and unit/basis stay tagged `UNKNOWN` absent proof.
- Negative: interrupted transaction, duplicate/correction/out-of-order records, simultaneous writes, restart with expired rights, no pointer without observation, never read/reuse legacy Fox writing store.
- Evidence: migration/checksum/version, deterministic offline fixtures and rollback/race tests, persisted record identity hashes, restart verification.
- Suggested mapped cases: `FOX2-06-T10/T11/T12/T17/T21/T23`, with provider-dependent cases explicitly deferred if actual rights needed.

### P2-03 — DSM Source Selection

- Separate network availability, rights (`read`, `redisplay`, `retained_use`), observed freshness/calendar, unit/time/basis mapping and per-capability status. No `LIVE` without valid source and requirements; `PROVIDER_NATIVE_UNVERIFIED` is diagnostic only.
- Offline sources only in P2; isolated fixtures in test harness. No transparent fallback from missing provider to synthetic investor values. Every decision records `selection_audit_id`, rejected candidates and reason codes without private data.
- Negative: provider disabled, entitlement expired, stale snapshot, missing mapping/calendar, quote/historical mismatches, no-trade vs outage, incomplete bars with gaps and unknown time basis.
- Evidence: source-decision matrix per capability, negative tests with source/set/revision, no-network proof, repeatable diagnostic trace.
- Suggested mapped cases: `FOX2-06-T02/T03/T04/T07/T08/T09/T15/T16/T18`, `FOX2-N1-T01/T02/T07/T09`; restrict any WS/Production-specific execution to later P6.

### P2-04 — API, Watchlist, Offline Integration

- Implement only approved endpoints: `GET /api/health`, `GET /api/data-sources/health`, `GET /api/market/overview`, `GET /api/stocks`, `GET /api/stocks/{symbol}`, `GET /api/stocks/{symbol}/bars`, `GET/PUT /api/watchlist`.
- Provider-down valid symbol yields status-safe envelope with `UNAVAILABLE/STALE`; unknown symbol 404; invalid query 422; unsafe store 503. Search bound length/limit/cursor, watchlist `expected_version`, max100 verified IDs, duplicate/invalid 422, conflict 409, atomic persistence across restart.
- Enforce loopback Host/Origin and JSON content-type on preference PUT. Browser will only call backend in P3. No profile broker write, token/secret exposure, phantom quote from historical close, or blocked account endpoints.
- Evidence: HTTP contract snapshots, negative-case/status test logs, restart persistence, no secret/reference leak, scoped Git diff and immutable result receipt.
- Suggested cases: `FOX2-08-T01/T02/T04/T05/T07/T10/T11/T13/T14`, `FOX2-06-T13/T14`, `FOX2-00-T03/T05`. UI-responsive cases `FOX2-08-T08/T09/T12` belong to P3, not P2.

## 4. Routing and handoff control (R0–R7)

- **R0 Task State:** No P2 code accepted; P1 result received and CHAT delivery-verified at `906adba0450781d1f8b05b0e9d471acf8a684f68`, P1 acceptance still partial. Do not reopen P0 source recovery without evidence of drift.
- **R1 Stage:** Planning and candidate source publication only. Do not promote to implementation by a work-package label.
- **R2 Policy/rights:** FOX2 Policy V1.7.1 effective, approved M1 v0.4 source exists, but `CODE_ALLOWED=NO` for P2 and no provider entitlement/merge/live grant. STOP on unknown rights for affected operation.
- **R3 Agent eligibility:** Copilot VS Code Windows previously provided Git report push; current model/mode/quota and coder/writer permissions remain **UNKNOWN**. Codex repository/host availability and quota also **UNKNOWN** until verified. WORK audit access risk-based, CHAT available for drafting.
- **R4 Comparison:** CHAT prepares/finalizes source/spec. COPILOT contender for P2-01 and P2-04 (routine Python/VS Code/Git, cost). CODEX contender for P2-02/03 (transactional state/invariants) but do not route by label alone; compare actual model, quotas, access, test competence and cost per safe acceptance, explicitly including both COPILOT and CODEX. WORK review only if concurrency/atomicity/security risk gate warrants; no blanket audit. No executable assignment in this candidate.
- **R5 Writer:** Reserve one writer at a time; verify real branch, worktree, WIP (tracked/untracked/ignored), path lease and branch protection before code. Path patterns in §2 are not yet owner-approved allowlists.
- **R6 Source/Handoff:** Effective Policy Git SHA+Library release, M1 BRD/contract/matrix source SHA, per-WP immutable task/source manifest, Report Contract v2 and report destination. A new task must record accepted upstream WP result commit and required dependencies.
- **R7 Selected plan:** CHAT prepares 4 bounded WPs; first possible DEV candidate is P2-01 **only after** accepted P1 host gate, exact scoped Owner DEV decision, Copilot/Codex comparison and technical credentials/one-writer proof. STOP on missing mandatory gates, data-license unknown, WIP collision, source mismatch, failure of negative tests.

## 5. Definition of Done for a future executable WP

1. Owner/CHAT has pinned exact accepted scope, full BRD+contract SHA and acceptance subset. No unapproved changes to BRD/DTOs.
2. Agent's actual model/mode, access, quota, branch, worktree and writer rights observed; explicit path-specific `CODE_ALLOWED=YES` recorded **separately** for that WP.
3. Build/test outputs persisted with raw hashes, run UTC/environment/source commit and negative controls; independent schema/semantic tests as applicable.
4. No secrets, licensed market feed, accounts/credentials or prohibited changes; Git diff only within approved allowlist and non-main branch; no `merge` unless separately granted.
5. Report+manifest satisfy Result Contract v2 at immutable commit; CHAT independently checks ancestry/hash/diff/evidence and records `ACCEPTED` or other disposition. Downstream WP starts only on accepted prerequisites, not self-reported DONE.

## 6. Precise next administrative steps (not an Agent dispatch)

1. Complete Issue #5's small FoxLe-PC P1 evidence delta; CHECK current branch/host/WIP/legacy hash parity. CHAT independently adjudicates P1 suitability for P2-01.
2. Freeze exact P2-01 source/contract and acceptance subset, including tests folder ownership. Record candidate/task source manifest after actual approval, not before.
3. Compare Copilot, Codex, CHAT, WORK on actual capability/access/model/quota and risk; document cost-based choice. This proposal does not itself approve either coding Agent.
4. Ask Owner for a **separate narrowly scoped implementation authorization** when evidence is sufficient. No implicit CODE_ALLOWED, code push, merge, Production, broker or LIVE.
