# FOX2-BRD-08 — Localhost Investor Dashboard & Presentation

**Version:** `0.5`  
**Status:** `RELEASED_EFFECTIVE / NO_DEV`  
**Change type:** `STRUCTURAL_SEPARATION_NO_BUSINESS_SEMANTIC_CHANGE`  
**Parent released BRD:** `FOX2-BRD-08 v0.4` at `955e74ff67e6b4ed184dc2c2dcd4260c51dc529b`  
**Technical counterpart:** `FOX2_M1_TECHNICAL_SPEC_v0.1.md`  
**Data contract:** Market Data Contract/schema v0.4 unchanged  
**Acceptance source:** Acceptance Matrix v0.4; IDs unchanged and `NOT_RUN`

## 1. Purpose and ownership

BRD-08 owns investor-facing presentation, navigation, source/data-state visibility, local watchlist behavior and UI safety boundaries. It defines **what the user must see/do**, not React/FastAPI routing, persistence mechanism or polling implementation.

## 2. User outcomes

- The localhost product remains usable when market sources are unavailable; it must show explicit state instead of fabricated prices.
- Market Overview, Watchlist/Search, Stock360/chart and Source Diagnostics are M1 presentation surfaces.
- UI never connects directly to DNSE or local database and never embeds provider secrets/private scope.
- Missing future-domain engines appear as unavailable explanations rather than fake scores/NAV/recommendations.
- Watchlist is a local user preference, not holdings/broker state.

## 3. Functional requirements

| Requirement | Normative outcome | Primary output | State | Acceptance IDs |
|---|---|---|---|---|
| `FOX2-08-R01` | Homepage presents supported market indices/breadth/turnover and other evidence only when methodology/source is available and correctly labeled. | `MarketOverview` | `SPECIFIED_APPROVED` | `FOX2-08-T05`, `FOX2-N1-T10` |
| `FOX2-08-R02` | Product provides Watchlist/Search/Stock360/PriceVolumeChart with correct basis/finality semantics and usable navigation. | `StockReview` | `SPECIFIED_APPROVED` | `FOX2-08-T02`, `FOX2-08-T03`, `FOX2-08-T10`, `FOX2-08-T11` |
| `FOX2-08-R03` | Every widget exposes truthful source/data state, as-of/coverage and unavailable explanation; stale/blocked data must not appear LIVE. | `SourceBadge` | `SPECIFIED_APPROVED` | `FOX2-08-T06`, `FOX2-08-T07`, `FOX2-08-T11` |
| `FOX2-08-R04` | UI renders approved server/domain snapshots and does not invent BUY/SELL or domain analysis in browser code. Snapshots combined in one assessment preserve the same assessment identity and version; UI must not silently combine incompatible assessments. | `EvidenceLinks` | `SPECIFIED_APPROVED` | `FOX2-08-T13` |
| `FOX2-08-R05` | Private/account-related pages do not expose private facts or fabricate NAV when identity/account capability is absent. | `PrivateView` | `SPECIFIED_APPROVED` | `FOX2-08-T04`, `FOX2-06-T13` |
| `FOX2-08-R06` | User interactions do not submit/modify/cancel orders; future trading UI requires separate authority. | `NoLiveOrderUI` | `SPECIFIED_APPROVED` | `FOX2-08-T04` |
| `FOX2-08-R07` | Dashboard is responsive/navigable, presents data diagnostics, uses real verified source data when available and never enables investor mock data by fallback. | `MVPUsability` | `SPECIFIED_APPROVED` | `FOX2-08-T01`, `FOX2-08-T02`, `FOX2-08-T12` |
| `FOX2-08-R08` | All market widgets consume the FOX2 DSM/service boundary and never directly call provider WebSocket/API or local DB. | `DSMViewAdapter` | `SPECIFIED_APPROVED` | `FOX2-08-T08`, `FOX2-08-T13` |
| `FOX2-08-R09` | UI exposes provider/source mode, actual event/as-of, revision, freshness, rights-safe status and missing-data health. | `DataProvenancePanel` | `SPECIFIED_APPROVED` | `FOX2-08-T05`, `FOX2-08-T06`, `FOX2-08-T07` |
| `FOX2-08-R10` | Investor mode has no fallback-to-synthetic behavior; test fixtures remain isolated. | `SourceIntegrityUX` | `SPECIFIED_APPROVED` | `FOX2-N1-T12`, `FOX2-08-T13` |
| `FOX2-08-R11` | Data-source diagnostics are read-only, redact entitlement/secret details and do not manipulate secrets in the browser. | `DataSourceDiagnostics` | `SPECIFIED_APPROVED` | `FOX2-06-T15`, `FOX2-08-T08` |
| `FOX2-08-R12` | M1 exposes Market Overview, Watchlist, Stock360 and Data Sources, while unavailable future domains explain their status; quote/history/gap/finality/time semantics must not be confused. | `M1ScreenContract` | `SPECIFIED_APPROVED` | `FOX2-08-T02`, `FOX2-08-T03`, `FOX2-08-T11`, `FOX2-08-T12` |
| `FOX2-08-R13` | Watchlist is a persistent single-user localhost preference over verified instruments with deterministic concurrent-update conflict behavior; it accepts at most 100 verified instrument IDs, is not broker state and does not cause provider/broker mutation. | `WatchlistPreference` | `SPECIFIED_APPROVED` | `FOX2-08-T10` |
| `FOX2-08-R14` | UI is reviewable across desktop/tablet/mobile targets, keeps navigation/tables free of page overflow at accepted viewport targets, communicates status by text as well as color, clearly labels unknown units/status and exposes relevant source/evidence context without requiring unavailable reference artwork. | `ReviewableResponsiveUI` | `SPECIFIED_APPROVED` | `FOX2-08-T09`, `FOX2-08-T12` |
| `FOX2-08-R15` | Browser only uses FOX2 backend/service boundaries; refresh behavior must not leak provider secrets, directly access DB/provider or create uncontrolled upstream/backfill load. | `RefreshBoundary` | `SPECIFIED_APPROVED` | `FOX2-08-T14`, `FOX2-08-T13` |

