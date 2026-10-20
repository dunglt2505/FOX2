# FOX2 — CHAT direct F0 safety-test intake: 254/254 focused PASS (Owner host)

**Date:** 2026-10-20 · **Whole-WP:** `FOX2-BRIDGE-RC1-TO-INTERNAL-READY` · **Feature:** `FOX2-BRIDGE-MANUAL-LOCAL-ADMISSION` · **Status:** `BUILD / BLOCKED` · **Verdict:** `ACCEPT_FOCUSED_SAFETY_TEST_GATE_HOST_REPORTED / F0_BUILD_ACCEPTANCE_HOLD`.

## Provenance and source lock

The Owner supplied complete final PowerShell stdout for `FOX2_F0_OFFLINE_FOCUSED_RESULT_V1` from Windows PowerShell7 using a new disposable Git test worktree. This is **Owner-host execution evidence**, not a CODEX/WORK completion, CI test result, Git-delivered Agent Result Contract or independently replayed CHAT pytest. No CODEX Agent invocation, installed Bridge execution or broker/provider/LIVE actions were requested by that test script.

**Source:** `work/FOX2-BRIDGE-F0-CHAT-DIRECT-SAFETY-COVERAGE-20261020@185bc9493d4a9e27f7a463d87313fc03ce32634d` (remote branch HEAD independently re-fetched by CHAT and matched). Compared with previously tested `1442cd6352cbfdd3684284cd83e572b71fabebf5`, SHA is a direct +2-commit descendant, only two changed paths:
- `agent_bridge/src/fox2_agent_bridge/ledger.py` (+7/-2), a **NECESSARY_DEPENDENCY** to add an installed-root claim-time fail-closed guard for direct claim callers and alias/custom installed DB paths;
- `agent_bridge/tests/test_runtime_ledger.py` (+147/-0), **REQUESTED/NECESSARY_DEPENDENCY**: four additional focused negative cases (existing SINGLE_ROOT bypass, alternate DB/canonical alias, abrupt SQLite transaction precommit child exit, E2E no post-claim Agent spawn).
- Original protected `agent_bridge/tests/test_e2e_runner.py` Git blob `7b2a2c48e6bf4225d849dc7a7a32126652b0c3be` unchanged, including six cross-root no-replay negative assertions.

Prior source preparation and review: `eb685218632155cfefd7d44a4f29ee4777b33f74:docs/roadmap/FOX2_F0_CLAIMTIME_CRASH_NOSPAWN_DIRECT_REVIEW_20261020.md`. The earlier 250/250 suite was run on the previous SHA only; it is historical now. The new result below is the *relevant* test gate for the new SHA.

## Submitted direct host result

```text
254 passed in 143.59s (0:02:23)
schema: FOX2_F0_OFFLINE_FOCUSED_RESULT_V1
source_sha: 185bc9493d4a9e27f7a463d87313fc03ce32634d
pytest_exit: 0
counts.tests: 254
counts.failures: 0
counts.errors: 0
counts.skipped: 0
original_negative_cases: 6
new_safety_cases: 4
failed_tests: []
agent_invoked: false
installed_bridge_tested: false
verdict: FOCUSED_PASS_PENDING_CHAT_REVIEW
f0_accepted: false
```

**Owner-host JUnit SHA-256:** `ACDFA9E021E1EFDB34A6EBFC3457074D68F11B2CAAAD37CDAF04680B43B6BCB9`.  
**Owner-host log SHA-256:** `653F7944D59A5DA245C4F8055F0FBBDA04F0C57E32B8E10B52E36765675E0292`.  
Files remain on Owner host under temporary run folder `FOX2_F0_FINAL_a61b033a6f5f4095af53ad3db8d63a69/evidence/{focused.xml,focused.log}`. **CHAT has not independently read those raw local bytes or recomputed their hashes.** They are pointers, not independently validated Git evidence. There is no published test-related commit in the code branch; no Agent Report Contract was forged for consumed Attempt06.

## Gate matrix and limits

| Gate | CHAT decision |
|---|---|
| Git code remote SHA, 2-commit ancestry, source changed-path allowlist | VERIFIED |
| Protected six negative test source blob | VERIFIED unchanged |
| Six original no-replay negatives (collected by host script) | PASS per host stdout |
| Four new safety negatives (collected by host script) | PASS per host stdout |
| Full focused modules (254, 0 failure/error/skip, exit 0) | **PASS_HOST_REPORTED / ACCEPT_SCOPED_TEST_GATE** |
| Raw JUnit/log independent ingestion + recomputed hashes | NOT_VERIFIED |
| Complete source-level F0 BUILD review and required broader regression/integrity | NOT_ACCEPTED / further evidence needed |
| Real post-agent-spawn crash and durable cross-root legacy restart prevention | NOT_RUN / F1 retirement not proven |
| Agent Attempt06 Result Contract v2 | NOT_DELIVERED; Attempt06 consumed, **NO_REPLAY** |
| Installed Bridge Worker and MANUAL_LOCAL positive admission | HOLD |
| Canary009, COMPAT001, main/merge, provider/broker, LIVE | HOLD |

### Important distinction

The positive synthetic single-root claim cases are controlled fixtures and are not authorization to claim from an installed current-root Bridge. The current F0 guard explicitly **DENIES** installed-root positive claims when legacy lifecycle/authority is unknown. A frozen legacy writer can still operate against its own ledger and ignore this new guard: **system-wide old executable fencing remains F1/HOLD**. Test child abruptly exiting inside an uncommitted transaction validates SQLite rollback under fixture conditions, not power-loss durability or a real paid Agent crash. The E2E no-spawn fixture intercepts pre-spawn boundaries; it does not invoke a real Agent.

## Outcome

**CHAT verdict:** `ACCEPT_SCOPED_FOCUSED_TEST_GATE_HOST_REPORTED`, without inferring `F0_FULL_BUILD_ACCEPTED` or `F1_READY`. Original Attempt06 code/result state remains separate and incomplete. No new CODEX Agent was issued, no previous identity replayed, and pinned CODEX model/effort remains unchanged.

**NEXT_SAFE_ACTION:** direct CHAT source/acceptance gap review, including crash-after-claim/post-agent-start, adversarial root path resolution and full source-diff result contract distinctions; request raw JUnit only if independent test-file authentication becomes material to final acceptance, not as an excuse to re-run unchanged successful focused tests. If a material safety code change is needed, bind a new candidate SHA and rerun only affected tests plus required regressions. Keep F0 BUILD/BLOCKED until independent acceptance; F1/Canary/LIVE HOLD.

**Skill coverage:** `fox2-result-review=APPLIED` (scoped intake only), `fox2-feature-certification=APPLIED`, `fox2-status-roadmap=APPLIED`, `fox2-source-resolver=APPLIED`, `fox2-execution-recovery=APPLIED`, `fox2-governance-preflight=APPLIED`; `fox2-agent-prompt-builder=NOT_APPLICABLE` (no new Agent assignment).
