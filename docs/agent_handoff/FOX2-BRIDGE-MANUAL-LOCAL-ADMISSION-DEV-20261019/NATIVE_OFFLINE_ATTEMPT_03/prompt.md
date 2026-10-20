# FOX2 — CODEX Native Offline Manual Local Admission: Attempt 03

**Agent Role:** CODEX coding/integration Agent · **Engine:** CODEX CLI · **Model:** `gpt-6.1-sol` PINNED · **Thinking:** `medium` · **Permission profile:** `FULL_ACCESS` with `danger-full-access` and approval `never`, restricted to the EXACT changed-path allowlist below · **Scope:** FOX2 only, existing Whole-WP `FOX2-BRIDGE-RC1-TO-INTERNAL-READY`, same infrastructure WP `FOX2-BRIDGE-MANUAL-LOCAL-ADMISSION-DEV-20261019` · **Execution:** one bounded native offline coding invocation; no delegation/retries/installed Bridge runtime · **Delivery:** Agent pushes actual non-main Git Result and returns remote result SHA OUTSIDE the committed files; CHAT separately accepts or holds.

## 1. Source, permission, task and binding

READ in full the **published scoped task**:
- `docs/agent_handoff/FOX2-BRIDGE-MANUAL-LOCAL-ADMISSION-DEV-20261019/NATIVE_OFFLINE_ATTEMPT_03/task.md`, immutable commit `04c9141f9a9bc47504473aa577b24201734d8c0b`, Git blob `f339288fb1ec12ca526bc4aabea74fb9ac51b410`, SHA-256 `0387dbaa3375ab763998b7ac24deb722a0c0fe71c585ac7711783b2b337df012`.
- CHAT's engineering-design candidate `bd5cd44e31ceb7384b558c8fb08ccefd98dfb9e6:docs/roadmap/FOX2_BRIDGE_CROSS_ROOT_NO_REPLAY_DESIGN_CONTRACT_CANDIDATE_20261020.md`, Git blob `6e6d56df130b7153539a2bf1dba9f86d2fe591e4`. A design candidate, not installed runtime permission.
- Scoped Owner engineering grant `c23d28bd56d9d06d64561dcf255b2d94227f6acc:docs/governance/releases/FOX2_MANUAL_LOCAL_ADMISSION_OWNER_EXECUTION_AUTHORIZATION_20261019.json`. Four exact conditional shared-layer paths are already K1-bound in the above design; other files remain forbidden for editing.
- Human operating Policy v2.0.0 CODE-FIRST scoped in projectwide Registry `d34da1e3b4918a902646621b487ca8ad3e05b0e0`; Dictionary v1.3 `b25f7f728de67cf8595bf24f22fcbd79ef50babc`, Routing v1.4.0 `bcd008983b61349646a5198ff243069f81484fae`, Git-first Protocol v12 `f2a8bc8e6ce0785a800d78a3c384f205fdc5a6fa`; Result Schema v2 `docs/agent_handoff/FOX2_AGENT_RESULT_SCHEMA_v2.json`. Scoped human permission is NOT installed machine runtime enforcement. Frozen Bridge RC1 source `f3d6468fedb553ba6c6192ba5811cb1b26a11ab9` cannot be silently replayed.
- **CODE branch:** `work/FOX2-BRIDGE-MANUAL-LOCAL-ADMISSION-DEV-20261019-NATIVE-ATTEMPT-03`; **expected local and remote start HEAD:** `3167d8502588dd106f9a4cea8ef931e9148040ff`; worktree `C:\Projects\FOX2-worktrees\FOX2-BRIDGE-MANUAL-LOCAL-ADMISSION-DEV-20261019-NATIVE-ATTEMPT-03`. Its immutable parent `5a82d08694f217415890f24802261aed625aa111` is the test-only new-attempt source, containing the original six failing no-replay cases in `agent_bridge/tests/test_e2e_runner.py`, blob `7b2a2c48e6bf4225d849dc7a7a32126652b0c3be`.
- **PreExec:** `3167d8502588dd106f9a4cea8ef931e9148040ff:reports/FOX2-BRIDGE-MANUAL-LOCAL-ADMISSION-DEV-20261019/preexec/native_offline_attempt03_preflight.json`, Git blob `3a00c1f5905cb6ef340673f5791b0d1cbc1527a6`, status PASS, all eight material capabilities PASS, 0 blockers, pinned CODEX gpt-6.1-sol medium FULL_ACCESS; source_head `5a82d08694f217415890f24802261aed625aa111`. A historical bounded route observation, NOT a current Windows process, no model/effort telemetry claim.
- **CHAT Final Admission:** a separate immutable `chat_final_admission.json` SHALL be published AFTER this prompt, referencing its exact Git commit/blob/raw SHA-256 and PreExec receipt. Host wrapper must validate the admission hash + authority + fresh local/remote/writer checks, then pass the entire admission to you. A published task or prompt alone DOES NOT grant execution. A missing/inconsistent admission = STOP.

