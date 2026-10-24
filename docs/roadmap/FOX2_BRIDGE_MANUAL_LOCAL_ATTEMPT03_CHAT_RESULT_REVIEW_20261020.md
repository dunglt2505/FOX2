# FOX2 — CHAT Independent Result Review: Native Offline Attempt 03

**Review date:** 2026-10-20 · **Stage:** TEST evidence intake for existing BUILD/BLOCKED feature · **Whole-WP:** FOX2-BRIDGE-RC1-TO-INTERNAL-READY · **WP:** FOX2-BRIDGE-MANUAL-LOCAL-ADMISSION-DEV-20261019.  
**Verdict:** `CHAT_ACCEPT_BLOCKED_EVIDENCE_ONLY / HOLD_BUILD / NO_NEW_AGENT_ATTEMPT_UNTIL_HOST_LIFECYCLE_EVIDENCE`. The CODEX run is **CONSUMED**, with no replay. Not an implementation acceptance, not an independent host or installed-runtime audit, not release.

## Immutable source lock / report provenance

- Attempt identity: `FOX2-BRIDGE-MANUAL-LOCAL-ADMISSION-DEV-20261019-NATIVE-OFFLINE-ATTEMPT-03`.
- Original task: `04c9141f9a9bc47504473aa577b24201734d8c0b:docs/agent_handoff/FOX2-BRIDGE-MANUAL-LOCAL-ADMISSION-DEV-20261019/NATIVE_OFFLINE_ATTEMPT_03/task.md`; blob `f339288fb1ec12ca526bc4aabea74fb9ac51b410`.
- Executable prompt: `ee76cec618276b8b5301e95d31339fe9da147230:docs/agent_handoff/FOX2-BRIDGE-MANUAL-LOCAL-ADMISSION-DEV-20261019/NATIVE_OFFLINE_ATTEMPT_03/prompt.md`; blob `7a59230759d1ad2e1fcca6752a746b636fa56bfb`.
- CHAT final admission: `26c112885a22752b47878b6b05bb61d65cae8631:docs/agent_handoff/FOX2-BRIDGE-MANUAL-LOCAL-ADMISSION-DEV-20261019/NATIVE_OFFLINE_ATTEMPT_03/chat_final_admission.json`; blob `f6bd6a127094fa15ee6b5ebf16f710cce3dd530b`. The admission was CONDITIONAL on fresh host writer/process and pinned CLI; historical PreExec is not perpetual host attestation.
- Fresh prior PreExec PASS: `3167d8502588dd106f9a4cea8ef931e9148040ff:reports/FOX2-BRIDGE-MANUAL-LOCAL-ADMISSION-DEV-20261019/preexec/native_offline_attempt03_preflight.json`; blob `3a00c1f5905cb6ef340673f5791b0d1cbc1527a6`. Eight material PASS, zero blockers at observed time, no coding Agent started when receipt issued.
- Remote CODEX result branch `work/FOX2-BRIDGE-MANUAL-LOCAL-ADMISSION-DEV-20261019-NATIVE-ATTEMPT-03` HEAD **`a3ad10d490993fb4ed4ccfd7d1a73f74cc465581`**, exactly one commit after expected code source `3167d8502588dd106f9a4cea8ef931e9148040ff`; CODEX console independently supplied the same actual SHA outside committed results, no invented result SHA.
- The commit changes **only** `reports/FOX2-BRIDGE-MANUAL-LOCAL-ADMISSION-DEV-20261019/{report.md,evidence_manifest.json,test_summary.json,diff_trace.json}`, all ADDED. Remote Git blobs respectively `de4d0dbdeaf0208118881075aeb3f07f8833d667`, `10d30e1b4de3f745879e354f9acc4442a61557e9`, `b240146a364fff9073b5fc87173221779ec8f982`, `d8525d8d98b954636539a619fdd389a4fb5ede44`. All original Git report bytes re-fetched independently; the manifest's three external SHA-256 evidence hashes and each non-self changed-path SHA-256 match actual remote UTF-8 bytes. The manifest self-hash is intentionally null; `source_manifest_sha256` matches `diff_trace.json`.
- Manifest `submission_state=BLOCKED` / `git.delivery_status=PUSHED_UNREVIEWED` truthfully represent Agent delivery before CHAT independent acceptance. The reported CODEX process exit 0 is not a successful code result. No new code/test hunks; Attempt02's six red tests remain blob `7b2a2c48e6bf4225d849dc7a7a32126652b0c3be`. K1 result-only hunks `JUSTIFIED_GENERATED`; engineering hunks empty.
- Git bytes and manifest fields independently checked; **full JSON Schema 2020-12 validation was reported by CODEX but not independently rerun by CHAT**. No new Windows local test process was executed by CHAT.

## Test / safety analysis, without promotion of FAIL

