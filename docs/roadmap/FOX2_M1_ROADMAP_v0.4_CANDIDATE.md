# FOX2 M1 ROADMAP v0.4 — CHAT Planning Candidate (2026-10-12)

**Record status:** `CHAT_PREPARED / OWNER_DECISION_PENDING / NOT_EXECUTABLE`  
**Purpose:** Correct the observable status of the existing `FOX2_M1_ROADMAP_v0.3.md` and decompose P2; does not alter any already-approved BRD, release, authority, or code.  
**Not an effective supersession:** The official M1 roadmap v0.3 and BRD-00/06/08 v0.4 remain the approved source until this specific roadmap candidate is accepted/published through the applicable FOX2 process.  
**Applicable Policy:** FOX2 Policy V1.7.1 (`FOX2-POLICY-V1`), raw SHA-256 `9c8784781d13e05a59749e33a72b2912ed29a9398aadcc2034fc7b60e044c99d`, Git commit `ef3975952006868ef2fd4e64619ebdbf3cfc8411`.  
**Official M1 source:** Git `955e74ff67e6b4ed184dc2c2dcd4260c51dc529b`; M1 v0.4 document set released to Library (8/8) and mirrored to Git (8 plus 2 companions). Source-only readiness is not DEV readiness.  
**Status observation cutoff:** 2026-10-12, Git refs and Issue states checked when drafting; result branches may change after this immutable candidate is issued.

## 1. Goals and immutable scope

M1 delivers a **localhost equity market intelligence website** using the FOX2 Data Source Manager (DSM). No synthetic values may appear as real investor prices. Every visible market value has justified source, timestamps, rights and quality/freshness state; unavailable/unknown stays unavailable/unknown. The current accepted M1 business scope is limited to FOX2-BRD-00/06/08 v0.4, FOX2 Market Data Contract v0.4, schemas and acceptance matrix. BRD-01/02/03/04/05/07 algorithms, account/portfolio execution and LIVE broker operations are not approved by M1. FOX legacy is a **READ-ONLY technical reference** and no FOX code/history/policy carries over automatically.

**Technology baseline specified, not built:** FastAPI modular monolith; SQLite single-ingest-writer transactional store; React/TypeScript/Vite UI at localhost. Default `provider_enabled=false`, loopback-only, no public Internet deployment and no order/account endpoints. Fixtures are isolated to tests; never auto-fallback to synthetic prices in investor runtime. Watchlist PUT is localhost **preference only**, no broker write.

## 2. Verified current state vs legacy roadmap label

| Step | Scope | Observed state at cutoff | Next gate |
| --- | --- | --- | --- |
| **P0** | Owner-approved M1 v0.4 BRD/contract/schema/acceptance source | `DOCS_LIBRARY_PUBLISHED / GIT_SOURCE_READBACK_VERIFIED` at M1 source commit; **NOT** application acceptance. Roadmap v0.3 itself remains effective | Preserve source/hash; reconcile stale Issue #3 only after actual receipt comparison |
| **P1** | Windows/IDE/Git/reuse preflight and evidence | `RESULT_DELIVERY_VERIFIED=YES`, `ACCEPTED_PARTIAL` for recovery/delivery; historic Windows/FOX/DNSE observations unverified. Copilot result SHA `906adba0450781d1f8b05b0e9d471acf8a684f68`; Issue #5 OPEN | Minimal current FoxLe-PC evidence: host/WIP, four legacy-file SHA parity, market-only cache metadata, offline M1-A readiness. Reuse independent read-only Fox Git evidence; no wholesale P1 rerun |
| **P2** | M1-A backend, DSM, transactional store and API | `NOT_STARTED / CODE_ALLOWED=NO` | Accept P1 host/worktree readiness, verify task source and scoped DEV rights separately; then execute P2-01 → P2-04 with tests |
| **P3** | M1-A local website | `NOT_STARTED` | Freeze accepted API DTOs, separate UI branch/worktree and scoped DEV grant; build responsive Overview/Watchlist/Stock360/Source Diagnostics |
| **P4** | M1-A offline checkpoint | `NOT_RUN` | Tests of API/SQLite/prefs/UI security/gaps/state/restart; independent review risk-based; no real feed needed |
| **P5** | M1-B DNSE REST historical market slice | `BLOCKED_RIGHTS_AND_MAPPING` | Verify read, redisplay, retained-use rights and expiry, source schema/time/unit/basis, safe host/credentials; grant capability-limited read-only network access separately |
| **P6** | M1-B DNSE market-only WebSocket slice | `BLOCKED_RIGHTS_AND_HANDSHAKE_EVIDENCE` | Entitlements, auth/ACK, mapping, bounded queue, calendar/freshness criteria, scoped environment and risk review |
| **P7** | M1-B recovery and end-to-end checkpoint | `NOT_RUN` | Disconnect/restart/overflow/no-trade/normal-close/backfill/revision and data quality tests; independent acceptance |
| **M2** | Coverage, point-in-time, corporate actions and soak | `NOT_STARTED` | Separate post-M1 acceptance and change approval |
| **M3/M4** | Analytics, risk, capital, exit, shadow | `NOT_STARTED` | Own BRDs, safety/acceptance/rights and explicit task grants |

**P0 and P1 are not equivalent to P2 DEV authorization.** No runtime code or tests of FOX2 M1 currently accepted. Source and Git evidence may be reused without recopying. P1 current host state can only be certified by an authorized observed host check; CHAT cannot infer FoxLe-PC WIP or quota from Git.

## 3. M1-A implementation milestones

