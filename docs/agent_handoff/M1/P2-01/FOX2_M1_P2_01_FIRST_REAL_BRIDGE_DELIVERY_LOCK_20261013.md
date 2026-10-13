# FOX2 — M1-P2-01 FIRST REAL BRIDGE DELIVERY LOCK

Date: 2026-10-13
Status: TASK_LOCKED / FIRST_REAL_BRIDGE_WP_SELECTED / DEV_NOT_YET_DISPATCHED
Tracking issue: https://github.com/dunglt2505/FOX2/issues/8

## 1. Selection decision

Selected first real product Work Package for execution through the FOX2 Bridge:

`FOX2-M1-P2-01 — Backend Foundation / API Contract`

Reason:
- The released M1 roadmap sequences P2 as P2-01 -> P2-02 -> P2-03 -> P2-04.
- P2-02 is source-dependent on accepted P2-01 interfaces; P2-03 depends on P2-02; P2-04 depends on P2-03.
- Remote source inspection at the selected base shows no accepted application implementation under `backend/**` or `tests/**`; only the baseline `.gitkeep` files are present.
- P2-01 is the lowest-risk routine Python foundation slice and is the best first real Bridge/Copilot delivery. It does not require DNSE Production, broker, LIVE, SQLite transactional implementation, DSM source-selection implementation, or frontend work.

This lock supersedes the historical routing preference in the V1.8.4 PRE-DEV rebind that preferred CODEX because COPILOT then owned the Bridge bootstrap lane. The Bridge bootstrap lane is now operationally proven and COPILOT CLI can receive a separate isolated worktree/branch.

## 2. Current authority/source bindings

### Governance
- FOX2 Policy V1.8.5 RELEASED_EFFECTIVE
  - Git release branch: `work/FOX2-SIMPLIFIED-BRIDGE-V185-V06-RELEASE-chat-20261013`
  - Policy blob: `5b38b6bd6776b5ef3a771ba2297f4565c2d9abed`
- FOX2 Agent Prompt Routing Index V1.2.6 EFFECTIVE_DERIVATIVE
  - blob: `263966d1c5e0eb3900a73c2f1327312f2cf94ec9`
- Bridge Technical Spec v0.6 RELEASED_EFFECTIVE
  - blob: `ad4f118f6d32408d3e39c2e71fafc81b4f571956`

### Product/technical source
Selected immutable base before this lock:
`588da7b1c1a642ddfd935ff6372af83a35acaa2f`

Current released business source in that base:
- `docs/brd_mirror/FOX2-BRD-00_v0.5.md`
  - blob `e353e6fe6d0aea3fd8cef21c8b12d9986d5160e8`
- `docs/brd_mirror/FOX2-BRD-06_v0.5.md`
  - blob `ee912b39cd009ba89a50cb28e4a3a6e76b52b5df`
- `docs/brd_mirror/FOX2-BRD-08_v0.5.md`
  - blob `66853c784c578c4cc75addd5bbf8ce565dd77d9e`
- `docs/architecture/FOX2_M1_TECHNICAL_SPEC_v0.1.md`
  - blob `e4a95b97039d482085996afbfad232b789d1b236`
- `docs/data_contracts/FOX2_MARKET_DATA_CONTRACT_v0.4.md`
  - blob `369a893a83dd140ce423c032784941a22d4a443e`
- `docs/data_contracts/FOX2_MARKET_DATA_v0.4.schema.json`
  - blob `fa395662b772658d782b46718b7eb8392f6bbf76`
- `docs/acceptance/FOX2_M1_ACCEPTANCE_v0.4.csv`
  - blob `0e7ff73eb58e11bba4b513f84199e96f0c0d6193`
- `docs/acceptance/FOX2_M1_V04_CHANGE_CONTRACT_AND_REQUIREMENT_MAP.md`
  - blob `321bc0e2525befa8842f09edfc09ce20c2cbab09`
- `docs/roadmap/FOX2_M1_ROADMAP_v0.4.md`
  - blob `ed842860259628cb1404b3a9fa7ad9e28eaa326c`
- `docs/roadmap/FOX2_M1_P2_WP_PLAN_v0.1.md`
  - blob `6612f7d05b4724be396214e5446eb685e58979c9`

BRD v0.5 is a structural separation release with no business-semantic change relative to the v0.4 M1 source. Market Data Contract/schema v0.4 and Acceptance Matrix v0.4 remain unchanged.

## 3. Exact product scope

Deliver only P2-01:
- backend foundation/package layout;
- typed DTOs for the public market contract families;
- separate shape/schema validation and semantic validation;
- conceptual port interfaces required by later P2 WPs;
- provider/network disabled by default;
- loopback/local-only safeguards;
- process/source diagnostics with truthful UNKNOWN/UNAVAILABLE states;
- isolated offline tests and fixtures for the P2-01-owned acceptance subset;
- sanitized result report.

Do not implement:
- P2-02 SQLite transactional store;
- P2-03 DSM source-selection engine;
- P2-04 full API/watchlist persistence wiring;
- frontend;
- DNSE/provider network access;
- broker/account/order/cash/margin routes;
- Production deployment, PR, merge, main, broker write or LIVE.

