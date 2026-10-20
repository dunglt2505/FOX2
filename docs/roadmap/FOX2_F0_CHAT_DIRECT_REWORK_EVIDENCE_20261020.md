# FOX2 — CHAT Direct F0 Rework: migration v3, durable denial and direct-installed-root guard

**Date:** 2026-10-20 · **Project:** FOX2 · **Whole-WP:** FOX2-BRIDGE-RC1-TO-INTERNAL-READY · **Feature:** FOX2-BRIDGE-MANUAL-LOCAL-ADMISSION · **Stage/Status:** BUILD/BLOCKED · **Current verdict:** `CHAT_DIRECT_CANDIDATE / SOURCE_DIFF_REVIEWED / NEW_TESTS_NOT_RUN / F0_NOT_ACCEPTED`. No new CODEX/WORK Agent was invoked; prior Attempt06 remains CONSUMED/NO_REPLAY.

## Instruction and intent boundaries

Owner's latest instruction `CHAT làm tiếp đi` authorizes direct continuation within the standing approved infrastructure engineering scope. This report treats it as **CHAT direct offline candidate corrections**, not as a new CODEX Agent admission or waiver of historical `Giữ gpt-6.1-sol; HOLD coding` for an Agent. The pinned `CODEX / gpt-6.1-sol / medium` remains unchanged and **CODEX execution still HOLD** pending fresh material gates. No automatic Worker/Canary/COMPAT/LIVE permission; no main/merge or installed writes.

## Source chain, original immutable evidence and fresh Git proof

- Existing CHAT Partial Review (not F0 acceptance) `621d683f83d90667faf532ac8d134bcbdbf75c1f:docs/agent_handoff/FOX2-BRIDGE-MANUAL-LOCAL-ADMISSION-DEV-20261019/F0_OFFLINE_ATTEMPT06/CHAT_REVIEW/CHAT_F0_PARTIAL_REVIEW_20261020.md`, Git blob `2a8446c08a54fbe3871e5ab8718fcc4f0b94ce10`; 243 PASS/1 FAIL historical observed **before** these new corrections.
- Consumed CODEX Attempt06 partial production snapshot `d2c595be123fa041720fd0467f9d94b2d4318bca` on `work/FOX2-BRIDGE-F0-OFFLINE-ATTEMPT06-20261020`, no Agent Result Contract v2, six protected negatives PASS, migration v3 regression FAIL. Do not replay or relabel Attempt06.
- **NEW CHAT-direct code source branch:** `work/FOX2-BRIDGE-F0-CHAT-DIRECT-REGRESSION-20261020@1442cd6352cbfdd3684284cd83e572b71fabebf5`. Git branch HEAD fetched/readback at exact SHA. Compared with `d2c595be123fa041720fd0467f9d94b2d4318bca` = `ahead` by 5 commits, 0 behind, with EXACT changed paths:
  1. `agent_bridge/tests/test_desktop.py` (+48/-10): `REQUESTED` truthful schema-v3 fixture.
  2. `agent_bridge/tests/test_runtime_ledger.py` (+158/-1): `NECESSARY_DEPENDENCY` six new negative/compatibility cases.
  3. `agent_bridge/src/fox2_agent_bridge/ledger.py` (+6/-0): `NECESSARY_DEPENDENCY` deny default when the installed current-root DB is initialized directly, not only through `desktop.initialize_runtime`.
- **Protected historical six tests:** `agent_bridge/tests/test_e2e_runner.py` unchanged Git blob `7b2a2c48e6bf4225d849dc7a7a32126652b0c3be`. This is byte-level proof, not an assertion that re-tests have passed on the NEW commit. No edits to `desktop.py` beyond the retained Attempt06 partial source.
- No changes to Governance/Policy/Dictionary/PreExec, installer, startup, Worker config/lock, legacy installed root, protected Dispatch, report manifests or outside ten allowed implementation paths.

## Analysis, K1 mapping and safety logic

**Migration v3 defect (previous historical 1 FAIL):** Old `test_v3_migration_preserves_dispatch_result_and_cursor` created v3 schema then called the *new* `SQLiteLedger.claim_dispatch` before migration. This is invalid because v3 has no `claim_authority`; fail-closed v5 denies, and `finish_execution` then sees no rows. It also hardcoded schema return `4` although F0 code schema is `5`. CHAT changed ONLY the test fixture so it seeds historical `dispatches` state, `executions.result_json` and `control_cursors` with SQL compatible with real v3, verifies pre-migration `claim_dispatch` denial without making an incompatible v3 `dispatch_status` read, runs `initialize`, and checks preservation of consumed identity, historical result and cursor across idempotent migration. No guard weakening or production compatibility assumption.
  
