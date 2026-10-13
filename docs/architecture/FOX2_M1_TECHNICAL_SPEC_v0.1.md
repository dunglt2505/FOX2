# FOX2 — M1 Technical Specification v0.1

**Document ID:** `FOX2-M1-TECH-SPEC`  
**Version:** `0.1`  
**Status:** `RELEASED_EFFECTIVE / NO_DEV`  
**Purpose:** Define HOW the approved M1 business/data requirements are implemented without owning business meaning.  
**Business owners:** BRD-00/06/08 released v0.5; released v0.5 is the current BRD source set; v0.4 remains immutable historical provenance.  
**Interface contract:** Market Data Contract/schema v0.4 unchanged.  
**Planning source:** released Roadmap v0.4 + P2 WP Plan v0.1; WORK design redlines already incorporated there.

## 1. Authority boundary

This Technical Specification owns implementation mechanisms only. It cannot:

- create DEV/Git/provider/broker/LIVE permission;
- redefine BRD requirements or acceptance meaning;
- redefine Market Data Contract semantics without its own change process;
- mark acceptance tests PASS;
- supersede released BRDs by itself.

If Technical and BRD conflict, stop and resolve through the owning BRD/Contract change process.

## 2. M1 technical architecture

M1 target is a localhost modular application with:

- Python/FastAPI backend;
- typed domain/DTO validation layer;
- SQLite local persistence with one ingest writer;
- DSM application/domain service for source selection;
- provider adapters disabled by default in M1-A;
- React/TypeScript/Vite frontend after API shape is stable;
- isolated test fixtures only;
- loopback/local-only default runtime.

Dependency direction:

`UI → FOX2 API/application service → DSM → Store/Provider ports`

Domain DTO/validators do not depend on FastAPI, SQLite or provider SDK. Store does not depend on DSM/router/provider. Provider transport is not constructed/used when disabled.

## 3. Technical modules

Proposed module groups (exact paths remain WP-scoped):

- `contracts`: market, health, instruments, watchlist DTOs;
- `validation`: schema/shape and semantic validators;
- `ports`: store, DSM, preference/provider interfaces;
- `store`: SQLite schema/migrations/repositories;
- `dsm`: source capability evaluation/selection/diagnostics;
- `provider`: DNSE REST/WS adapters, only in separately authorized phases;
- `api`: loopback market/health/watchlist routes;
- `ui`: Overview/Watchlist/Stock360/Data Sources;
- `tests`: P2/P3/P4 scoped test suites and fixtures.

## 4. Data Contract use

Use `FOX2_MARKET_DATA_CONTRACT_v0.4.md` and its JSON schema as the canonical interface/data contract.

Implementation must keep **shape validation** separate from **semantic validation**. Schema PASS does not prove positive quote price, OHLC bounds, time ordering, rights, basis, gap completeness or PIT correctness.

DTO families are separate:

- `MarketDataEnvelope`;
- process/source health;
- instrument/search;
- watchlist preference.

Do not apply market-observation schema to health/preferences/search payloads.

## 5. DSM implementation

DSM chooses sources by typed capability (`QUOTE`, `BARS`, `INDEX`, and later approved capabilities) and use context.

At each service/read/selection, DSM reevaluates applicable rights/expiry, provenance, mapping, unit/basis/time/calendar, freshness and relevant gaps. A cached positive decision cannot outlive revoked/expired rights.

Provider disabled means **no provider transport construction or network call**, including startup, refresh, retry, scheduler or backfill.

No synthetic fallback into investor runtime.

Each decision emits a sanitized selection/audit identity and reason; missing observation/source IDs/timestamps remain null according to the Data Contract.

## 6. SQLite observation store

SQLite is the initial M1 persistence mechanism.

Technical invariants:

- schema/migration versioning;
- one bounded ingest writer;
- append/revision model for real observations;
- deterministic market identity separated from receipt/audit identity;
- `first_available_at` records actual first local observation of a revision/correction and is never backdated;
- identical polling may create receipt/audit evidence but must not mint a market revision;
- current projection promotes only a deterministically verified newer/final/corrected valid revision in the same identity/basis series;
- ambiguous/out-of-order data does not silently regress current state;
- observation/revision/current pointer/ingest-audit mutation is atomic;
- rollback retains previous valid current state;
- no DB write transaction across network await;
- readers observe transaction-consistent state;
- request-local metadata cannot use shared mutable `last_metadata` style state;
- FOX legacy cache is read-only reference, never FOX2 writable store.