## 2. Host-gate evidence and STOP semantics

The owner-host PowerShell 7 launcher must (1) authenticate supported CODEX CLI and pin requested model/effort/sandbox/no-fallback arguments, (2) verify immutable task/prompt/admission objects and remote head, (3) verify exact receipt and unmodified test-only source, (4) check fresh no-competing-writer process snapshot AND retain named exclusive cooperating Windows mutex across full CODEX invocation, (5) confirm Attempt01/02 durable markers preserved and Attempt03 one-shot marker absent, then atomically CreateNew an Attempt03 durable marker before start. Marker creation or uncertain launch consumes Attempt03: DO NOT REPLAY or self-invoke another CODEX. Host-observed CLI invocation/PreExec+CHAT admission is valid bounded launch evidence; do not manufacture `observed_model`, `observed_effort`, `quota` telemetry if CLI does not expose it. An explicit mismatch, fallback, failure, drift, conflict or quota exhaustion => STOP.

Do not waste another coding attempt demanding nonexistent additional host telemetry when the verified wrapper has provided its signed-off admission bundle and no contradictory runtime evidence. Conversely, do not assume wrapper claims waive missing admission or failed material checks. Never act on installed Worker, old Canary/COMPAT001, provider, broker or LIVE.

## 3. Engineering objective — sound no-replay before Manual admission

Use the SHARED Bridge runtime pipeline (strict validation, durable claim/checkpoint/adapter/result) for an explicitly selected `MANUAL_LOCAL` path. Avoid duplicating poller/ledger/agent driver or creating an alternate marker bypass. Preserve BRIDGE-only auto selection; `run-next` MUST reject MANUAL_LOCAL. Guard all ordinary claim consumers, including direct `SQLiteLedger.claim_dispatch` with a sound durable fence; never bypass existing `honor_controls=True` / PAUSED / stop_requested.

The six existing Attempt02 negative tests intentionally failed and were carried forward unchanged. They demonstrate: current DB already exists but legacy consumed identity appears later (FAILED/PUSHED_UNREVIEWED/NEEDS_RECONCILIATION); valid or malformed legacy manual consumption marker; and late legacy claim after a one-time snapshot. **Make the tests PASS through real safety enforcement, NOT by weakening tests, skipping, XFAIL, or suppressing errors.**

The hard case: a legacy supervisor may restart after current exits. A temporary migration lock or current-lifetime double lock cannot prove no-replay against that. Require a durable, independently verifiable legacy retirement/fencing or an actual jointly understood single identity authority; otherwise fail closed at claim and report BLOCKED for positive admission. If making a claim-safe minimal fixture-level solution requires an unapproved path or an unproven "fencing" assertion, STOP with K1 dependency and truthful BLOCKED result. Do not create a dummy green test path which leaves real launch safety ambiguous.

Required synthetic fixture coverage: 6 preserved cross-root assertions; current/legacy split state and marker corruption; simultaneous and sequential claims across roots; legacy writer reappearance; current process restart; claim-before-spawn and crash windows; PAUSED/stop; normal BRIDGE auto rejection of MANUAL_LOCAL; source/task/Owner/hash drift; old schema and PreExec v1 regressions as applicable. A positive manual test is only eligible in a *provably fenced fixture* with an explicit safe identity authority. NO real protected Dispatch ID/Canary, installed bridge/SQLite or paid Agent invocation as a test.

## 4. EXACT changed-path allowlist

Only the following 10 engineering paths may be edited, and only if K1 mapping justifies each material hunk:

