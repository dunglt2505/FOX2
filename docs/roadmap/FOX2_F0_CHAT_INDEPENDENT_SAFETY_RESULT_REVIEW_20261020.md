# FOX2 — CHAT independent Git Result Review: F0 safety delivery (2026-10-20)

**Project:** FOX2 · **Whole-WP:** `FOX2-BRIDGE-RC1-TO-INTERNAL-READY` · **Feature:** `FOX2-BRIDGE-MANUAL-LOCAL-ADMISSION` · **Stage:** BUILD/BLOCKED.  
**Decision:** `ACCEPT_SCOPED_OFFLINE_SAFETY_SOURCE_AND_TEST_SUBGATES` / `HOLD_FULL_F0_BUILD` / `HOLD_F1_INSTALLED_ADMISSION` / `HOLD_CANARY009_LIVE`.

This is a **separate CHAT review of the returned Work-produced Git evidence**, not the return's self-declared CHAT acceptance, not a new task/Agent Dispatch, and not an Agent-authored Result v2. No previous consumed task/attempt is replayed.

## Verified immutable Git identities and K1 scope

- Work-reported remote head `11900a9dc8ab96ef3570d3c6e4c0e995651a8fc3`, branch `work/FOX2-BRIDGE-F0-CHAT-CRASH-REVIEW-20261020`, was independently fetched. Its parent `008c6e7d1a1c2d7456a3530ce6e3f38e88510600` is the report/JUnit publication; status and remote_intake are the only files added/modified in `11900a9`. **The code source is separately `611ec26c28484de740e963d86de6b00946f1492d`**, not `11900a9`.
- Compared with previously accepted focused baseline `185bc9493d4a9e27f7a463d87313fc03ce32634d`, code source `611ec26...` is two commits ahead, zero behind. Exactly THREE modified paths: `agent_bridge/src/fox2_agent_bridge/desktop.py` (+6/-2, `NECESSARY_DEPENDENCY`), `agent_bridge/tests/test_runtime_ledger.py` (+142, `REQUESTED/NECESSARY_DEPENDENCY`), `agent_bridge/tests/test_lock_logging_health.py` (+6/-1, `NECESSARY_CONSUMER_COMPATIBILITY`). Third path is outside prior narrow ten-path coding allowlist but is explicitly a corresponding health-consumer test impacted by schema v5 and was scoped in current CHAT-direct continuation; **its addition is NOT evidence of a retroactively expanded Attempt06 Agent grant**.
- The protected original six cases reside in `agent_bridge/tests/test_e2e_runner.py`, unchanged blob `7b2a2c48e6bf4225d849dc7a7a32126652b0c3be`. Nine selected focused test/source file blobs, including `desktop.py` and `ledger.py`, were compared individually and are identical between focused execution source `ba1cbdf2c8bc2b74bd7cac7f6a43065a54c5d4f0` and final `611ec26...`. Final source changes from `ba1cbdf...` only in the health-consumer test, which was covered by a distinct final-source 88-test run.
- The code change in `desktop.initialize_runtime` unconditionally calls `ledger.initialize(cross_root_authority_unknown=True)` even when `--config` selects a root outside canonical `BRIDGE_ROOT`. Test covers fresh and pre-existing `SINGLE_ROOT` metadata and failure to claim. This plugs a reproduced **configured runtime root** positive-claim bypass without asserting that arbitrary raw `SQLiteLedger` use from an unrelated filesystem root is governed.
- These three paths have a genuine F0 cause/effect K1 explanation and are not changes to governance, installed launcher, CLI permissions, protected tests, Policy, frozen Agent Result or Canary. No source/feature gate is promoted EFFECTIVE.

## Test evidence, independently read and verified

Work result: `008c6e7d1a1c2d7456a3530ce6e3f38e88510600:reports/FOX2-F0-CHAT-SAFETY-REVIEW-20261020/` includes `report.md`, `test_summary.json`, raw focused and consumer JUnit/log, baseline owner 254 JUnit/log, failing red-run and environment failures. Work's `remote_intake.json` at `11900a9...` asserts its own readback; independent CHAT checks follow.

CHAT fetched actual Git bytes and **independently recomputed SHA-256** with a UTF-8 implementation self-tested against the standard `abc` digest. All seven selected raw files equal published `evidence_hashes.json`:
- `focused.xml` `4eecaf456995c95b40b078443b45a65195baeec83c69e9e5ccd608edb9ea5b14`;
- `focused.log` `d8dfaf85478086874bdea43af2791d88e2b69ece6b763c67aae6b921e8224f54`;
- `short-runtime-consumers.xml` `ec1018ecf23ba1e427883e2a619a63e17c74359a7571f715d4d9dfb3bfb450bb`;
- `short-runtime-consumers.log` `51645f7f74381c1d17ec308be2eebca75995786c9f0bbac37ae1bd1bdfa29e27`;
- `owner-185-focused.xml` `acdfa9e021e1efdb34a6ebfc3457074d68f11b2caaad37cdaf04680b43b6bcb9`;
- `owner-185-focused.log` `653f7944d59a5da245c4f8055f0fbbda04f0c57e32b8e10b52e36765675e0292`;
- `red.xml` `23a283844867dfaa25ccd3ef303c266a2fc9606259ba69675eb7b85d67c1cde8`.

