# FOX2 F0 — CHAT direct claim-time safety review and remaining test gate
Date: 2026-10-20 · Whole-WP: `FOX2-BRIDGE-RC1-TO-INTERNAL-READY` · Feature: `FOX2-BRIDGE-MANUAL-LOCAL-ADMISSION`.

**Verdict:** `SAFETY_PATCH_CANDIDATE_PUBLISHED_SOURCE_VERIFIED` / `FRESH_TEST_NOT_RUN` / `F0_BUILD_HOLD` / `F1_INSTALLED_ADMISSION_HOLD`.

## Existing evidence and strict nonreplay

- Original Owner PowerShell7/Python3.13 pytest8.3.5 focused result: **250 tests PASS, 0 FAIL/ERROR/SKIP, exit 0**, exact source `1442cd6352cbfdd3684284cd83e572b71fabebf5`. Bounded Owner-host readback receipt: `f1431fddf9034db0eb45d76af1b71c53d9f27d62:docs/roadmap/FOX2_F0_FOCUSED_TEST_RESULT_OWNER_HOST_20261020.md`. The 250 PASS **do not certify the newer code**. Raw private JUnit bytes were not copied to Git.
- CODEX Attempt06 code snapshot `d2c595be123fa041720fd0467f9d94b2d4318bca` remains consumed, not replayed; old Attempt01–05 and legacy host-audit likewise no replay. Pinned CODEX `gpt-6.1-sol/medium` remains under Agent coding HOLD; CHAT did this small source/safety test addition directly and launched no Agent. No automatic internal-ready, installed Worker, Canary, broker/provider, LIVE.
- Current prior feature registry evidence at `530568ca075b918a7f69e8e05949772ef24e932d:docs/roadmap/FOX2_FEATURE_STATUS.json` reports `BUILD/BLOCKED`, `F0_FOCUSED_TEST_SUBGATE_PASS`, full F0 acceptance HOLD.

## New source branch and code review

`work/FOX2-BRIDGE-F0-CHAT-DIRECT-SAFETY-COVERAGE-20261020@185bc9493d4a9e27f7a463d87313fc03ce32634d` is an immutable descendant (+2 commits) of passing source SHA `1442cd6352cbfdd3684284cd83e572b71fabebf5`.

Exact diff allowlist (Git `compare_commits`, remote-readback verified):

1. `agent_bridge/src/fox2_agent_bridge/ledger.py` · blob `e97ad916b3d78f085a106bad74bc0ddd2aec82f4`. K1 `NECESSARY_DEPENDENCY`: In `initialize()` classify *any* DB under canonical installed `BRIDGE_ROOT` as `DENY_CROSS_ROOT_UNKNOWN`, not just exact `data/bridge.db`; at the shared `claim_dispatch()` interface, independently reject any resolved database path under installed BRIDGE_ROOT **before SQLite begins its claim transaction**. This closes a bypass where a preexisting DB's `claim_authority=SINGLE_ROOT` could be accepted if a direct caller skipped initializer. It does not modify frozen legacy executable or provide positive F1 admission.
2. `agent_bridge/tests/test_runtime_ledger.py` · blob `d6de83e81f138daceb5e656bafc7a5dc91a8a161`. K1 `REQUESTED/NECESSARY_DEPENDENCY`: four new fixture tests for (a) existing SINGLE_ROOT bypass, (b) alternate DB name/canonicalized relative alias within installed root, (c) abruptly exited *synthetic child process before SQLite transaction commit* with rollback and retained authority-denial, and (d) `BridgeE2ERunner.run_once` simulated valid upstream transport/prompt/worktree but DENY before agent preparation/spawn and no claim/execution rows. No paid Agent, protected Dispatch, real transport or installed DB touched by these tests.
3. Protected test file `agent_bridge/tests/test_e2e_runner.py` unchanged blob `7b2a2c48e6bf4225d849dc7a7a32126652b0c3be`; original six negatives not weakened.

**Test limits:** The abrupt-exit child test exercises an *uncommitted SQLite transaction*, not a real power failure/fsync guarantee. The E2E no-spawn test uses stubbed transport/poller and a forbidden post-claim preparation callback; not an installed paid CLI. Path alias test handles lexical/canonical variants within installed root, not arbitrary Windows volume/mount aliases. Other legacy executable might still restart and claim from its own database; no current-root-only change can certify global dual-root safety.

## Gate matrix

| Gate | Verdict |
|---|---|
| Source remote HEAD and ancestry | VERIFIED |
| Exactly 2 changed allowlisted paths, protected six tests unchanged | VERIFIED |
| Historical focused suite on earlier SHA | PASS 250/250, HISTORICAL |
| **Fresh pytest on SHA 185bc949...** | **NOT_RUN** |
| New no-spawn / alternate-DB / pre-commit child-exit tests | NOT_RUN |
| Real crash-after-commit/Agent-spawn and Windows installed restart test | NOT_RUN / separately gated |
| Raw owner JUnit independent intake | NOT_VERIFIED |
| Original CODEX Attempt06 Agent Result Contract v2 | NOT_DELIVERED; never synthesize |
| Complete F0 CHAT acceptance / TEST accepted | HOLD |
| F1 positive installed/root dual authority and Canary009 | HOLD |

**NEXT_SAFE_ACTION:** Run six focused modules and four new cases on exact `185bc9493d4a9e27f7a463d87313fc03ce32634d` in disposable worktree, collect exit/JUnit, independently compare raw evidence when accessible, then code-review/test-result intake. Only re-run 250 previous tests because source has materially changed; never reuse older PASS for newer SHA. If any new test fails, keep BUILD/BLOCKED and repair code or test without weakening assertion. No new CODEX Agent task, dispatch, PreExec or authorizations are implied by CHAT direct candidate publication.

**Skill application:** `fox2-source-resolver=REQUIRED/APPLIED`, `fox2-governance-preflight=APPLIED (CHAT_DIRECT_OFFLINE)`, `fox2-result-review=APPLIED (bounded evidence, no Agent Result)`, `fox2-feature-certification=APPLIED`, `fox2-status-roadmap=APPLIED`, `fox2-execution-recovery=APPLIED`, `fox2-agent-route-runtime=APPLIED`. `fox2-agent-prompt-builder=NOT_APPLICABLE`: no new Agent assignment.
