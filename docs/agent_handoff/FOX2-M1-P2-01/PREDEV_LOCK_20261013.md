# FOX2-M1-P2-01 — PRE-DEV Foundation / Contract Lock

**Status:** `PREDEV_CONTRACT_LOCKED / CODING_HOST_RESULT_PENDING / CODE_ALLOWED=NO`  
**Date:** 2026-10-13  
**Project:** FOX2  
**WP:** `FOX2-M1-P2-01`  
**Stage:** Foundation / Contract Readiness only. No application-code mutation is authorized by this record.

## 1. Active governance and source binding

- Active Policy: `FOX2_POLICY_V1.8.2.md`, RELEASED_EFFECTIVE.
- Library SHA-256: `552d36d910a020de4475b1994975d09a30dd09a138476b03a4a2250d543181dc`.
- Git policy blob at task source: `0783c024d19f96a0b87ab770dad80bab449fa21f`.
- Frozen task source commit: `c9dc41b97ca8bc58f06cc2f3701832ba083422e3`.
- This source commit is immutable input for the PRE-DEV lock; moving branch HEAD is not authority.

Exact required sources at that commit:

| Role | Git path | Blob SHA |
|---|---|---|
| Policy | `docs/governance/FOX2_POLICY_V1.8.2.md` | `0783c024d19f96a0b87ab770dad80bab449fa21f` |
| BRD-00 | `docs/brd_mirror/FOX2-BRD-00_v0.5.md` | `e353e6fe6d0aea3fd8cef21c8b12d9986d5160e8` |
| BRD-06 | `docs/brd_mirror/FOX2-BRD-06_v0.5.md` | `ee912b39cd009ba89a50cb28e4a3a6e76b52b5df` |
| BRD-08 | `docs/brd_mirror/FOX2-BRD-08_v0.5.md` | `66853c784c578c4cc75addd5bbf8ce565dd77d9e` |
| M1 Technical Spec | `docs/architecture/FOX2_M1_TECHNICAL_SPEC_v0.1.md` | `e4a95b97039d482085996afbfad232b789d1b236` |
| BRD↔Technical mapping | `docs/architecture/FOX2_M1_BRD_TECH_MAPPING_v0.1.md` | `b9e860af21bb2bc04ba53b1ec2ce0ed70ccd76e3` |
| Market Data Contract | `docs/data_contracts/FOX2_MARKET_DATA_CONTRACT_v0.4.md` | `369a893a83dd140ce423c032784941a22d4a443e` |
| Market Data schema | `docs/data_contracts/FOX2_MARKET_DATA_v0.4.schema.json` | `fa395662b772658d782b46718b7eb8392f6bbf76` |
| Acceptance matrix | `docs/acceptance/FOX2_M1_ACCEPTANCE_v0.4.csv` | `0e7ff73eb58e11bba4b513f84199e96f0c0d6193` |
| Roadmap | `docs/roadmap/FOX2_M1_ROADMAP_v0.4.md` | `ed842860259628cb1404b3a9fa7ad9e28eaa326c` |
| P2 WP Plan | `docs/roadmap/FOX2_M1_P2_WP_PLAN_v0.1.md` | `6612f7d05b4724be396214e5446eb685e58979c9` |

## 2. API interface lock

Canonical API v0.4 remains unchanged. All market responses use `{contract_version, request_id, generated_at, data}`; `generated_at` is response creation time and never substitutes for observation/event timestamps.

Frozen public interface:

- `GET /api/health` → process health, contract version, provider_enabled; sanitized; unhealthy process may return 503.
- `GET /api/data-sources/health` → per-capability state/readiness/gap/rights-expiry and sanitized reason; absent source is diagnostic, not fabricated LIVE.
- `GET /api/market/overview` → index envelopes with item-level unavailable state.
- `GET /api/stocks?query=&limit=&cursor=` → verified instrument results; query <= 32, limit 1..100, invalid input 422.
- `GET /api/stocks/{symbol}` → instrument metadata + quote envelope; unknown instrument 404; valid instrument without quote is 200 unavailable.
- `GET /api/stocks/{symbol}/bars?timeframe=&from=&to=&basis=` → bar envelope + explicit gaps; M1 timeframe 1D; UTC range 1..366 days; invalid input 422; unsupported basis is 200 unavailable.
- `GET /api/watchlist` → `{version,items:[instrument_id],updated_at}`; empty list is a valid preference.
- `PUT /api/watchlist` with `{expected_version,items}` → atomic replacement; version conflict 409; invalid/unknown/duplicate IDs 422; max 100.
- Unsafe/unreadable store or transaction failure → sanitized 503.
- Provider failure for an otherwise valid resource → 200 explicit unavailable/stale envelope.
- No account/order/margin/broker-write route is permitted.

P2-01 implementation scope is narrower than the full frozen route contract: foundation DTOs/validators/configuration, loopback safeguards and health diagnostics only. Market service wiring and watchlist integration remain P2-04 responsibilities.

## 3. DTO and port interface lock

DTO families are separate and must not share one market-observation schema:

- `MarketDataEnvelope`
- `ProcessHealth` / `SourceHealth`
- `InstrumentSearchResult`
- `WatchlistPreference`

Language-neutral port signatures frozen for cross-WP compatibility:

