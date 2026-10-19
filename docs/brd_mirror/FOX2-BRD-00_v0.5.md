# FOX2-BRD-00 — Product Vision, Requirements & Common Rules

**Version:** `0.5`  
**Status:** `RELEASED_EFFECTIVE / NO_DEV`  
**Change type:** `STRUCTURAL_SEPARATION_NO_BUSINESS_SEMANTIC_CHANGE`  
**Parent released BRD:** `FOX2-BRD-00 v0.4` at M1 source commit `955e74ff67e6b4ed184dc2c2dcd4260c51dc529b`  
**Technical counterpart:** `FOX2_M1_TECHNICAL_SPEC_v0.1.md`  
**Data contract:** `FOX2_MARKET_DATA_CONTRACT_v0.4.md` + schema v0.4, unchanged  
**Acceptance source:** `FOX2_M1_ACCEPTANCE_v0.4.csv`, IDs unchanged and runtime remains `NOT_RUN`  
**Governance:** released FOX2 Policy remains V1.8.1 until a later Policy is actually released; historical Policy references in v0.4 are provenance, not a reason to bump this BRD.

## 1. Purpose and ownership

BRD-00 owns FOX2 product scope, requirement ownership, decision-state semantics, common evidence/data rules and M1 milestone boundaries. It defines **what FOX2 must do**, not implementation architecture or framework choices.

Technical implementation choices belong to the separately versioned Technical Specification. A Technical Spec may not grant authority, redefine these requirements or change acceptance semantics.

## 2. Product scope and outcomes

- FOX2 is a Vietnam equities investment-intelligence product covering the market universe allowed by verified sources; it is not permanently hardcoded to a small symbol set.
- Maintain one source-backed StockMaster with availability and symbol/venue/classification history.
- Preserve the product context market → sector → stock and its evidence-based analysis, risk, capital-allocation and profit-protection objectives; later-domain objectives remain outside M1 execution scope until their owning BRDs are accepted.
- M1 provides a localhost investor-facing experience backed by FOX2 data services. Verified real market data is displayed when rights, mapping and quality gates allow it; otherwise the product must show explicit unavailable/stale states rather than synthetic investor values.
- V1 is research/analysis/decision-support only. No order-write, margin or cash-transfer capability is implied.
- FOX2 may legitimately conclude `HOLD_CASH / NO_OPPORTUNITY`.
- M1 scope is the approved slice BRD-00/06/08 plus Market Data Contract and Acceptance Matrix. BRD-01/02/03/04/05/07 algorithms are not implicitly accepted by this slice.

## 3. Cross-BRD responsibility

- BRD-00 owns common IDs, state semantics and project boundaries.
- BRD-06 owns market-data facts/source truth and source selection semantics.
- BRD-08 owns presentation/user interaction semantics.
- Other BRDs remain owners of their respective capital, discovery, risk, exit, analytics and validation domains.
- Data/technical dependency never creates document-approval authority.

## 4. Functional requirements

| Requirement | Normative outcome | Primary output | Priority | State | Acceptance IDs |
|---|---|---|---|---|---|
| `FOX2-00-R01` | Every requirement has a FOX2 requirement ID, one owning BRD, source evidence, priority, state and acceptance linkage. | `RequirementRegister` | P0 | `SPECIFIED_APPROVED` | `FOX2-00-T01` |
| `FOX2-00-R02` | Decision states distinguish PROPOSED, SPECIFIED, IMPLEMENTED, VERIFIED and ACCEPTED; hypotheses separately use ACCEPT/REJECT/DEFER. | `DecisionRegister` | P0 | `SPECIFIED_APPROVED` | `FOX2-00-T05` |
| `FOX2-00-R03` | Missing/unknown data must not be represented as fabricated probability, zero, safe or flat state. Confidence must not be presented as a calibrated probability without supporting validation, independently of whether input data are missing. | `CommonStatus` | P0 | `SPECIFIED_APPROVED` | `FOX2-00-T02`, `FOX2-N1-T03` |
| `FOX2-00-R04` | Evidence-backed outputs preserve source, issued time, data-as-of, availability cutoff, version and reason/counterevidence. | `EvidenceEnvelope` | P0 | `SPECIFIED_APPROVED` | `FOX2-N1-T01`, `FOX2-N1-T06` |
| `FOX2-00-R05` | V1 explicitly has no order write and no margin; `HOLD_CASH / NO_OPPORTUNITY` are valid outcomes. | `CapabilityBoundary` | P0 | `SPECIFIED_APPROVED` | `FOX2-00-T03` |
| `FOX2-00-R06` | User/account permissions, data scope and shadow state remain distinct from real broker state. | `IdentityBoundary` | P0 | `SPECIFIED_APPROVED` | `FOX2-06-T13`, `FOX2-08-T04` |
| `FOX2-00-R07` | Domain ownership remains explicit: BRD-06 data truth, BRD-05 evidence, BRD-02 Entry, BRD-03 RiskVeto, BRD-01 Capital, BRD-04 Exit, BRD-07 Validation, BRD-08 Presentation. | `BRDOwnership` | P0 | `SPECIFIED_APPROVED` | `FOX2-00-T01`, `FOX2-00-T06` |
| `FOX2-00-R08` | FOX2 governance is FOX2-only; no other-project policy, approval, release or permission is imported by implication. | `ProjectIndependenceBoundary` | P0 | `SPECIFIED_APPROVED` | `FOX2-00-T90` |
| `FOX2-00-R09` | Maintain the internal BRD/data-owner/producer-consumer/requirement dependency map without confusing technical dependency with approval authority. | `InternalDependencyRegistry` | P0 | `SPECIFIED_APPROVED` | `FOX2-00-T01`, `FOX2-00-T91` |
| `FOX2-00-R10` | M1 investor mode never defaults to synthetic market data. BRD-06 is the sole owner of source-selection semantics; investor UI shows verified real data or explicit missing/stale states. | `M1DataSourceBoundary` | P0 | `SPECIFIED_APPROVED` | `FOX2-00-T04`, `FOX2-06-T14`, `FOX2-N1-T12` |
| `FOX2-00-R11` | M1 acceptance is milestone-scoped: M1-A foundation/offline does not close M1-B real-data capability; M1 completion does not imply later analytics domains or LIVE trading. | `MilestoneBoundary` | P0 | `SPECIFIED_APPROVED` | `FOX2-00-T05`, `FOX2-00-T06`, `FOX2-00-T07` |

