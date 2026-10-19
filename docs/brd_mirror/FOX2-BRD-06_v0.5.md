# FOX2-BRD-06 — Data Foundation & Data Source Manager

**Version:** `0.5`  
**Status:** `RELEASED_EFFECTIVE / NO_DEV`  
**Change type:** `STRUCTURAL_SEPARATION_NO_BUSINESS_SEMANTIC_CHANGE`  
**Parent released BRD:** `FOX2-BRD-06 v0.4` at `955e74ff67e6b4ed184dc2c2dcd4260c51dc529b`  
**Technical counterpart:** `FOX2_M1_TECHNICAL_SPEC_v0.1.md`  
**Data contract:** Market Data Contract/schema v0.4 unchanged  
**Acceptance source:** Acceptance Matrix v0.4; IDs unchanged, runtime `NOT_RUN`

## 1. Purpose and ownership

BRD-06 owns FOX2 market-data truth: instrument/calendar facts, data provenance, source capability/rights/quality states, source-selection semantics, storage semantics visible to consumers and the DSM domain boundary.

This BRD specifies **required behavior and invariants**. Provider protocol details, module design, SQLite schema, concurrency mechanism, route layout, retry strategy and other HOW decisions belong to the M1 Technical Specification.

## 2. User and consumer outcomes

- FOX2 has one Data Source Manager (DSM) boundary for market-data source selection.
- Consumers do not independently choose or connect to DNSE/WebSocket/local storage.
- Real provider data is usable only when rights, provenance, mapping, quality/freshness and requested capability allow it.
- Missing/blocked/partial/stale data remains explicit; synthetic fixtures never silently replace investor data.
- Public market data and any future private account data remain separated.

## 3. Functional requirements

| Requirement | Normative outcome | Primary output | State | Acceptance IDs |
|---|---|---|---|---|
| `FOX2-06-R01` | Every market datum preserves source, event/receipt/as-of semantics, session, quality/finality and unit/basis information required by the Data Contract. | `MarketDataEnvelope` | `SPECIFIED_APPROVED` | `FOX2-06-T18`, `FOX2-06-T24` |
| `FOX2-06-R02` | Feed/source states such as LIVE, PERIODIC_LIVE, LATEST_VALID, EOD_CONFIRMED, STALE, GAP_RECOVERING, DELAYED, ENTITLEMENT_BLOCKED and UNAVAILABLE must reflect reality. | `FeedStatus` | `SPECIFIED_APPROVED` | `FOX2-06-T06`, `FOX2-06-T07`, `FOX2-N1-T02` |
| `FOX2-06-R03` | Session/calendar semantics are venue/version aware; no fake bars are created for midday/no-trade periods. | `TradingCalendar` | `SPECIFIED_APPROVED` | `FOX2-06-T03`, `FOX2-N1-T09` |
| `FOX2-06-R04` | Duplicate, out-of-order, reconnect/backfill and provider corrections preserve deterministic lineage, revisions and explicit gaps. | `FeedPipeline` | `SPECIFIED_APPROVED` | `FOX2-06-T10`, `FOX2-06-T19`, `FOX2-06-T20`, `FOX2-06-T21`, `FOX2-06-T22` |
| `FOX2-06-R05` | Account/private snapshots are distinct from public quote state and must not share an unsafe public cache scope. | `BrokerSnapshotBoundary` | `SPECIFIED_APPROVED` | `FOX2-06-T13` |
| `FOX2-06-R06` | Secrets/credentials remain protected; missing data rights never justify scraping, source forgery or secret exposure. | `SourceEntitlement` | `SPECIFIED_APPROVED` | `FOX2-06-T09`, `FOX2-06-T16` |
| `FOX2-06-R07` | M1 exposes no broker order/cancel/amend/cash/margin capability. | `NoBrokerWrites` | `SPECIFIED_APPROVED` | `FOX2-06-T05`, `FOX2-06-T16` |
| `FOX2-06-R08` | DSM is the sole source-selection owner and consumers use the FOX2 data service boundary rather than direct provider connections. | `DataSourceManager` | `SPECIFIED_APPROVED` | `FOX2-06-T15`, `FOX2-08-T08` |
| `FOX2-06-R09` | Any DNSE production path is subject to verified entitlement, provenance, schema/mapping and read-only isolation. | `DNSEProviderBoundary` | `SPECIFIED_APPROVED` | `FOX2-06-T16`, `FOX2-06-T24` |
| `FOX2-06-R10` | Source selection considers requested capability, freshness/calendar/revision/availability and returns an auditable decision. | `SourceSelectionDecision` | `SPECIFIED_APPROVED` | `FOX2-06-T06`, `FOX2-06-T07`, `FOX2-06-T08`, `FOX2-06-T11` |
| `FOX2-06-R11` | Local persistence supports approved historical/recovery use while preserving provenance and original availability/freshness semantics across restart. | `VersionedLocalMarketStore` | `SPECIFIED_APPROVED` | `FOX2-06-T12`, `FOX2-06-T17`, `FOX2-06-T23` |
| `FOX2-06-R12` | Disconnect, gaps, out-of-order and recovery remain explicit; recovery may not hide missing continuity or substitute fixtures. | `FeedRecoveryStatus` | `SPECIFIED_APPROVED` | `FOX2-06-T19`, `FOX2-06-T20`, `FOX2-06-T22` |
| `FOX2-06-R13` | Provider auth/quota/license/storage/redistribution/tenant scope are separately evidenced; UNKNOWN blocks only affected capability. | `ProviderReadinessGate` | `SPECIFIED_APPROVED` | `FOX2-06-T09`, `FOX2-N1-T07` |
| `FOX2-06-R14` | FOX2 data service exposes typed provenance, retrieval/source revision, freshness, quality, as-of and health semantics. | `UnifiedMarketDataAPI` | `SPECIFIED_APPROVED` | `FOX2-N1-T11`, `FOX2-06-T18` |
| `FOX2-06-R15` | Synthetic fixtures are isolated to automated tests and never silently appear as investor market values. | `ProductionDataIntegrity` | `SPECIFIED_APPROVED` | `FOX2-06-T14`, `FOX2-N1-T12` |
| `FOX2-06-R16` | Legacy FOX may be used only as scoped technical reference/reuse evidence; FOX2 must not inherit private account, synthetic-analysis, bootstrap or other unapproved legacy behavior. | `LegacyReuseBoundary` | `SPECIFIED_APPROVED` | `FOX2-WS08`, `FOX2-06-T16` |
| `FOX2-06-R17` | Observations/revisions/current-view updates preserve immutable lineage, actual first availability, atomic consistency and restart correctness; FOX legacy cache is not FOX2 writable storage. | `ObservationStoreInvariant` | `SPECIFIED_APPROVED` | `FOX2-06-T17`, `FOX2-06-T12`, `FOX2-N1-T06` |
| `FOX2-06-R18` | Real-time provider capability is market-only, authenticated/subscribed explicitly, bounded by verified provider limits and separated from broker/order paths; readiness requires confirmed subscription plus usable data state. | `MarketRealtimeCapability` | `SPECIFIED_APPROVED` | `FOX2-WS01`, `FOX2-WS02`, `FOX2-WS03`, `FOX2-WS04`, `FOX2-06-T19` |
| `FOX2-06-R19` | Provider field/time/unit/basis semantics must be evidence-backed; cumulative/provisional/correction semantics must not double-count or fabricate continuity. | `ProviderMappingInvariant` | `SPECIFIED_APPROVED` | `FOX2-WS05`, `FOX2-WS07`, `FOX2-06-T22`, `FOX2-06-T24` |
| `FOX2-06-R20` | Read/redisplay/retained-use/network/mapping/calendar/freshness gates are capability-scoped and independently evidenced; schema-shape PASS never substitutes for semantic validity. | `CapabilityGate` | `SPECIFIED_APPROVED` | `FOX2-N1-T02`, `FOX2-N1-T07`, `FOX2-06-T23` |