| Evidence item | Outcome | Scope and limitation |
|---|---|---|
| Initial collection | FAIL, exit 4 | Missing package import / PYTHONPATH. Corrected then reran. Preserve first failure. |
| Fresh focused suite six modules | FAIL, exit 1 | 244 collected: **210 PASS / 34 FAIL**. Six persistent no-replay failures plus 28 PreExec Git long-path failures. |
| PreExec isolated module rerun | PASS, exit 0 | **65 PASS** with process-local `core.longpaths=true`; Git config files unchanged. This narrows the 28 PreExec failures to fixture path environment but DOES NOT turn whole focused suite green. |
| Sequential current-exit then legacy-process-restart fixture | FAIL safety | Current and restarted legacy each returned `claimed=true` for the same synthetic identity, both process exit 0. Demonstrates no durable cross-root claim guarantee under the fixture. |
| Positive MANUAL_LOCAL / new crash/concurrent/safety matrix | NOT_RUN | No production code and no implemented guarded positive route. |

**Critical scope distinction:** The sequential fixture runs two Python subprocesses using fixture current/legacy roots and code in this repository, NOT the actual frozen executable or installed Windows legacy supervisor. The failing fixture is sufficient to disprove a claimed general no-replay invariant for those source paths. It **does not prove** a legacy executable is currently installed, auto-started or enabled on FOXLE-PC.

Source inspection remains consistent with the test findings: `desktop.initialize_runtime` uses a temporary legacy lock and once-only copy when the current DB does not yet exist; manual consumption parsing covers only current root. `ledger.claim_dispatch` uses `BEGIN IMMEDIATE` within one DB, which cannot atomically bind independent old/new ledgers. Process lock release at process exit does not durably fence an old executable after restart. A new current-root flag is not evidence that a historical legacy program reads it.

## Correctness and K1 decision

The earlier candidate design `bd5cd44e31ceb7384b558c8fb08ccefd98dfb9e6:docs/roadmap/FOX2_BRIDGE_CROSS_ROOT_NO_REPLAY_DESIGN_CONTRACT_CANDIDATE_20261020.md` correctly requires fail-closed when old-writer retirement/fencing cannot be established. Exact code paths previously approved for the **new attempt's bounded implementation** remain `desktop.py`, `ledger.py`, `test_desktop.py`, `test_runtime_ledger.py` plus the six original primary paths. No authorization to edit `process_lock.py`, `startup.py`, `installation.py`, `ops_runner.py` or other files, and no permission to modify installed Worker/ledger/launcher.

**CHAT review conclusion:** More implementation attempts under the same unproved positive identity-lifecycle premise risk another safety-driven STOP and wasted credits. First collect **READ-ONLY HOST LIFECYCLE EVIDENCE** for exact legacy/current roots, installed versions/entrypoints, active processes and the per-user scheduled tasks/Run-key/Startup shortcut registrations. This is a bounded host inventory, **not a request to disable/uninstall/stop/run** a legacy Worker. Treat UNKNOWN/no visibility as UNKNOWN, never `LEGACY_RETIRED`.

After actual host evidence:
1. If an old executable/launcher remains active, present a separate authorized quiescence/retirement procedure with no-replay/rollback preservation and require fresh host PreExec/Owner permission for any operational change; do not do it from Chat implicitly.
2. If no old launcher found, absence in a bounded inventory alone is NOT cryptographic durable retirement proof. Resolve how all authorized startup surfaces and old worktrees are controlled; then design a testable admissible transition. If this cannot be guaranteed, implement fail-closed offline guard and keep all positive/manual LIVE paths HOLD.
3. If a genuinely shared identity authority can be proven compatible with **both** executables, document exact compatibility and concurrency semantics before code. Do not claim an old binary honors a new flag without code/version evidence.
4. Only then issue a **new non-replayed Attempt 04** under the existing Whole-WP after Prompt Builder + fresh route-specific host PreExec + one-writer. Preserve all prior markers, receipts and Git history. Never rerun Attempt 03.

## Feature/status and protected gates

`STAGE=BUILD` · `STATUS=BLOCKED` · `EVIDENCE=CHAT_ACCEPTED_BLOCKED_ONLY` · `EXIT_GATE=HOST_LEGACY_LIFECYCLE_EVIDENCE_AND_PROVEN_DURABLE_CROSS_ROOT_NO_REPLAY`. Six negative test identities remain FAIL, new positive MANUAL_LOCAL NOT_RUN, installed Bridge readiness NOT_ATTESTED. Original Bridge bootstrap PreExec BLOCKED, COMPAT001 PUBLISHED_HOLD, Canary009 HOLD. No main/merge/installed adoption, Worker resume, Dispatch activation, broker/provider or LIVE.

**Skills:** `fox2-result-review` REQUIRED/APPLIED; `fox2-execution-recovery` APPLIED no-replay; `fox2-source-resolver` APPLIED; `fox2-governance-preflight` APPLIED (read-only/CHAT review), `fox2-status-roadmap` APPLIED lazy feature update; `fox2-techspec-validator` APPLIED design-consumer semantics read-only; `fox2-agent-prompt-builder` NOT_APPLICABLE to existing returned result, REQUIRED only for any later NEW assignment.

**GOAL_REPORT_REVIEW_MET=YES / GOAL_IMPLEMENTATION_MET=NO / NEXT_SAFE_ACTION=READ_ONLY_HOST_LEGACY_LIFECYCLE_INVENTORY / REAL_BLOCKER=NO_INSTALLED_HOST_RETIREMENT_AUTHORITY_EVIDENCE**. CHAT remains orchestrator; no autonomous/background action asserted.
