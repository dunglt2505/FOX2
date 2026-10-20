# FOX2 — CHAT Intake: F0 focused pytest, Owner Windows host run (2026-10-20)

**Whole-WP:** `FOX2-BRIDGE-RC1-TO-INTERNAL-READY` · **Feature:** `FOX2-BRIDGE-MANUAL-LOCAL-ADMISSION` · **Stage:** BUILD · **Acceptance verdict:** `FOCUSED_TEST_GATE_PASS_HOST_REPORTED / F0_FULL_ACCEPTANCE_HOLD` · **Agent execution:** NONE on this test. `CODEX/gpt-6.1-sol/medium` remains pinned and no new Agent attempt created. Attempt06 previously CONSUMED/NO_REPLAY.

## Provenance of test result

The Owner pasted the full output from an explicitly isolated local PowerShell 7.6.7 invocation on FOXLE-PC, running pytest 8.3.5 against the Git-source-locked branch `work/FOX2-BRIDGE-F0-CHAT-DIRECT-REGRESSION-20261020@1442cd6352cbfdd3684284cd83e572b71fabebf5`:

```text
........................................................................ [ 28%]
........................................................................ [ 57%]
........................................................................ [ 86%]
..................................                                       [100%]
250 passed in 133.34s (0:02:13)
source_sha = 1442cd6352cbfdd3684284cd83e572b71fabebf5
test_exit_code = 0
counts.tests = 250
counts.failures = 0
counts.errors = 0
counts.skipped = 0
failed_tests = []
codex_invoked = false
f0_accepted = false
status = FOCUSED_PASS_PENDING_CHAT_REVIEW
```

Evidence files were produced locally at the host path ending in `FOX2_F0_RESUME_6b9e34998b07/focused.xml` and `focused.log`. **Their bytes and cryptographic hashes were NOT transferred to CHAT; CHAT has NOT independently read or parsed JUnit/log content.** This is **Owner-host reported direct stdout** plus Git source readback, not an Agent-authored Git Result v2, CI run or independently repeated pytest. The test was intentionally offline, without installed Bridge/Worker, protected dispatch, paid Agent, broker/provider or LIVE. The host script did create disposable local test files/worktree; it did not install or run Bridge.

## Separate Git source review

CHAT re-fetched source branch: unchanged exact HEAD `1442cd6352cbfdd3684284cd83e572b71fabebf5`, descendant of consumed Attempt06 partial code `d2c595be123fa041720fd0467f9d94b2d4318bca` by five commits and no behind. Actual changed paths from Attempt06 snapshot:
- `agent_bridge/src/fox2_agent_bridge/ledger.py` — only six-line direct-installed-current-root default DENY guard; Git blob `c69b63dc7afd4b26a2701cb24c795b6d8c1a1f3f`.
- `agent_bridge/tests/test_desktop.py` — genuine schema-v3 historical fixture/migration preservation of result+cursor; Git blob `0bfc180259dc23e6aa4e1a33b8deb735a18df0ca`.
- `agent_bridge/tests/test_runtime_ledger.py` — six offline tests for sticky unknown, missing/invalid authority, v4→v5 migration, concurrency deny, isolated single-root atomic uniqueness and direct-root initialization; Git blob `31a78abb273d2052b0696e89e24b5a513e331551`.
- Original protected `agent_bridge/tests/test_e2e_runner.py` retained exact blob `7b2a2c48e6bf4225d849dc7a7a32126652b0c3be` including six negative cross-root no-replay assertions.

Diff test scope is the ten earlier bound paths; no historical Agent report, marker/receipt, governance authority, installed runtime or Task Scheduler modified. **This source evidence supports bounded K1/scope PASS for the three new diff paths**, not installed or global safety certification.

## What PASS proves, and what it does not

**PASS as Owner-host observation only:** the six named focused modules (`test_e2e_runner.py`, `test_project_dictionary.py`, `test_desktop.py`, `test_runtime_ledger.py`, `test_ops_runner.py`, `test_preexec.py`) completed at locked source SHA with exit 0, all 250 testcases passed. The *previous* single migration v3 regression is no longer present in failed tests; the six preserved original negative tests are within passing focused suite.

**Still NOT VERIFIED:** raw JUnit/log authenticity and completeness, full repository test suites, independently sourced Windows test reproduction, separate destructive/crash-window injection (power loss, pre/post claim persistence, post-spawn), positive installed Manual Local, Agent result publication schema v2 for consumed Attempt06, old executable restart prevention or shared atomic authority, installed bridge ledger/one-writer runtime state. Frozen legacy executable is not made aware of new claim guard by a current-root patch. Existing F1 (durable retirement) is a separate HOLD and never implied by 250 green tests.

**F0 completion distinction:** This is `FOCUSED_TEST_SUBGATE_PASS` in the continuing F0 source BUILD candidate, **not `CHAT_ACCEPT_F0`**. No false historical conversion: Attempt06 remains incomplete with actual model-capacity failure, partial code captured, no Agent-authored Result Contract. CHAT-direct source corrections and owner tests are separately attributed; do not reconstruct an Agent-authored report.

**CHAT decision:** `ACCEPT_SCOPED_FOCUSED_TEST_EVIDENCE / FULL_F0_BUILD_HOLD`. Continue further bounded safety test coverage and implementation evaluation; don't create another coding attempt or replay unless a new task is warranted and real route-specific gates are observed. F1, Canary009, COMPAT001 and LIVE remain HOLD.

**NEXT_SAFE_ACTION:** independently inspect fresh structured JUnit/log bytes when available; examine F0 crash-window/no-spawn/alternate-root coverage and source correctness with code-first review before any BUILD acceptance; any additional edits require fresh source-specific tests. Continue only on a bounded CHAT direct source route or newly authorized source-bound Agent task. Owner's result removes the earlier blocker 'focused pytest not run'—do not ask to rerun that same passing suite without a material source change.
