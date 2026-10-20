# FOX2 F0 — CHAT partial output review and Owner coding HOLD

Whole-WP: FOX2-BRIDGE-RC1-TO-INTERNAL-READY. Feature: FOX2-BRIDGE-MANUAL-LOCAL-ADMISSION.
Infrastructure WP: FOX2-BRIDGE-MANUAL-LOCAL-ADMISSION-DEV-20261019. Date: 2026-10-20.

**Verdict: REWORK / BUILD BLOCKED / CODING HOLD BY OWNER. F0 NOT ACCEPTED.**

## Immutable chain and provenance

- Candidate: `7d8a2f92ba43308c8b5a221080e3dd94560347c9`; original test-only code source: `5a82d08694f217415890f24802261aed625aa111`.
- Attempt06 task/prompt/source lock: `6c9f4d8a2167904ceb72b11dad8f8670cd3a4ca2`, directory `docs/agent_handoff/FOX2-BRIDGE-MANUAL-LOCAL-ADMISSION-DEV-20261019/F0_OFFLINE_ATTEMPT06/`.
- Fresh shared PreExec PASS and exact remote readback: `2a5be23098542bb45a676546a4f60820f65960b6`, receipt `reports/FOX2-BRIDGE-MANUAL-LOCAL-ADMISSION-DEV-20261019/preexec/F0_OFFLINE_ATTEMPT06/preflight_receipt.json`. Includes all 34 locked local Git sources, tooling, quota, pinned marker, isolated worktree/writer, Git delivery dry-run.
- Separate CHAT admission: `6ebe9e158effbc21ca9b23589487b830a5f36220`. Exact tuple CODEX / gpt-6.1-sol / medium; native offline architecture; supervisor-held exclusive OS lock with live ancestor PID verification.
- Partial code snapshot: `d2c595be123fa041720fd0467f9d94b2d4318bca`, branch `work/FOX2-BRIDGE-F0-OFFLINE-ATTEMPT06-20261020`. Only desktop.py and ledger.py changed (+32/-4). CODEX authored the actual file bytes; CHAT captured and published those identical bytes after the Agent failed. Both remote files were read back byte-for-byte.
- Snapshot is **not a completed Agent Git Result**. Agent-authored Result Contract v2/report/test/trace were not delivered. CHAT does not fabricate those artifacts or claim Agent acceptance.

## Actual execution and no-replay reconciliation

Attempt06 started once, wrote two source files, then returned CLI exit 1 with `Selected model is at capacity. Please try a different model.` at 2026-10-20T08:01:56Z. No Agent test/commit/push was observed. Actual post-start capacity failure supersedes earlier readiness for future execution; the original PreExec PASS remains historical evidence of the checks at that time.

Attempts04/05/06 are CONSUMED and may not resume/replay. Attempt04 stopped before product mutation due missing local immutable commit objects; remote source bytes were valid. Reconciliation `ade52ce9dca47d7adc8808eff934840b1acac0ef` records repair and all-source hash verification. Attempt05 stopped before product mutation because it tried to reacquire the supervisor's intentionally held lock; reconciliation `0cd63bcc338290f6aa13554e7b945e8ba601161f` clarified the supervisor-held lease for the separate Attempt06. Attempts01–03 and the host audit remain consumed under their original identities.

The Owner subsequently selected exactly **“Giữ gpt-6.1-sol; HOLD coding”** in this chat. Keep the pinned tuple, issue no new coding attempt, and do not silently switch model. Report/status publication and preservation of existing output complete the current reporting stage only.

## CHAT tests on captured partial bytes

CHAT independently ran the six required focused modules under an exclusive OS writer lock, with disposable fixtures and process-local `core.longpaths=true`; no global Git configuration, installed runtime, paid Agent test, provider, broker, Canary or LIVE call.

Command: `python -m pytest tests/test_e2e_runner.py tests/test_project_dictionary.py tests/test_desktop.py tests/test_runtime_ledger.py tests/test_ops_runner.py tests/test_preexec.py -q --junitxml=<host evidence>`.

Actual result: **243 PASS / 1 FAIL / 244 total**, exit 1, 129.51 seconds. All **six protected cross-root negative cases PASS**. The **entire original test_e2e_runner.py is byte-for-byte unchanged**, a stronger check than only preserving the six cases. Test evidence in this review bundle is CHAT-authored/observed, not an Agent-authored result manifest.

