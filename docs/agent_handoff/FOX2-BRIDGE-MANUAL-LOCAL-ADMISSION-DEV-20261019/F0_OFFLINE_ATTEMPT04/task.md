# F0 offline implementation — conditional task binding, Attempt04

Whole-WP: FOX2-BRIDGE-RC1-TO-INTERNAL-READY. Feature: FOX2-BRIDGE-MANUAL-LOCAL-ADMISSION.
Infrastructure WP: FOX2-BRIDGE-MANUAL-LOCAL-ADMISSION-DEV-20261019. New one-shot identity: FOX2-BRIDGE-F0-OFFLINE-ATTEMPT04-20261020. This is the existing Whole-WP.
Prepared by CHAT under the current Owner request of 2026-10-20. SOURCE_READY / NOT_ADMITTED.
No executable start until a distinct CHAT admission binds the remote schema-v1 receipt and this exact task/prompt.

Role: CODEX coding/integration. Engine: native CODEX CLI 0.162.1 (observed). Model: gpt-6.1-sol PINNED.
Thinking: medium. Permission profile: FULL_ACCESS as source-defined capability, bounded by exact paths/actions below.
Architecture: NATIVE_OFFLINE_DEV, independent of installed Bridge. Not a Bridge Dispatch, MANUAL_LOCAL runtime activation, or renamed old attempt.
Git code source: 5a82d08694f217415890f24802261aed625aa111. Branch: work/FOX2-BRIDGE-F0-OFFLINE-ATTEMPT04-20261020. Worktree: C:\Users\Fox Le\.codex\.chatgpt-projects\g-p-6abcbc976b948191a760dbb0c316a64d\work\f0_offline_20261020\repo.
Delivery owner: AGENT; CHAT performs readback/intake separately. No WORK or parallel writer.

## Source/authority resolution and material gates
Use source_lock.json beside this task for immutable path/commit/blob/SHA256. Registry readback on its authorized release branch matched blob 1c28a6372a1cbbfd5341691ac9a5f98c8aa03e35.
Policy 2.0.0 / Dictionary 1.3 / Routing 1.4 apply to new human coordination under scoped Owner authority;
Protocol v12, PreExec v1.1, receipt v1 and result v2 remain unchanged. The source's generated machine Dictionary v1.2 is retained for shared PreExec contract verification; this task does not claim installed v1.3 adoption.
Do not change governance, generated binding, schemas, source locks or old receipts.
BRD-00/06/08 v0.5 and M1 acceptance v0.4 semantics unchanged; Bridge TechSpec v0.7 remains candidate.

Required route-specific PreExec: exact clean task/source/worktree/branch; shared engine and contracts;
exclusive writer observation + OS lock; Python/pytest/jsonschema/Git/PowerShell tooling; remote branch/permission;
actual pinned CLI marker/auth/config capability; current account quota; isolated offline fixture roots; no consumed marker/result-slot collision.
Installed Bridge lock/PAUSED/retirement is NOT a native offline DEV dependency under Policy 2.0.0 section 8.
Existing installed Worker is observed but untouched; no runtime DB, controls, locks or installed-root access is authorized.
If a proposed test would use it, STOP before that test. This confines the earlier design's Worker-state STOP to the dependent installed route; no waiver or false technical PASS.

## R0–R7
R0 existing WP BUILD/BLOCKED; Attempts01–03 and host audit consumed. R1 offline F0 only.
R2 scoped Owner authorization/current request, immutable source_lock. R3 actual host PreExec required, not historical PASS.
R4 CHAT completed direct source work; pinned CODEX for isolated Windows implementation; Copilot not selected, WORK not required.
R5 new worktree, exclusive lock/writer and quota must be observed. R6 new branch/result slot and exact Git publication/readback.
R7 exact tuple, paths, STOP, acceptance and Git delivery below. ASSIGNMENT_CHECK=HOLD_UNTIL_FRESH_RECEIPT_AND_CHAT_ADMISSION.

## Paths, acceptance, no-replay
Only these implementation/result paths may change after admission:
- `agent_bridge/src/fox2_agent_bridge/dispatch_normalizer.py`
- `agent_bridge/src/fox2_agent_bridge/e2e_runner.py`
- `agent_bridge/src/fox2_agent_bridge/app.py`
- `agent_bridge/src/fox2_agent_bridge/__main__.py`
- `agent_bridge/tests/test_project_dictionary.py`
- `agent_bridge/tests/test_e2e_runner.py`
- `agent_bridge/src/fox2_agent_bridge/desktop.py`
- `agent_bridge/tests/test_desktop.py`
- `agent_bridge/src/fox2_agent_bridge/ledger.py`
- `agent_bridge/tests/test_runtime_ledger.py`
- `reports/FOX2-BRIDGE-MANUAL-LOCAL-ADMISSION-DEV-20261019/report.md`
- `reports/FOX2-BRIDGE-MANUAL-LOCAL-ADMISSION-DEV-20261019/evidence_manifest.json`
- `reports/FOX2-BRIDGE-MANUAL-LOCAL-ADMISSION-DEV-20261019/test_summary.json`
- `reports/FOX2-BRIDGE-MANUAL-LOCAL-ADMISSION-DEV-20261019/diff_trace.json`