CHAT parsed the Git-sourced JUnit XML text independently (testsuite attributes and testcase nodes): **267/267 focused** with 0 failures/errors/skips, **88/88 consumer** with 0 failures/errors/skips, six protected no-replay testcase names present, 13 new configured-root/crash/configuration-recovery testcase instances present. The 267-suite reported 252.189 seconds, the 88-suite 59.651 seconds. Work result reports actual pytest exit 0 for both runs, **not independently observed process exit** by this CHAT thread. The 254 Owner-host baseline is also hash-matched, not transferred merely by repeated verbal assertion.

Scope caveat: `267 focused` executed on `ba1cbdf...`, not byte-for-byte the *whole final* code tree at `611ec26...` (but all six selected test modules and key production sources identical); `88 consumer` executed at exact final `611ec26...`. Thus the two suites are **complementary**, not a literal single execution of all 355 tests against one entire tree. No claim of complete repository test or installed acceptance is made.

Previously failing evidence is **preserved**, not converted to PASS: `red.xml` demonstrates old configured-root bypass (1 FAIL), `sandbox-focused.xml` had 3 FAIL/43 ERROR from constrained Git/temp sandbox, `runtime-consumers.xml` had 16 FAIL (mostly WinError 206 deep paths, one stale health assertion). The later successful suites used an isolated short-path worktree and fixed the schema assertion. Underlying failures are not erased and remain separately labeled.

## Contract and risk limits

1. **Consumed Attempt06:** `CODEX/gpt-6.1-sol/medium` remains pinned/HOLD. The original CODEX Attempt06 Result Contract v2 was NOT delivered. The new Work/CHAT-owned report and Git evidence are authentic **as their own artifact**, but **cannot be substituted as Agent-authored Result v2 without an explicit scoped protocol disposition**. An earlier conversational Work handoff is not independent proof of a Git-first Agent task/prompt for this separate review; no retrospective PASS on that assignment is asserted.
2. **Offline F0 safety:** All scoped source/test acceptance surfaces named above meet the evidence threshold for `ACCEPT_SCOPED_OFFLINE_SAFETY_SOURCE_AND_TEST_SUBGATES`. This is not `ACCEPT_F0_BUILD`; formal delivery gating remains unresolved.
3. **Claim boundary:** F0 denies current configured Bridge runtime claims while legacy authority is UNKNOWN. It does not change/retire the legacy executable or prove a dual-version atomic consumed-identity authority. Direct raw `SQLiteLedger` fixtures outside an installed/configured runtime can still accept claims; the code report explicitly acknowledges this API boundary.
4. **Crash:** Synthetic Python child tests exercise durable stages and no replay after interrupt; no actual paid Agent, still-running child lifecycle, Windows power-loss/fsync or installed worker recovery was executed.
5. **Release:** F1 durable legacy fencing/retirement, installed artifact binding/adoption/rollback, Canary009 EXACTLY_ONCE, exact configuration/full access/usage/restart/readback/CHAT final intake are all `HOLD/NOT_RUN`. No merge/main, provider/broker/LIVE, Worker resume or frozen Dispatch replay.

## Reconciled Feature Status and next safe action

CHAT independently diffed operational `docs/roadmap/FOX2_FEATURE_STATUS.json` between `4cdb2b26861eeb3a84d31536d6c4138731ad60c8` and `11900a9dc8ab96ef3570d3c6e4c0e995651a8fc3`: same two feature IDs, non-target feature structurally unchanged, global fields unchanged, only `FOX2-BRIDGE-MANUAL-LOCAL-ADMISSION` updated. It correctly records `stage=BUILD`, `status=BLOCKED`, `source_sha=611ec26...`, `f0=SCOPED_SOURCE_AND_OFFLINE_SAFETY_ACCEPTED; FULL_BUILD_HOLD_RESULT_DELIVERY_GATE`, `F1=HOLD`. **No further Feature Registry mutation needed** from this independent review.

**CHAT verdict:** `ACCEPT_SCOPED_OFFLINE_SAFETY_SOURCE_AND_TEST_SUBGATES`; `HOLD_FULL_F0_BUILD`, `HOLD_AGENT_RESULT_V2_SUBSTITUTION`, `HOLD_INSTALLED_F1_AND_CANARY`.

**NEXT_SAFE_ACTION:** resolve formal delivery disposition *prospectively* for CHAT-direct F0 versus immutable consumed Attempt06 Agent Result v2, without silently waiving/recreating the old Agent output. If Policy/Protocol allows a separate CHAT-direct completed-delivery contract, publish it as CHAT-authored with source SHA/test manifest and independent acceptance; if the protocol unambiguously requires Agent Result v2 for this Whole-WP, hold until an explicit scoped Owner governance exception or a new governed eligible attempt (not replay) is authorized. No extra repeated test runs needed on unchanged code. Keep F1 installed retirement and Canary gates separate.

**Skill application:** `fox2-result-review=REQUIRED/APPLIED`, `fox2-source-resolver=APPLIED`, `fox2-feature-certification=APPLIED`, `fox2-status-roadmap=APPLIED`, `fox2-execution-recovery=APPLIED`, `fox2-governance-preflight=APPLIED`. `fox2-agent-prompt-builder=NOT_APPLICABLE` for returned artifact intake; REQUIRED for any new Agent task. Independent runtime audit `NOT_APPLICABLE` to offline scoped test acceptance, REQUIRED only at release-specific gate.

**GOAL_MET:** independent review of returned Git artifacts and safety subgates YES; full F0 BUILD NO. **REAL_BLOCKER:** original consumed Agent Result Contract and installed dual-root safety unsatisfied. No background work.