## 4. Presentation semantics

- `LIVE` only when the upstream domain declares it valid for that capability.
- `LATEST_VALID/EOD_CONFIRMED` clearly communicate final/last-known context.
- `STALE/DELAYED/GAP_RECOVERING` display cutoff/warning rather than LIVE styling.
- `ENTITLEMENT_BLOCKED/UNAVAILABLE` display no fake zero/price/trend.
- History close must not masquerade as latest trade/quote.
- Chart gaps/provisional/revisions remain visible when relevant.
- Price and volume shown together use a consistent dataset/assessment identity; incompatible assessments are not silently combined.

## 5. Watchlist product semantics

- Local single-user preference only; no broker/holdings meaning.
- Add/remove/update is explicit user intent.
- Persistent across restart.
- Concurrent stale update produces a conflict outcome rather than silent lost update.
- Invalid/unknown instrument requests are rejected rather than silently stored.
- The product limit is at most 100 verified instrument IDs in the M1 watchlist.
- Exact HTTP method/status/storage implementation belongs to Technical Spec/Data Contract where applicable.

## 6. Acceptance and traceability

Canonical scenarios remain Acceptance Matrix v0.4, including `FOX2-08-T01..T14` and mapped BRD-06/N1/WS tests. All remain `NOT_RUN` absent runtime evidence.

The semantic source for every retained acceptance ID is the exact released owner BRD scenario/expected outcome at commit `955e74ff67e6b4ed184dc2c2dcd4260c51dc529b`, path `docs/brd_mirror/FOX2-BRD-08_v0.4.md`, together with `docs/acceptance/FOX2_M1_ACCEPTANCE_v0.4.csv` and `docs/acceptance/FOX2_M1_V04_CHANGE_CONTRACT_AND_REQUIREMENT_MAP.md`. Where the CSV delegates expected semantics to the owner BRD, the pinned v0.4 BRD text remains authoritative until an explicit approved semantic replacement exists.


## 7. Technical material moved out of BRD

Framework selection, exact frontend/backend routes, module layout, API endpoint encoding, optimistic-lock wire format, HTTP status implementation, loopback Host/Origin/content-type enforcement, persistence mechanism, polling/cache/scheduler behavior and UI library/lockfile choices move to the M1 Technical Specification.

## 8. Out of scope / open gates

No DEV/Git/merge/provider/broker/LIVE authority. No multi-user authentication in M1. Future trading capability requires separate BRD/authority.

## 9. Revision disposition

`v0.5` preserves BRD-08 requirement IDs and user/acceptance semantics while moving implementation mechanics to the Technical Specification. Released v0.4 remains immutable history until the candidate package is approved and published.
