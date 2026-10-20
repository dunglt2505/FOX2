# FOX2 — Native Offline Manual Local Admission implementation, Attempt 02

**Status:** SOURCE-LOCKED EXECUTION TASK CANDIDATE; **NOT YET ASSIGNED**, no coding prompt issued or Agent launch authorized until fresh Attempt 02 PreExec and a subsequent CHAT final-admission receipt.
**Whole-WP:** `FOX2-BRIDGE-RC1-TO-INTERNAL-READY`; reuse existing infrastructure WP `FOX2-BRIDGE-MANUAL-LOCAL-ADMISSION-DEV-20261019`, not a new micro-WP.
**Attempt ID:** `FOX2-BRIDGE-MANUAL-LOCAL-ADMISSION-DEV-20261019-NATIVE-OFFLINE-ATTEMPT-02`. Attempt 01 is **CONSUMED**, result `CHAT_ACCEPT_REPORT_ONLY / CHAT_HOLD_IMPLEMENTATION`; no replay or marker deletion.
**Agent route:** `CODEX / CLI gpt-6.1-sol PINNED / Thinking medium / FULL_ACCESS` limited by exact path allowlist; single coding invocation, Agent Git Result delivery, CHAT Result Review acceptance. Never use installed FOX2 Bridge to admit this offline development task.

## 1. Authority, existing immutable records and source lock

- Owner scoped grant `c23d28bd56d9d06d64561dcf255b2d94227f6acc:docs/governance/releases/FOX2_MANUAL_LOCAL_ADMISSION_OWNER_EXECUTION_AUTHORIZATION_20261019.json` authorizes 6 primary code/test files and conditionally justified shared dependencies subject to separate exact CHAT scope binding. This task grants **only the six primary files**.
- New/re-scoped human operating Governance Registry at `d34da1e3b4918a902646621b487ca8ad3e05b0e0:docs/governance/FOX2_PROJECTWIDE_GOVERNANCE_REGISTRY.json`; scoped Policy 2.0.0 at `96175ac4f39197794a04e695f0046fa7ef9321fe`, Dictionary 1.3 at `b25f7f728de67cf8595bf24f22fcbd79ef50babc`, Routing 1.4.0 at `bcd008983b61349646a5198ff243069f81484fae`, Git-first Protocol 12 at `f2a8bc8e6ce0785a800d78a3c384f205fdc5a6fa`. Scoped governance release does not imply Windows runtime/machine adoption.
- Historical original infrastructure `task.md` from `482d26d71c5c95f028f9b4110349e4d318bcb342`, Bridge RC1 code `f3d6468fedb553ba6c6192ba5811cb1b26a11ab9`, native offline route addendum at `9106e8d4465db5f313911394579da9d39f296f73`.
- Original Bridge bootstrap preflight stays `BLOCKED` at `CHECK_BRIDGE_BOOTSTRAP_CONTROLS` and has no operational permission; separate native offline WP PreExec is `PASS` on its prior route/worktree snapshot (receipt `23afe56675b9b3698d47c192d4e22b62c82be435`), but **Attempt 02 requires a fresh host/worktree task-scoped PreExec** before issuance.
- Attempt 01 CODEX authored four truthful local reports, later published verbatim by CHAT at `252d5c78f8ffc1c7b177d028b8e0d3ffa9fb021e` on the original infrastructure branch. Immutable CHAT review on roadmap branch `5e4410838a621849d126388352195bad6b3ef03d:docs/roadmap/FOX2_BRIDGE_MANUAL_LOCAL_ATTEMPT01_CHAT_RESULT_REVIEW_20261020.md`. Never rewrite this history, never delete Attempt01 host marker.
- **Critical branch isolation:** New CODE branch `work/FOX2-BRIDGE-MANUAL-LOCAL-ADMISSION-DEV-20261019-NATIVE-ATTEMPT-02` created from exact `23afe56675b9b3698d47c192d4e22b62c82be435`. This immutable commit precedes the CHAT-owned report-only Attempt 01 commit. Fresh separate Windows worktree `C:\Projects\FOX2-worktrees\FOX2-BRIDGE-MANUAL-LOCAL-ADMISSION-DEV-20261019-NATIVE-ATTEMPT-02`. The earlier CODE branch/worktree, files, attempt marker, and historical reports are untouched. New branch is a route/attempt branch of the **same** WP, not a duplicate WP.
- **Handoff branch:** `work/FOX2-BRIDGE-NATIVE-OFFLINE-ATTEMPT02-HANDOFF-20261020`, distinct from result branch. This `task.md` shall be hashed and pinned to its actual publication commit in the next Prompt Builder step. Final `prompt.md` and CHAT final-admission receipt must be separately Git-published and immutable-read back before running coding Agent. At this stage they are **not issued**.

## 2. Path-bound implementation scope

Code/test exact allowlist:
1. `agent_bridge/src/fox2_agent_bridge/dispatch_normalizer.py`
2. `agent_bridge/src/fox2_agent_bridge/e2e_runner.py`
3. `agent_bridge/src/fox2_agent_bridge/app.py`
4. `agent_bridge/src/fox2_agent_bridge/__main__.py`
5. `agent_bridge/tests/test_project_dictionary.py`
6. `agent_bridge/tests/test_e2e_runner.py`

Result-only exact allowlist on this **new branch**:
- `reports/FOX2-BRIDGE-MANUAL-LOCAL-ADMISSION-DEV-20261019/report.md`
- `reports/FOX2-BRIDGE-MANUAL-LOCAL-ADMISSION-DEV-20261019/evidence_manifest.json`
- `reports/FOX2-BRIDGE-MANUAL-LOCAL-ADMISSION-DEV-20261019/test_summary.json`
- `reports/FOX2-BRIDGE-MANUAL-LOCAL-ADMISSION-DEV-20261019/diff_trace.json`