1. `agent_bridge/src/fox2_agent_bridge/dispatch_normalizer.py`
2. `agent_bridge/src/fox2_agent_bridge/e2e_runner.py`
3. `agent_bridge/src/fox2_agent_bridge/app.py`
4. `agent_bridge/src/fox2_agent_bridge/__main__.py`
5. `agent_bridge/tests/test_project_dictionary.py`
6. `agent_bridge/tests/test_e2e_runner.py`
7. `agent_bridge/src/fox2_agent_bridge/desktop.py` — confirmed Owner-conditional K1 dependency.
8. `agent_bridge/tests/test_desktop.py` — confirmed K1 test.
9. `agent_bridge/src/fox2_agent_bridge/ledger.py` — bound claim-time fence only.
10. `agent_bridge/tests/test_runtime_ledger.py` — bound claim-time test only.

Delivery path allowlist only:
- `reports/FOX2-BRIDGE-MANUAL-LOCAL-ADMISSION-DEV-20261019/report.md`
- `reports/FOX2-BRIDGE-MANUAL-LOCAL-ADMISSION-DEV-20261019/evidence_manifest.json`
- `reports/FOX2-BRIDGE-MANUAL-LOCAL-ADMISSION-DEV-20261019/test_summary.json`
- `reports/FOX2-BRIDGE-MANUAL-LOCAL-ADMISSION-DEV-20261019/diff_trace.json`

No changes to `process_lock.py`, `ops_runner.py`, `config.py`, `project_dictionary.py`, generated schema/Registry/Dictionary, tests outside the listed ten paths, PreExec files, branch configuration, startup/install, protected Dispatch/task/Canary, main or other unrelated code. If a necessary additional file emerges, do NOT mutate it: STOP with exact file, consumer, contract break and suggested K1/approval action. Existing test modules outside allowlist may be run READ-ONLY. Do not change old red test identities or assertion meanings.

## 5. Real tests, K1 and delivery

Run focused `python -m pytest -q -p no:cacheprovider tests/test_e2e_runner.py tests/test_project_dictionary.py` plus `tests/test_desktop.py tests/test_ops_runner.py tests/test_runtime_ledger.py tests/test_preexec.py` from the `agent_bridge` directory with fixture-only conditions. Include targeted concurrency/restart/legacy-marker tests with real exit codes. State actual PASS/FAIL/NOT_RUN, never inherit 162 previous PASS as current proof. Preserve honest red tests when blocked, including actual failing IDs. Verify old PreExec v1 compatibility and startup pause controls.

For each code/test change, write K1 `REQUESTED`/`NECESSARY_DEPENDENCY`/`JUSTIFIED_GENERATED`, exact consumer, risk and tests in `diff_trace.json`. Check changed/untracked paths, `git diff --check`, no secrets, result-schema validation, report evidence hashes, CODE branch remote HEAD expected parent before push; fast-forward only, never force. Write real Result Schema v2 `reports/FOX2-BRIDGE-MANUAL-LOCAL-ADMISSION-DEV-20261019/report.md` + `evidence_manifest.json` and companion `test_summary.json`, `diff_trace.json`, including BLOCKED result if safety cannot be proven. Do not self-claim acceptance.

Commit and push on exact non-main CODE branch. Provide `OBSERVED_REMOTE_RESULT_SHA` **outside** committed result files; remote-readback all changed files and report paths. If push impossible, export actual files to Owner/CHAT; mark `DELIVERY_BLOCKED`, no invented SHA and no silent replay.

## 6. Hard STOP and acceptance authority

STOP on: absent CHAT admission, any immutable source mismatch, live writer conflict, consumed Attempt03 marker, unsupported model/sandbox, quota error, unapproved path dependency, unclear legacy lifecycle, inability to preserve no-replay, failed material safety test, changed remote head or unsafe write. Partial evidence and red tests are better than an unproved green release.

Preserve Attempt01/02 receipts, consumed markers, report commits and tested failures exactly. Installed Bridge Worker PAUSED, Canary009 HOLD, COMPAT001 PUBLISHED_HOLD, original Bridge bootstrap BLOCKED, no main/merge/deploy/installed adoption/provider/broker/LIVE. Only CHAT may issue ACCEPT/REWORK/HOLD after independent Git Result Review, with fresh host evidence for any next task.