Indicative entities: instruments, observations, revisions, current projection, gaps, selection audit, rights registry and watchlist preferences. Exact schema is a Technical/WP artifact, not BRD text.

## 7. Provider / WebSocket implementation

Real DNSE transport belongs to M1-B or later separately authorized provider tasks.

Technical design must preserve distinct REST vs WS authentication/semantics, explicit auth/subscription confirmation, bounded provider limits, reconnect/re-auth/resubscribe, finite queues/backpressure and separate control heartbeat from market callback processing.

Provider connection/socket success alone never means data capability READY. Auth, desired subscriptions, confirmed subscriptions, transport health and data freshness are separate states.

Historical bar recovery cannot be labeled restored tick continuity.

Provider-specific implementation inputs are pinned in this Technical Specification appendix rather than left in an unnamed future adapter document. They remain technical design inputs, not proof of current provider capability.

## 8. Provider mapping implementation

Preserve raw provider precision and separately normalize only after accepted field/unit/basis semantics exist. Do not infer price multipliers from examples.

Cumulative fields must not be summed as per-event increments. Provisional/open-bar updates replace/update the same logical bar; closed-provider bar does not automatically mean adjusted/exchange-final semantics.

Time fields preserve their documented meaning (event, start, update, received) and UTC-normalized representation where contract requires it.

## 9. API design

Initial approved route family from current M1 planning:

- `GET /api/health`
- `GET /api/data-sources/health`
- `GET /api/market/overview`
- `GET /api/stocks`
- `GET /api/stocks/{symbol}`
- `GET /api/stocks/{symbol}/bars`
- `GET /api/watchlist`
- `PUT /api/watchlist`

These are technical/API-shape decisions, not new BRD requirements.

Behavioral rules:

- unknown resource → sanitized 404;
- invalid query/body → 422;
- valid resource but unavailable capability may return typed unavailable semantics without fabricated data;
- unsafe store/service failure → sanitized 503;
- no account/order endpoints;
- no history-to-quote fallback;
- no raw licensed/private/provider secret leakage.

Exact status/payload details remain subject to Data Contract/API contract freeze.

## 10. Watchlist implementation

P2 store layer owns watchlist persistence schema/migration/repository. API/UI layer owns preference service and user behavior.

`PUT` uses optimistic compare-and-replace semantics: version check, list replacement, version increment and updated timestamp occur atomically. Stale version produces conflict without lost update; invalid/unknown/duplicate/>100 items are rejected; DB failure rolls back with unchanged list/version.

Mutation does not call broker/provider.

Loopback Host/Origin and JSON content-type guards apply to mutating local preference endpoints.

## 11. Frontend implementation

Target pages/routes:

- `/overview`
- `/watchlist`
- `/stocks/:symbol`
- `/settings/data-sources`

Future `/sectors`, `/discovery`, `/portfolio`, `/risk`, `/research` may display unavailable explanations until their engines are accepted.

UI calls FOX2 API only. It never calls DNSE directly or reads local DB. It renders server-provided source/state/time/basis/gap semantics and does not calculate trading signals/risk/net money flow independently.

Responsive verification targets remain 1440, 1024 and 390 widths. Exact component/chart library is implementation lockfile scope.

## 12. Refresh/network behavior

Default browser refresh is manual unless an approved polling budget/capability is configured. Conditional GET/cache-revision may be used. Browser refresh does not directly trigger provider backfill. Historical backfill is a DSM/backend responsibility with bounded scheduling.

When provider is disabled, no UI action may create an upstream provider call.

## 13. Security boundaries

- loopback/local-only default;
- no secret/token/provider topic URL in frontend bundle/log/error;
- no private account facts in public market path;
- no broker/order/cash/margin endpoints;
- sanitize error/diagnostic payloads;
- fixtures/test connectors are runtime-isolated from investor mode.

## 14. Technical state model

DSM/provider implementation may use technical runtime states such as `DISABLED → CONNECTING → AUTHENTICATING → SUBSCRIBING → SYNCING → READY`, plus reconnect/degraded/blocked states. These are Technical mechanisms implementing BRD capability semantics; they do not replace BRD-facing FeedStatus/Data Contract states.

