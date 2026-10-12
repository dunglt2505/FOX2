# FOX2 Market Data Contract v0.4 — DESIGN SPECIFICATION
> **FOX2 release edition · v0.4 · 2026-10-11 · OWNER_APPROVED / LIBRARY_PUBLISHED (subject to verified publication receipt).** This document derives from exact immutable M1 v0.4 ZIP source SHA-256 `1b9fcbc3ad9c79b1c9451b97223862d9de931501309d3543f24fb8dac4125895` (source manifest `0f3ad8f0231e5caef5e054a9ee6486471790b72f21aed1888eb0e10248f8845b`). Original market data contract candidate SHA-256 `1f2ae309833a1753b6e4e6aa5ca6589888a77d88a4679d13598151f12f30b539` is retained unchanged inside that ZIP. All normative functional requirements and technical guards are preserved; editorial status changes only. This document alone does not grant DEV, Git, DNSE access, merge, push, broker access or LIVE. Status of automated tests: `NOT_RUN`. See the FOX2 M1 v0.4 publication receipt for actual Library file identity/readback.

Owner: BRD-06. OWNER_APPROVED / LIBRARY_PUBLISHED; JSON schema is shape specification, not implemented validator.

## API v0.4
All responses {contract_version,request_id,generated_at,data}. generated_at is response creation time; never fills data timestamps. No arbitrary values map; payload kind quote/bars/index_summary. Health and preference have separate DTOs.
| Method/path | Output | Error behavior |
|---|---|---|
| GET /api/health | process health, contract version, provider_enabled; no secret/config paths | 503 unhealthy process |
| GET /api/data-sources/health | per-capability readiness/state/gap/rights expiry + sanitized reason | 200 diagnostics even source absent |
| GET /api/market/overview | array of index envelopes, unavailable per requested item | no global fake LIVE |
| GET /api/stocks?query=&limit=&cursor= | verified instrument DTO list, universe source/revision/coverage, opaque continuation | query <=32 chars, limit1..100;422 invalid |
| GET /api/stocks/{symbol} | verified instrument metadata + quote envelope | unknown instrument404; valid instrument lacking quote200 unavailable |
| GET /api/stocks/{symbol}/bars?timeframe=&from=&to=&basis= | bars envelope + explicit gap ranges | timeframe M1=1D;UTC from/to;1..366 days;RAW/ADJUSTED/UNKNOWN;422 invalid;unsupported basis200 unavailable |
| GET /api/watchlist | {version,items:[instrument_id],updated_at} | default empty preference list is valid, not fabricated market data |
| PUT /api/watchlist | same DTO;body {expected_version,items} | atomic;409 mismatch;422 invalid/unknown/duplicate IDs;max100 |
If store unsafe/unreadable or transaction fails:503 sanitized. Provider failure for valid resource:200 explicit unavailable/stale envelope. Exceptions never echo headers/auth/provider raw errors. All market paths downstream only; browser provider calls prohibited.

## Semantics
- IDs come from verified instrument source; a configured seven-symbol list is declared partial coverage, not StockMaster. Index IDs have type INDEX and provider identity; venue UNKNOWN blocks venue-dependent claims.
- observation times are UTC date-time or null with missing_fields/reason. event_at is provider event; as_of is freshest time justified by that capability; bar.start_at is interval start; lastUpdated maps update_at. received_at is local receipt; first_available_at is first local verified observation unless independently proven earlier.
- record_id/revision identify immutable observation/version; source_revision nullable if provider does not expose it. local correction revision does not invent provider revision. Store reads preserve all times.
- Rights object requires read/redisplay/retained_use states and evidence ref, verified_until. Network read and display require respective VERIFIED unexpired rights. Store origin remains DNSE; expired retained-use disallows store reads unless another current grant permits that use.
- VERIFIED_PROVIDER requires schema/time/unit/basis mapping accepted. PROVIDER_NATIVE_UNVERIFIED is diagnostic-only (rights verified), non-LIVE, quality PARTIAL/UNKNOWN, never analysis. UNKNOWN unit is explicit. Price basis UNKNOWN must not be advertised RAW or ADJUSTED.
- LIVE/PERIODIC_LIVE requires observed non-synthetic payload, rights, unit/time/instrument/session mapping, calendar/freshness policy version, socket and subscriptions accepted, no unresolved relevant gap. No-trade/batch cadence handled independently from transport heartbeat.
- UNAVAILABLE no observation: payload/source IDs/times null, reason populated; ENTITLEMENT_BLOCKED cannot leak cached values. A genuine zero quantity remains zero; missing value stays null.
- Positive quote prices only; bar high>=max(open,close,low), low<=min(open,close,high),start<end,nonnegative volume/turnover or null. Historical daily end requires verified session mapping; if end unknown keep null and block closed interval claims. Neither provider closed stream nor exclusion of current date alone proves exchange EOD.
- RAW/ADJUSTED never concatenate silently; adjusted requires adjustment_version/evidence. PIT selects revision available by cutoff; fetch today cannot backdate history into research.
- Cumulative volume is replacement value, not increment. Repeated provisional candle updates revise one bar; closed/corrected records preserve prior versions. Tick IDs cannot rely on timestamp alone if multiple events share time.
- Completeness COMPLETE only relative to a declared coverage window/universe and validated session; provider nextTime no-progress/duplicate/out-of-order is error/partial, never endless loop. HTTP fallback may repair bars; cannot prove missing ticks reconstructed.
- selection_audit_id mandatory even unavailable; ledger records candidates/rejection reasons/capability/config/source-set/revision without secrets. Incoming unknown fields remain raw hash/evidence, not arbitrary API payload additions.

## Candidate operational configuration
Provider enabled=false by default; no network at startup M1-A. DEV store root must be FOX2-only explicit config outside repo, not Fox cache. Loopback127.0.0.1 only. Single DSM ingest writer; API/browser readers.
M1-B input config includes rights evidence/expiry, unit/time/basis mapping IDs, venue/calendar version, per-channel freshness budgets, subscription set, request limits, retry/backoff/queue/retention. Provider caps are constraints; actual share with existing Fox connections must be measured. Missing accepted freshness blocks LIVE; no guessed safety budget.
Queue size/retry/polling are implementation settings, must be finite and tested under measured load; tuning does not grant rights or change data truth. Manual refresh default avoids invented polling interval. Clock skew/latency observations stored, not declared SLA without accepted config.

## Storage and identity
Tables logical design: instruments; observations; bar_revisions; current_projection; gaps; selection_audit; rights_registry; watchlist_preferences. Schema migration/version and transactions required. Only one writer, crash between stages leaves rollback or recoverable committed revision, never current pointer without observation. No public cache includes account IDs, holdings or financial facts.

## Watchlist DTO
items instrument IDs only;version nonnegative integer;updated_at UTC/null initial. expected_version matches before transaction; duplicate IDs rejected. Single local profile ID is configured, not secret/user login. Loopback/Host/Origin checks prevent unsolicited website mutation; no cross-origin wildcard. Preferences never reserve cash or initiate provider/broker action.