- `MarketValidator.validate_shape(payload, kind) -> ValidationResult`
- `MarketValidator.validate_semantics(observation, capability_context) -> SemanticVerdict`
- `StoreReadPort.get_observation(instrument_id, capability, at_or_before) -> ObservationOrUnavailable`
- `StoreWritePort.append_and_promote(candidate, ingest_audit) -> CommitResult` — implementation deferred to P2-02
- `DSMSelectPort.select(capability, instrument_id, use_context) -> SelectionDecision` — implementation deferred to P2-03
- `PreferenceRepositoryPort.replace_if_version(expected_version, items) -> PreferenceResultOrConflict` — implementation deferred to P2-02/P2-04

Exact Python representation may be selected by the implementation WP only if it preserves these argument meanings, error classes, nullability, ownership boundaries and Contract v0.4 behavior.

## 4. Validation semantics lock

Shape/schema validation and semantic validation are distinct gates. Schema PASS never implies semantic PASS.

Mandatory semantic rules for P2-01 tests include:

- quote price must be semantically positive where a quote exists;
- OHLC bounds/order must be valid;
- event/start/update/observation time semantics remain distinct and ordered where required;
- missing values remain null/UNKNOWN/UNAVAILABLE, never fabricated zero;
- genuine zero volume remains zero and is not converted to missing;
- `generated_at` must never fill missing market timestamps;
- unit/basis/rights/freshness uncertainty blocks claims that require them;
- unavailable timestamps are nullable with explicit reason/missing_fields;
- fixtures are isolated to tests and cannot enter investor runtime;
- provider transport is not constructed or called when disabled;
- secrets/provider raw errors/headers must not be echoed.

Dependency rule: DTO/domain validators do not import FastAPI, SQLite, DSM, provider SDK or runtime fixtures. Store does not depend on DSM/router/provider.

## 5. Frozen P2-01 acceptance subset

Evidence may be produced only for the scoped subcases below. No blanket 105/105 PASS is allowed, and all are currently `NOT_RUN`:

`FOX2-00-T01`, `FOX2-00-T02`, `FOX2-00-T03`, `FOX2-00-T04`,
`FOX2-06-T05`, `FOX2-06-T13`, `FOX2-06-T14`, `FOX2-06-T16`, `FOX2-06-T18`,
`FOX2-N1-T01`, `FOX2-N1-T02`, `FOX2-N1-T03`, `FOX2-N1-T04`, `FOX2-N1-T12`.

P2-01 can close only its offline DTO/validator/configuration/fixture-boundary sub-evidence. Provider, DSM, UI, persistence or full M1 scenarios remain open for their owning later WPs.

## 6. Task ownership / path lock

Current PRE-DEV owner: **CHAT** for source/interface/acceptance locking and remote evidence review.

Future application-code writer: **UNASSIGNED** until the coding-host readiness result is independently read and accepted.

Reserved future P2-01 path candidates — reservation only, not a write grant:

- `backend/pyproject.toml`
- `backend/src/fox2/__init__.py`
- `backend/src/fox2/main.py`
- `backend/src/fox2/config.py`
- `backend/src/fox2/contracts/**`
- `backend/src/fox2/validation/**`
- `backend/src/fox2/ports/**` — interfaces only
- `backend/src/fox2/api/__init__.py`
- `backend/src/fox2/api/health.py`
- `tests/p2_01/**`

Explicitly outside P2-01 mutation scope unless separately re-scoped: `backend/**/store/**`, `backend/**/dsm/**` implementation, `backend/**/provider/**`, frontend, provider/network code, canonical Policy/BRD/Contract/Acceptance files, broker/account/order paths, main branch, merge/deploy/LIVE.

Actual file existence/WIP/ignored-path collision, worktree and exclusive writer must be observed on the Windows coding host before any DEV grant.

## 7. Coding-host precheck state

Historical precheck Issue #9 and its dispatch were bound to Policy V1.8 and older source identities. As of this lock, remote evidence shows:

- Issue #9 remains open.
- Result branch `work/FOX2-WP-M1-P2-01-DEV-READINESS-copilot` still points to task-publication commit `959bd0f32d1a87015f7144bedb910d86b74fab21`.
- No Copilot readiness result commit has been observed.
- Therefore there is no coding-host result to accept yet.
- The old dispatch must not be treated as sufficient execution evidence for the current V1.8.2 / `c9dc41...` source lock without an explicit transition/rebind and fresh host observation.

## 8. Gate disposition

- `POLICY_CHECK=PASS`
- `TASK_STATE_CHECK=PASS`
- `API_INTERFACE_LOCK=PASS`
- `VALIDATION_SEMANTICS_LOCK=PASS`
- `ACCEPTANCE_SUBSET_LOCK=PASS`
- `SOURCE_BINDING_LOCK=PASS`
- `TASK_PATH_SCOPE_LOCK=PASS_AS_RESERVATION_ONLY`
- `CODING_HOST_PRECHECK_RESULT=NOT_OBSERVED`
- `EXCLUSIVE_CODE_WRITER=UNKNOWN`
- `AGENT_MODEL_MODE_QUOTA=UNKNOWN`
- `CODE_ALLOWED=NO`
- `GIT_CODE_PUSH=NO`
- `PR_CREATE=NO`
- `MERGE_ALLOWED=NO`
- `DNSE_PRODUCTION=NO`
- `BROKER_WRITE=NO`
- `LIVE=NO`

**STOP:** do not select or dispatch the P2-01 implementation Agent until a current coding-host precheck is bound to this source lock, remotely delivered, and independently accepted by CHAT.