## 15. Test strategy and acceptance evidence

Canonical Acceptance Matrix v0.4 remains unchanged. Technical tests produce evidence **for** those IDs but do not redefine them.

P2-01 focuses DTO/validators/offline startup/security boundary; P2-02 store/transaction/revision; P2-03 DSM/source state/no-network; P2-04 API/watchlist/offline integration; P3 frontend; P4 M1-A checkpoint; P5–P7 provider/WS/M1-B.

Backend sub-evidence never marks UI/WS/provider full scenarios PASS. Each result records test ID, covered subcase, environment/source, evidence and remaining obligation.

## 16. Phase and authority gates

- M1-A can be developed/tested offline without DNSE Production rights.
- M1-B provider work requires separate read/redisplay/retained-use/network/secret/mapping/calendar/freshness gates.
- Technical Spec approval is not DEV authorization.
- Each WP still requires source-ready, host/writer/Agent capability and scoped DEV authorization under active governance.

## 17. Open technical locks before DEV

Before P2-01 execution, freeze exact task source, DTO/interface signatures, allowed paths, acceptance subset and writer/worktree. Before P2-02, freeze observation identity/revision/current-promotion semantics. Provider tasks remain blocked until rights/mapping/runtime evidence is available.

## 18. Revision disposition

This v0.1 release consolidates HOW material previously embedded across BRD-00/06/08 v0.4 and the released P2 planning design. It does not create new business requirements. WORK should later verify semantic completeness against the mapping before publication.

## 19. Pinned provider technical appendix — inherited from BRD-06 v0.4

**Released technical source:** commit `955e74ff67e6b4ed184dc2c2dcd4260c51dc529b`, `docs/brd_mirror/FOX2-BRD-06_v0.4.md`, sections `FOX2-06-R18` and `FOX2-06-R19`.  
**Reference implementation evidence:** Fox commit `740051933ec4fbf29180d0f5fb698c34e8c91ece`; DNSE SDK commit `aa55a5117de2534707bca6165b6738e1cc6fc6a4`; provider guide `https://developers.dnse.com.vn/docs/guide/market-data/connect/`.

Inherited technical design inputs:

- Production WS base: `wss://ws-openapi.dnse.com.vn`; SDK path `/v1/stream?encoding=json|msgpack`.
- Expected flow: welcome → `action=auth` → `auth_success` → subscribe `channels[{name,symbols}]` → explicit subscription confirmation. Send-success alone is not subscription readiness.
- WS signing is distinct from REST signing; the inherited design records HMAC hex over `api_key:timestamp:nonce`. Do not silently reuse REST Date/Base64 semantics.
- Initial bounded slice: explicit `G1`, one equity and `1D` history/realtime continuity path. release channels include `tick.G1.json`, `security_definition.G1.json`, `ohlc.1D.json`, `ohlc_closed.1D.json`, `market_index.VNINDEX.json` and `market_index.VN30.json`. Intraday `1/5/15` and other board/resolution coverage require separate evidence/tests.
- Provider limits/timers inherited as **unverified runtime inputs**: connection lifetime up to 8h; provider examples describe server PING about every 3 minutes and PONG deadline about 1 minute; 10 connections/user and 200 streams/connection. These values must be revalidated against the pinned guide/SDK/observed handshake before capability certification and must not be reused as market-data stale thresholds.
- Transport control heartbeat is separate from market callback processing. Slow consumers cannot block control heartbeat; queues are finite and overflow/out-of-order conditions create explicit gap/recovery state.
- Precision/mapping: preserve Seconds/Nanos raw precision; validate Nanos `0..999999999`; do not use floating timestamps as identity. `matchQtty` is per-trade while `totalVolumeTraded` is cumulative. OHLC `time` is bar start and `lastUpdated` is update time. Provisional open-bar updates replace/update the same logical bar; provider-closed does not imply adjusted/exchange-final semantics.
- Gap recovery is capability-scoped: historical bars may recover bar completeness but do not prove restored tick continuity.
- No secret-like SDK literals, UAT/private subscription, broker/account method or raw provider log is copied into investor runtime.

These inputs are **pinned inherited technical design**, not runtime PASS. Any changed endpoint/signing/channel/limit/codec requires evidence and impact review; unresolved mapping blocks only the affected provider capability.