No other path change. Every material hunk requires REQUESTED/NECESSARY_DEPENDENCY/JUSTIFIED_GENERATED trace.
Protect the six source test cases and all assertions in test_e2e_runner.py lines 404–488 byte-for-byte; add new tests without weakening old ones.
Durable shared claim-time DENY while cross-root authority is UNKNOWN, propagated from initialized runtime roots to direct ledger claim; no hardcoded real-host-only condition or test special case.
Persist deny through reopening SQLiteLedger and process restart; do not read legacy live host DB. Single-root fixtures remain compatible.
No positive installed claim from simulated token; no current-only fence claim about old binary. F1 remains HOLD.
Focused tests: test_e2e_runner.py, test_project_dictionary.py, test_desktop.py, test_runtime_ledger.py, test_ops_runner.py, test_preexec.py.
Add meaningful restart/concurrency/crash/absent-corrupt-marker/no-spawn tests with synthetic roots. Preserve controls and SQLite BEGIN IMMEDIATE.
Use process-local git core.longpaths=true only if actually needed; never global Git changes.
No paid model calls in tests. No install, Worker start/stop/pause/resume, control polling/claim, protected Dispatch, Canary, provider/broker/LIVE/main/merge.
Any path/source/tuple/permission/writer drift or missing gate: STOP and report truthfully. Post-start failure consumes this attempt; no resume/retry.

## Git Result Contract
On the same authorized branch commit/push code and exactly four result files. evidence_manifest.json must validate against docs/agent_handoff/FOX2_AGENT_RESULT_SCHEMA_v2.json using FormatChecker.
Use source task commit as source, task_id as this attempt, real timestamps, test commands/counts/exits, K1 diff_trace and no secrets. Read the schema and report template; do not invent fields.
The manifest MUST NOT self-reference its containing commit. Supply remote result SHA separately in final stdout. git push is PUSHED_UNREVIEWED, never self-ACCEPT.
If push unavailable: preserve actual file bytes and report DELIVERY_BLOCKED; CHAT may publish only the same bytes with provenance and readback.

## Preserved candidate acceptance/source rationale
The following quoted candidate is reference data, subordinate to the exact binding/gates above; it is not an executable Dispatch:
# FOX2 — F0 Offline Fail-Closed Cross-root Claim Guard: SAME Whole-WP Task Candidate

**Publication kind:** `PREEXEC_CANDIDATE_ONLY / NOT_AGENT_DISPATCH / NOT_ADMISSION / NO_HOST_EXECUTION`. Date 2026-10-20. **Whole-WP:** FOX2-BRIDGE-RC1-TO-INTERNAL-READY. **Original infrastructure WP:** FOX2-BRIDGE-MANUAL-LOCAL-ADMISSION-DEV-20261019. This is the *next bounded coding candidate* inside the same existing WP, not a separate micro-WP; no consumed Attempt01/02/03 or host-audit identity is reused.

## Goal and R0–R7 state

**Technical F0 outcome:** implement an immutable/transaction-safe SHARED **DENY-BY-DEFAULT** claim-time gate while legacy/current root authority remains unverifiable. Make six previously failing cross-root fixture assertions PASS because newly admitted current claims are correctly rejected, not because tests are loosened. Permit no positive installed Manual Local/Worker claim or Canary as a side effect. **F1** (proving old writer retirement or a dual-version atomic authority and positive admission) is separate, HOLD, not implemented under F0.

**Role (tentative):** CODEX coding/integration, **Engine:** CODEX CLI; **Model:** PINNED `gpt-6.1-sol`; **Thinking:** medium; **Scope:** same WP, OFFLINE source/test only; **Permissions:** bounded exact allowlist and Git non-main, no installed runtime/broker/provider/main/merge/Canary; **STOP:** fail-closed if unverified identity/authority or unsafe dependency; **Result Delivery:** agent-generated report/manifest/trace/tests on authorized isolated code branch, remote result SHA external, CHAT independent intake. CHAT retains direct orchestration.