Results must conform to Dictionary-resolved `docs/agent_handoff/FOX2_AGENT_RESULT_SCHEMA_v2.json`; the schema's `git.report_path` requires `reports/FOX2-BRIDGE-MANUAL-LOCAL-ADMISSION-DEV-20261019/report.md`, which is why the new isolated attempt/result branch is necessary. The result commit SHA must be supplied *outside* the committed files.

`ledger.py`, `desktop.py`, `process_lock.py`, `ops_runner.py`, `dispatch_poller.py`, `project_dictionary.py`, generated Registry/Dictionary, schema, original dispatches/PreExec receipt, Worker controls, and any additional path are excluded. If a required atomic claim or no-replay fix provably depends on an excluded file, STOP; describe exact dependency + K1 reason and tests for CHAT, do not edit it without new approved binding. No code/test wildcard.

## 3. Implementation objective and negative acceptance

Build one explicit operator-selected **MANUAL_LOCAL admission** reusing existing shared strict validation, locked-source identity, claim/checkpoint/adapter pipeline where compatible, without cloning the full Bridge engine. Preserve automatic BRIDGE-only dispatch selection and rejection of MANUAL_LOCAL in normal `run-next`, and preserve `PAUSED` / `stop_requested` protection (never bypass `honor_controls`, manipulate SQLite or auto-resume). Do not operate on the installed Windows Bridge at any stage of this offline assignment.

Negative/positive synthetic tests on disposable fixtures: permission/Owner/Task/Policy/schema/route/prompt hash/source drift; allowed explicit MANUAL_LOCAL only; paused/stop deny; fresh vs failed/consumed/unknown across current/legacy ledger and marker; concurrency/race; durable claim before Agent spawn; crash before/after claim and after Agent execution; delivery ambiguity/no replay; old PreExec contract and legacy Canary v0.6/schema v3 regression. Report true PASS/FAIL/NOT_RUN; no historical pass substitution. Run focused `pytest` for the two changed test modules and relevant existing `test_desktop.py`, `test_ops_runner.py` regression **without installed Bridge or real protected Dispatch IDs**.

K1: every material diff hunk maps to `REQUESTED / NECESSARY_DEPENDENCY / JUSTIFIED_GENERATED`, exact file, consumer and test; no drive-by refactor. No new dependencies requiring changes outside allowlist.

## 4. Corrected admission evidence contract — resolves Attempt 01 self-block

1. **CHAT final admission** is an independently Git-published exact file (separate after prompt publication) binding task, prompt commit/blobs/SHA-256, selected PreExec receipt, result branch/source SHA and R0–R7 verdict. The host operator script verifies its immutable Git bytes/hash and includes its exact identity in the Agent's initial context. Never require Agent to infer permission from the mere presence of task or prompt files.
2. **Current model/thinking:** host launches supported `codex-cli` using explicit `--model gpt-6.1-sol` and `-c model_reasoning_effort="medium"` with `--sandbox danger-full-access` and approval `never`; a same-route fresh PreExec bounded marker must PASS. An unreported `observed_model` or `observed_effort` is **UNKNOWN telemetry**, NOT contradictory evidence and not by itself an automatic STOP for isolated offline build *when* route authority and PreExec probe and literal CLI invocation are verified. An explicit mismatch/error/fallback IS STOP. Never falsely report requested config as observed. Capacity/remaining quota may remain `NOT_EXPOSED`; a quota error is STOP, do not retry automatically.
3. **One-writer:** the host operator must verify exact fresh clean worktree, remote SHA, no competing/unknown CODEX writer for the same worktree, absence of previous Attempt 02 marker, and hold a named exclusive Windows admission mutex during the Agent invocation. These are **host-witnessed prelaunch and continuous cooperating-launcher exclusion**; they are not evidence that all unrelated/hostile writers globally obey the mutex. Agent should rely on the exact sanitized evidence furnished by the verified launcher and still STOP on observable conflicts/source drift, not demand inaccessible OS telemetry from within the Agent.
4. **No-replay:** use separate durable Attempt 02 marker with atomic `CreateNew` before launch, preserved on any unknown/failure. Attempt 01 marker and original worktree never touched. Max one coding invocation; after uncertain Agent start or failed delivery, CHAT reconciles, no blind retry.

## 5. Host/assignment STOP and results

**Before execution:** (a) new target branch/worktree is created and verified against base source; (b) genuine task/route-specific shared PreExec receipt **PASS** on that worktree and remote-readback by CHAT; (c) exact immutable prompt published/readback under Prompt Builder; (d) a separate final CHAT assignment/admission file published/readback; (e) host one-writer and no-replay marker checks fresh; (f) correct CODEX CLI/sandbox, model, effort and rights; (g) no original protected Worker/Canary/COMPAT001 touched. Any absent gate: HOLD without creating/consuming Attempt 02 marker or starting Agent.

**Execution results:** CODEX produces Git Result v2 manifest, real logs/tests, K1 diff trace, exact non-main result remote SHA as separate message; CHAT independently verifies commit/paths/hashes and returns `ACCEPT / REWORK / HOLD`. If unable to push, supply actual file bytes to CHAT, no fabricated result SHA. No main, merge, install, provider/broker, Canary, LIVE, or feature release from this task.

**NEXT_SAFE_ACTION:** publish/read back THIS task candidate; create/verify independent Windows worktree and one-time **PreExec** on new branch. Only after CHAT receipt intake issue immutable Attempt 02 prompt and final admission; no coding starts from this task alone.