**P2 — backend first, P2-01 → P2-04.** Detailed task decomposition and gates in `FOX2_M1_P2_WP_PLAN_v0.1_CANDIDATE.md`. Limit one writer per file/worktree. Obtain a task-specific Owner DEV grant only after Policy/source/host/one-writer/role/model/quota gates are observed. If no grant, outputs remain planning docs. Prefer bounded offline fixtures and negative controls, no network to DNSE.

**P3 — UI after API shape has passed contract tests.** React/TS/Vite screens: `/overview`, `/watchlist`, `/stocks/:symbol`, `/settings/data-sources`. Later domains `/sectors`, `/discovery`, `/portfolio`, `/risk`, `/research` may show unavailable explanations rather than pretending completed engines. UI uses FOX2 API only, never DNSE directly. Render actual source, age/as_of, coverage, unit/basis/unknown, gaps and provisional state. Browser manual refresh by default. Responsive 1440/1024/390; no fake trend or zero-card for missing market values. Confirm Node/npm installation authority separately if absent; do not install under P1.

**P4 — independent M1-A acceptance gate.** Validate focused cases mapped to BRD00/06/08 and M1-A scope: provider-disabled/offline, rights blocked, no synthetic investor values, no account/order/write, UTC timestamps and genuine-zero semantics, persistence/atomicity/restart, optimistic watchlist `409`, invalid input `422`, loopback/Origin/Host, API error sanitization, browser no upstream calls, reviewable responsive UI. **No blanket 105/105 PASS:** immutable Acceptance Matrix v0.4 currently has 105 NOT_RUN: 65 M1-A/B, 22 later, 18 document. Select only applicable cases; all remaining explicitly NOT_RUN/NOT_APPLICABLE with explanation. Do not call P4 ACCEPTED from a development self-report.

## 4. M1-B rollout, separate provider gates

**P5 REST:** provider rights (`read`, `redisplay`, `retained_use`) and license/provenance/expiry; network/credentials authority; OHLC date/UTC, price/volume unit/basis and revision semantics; gap/no-progress pagination; store retention. Do not reuse `D:\Data\Fox` as FOX2 writing store or infer licensing from an old cache. Read-only public market only, not broker/account data.

**P6 WebSocket:** independently verify market-only auth and subscribe ACK, socket vs data readiness, heartbeat, duplicate/provisional/correction, queue overflow, normal 8-hour closure/reconnect, bounded retry, restart and fresh/UNKNOWN states. No implicit LIVE flag based on connected socket. Provider-specific limits are reference constraints to verify on actual subscription. No broker/order channel.

**P7:** full E2E evidence and separate acceptance. P5/P6 can be designed offline during M1-A, **but Production network calls remain disallowed** until exact capability grants and data-provider rights are verified. Do not merge/release/live from design approval.

## 5. Dependency/critical path and sequencing

`P1 evidence gate → P2-01 contract/foundation → P2-02 store → P2-03 DSM → P2-04 API/prefs/tests → P3 UI → P4 M1-A acceptance → P5 REST + P6 WS gated separately → P7 M1-B acceptance`.

CHAT may in parallel do a **read-only documentary** DNSE rights matrix and UI screen-contract review; these do not trigger Production access. Parallel P2/P3 or multiple coding Agents is deferred until immutable shared API DTOs, verified non-overlapping worktrees and explicit writer leases. No calendar deadlines committed without actual effort capacity.

## 6. Milestone release gates and STOP

1. `POLICY_CHECK` and `TASK_STATE_CHECK`: V1.7.1 effective, existing accepted reports reused, no unnecessary redo; P1 latest remote evidence checked.
2. `SOURCE_READY`: M1 v0.4 official source receipt and raw Git SHA pinned; required contractual change requires BCC/source rebind rather than undocumented drift.
3. `HOST_READY`: current OS/toolchain/origin/HEAD/tracked/untracked/ignored WIP, source parity, named writer, actual access and quota observed on target machine; missing critical proof means `UNKNOWN/BLOCKED` for execution.
4. `DEV_GRANT`: separate explicit scope/path/branch/role and `CODE_ALLOWED=YES` after gates. Owner planning approval and standing Copilot report authority **do not grant DEV**.
5. `REPORT_ONLY`: under FOX2 Policy C6F.2A, eligible Copilot can write/push sanitized `reports/<WP_ID>/**` when actual host/branch/writer rights PASS; does not grant code/main/merge.
6. `VALIDATION`: Result Contract v2, tests/negative evidence, 1 writer, full SHA remote readback, independent CHAT acceptance before next checkpoint. No source authority from FOX legacy.
7. `PROVIDER`: P5/P6 need separate documented third-party data rights and scoped network grants; `BROKER_WRITE=NO`, `LIVE=NO`, `MERGE_ALLOWED=NO` by default.

**Immediate next step:** Finish minimum P1 host evidence while CHAT freezes P2-01 spec and exact acceptance subset. When P1 host/readiness is actually accepted, assess Copilot vs Codex vs CHAT vs WORK (access, quota, quality, risk, total acceptance cost), and request the *separate* scoped code grant for the selected P2 WP. **STOP if branch owner/permissions or dev grant unknown.**

## 7. Publication and change control

This is a **CHAT-prepared planning candidate**, not an approved BRD revision or a Git-merged roadmap. Source immutable Policy/M1 versions above are references, not reissued documents. Prior roadmap v0.3 is retained unchanged. If Owner approves this candidate as operating roadmap, publish the exact accepted revision to the official FOX2 Roadmap Library path, independently read back bytes/hash, record supersession and mirror to the approved Git branch; only then label `ROADMAP_V04_RELEASED`. No DEV/merge permission follows from this publication. Any changed business requirement goes through BCC, not a silent roadmap edit.
