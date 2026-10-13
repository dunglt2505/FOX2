# FOX2 — M1-P2-01 PRE-DEV REBIND / EXECUTION SOURCE LOCK — V1.8.4
Date: 2026-10-13
Status: PRE-DEV_REBOUND / PROMPT_NOT_YET_EXECUTABLE / CODE_ALLOWED=NO
Issue: https://github.com/dunglt2505/FOX2/issues/8

## 1. Authority
- Policy: FOX2 Policy V1.8.4 RELEASED_EFFECTIVE
  - Library SHA256: 481790b2512ea1cd4891fe1b03258175d68d9bfae71158d19283bd003c560f5a
  - Git: a366f509899cec97f64316cb111b29a3849325b5:docs/governance/FOX2_POLICY_V1.8.4.md
  - Blob: 483a74ff39339e653bbd7bbfba0feaf7b1c003e9
- Routing Index: V1.2.4 EFFECTIVE_DERIVATIVE
  - Git: 43c3d240615bce7279f2665fa1c1c0afb7f49021:docs/governance/FOX2_AGENT_PROMPT_POLICY_V1_2_4_EFFECTIVE_ROUTING_INDEX_20261013.md
  - Blob: ff039df00a5dd449077974fd9d3ee68307176be4
- M1 source set: BRD-00/06/08 v0.4 + contract/schema/acceptance at immutable M1 source commit 955e74ff67e6b4ed184dc2c2dcd4260c51dc529b.
- Market Data Contract v0.4 blob: 369a893a83dd140ce423c032784941a22d4a443e.
- M1 Acceptance v0.4 blob: 0e7ff73eb58e11bba4b513f84199e96f0c0d6193.
- M1 Requirement Map blob: 321bc0e2525befa8842f09edfc09ce20c2cbab09.
- M1 Roadmap v0.4: 282fe0654de13e8d9c679e171e7ac81f29a545ca:docs/roadmap/FOX2_M1_ROADMAP_v0.4.md, blob ed842860259628cb1404b3a9fa7ad9e28eaa326c.
- P2 WP Plan v0.1: 282fe0654de13e8d9c679e171e7ac81f29a545ca:docs/roadmap/FOX2_M1_P2_WP_PLAN_v0.1.md, blob 6612f7d05b4724be396214e5446eb685e58979c9.
- Accepted P1 evidence remains immutable; do not redo P1.

## 2. Architecture–Stage Alignment
```yaml
architecture_stage_alignment:
  target_architecture: FastAPI modular localhost backend with typed public market DTO/validation, loopback safeguards, provider disabled by default, later Store->DSM->API layering
  actual_stage: PRE-DEV
  observed_capabilities:
    - released M1 documents and contract source are available in Git
    - no accepted application implementation exists
    - BRG/SFR are separate infrastructure lanes
  unmet_dependencies_or_gates:
    - dedicated task branch/worktree
    - single writer
    - task-specific local toolchain observation
    - scoped material DEV authorization
  execution_path_class: TARGET_PATH
  path_reason: P2-01 does not technically depend on Bridge Gate A or SFR-010
  target_transition: ACCEPTED P2-01 interfaces and offline evidence
  fallback_retirement_condition: NOT_APPLICABLE
  alignment_verdict: PASS_TARGET
```

## 3. Exact P2-01 scope
Deliver only:
- backend foundation/package layout;
- typed DTOs for public market contract families;
- separate shape/schema vs semantic validator interfaces;
- config with provider/network disabled by default;
- loopback safeguards;
- health/source diagnostics with UNKNOWN/UNAVAILABLE semantics;
- WP-specific offline tests/fixtures needed for the frozen P2-01 acceptance subset.

Do NOT implement:
- SQLite transactional store (P2-02);
- DSM source-selection implementation (P2-03);
- API wiring beyond the minimal foundation/diagnostic boundary owned by P2-01;
- frontend;
- DNSE/provider network;
- broker/account/order routes;
- synthetic investor-runtime fallback;
- production deployment, merge or LIVE.

## 4. Frozen design semantics
Preserve the already accepted PRE-DEV design lock:
- DTO/domain validators do not depend on FastAPI, SQLite, DSM, provider SDK or runtime fixtures.
- `MarketValidator.validate_shape(payload, kind) -> ValidationResult`.
- `MarketValidator.validate_semantics(observation, capability_context) -> SemanticVerdict`.
- Conceptual ports remain frozen for later WPs: StoreReadPort, StoreWritePort, DSMSelectPort, PreferenceRepositoryPort.
- Positive quote price, OHLC bounds, timestamp/availability/unit/basis/rights/freshness semantics are separate from JSON shape validity.
- `generated_at` is response creation time, not market-event time.
- Provider transport is not constructed/used when disabled.
- Diagnostics never fabricate READY/LIVE data.

## 5. Planned acceptance subset
Reuse the P2 plan allocation:
FOX2-00-T01/T02/T03/T04;
FOX2-06-T05/T13/T14/T16/T18;
FOX2-N1-T01/T02/T03/T04/T12.
Only P2-01-owned offline subcases may be reported PASS/PARTIAL; integrated/provider obligations remain NOT_RUN.

## 6. Routing / candidate comparison
- CHAT: owns source lock, remote Git/Library evidence, status and acceptance.
- COPILOT: currently owns Bridge bootstrap writer lane; do not overlap.
- CODEX: preferred P2-01 coding candidate once an isolated writer destination and task-specific DEV gate exist.
- WORK: not needed before code; independent review only if a material safety/concurrency/release checkpoint warrants it.

## 7. Current gates
```text
GIT_SOURCE_READY_FOR_DOCUMENT_INPUTS=YES
ARCHITECTURE_STAGE_ALIGNMENT=PASS_TARGET
OWNER_PLAN_APPROVAL=YES
CODE_BRANCH=NOT_YET_VERIFIED
WORKTREE=NOT_YET_VERIFIED
SINGLE_WRITER=NOT_YET_VERIFIED
LOCAL_TOOLCHAIN=NOT_YET_VERIFIED_FOR_THIS_WP
CODE_ALLOWED=NO
GIT_CODE_PUSH=NO
MERGE=NO
DNSE_PRODUCTION=NO
BROKER_WRITE=NO
LIVE=NO
```

Next step: establish the legitimate task branch/worktree/writer lane, then perform only the minimal local runtime check needed for this WP before an executable coding handoff.