## 4. Data and source invariants

- Data Contract v0.4 owns wire/data shape and semantic contract details; this BRD references rather than duplicates it.
- `UNKNOWN ≠ 0`; genuine zero remains zero.
- Observation time, market event time and first availability are distinct concepts.
- Historical bars do not automatically prove real-time quote capability or restored tick continuity.
- Provider-native data with unknown unit/basis can only be exposed under approved diagnostic semantics and valid rights.

## 5. M1 capability boundaries

### M1-A

Offline/provider-disabled foundation must prove source isolation, semantic validation, persistence safety and truthful unavailable states without real provider network calls.

### M1-B

Real provider capability requires separately verified rights, auth/network, mapping, calendar/freshness and provider-specific recovery behavior.

M1-A PASS never closes M1-B.

## 6. Acceptance and traceability

Canonical tests remain in Acceptance Matrix v0.4. Relevant IDs include `FOX2-06-T01..T24`, `FOX2-N1-T01..T12`, `FOX2-WS01..WS08` as mapped by the released requirement map. This release neither renumbers nor marks them PASS.

The semantic source for every retained acceptance ID is the exact released owner BRD scenario/expected outcome at commit `955e74ff67e6b4ed184dc2c2dcd4260c51dc529b`, path `docs/brd_mirror/FOX2-BRD-06_v0.4.md`, together with `docs/acceptance/FOX2_M1_ACCEPTANCE_v0.4.csv` and `docs/acceptance/FOX2_M1_V04_CHANGE_CONTRACT_AND_REQUIREMENT_MAP.md`. Where the CSV delegates expected semantics to the owner BRD, the pinned v0.4 BRD text remains authoritative until an explicit approved semantic replacement exists.


## 7. Technical material moved out of BRD

The following v0.4 material is retained as technical intent/evidence but moves to the M1 Technical Specification: concrete DSM module decomposition, source-selection algorithm, SQLite tables/transactions, runtime state machine, WebSocket URL/HMAC/channels/heartbeat/caps/reconnect implementation, provider field codecs, queue/backpressure mechanics, exact API routes and concurrency implementation.

## 8. Out of scope / open gates

No DEV/Git/provider/broker/LIVE authority is granted. Technical implementation remains Candidate until separately approved and source-bound.

## 9. Revision disposition

`v0.5` preserves BRD-06 requirement IDs and business/data invariants while moving HOW details to the Technical Specification. Released v0.4 remains immutable history until this candidate set is approved/published and source-transition evidence is complete.