Failure: `test_desktop.py::test_v3_migration_preserves_dispatch_result_and_cursor`. The test constructs a schema-v3 ledger and calls the new `claim_dispatch` before migration. The new gate correctly denies missing claim-authority metadata, so the fixture never creates the historical dispatch/execution rows; `finish_execution` raises `DatabaseError: dispatch or execution row disappeared before completion`. The same test also contains later hard-coded version-4 expectations which will need review after truthful v3 fixture seeding. It is **not sufficient** merely to change 4 to 5 or weaken the fail-closed guard. Preserve historical result/cursor and idempotent migration assertions using a faithful legacy fixture.

## Standards, specification and K1 review

- Scope/permissions: PASS for the captured two-file diff. No other product paths changed. `ledger.py`: REQUESTED shared transactional claim-time gate; schema v5 initializes single-root authority, sticky UNKNOWN denial, and missing/corrupt authority denies under the same BEGIN IMMEDIATE as claim. `desktop.py`: NECESSARY_DEPENDENCY propagates current/legacy root context into initialization and places denial on a migration snapshot before publication. Both are among the ten previously bound paths. No unexplained or generated hunks.
- Six source-bound negative callsites: PASS, without assertion/test changes. Their patched disposable current/legacy roots activate runtime binding; protection is not limited to a hard-coded real installed path or Worker-only callsite.
- Regression compatibility: FAIL as described above. Do not accept the implementation while this required suite fails.
- Additional durable-guard evidence: NOT DELIVERED. Add committed, meaningful tests for reopening/default initialization, missing/corrupt authority state, restart/crash boundaries, concurrency, and no spawn, while preserving ordinary isolated single-root claims and control semantics. Existing historical tests and a six-case PASS do not substitute for the interrupted task's requested new coverage.
- Result Contract v2/K1 trace/delivery: INCOMPLETE. CHAT captured a permitted snapshot with explicit producer/publisher provenance; that does not replace the missing Agent-authored report/manifest/test_summary/diff_trace.
- Installed/global cross-root correctness: NOT VERIFIED. The frozen legacy binary does not learn this new guard. F1 positive admission still requires durable retirement or an authority protocol verifiably shared by both versions.

## Gates and status

SOURCE_BYTES_VERIFIED: 34 immutable references verified locally and against connector data. Scoped human authority: current Owner request plus recorded engineering approval. PUBLISHED_EFFECTIVE: scoped governance only. RUNTIME_ENFORCED: NOT_ATTESTED. No installed adoption or global machine effectivity is claimed.

F0: REWORK, not accepted. Feature: BUILD/BLOCKED, evidence TEST_EVIDENCED for partial output only. Positive installed Manual Local/F1/Canary009/COMPAT001/internal-ready remain HOLD/NOT_ATTESTED. No main/merge/deploy/runtime mutation occurred.

NEXT_SAFE_ACTION: retain this code/evidence snapshot and coding HOLD. After a new Owner instruction permits continuation, reconcile this consumed attempt and issue a **new** source-bound attempt with fresh material PreExec and admission, retaining gpt-6.1-sol/medium unless the Owner explicitly changes it. Do not resume Attempt06 and do not treat a future marker alone as completed implementation.

## Skill coverage

REQUIRED/APPLIED: source-resolver, governance-preflight, agent-route-runtime, agent-prompt-builder, execution-recovery, status-roadmap, result-review, feature-certification. Shared SDLC routing matrix was read. NOT_APPLICABLE: thread-handoff (no chat context transfer), brd-change-control/dictionary-impact (no business or Dictionary mutation), source-sync/document-publication (no Library sync or governed document release). No independent WORK assignment was necessary; CHAT reviewed a separate CODEX output. No mandatory Skill was unavailable.

GOAL_MET: NO, F0 incomplete. NEXT_SAFE_ACTION: reporting/preservation completed; coding waits for Owner continuation and a new valid route. REAL_BLOCKER: actual pinned-model capacity failure, regression FAIL, unfinished coverage and Result Contract, plus explicit Owner coding HOLD. No background work is assumed.