**R0** WP exists / feature BUILD BLOCKED; **R1** candidate offline DEV; **R2** Owner scoped engineering grant exists but source-design/installed effectivity must not be conflated; **R3** fresh target host CLI/task-specific PreExec `NOT_RUN`; **R4** CODEX selected candidate, not presently executing; **R5** host one-writer/quota `NOT_ATTESTED`; **R6** immutable Git test-only source verified, resulting branch/source must be locked when actual execution is issued; **R7** actor/model/scope/paths/STOP/result defined in this candidate; **ASSIGNMENT_CHECK=HOLD_R3_R5_NEW_PROMPT_AND_FINAL_ADMISSION`.

## Source set, authority and non-replay

- **Exact test-only source SHA:** `5a82d08694f217415890f24802261aed625aa111` on fresh branch `work/FOX2-BRIDGE-MANUAL-LOCAL-ADMISSION-F0-FAILCLOSED-SOURCE-20261020`. It is child of `65c50f7831722300a5418d0e9bc21f9f95988147`, adds only `agent_bridge/tests/test_e2e_runner.py` (+90 lines), test blob `7b2a2c48e6bf4225d849dc7a7a32126652b0c3be`. No earlier Attempt02/03 report namespace imported. The six negative tests are still FAIL at source-lock point.
- **CHAT latest design decision:** `44390e142f3dc5a7eace0a97c5b28c545d376b0b:docs/roadmap/FOX2_BRIDGE_DURABLE_FENCING_OFFLINE_BUILD_DECISION_20261020.md`, blob `418637fe553400f1533cab1c5d2da1485c6f6521`. Design candidate/bounded authorization for safe offline F0, NOT EFFECTIVE installed governance.
- **Prior technical design/K1:** `bd5cd44e31ceb7384b558c8fb08ccefd98dfb9e6:docs/roadmap/FOX2_BRIDGE_CROSS_ROOT_NO_REPLAY_DESIGN_CONTRACT_CANDIDATE_20261020.md`; blob `6e6d56df130b7153539a2bf1dba9f86d2fe591e4`.
- **Owner scope source:** `c23d28bd56d9d06d64561dcf255b2d94227f6acc:docs/governance/releases/FOX2_MANUAL_LOCAL_ADMISSION_OWNER_EXECUTION_AUTHORIZATION_20261019.json`, blob `dbc397375bb50ff4d87e093b114d5dda44d159b7`, CHAT-recorded Owner approval of conditional shared-layer engineering; not blanket write authority. No Owner reapproval for this bounded scope.
- **Actual failure/provenance:** CODEX Attempt03 report-only `a3ad10d490993fb4ed4ccfd7d1a73f74cc465581` and CHAT review `c659100b785ee75fdbe12b851ee30ec1d3aaf352`; 6 persistent negative no-replay FAIL, sequential current-exit legacy-restart synthetic claim=TRUE in both roots. Attempts01–03 **CONSUMED**, no replay.
- **Last host evidence:** Owner-provided `FOX2_HOST_FINAL_LAUNCHER_ATTRIBUTION_V1` 2026-10-20T07:22:08.1889295Z. Current Bridge Desktop/two Python processes and current logon task observed; legacy root `data/bridge.db` exists 294,912 bytes; exact old launcher paths absent; one unrelated disabled FOX2 task remains unresolved. This is not installed legacy retirement proof. Git review `eb760d67bc6c98b444d56090646f34fbdb47c3fb`. Current Registry `a4730bfa52b401b17716ecdc08bd11397a1c9713` BUILD/BLOCKED.
- Human operating scoped Policy v2.0.0 CODE-FIRST vs machine installed Bridge Policy 1.8.9 / frozen RC1 `f3d6468fedb553ba6c6192ba5811cb1b26a11ab9`: distinct; avoid fake effective upgrade. Further binding must resolve Git Registry/Dictionary/TechSpec/release chain explicitly, not assume main authority.

## Exact future code/test allowlist (10 paths, K1 required)

`agent_bridge/src/fox2_agent_bridge/dispatch_normalizer.py`; `agent_bridge/src/fox2_agent_bridge/e2e_runner.py`; `agent_bridge/src/fox2_agent_bridge/app.py`; `agent_bridge/src/fox2_agent_bridge/__main__.py`; `agent_bridge/tests/test_project_dictionary.py`; `agent_bridge/tests/test_e2e_runner.py`; `agent_bridge/src/fox2_agent_bridge/desktop.py`; `agent_bridge/tests/test_desktop.py`; `agent_bridge/src/fox2_agent_bridge/ledger.py`; `agent_bridge/tests/test_runtime_ledger.py`.

Every material hunk requires `REQUESTED/NECESSARY_DEPENDENCY/JUSTIFIED_GENERATED` consumer impact; no edits to `process_lock.py`, `config.py`, `ops_runner.py`, installer/startup, existing PreExec, Governance, Dictionary, Agent adapter or unexpected files without new exact K1. Preserve existing tests and receipts. If guarded direct claim semantics require additional path, STOP for CHAT review, don't bypass.

Only four result paths in new isolated code branch: `reports/FOX2-BRIDGE-MANUAL-LOCAL-ADMISSION-DEV-20261019/{report.md,evidence_manifest.json,test_summary.json,diff_trace.json}`. A new host PreExec receipt, if published, uses separate `reports/FOX2-BRIDGE-MANUAL-LOCAL-ADMISSION-DEV-20261019/preexec/` identity and cannot inherit old Attempt03 result/receipt. Full schema and no-secrets must be checked.

## F0 acceptance gates

**Test-fixture source binding:** The six preserved tests are in `agent_bridge/tests/test_e2e_runner.py` lines 404–488 of source `5a82d08694f217415890f24802261aed625aa111`. They patch `fox2_agent_bridge.desktop.LEGACY_ROOT` and `BRIDGE_ROOT` to disposable fixture paths; initialize a `current` SQLiteLedger via `initialize_runtime`, and then call `current.claim_dispatch` **directly**. Thus a guard that activates ONLY when a hard-coded real `%LOCALAPPDATA%` path is used, or only on the normal `run_once`/Worker path, would be a false implementation and keep these tests failing. The runtime-context/legacy-authority binding must be carried from configuration/init to shared claim-time and work with explicitly bound fixture roots, without globally denying unrelated single-root fixture ledgers. The hard race test starts current under its own bridge.lock, acquires legacy bridge.lock later to permit an old claim, and then demands current reject. It remains insufficient to claim the unmodified old writer honors the new guard. Preserve these exact test semantics.

- Required negative behavior: current-root claim denied when legacy retirement/atomic shared identity is unknown, legacy DB exists or unaccounted marker/consumption, or prior/split-root claim is missing from current snapshot. In synthetic fixtures, including current-exit then legacy restart, **no two successful claims** for same ID.
- Claim-time durable protection, not just migration-time `ProcessLock`; persist explicit UNKNOWN/BLOCKED state across current restart; no dummy in-memory flag, global toggle or hard-coded test exception. Preserve pause/stop/one-writer and same-DB BEGIN IMMEDIATE. Direct ledger claims must respect the configured gate; isolated unrelated single-root ledger tests should not accidentally inherit an installed-host lock.
- Never claim that a current-only fence is obeyed by frozen legacy binary. If old executable can still claim prior current identities, F1 must remain HOLD and report limitation. F0 may DENY ALL current new claims until valid retirement proof.
- Six original failing tests preserved **byte-for-byte or semantically unchanged**; new tests cover absent/corrupt marker, split DB, restart, concurrency, crash and no silent Agent spawn; verify negative denial and no weakened assertion.
- Fresh focused `test_e2e_runner.py`, `test_project_dictionary.py`, `test_desktop.py`, `test_runtime_ledger.py`, `test_ops_runner.py`, `test_preexec.py` where applicable, actual exit codes and pass/fail/NOT_RUN. Explicitly account for Windows long-path diagnostic in Attempt03 (isolated PreExec 65 PASS with process-local Git `core.longpaths=true`); do NOT set global Git config as workaround.
- No installed Bridge/Worker/Canary run, protected Dispatch, provider, broker, paid Agent test or positive installed MANUAL_LOCAL. Result contract v2 + changed-path allowlist + Git remote readback + independent CHAT Result Review; Agent cannot self-ACCEPT.

## Executable handoff remains HOLD

This candidate task is not the coding executable prompt or Final Admission. A **NEW** one-shot identity/attempt under the original Whole-WP is required only after real source-head/worktree and permission selection. CHAT must use `fox2-agent-prompt-builder` to publish a separately immutable task and exact prompt, then a distinct final CHAT admission after **fresh route-specific host PreExec**, one-writer check, actual CLI model/effort and quota inspection as exposed, and result-branch slot verification. When Owner must run Windows CLI manually, the **complete tested/copy-ready PowerShell launcher must be visible inline in CHAT**; not just a link. Missing any material gate => `HOLD` (no CODEX start, no fake PASS). Do not reuse old host-audit marker or coding Attempt03.

**NEXT_SAFE_ACTION:** use this source/task candidate to conduct F0-specific fresh PreExec, publish exact Prompt Builder execution bundle if and only if host admission becomes sound, and finish remaining permitted F0 implementation. Keep F1/Canary release gates separate and HOLD.