**New bounded tests:** `test_runtime_ledger.py` adds:
- sticky `DENY_CROSS_ROOT_UNKNOWN` after reopen and pause/resume, without untrusted direct claims;
- missing, corrupt and UNKNOWN `claim_authority` all deny with **zero** inserted claim/execution rows;
- v4 → v5 migration must preserve an existing DENY instead of creating `SINGLE_ROOT`;
- concurrent claims in UNKNOWN authority deny consistently without persistent side effects;
- proven isolated single-root claims remain atomic under concurrent callers and across restart;
- direct current-installed-root ledger initialization must DENY even when bypassing the Desktop initializer (tested using a disposable monkeypatched root).

**Actual source guard change:** `SQLiteLedger.initialize` now compares its resolved `database_path` to the resolved canonical `paths.BRIDGE_ROOT/data/bridge.db` and sets `cross_root_authority_unknown` when they match. Only 6 source lines added; `BEGIN IMMEDIATE`, sticky DENY, `honor_controls`, no-spawn paths and returned claim semantics otherwise unchanged. This closes a direct `SQLiteLedger.initialize()` bypass on the known installed current-root DB. It does **NOT** retire or modify any already frozen legacy executable, nor prove custom installation aliases/alternative DB paths cannot claim; keep F1 HOLD. Dynamic synthetic `desktop.BRIDGE_ROOT` patch still supplies `cross_root_authority_unknown=True` for original six fixtures.

## Actual tests and acceptance

- Historical tests on prior `d2c595be...` bytes: 243 PASS/1 FAIL, six protected negatives PASS, documented in prior CHAT receipt and canonical JUnit on Git. **Do not transfer these results to this new SHA.**
- **NEW SHA `1442cd6352cbfdd3684284cd83e572b71fabebf5`: `PYTEST=NOT_RUN`, `WIN_HOST_PREEXEC=NOT_RUN`, `SOURCE_BASED_STATIC_REVIEW=COMPLETE`, `ACTUAL_RUNTIME/INSTALLED=NOT_RUN`, `AGENT_RESULT_V2=NOT_DELIVERED_FOR_CONSUMED_ATTEMPT06`. GitHub connector cannot execute Python tests on FOXLE-PC; container cannot reach live repo. Do not claim new 243/244+ PASS or F0 BUILD acceptance.
- **Next test gate:** fresh focused suite of `test_e2e_runner.py,test_project_dictionary.py,test_desktop.py,test_runtime_ledger.py,test_ops_runner.py,test_preexec.py`, isolated Windows source branch, process-local longpath settings only. Require preserved 6 tests PASS, migration v3 PASS, six new tests PASS and no other regressions; inspect negative return/no side effects. Capture actual test exit, JUnit, summary and Git source HEAD; do not run installed Worker/paid Agent.
- Later gate: independent CHAT review of actual test output, K1 diff and source binding; broader integration/driver tests, runtime source lock, durable legacy retirement evidence F1 remain conditional. A CHAT-direct source change **cannot fabricate Agent-author Result Contract v2** for consumed Attempt06. New coding Agent needs separate one-shot identity, Prompt Builder, host capability/writer/quota, PreExec and separate admission; none issued here.

## Truthful state

`CHAT_DIRECT_REWORK_DIFF=GIT_VERIFIED` · `F0_CURRENT_CODE=PARTIAL_CANDIDATE` · `F0_FOCUSED_TESTS=NOT_RUN_NEW_SHA` · `MIGRATION_FIX_CORRECTNESS=NOT_VERIFIED_BY_TEST` · `F0_BUILD=BLOCKED` · `F1_LEGACY_RETIREMENT=NOT_VERIFIED` · `CANARY009=HOLD` · `COMPAT001=PUBLISHED_HOLD` · `INTERNAL_READY=NOT_ATTESTED`.

**NEXT_SAFE_ACTION:** run fresh offline test suite on new SHA through a verified isolated host/testing route (no Agent); inspect result and fix bounded remaining failures if any. No replay of Attempt06 and no new CODEX execution without separate binding. **GOAL_MET:** partial source correction and test expansion delivered; F0 full acceptance NO. **REAL_BLOCKER:** actual fresh test runner/host evidence unavailable to CHAT at this point; installed retirement still F1 HOLD.

**Skill use:** fox2-source-resolver REQUIRED/APPLIED; fox2-execution-recovery APPLIED; fox2-result-review APPLIED (original Agent return, not synthetic new result); fox2-agent-route-runtime APPLIED; fox2-governance-preflight APPLIED (direct offline only); fox2-status-roadmap APPLIED; fox2-feature-certification APPLIED; fox2-agent-prompt-builder NOT_APPLICABLE to CHAT-direct correction (REQUIRED if new Agent dispatched).