## 4. Frozen design semantics

- DTO/domain validators must not depend on FastAPI, SQLite, DSM, provider SDK, or runtime fixture modules.
- Keep distinct DTO families: MarketDataEnvelope, ProcessHealth/SourceHealth, InstrumentSearchResult, WatchlistPreference.
- Keep shape/schema validation separate from semantic validation.
- `MarketValidator.validate_shape(payload, kind) -> ValidationResult`.
- `MarketValidator.validate_semantics(observation, capability_context) -> SemanticVerdict`.
- Later-WP conceptual ports remain frozen: StoreReadPort, StoreWritePort, DSMSelectPort, PreferenceRepositoryPort.
- Positive quote price, OHLC bounds, timestamp ordering, genuine-zero volume, availability timestamps, unit/basis/rights/freshness semantics are not proven by JSON schema alone.
- `generated_at` is response creation time, never a substitute for market-event/observation time.
- Provider transport must not be constructed or called when disabled.
- Diagnostics never fabricate READY/LIVE data.

## 5. Frozen acceptance subset

Only P2-01-owned offline subcases may be claimed:

`FOX2-00-T01/T02/T03/T04`
`FOX2-06-T05/T13/T14/T16/T18`
`FOX2-N1-T01/T02/T03/T04/T12`

Integrated/provider/UI obligations remain NOT_RUN.

Required product evidence:
- offline startup;
- contract/schema and semantic validation tests;
- provider disabled/no upstream market network;
- no secret exposure;
- no broker/account/order routes;
- truthful UNKNOWN/UNAVAILABLE diagnostics;
- negative tests for invalid price/OHLC/time/rights semantics;
- true zero volume retained, missing stays null;
- canonical source/contract files unchanged.

## 6. Reserved writer lane

Selected Agent:
- Role: implementation
- Product: GitHub Copilot CLI through FOX2 Bridge
- Model: supported configured/default Copilot CLI model; not pinned by CHAT
- Thinking: Agent-managed/default; no model claim without runtime exposure

Reserved task branch:
`work/FOX2-M1-P2-01-BRIDGE-copilot`

Reserved task worktree:
`C:\Projects\FOX2-worktrees\FOX2-M1-P2-01-BRIDGE-COPILOT`

One-writer rule:
- Bridge Copilot CLI is the only material writer to the reserved task worktree during execution.
- Existing `work/FOX2-M1-P2-01-foundation-codex` lane is not imported, mutated, or treated as accepted implementation source.
- VS Code Copilot/Codex must not concurrently write this reserved Bridge worktree.

## 7. Proposed executable allowlist

Code:
- `backend/fox2_m1/**`
- `backend/pyproject.toml`

Tests:
- `tests/m1_p2_01/**`

Result:
- `reports/FOX2-M1-P2-01/**`

Canonical source documents, governance, `agent_bridge/**`, frontend, provider/DSM/store implementation paths are read-only/out of scope.

## 8. Current gates after selection

```text
ROADMAP_SELECTION=PASS
FIRST_REAL_BRIDGE_WP=FOX2-M1-P2-01
SOURCE_FAMILY_READBACK=YES
BRD_CURRENT_SOURCE=v0.5
MARKET_CONTRACT_SOURCE=v0.4_UNCHANGED
ACCEPTANCE_SOURCE=v0.4_UNCHANGED
CODE_BRANCH=RESERVED
WORKTREE=RESERVED_PATH_NOT_YET_CREATED
SINGLE_WRITER=RESERVED_FOR_BRIDGE_COPILOT
COPILOT_BRIDGE_TRANSPORT=PASS
COPILOT_GIT_PUSH=PASS
BRIDGE_RUN_NEXT=PASS
BRIDGE_PYTEST_SHELL_PERMISSION=NOT_YET_IMPLEMENTED
LOCAL_BACKEND_DEPENDENCY_CHECK=NOT_YET_RUN
OWNER_SELECTION_APPROVAL=YES
OWNER_DEV_AUTHORIZATION=NOT_YET_GRANTED
CODE_ALLOWED=NO
GIT_CODE_PUSH=NO_FOR_PRODUCT_WP
MERGE=NO
DNSE_PRODUCTION=NO
BROKER_WRITE=NO
LIVE=NO
```

## 9. Material blocker before real execution

The current Operational MVP proved write + Git commit/push, but it pre-approves only file-write and `shell(git:*)` for Copilot CLI. P2-01 acceptance requires Python/pytest execution.

Therefore the real product dispatch must not be published as `auto_execute=true` until Bridge supports a bounded dispatch-specific shell permission for the exact required test/tool commands (for example a restricted `python -m pytest` permission) and that extension passes its own tests.

This is an execution-environment blocker, not a P2-01 product-design blocker.

## 10. Next transition

Next infrastructure action:
`FOX2-BRIDGE-OPS-DEV-01` — bounded task-specific test-shell permission for real DEV execution, preserving no provider/broker/LIVE authority.

After that PASS, CHAT may bind an immutable P2-01 execution prompt + dispatch using this reserved branch/worktree and request the separate Owner DEV grant.