## 5. M1 business scope

### M1-A

Localhost market intelligence foundation must operate safely even when real provider access is unavailable. It must expose truthful source/data states and keep synthetic fixtures isolated to tests.

### M1-B

At least one real-data vertical slice must be demonstrated through the approved data-source lifecycle with provenance/quality semantics preserved. Real-data capability does not imply broker write or LIVE trading authority.

### Investor-facing scope

- Market overview initially includes VNINDEX/VN30; other indices appear only when source support is verified.
- Stock360 presents quote/history information only when the appropriate capability exists.
- Search/watchlist uses a verified instrument universe; watchlist is a local preference, not holdings.
- Source diagnostics expose safe source/quality/rights state without leaking secrets/private data.
- Unimplemented Sector/Discovery/Risk/Capital/Exit/Portfolio/Research domains may be visible as navigation with explicit unavailable reasons; they must not display fabricated scores/NAV/recommendations.

## 6. Data semantics owned or referenced by BRD-00

- `UNKNOWN ≠ 0`.
- Historical or provider-native data with unverified unit/basis may be shown only under the approved diagnostic semantics and must not masquerade as normalized analysis.
- Data Contract v0.4 remains the canonical interface/data-shape contract. This BRD does not duplicate its schema.

## 7. Acceptance and traceability

The canonical acceptance scenarios remain in `FOX2_M1_ACCEPTANCE_v0.4.csv`; all IDs are preserved and remain `NOT_RUN` until actual execution evidence exists. This release changes document placement only and cannot convert a test to PASS.

Document-integrity checks remain `FOX2-00-T90` and `FOX2-00-T91`.

The semantic source for every retained acceptance ID is the exact released owner BRD scenario/expected outcome at commit `955e74ff67e6b4ed184dc2c2dcd4260c51dc529b`, path `docs/brd_mirror/FOX2-BRD-00_v0.4.md`, together with `docs/acceptance/FOX2_M1_ACCEPTANCE_v0.4.csv` and `docs/acceptance/FOX2_M1_V04_CHANGE_CONTRACT_AND_REQUIREMENT_MAP.md`. Where the CSV delegates expected semantics to the owner BRD, the pinned v0.4 BRD text remains authoritative until an explicit approved semantic replacement exists. ID preservation alone is not semantic-preservation proof.

## 8. Out of scope / open gates

- No DEV/Git/merge/Production/provider/broker/LIVE permission is created by this release.
- Provider rights, mapping and host/runtime readiness remain separately gated.
- Framework, module, route, persistence, concurrency, retry and deployment mechanisms belong to the Technical Specification.

## 9. Revision disposition

`v0.5` is a released structural refactor of v0.4. The v0.4 bytes remain immutable history and provenance. **Document supersession follows exact Owner approval and Library publication/readback; Git verification and `GIT_SOURCE_READY` gate executable handoff separately.** A Git mirror failure does not invalidate a successfully published document; it blocks only the dependent Git-based implementation handoff. No business requirement or acceptance ID is intentionally changed.
