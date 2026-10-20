# FOX2 — CODEX executable implementation prompt: native offline attempt 01

**Role:** CODEX — bounded implementation Agent; **Engine / Model:** OpenAI CODEX CLI / PINNED `gpt-6.1-sol`; **Thinking:** Medium; **Scope:** existing `FOX2-BRIDGE-MANUAL-LOCAL-ADMISSION-DEV-20261019` within FOX2 Bridge RC1 Whole-WP; **Execution:** NATIVE_LOCAL_CODEX_CLI_OFFLINE_DEV; **Permission:** requested FULL_ACCESS (`danger-full-access`, approval `never`) with explicit permitted file/path scope. **Delivery owner:** AGENT, via Git non-main. **MAX RUNS:** one for this attempt; no retry or spontaneous replay.

**READ THIS SOURCE-BOUND TASK FIRST (no substitution):**
`docs/agent_handoff/FOX2-BRIDGE-MANUAL-LOCAL-ADMISSION-DEV-20261019/NATIVE_OFFLINE_ATTEMPT_01/task.md`
at exact task publication commit `e772b6d371ac1ecbf5eea65240968300005e3fc5`,
Git blob SHA-1 `83a6a19b2f43886e968eccb970343cdd76889de5`,
raw UTF-8 SHA-256 `c6498a9c256be6e965381973ea73052aed95344d1e60148f8f9d7e926d40bb45`.
The handoff branch is `work/FOX2-BRIDGE-NATIVE-OFFLINE-IMPL-HANDOFF-20261020`; this prompt is bound by CHAT via immutable prompt commit and SHA hashes separately verified before Agent launch. Do not rely on chat text or a moving branch tip instead of the immutable Git source.

**CODE TARGET** (not the handoff docs branch):
`C:\Projects\FOX2-worktrees\FOX2-BRIDGE-MANUAL-LOCAL-ADMISSION-DEV-20261019`
on exact `work/FOX2-BRIDGE-MANUAL-LOCAL-ADMISSION-DEV-20261019`
with source HEAD and origin remote HEAD both exactly `23afe56675b9b3698d47c192d4e22b62c82be435`.
Do not merge/rebase/rewrite/force push or fetch then checkout another branch if mismatched. Stop and report mismatch.

**Governance and no-replay gates:** Owner exact code-rights grant `c23d28bd56d9d06d64561dcf255b2d94227f6acc`; source-bound original task `482d26d71c5c95f028f9b4110349e4d318bcb342`; projectwide human governance Registry `d34da1e3b4918a902646621b487ca8ad3e05b0e0` (scoped Policy v2.0.0, Routing v1.4.0, Protocol v12, not installed adoption). Task PreExec native offline receipt `23afe56675b9b3698d47c192d4e22b62c82be435:reports/FOX2-BRIDGE-MANUAL-LOCAL-ADMISSION-DEV-20261019/preexec/native_offline_preflight_20261020.json` status PASS, eight material capabilities PASS, no blockers, exact CODEX model/effort and FULL_ACCESS candidate. This is not a Bridge operational bootstrap. The separate original Bridge bootstrap receipt at `reports/FOX2-BRIDGE-MANUAL-LOCAL-ADMISSION-DEV-20261019/preexec/preflight_receipt.json` remains BLOCKED. No real Canary009 or COMPAT001 execution; no restart/resume/stop Worker. Do not reuse or modify any old published Dispatch.

## Mandatory pre-action checks

1. Confirm target repo `dunglt2505/FOX2`, branch, clean worktree, exact local and remote SHA above. Confirm no competing writer/active overlapping attempt or existing `reports/FOX2-BRIDGE-MANUAL-LOCAL-ADMISSION-DEV-20261019/report.md` for this attempt. No duplicate output from a preceding unknown run; if any doubt, STOP for CHAT reconciliation.
2. Read original `task.md` and the newer non-retroactive `NATIVE_OFFLINE_ROUTE_ADDENDUM_CANDIDATE_20261020.md`, source-impact and Owner grant. Current code files at start must match frozen Bridge baseline `f3d6468fedb553ba6c6192ba5811cb1b26a11ab9`.
3. **No implementation before any material source/authority/model/permission/writer gate fails closed.** Do not call CODEX agents recursively, use a different model, downgrade sandbox or expand rights. Quota/capacity may not be exposed; if runtime error occurs, classify accurately and stop, not a "PASS" fabricated from requests.
4. Never connect installed FOX2 worker/bridge.lock/SQLite, no network service to host, no provider/broker, no production orders. Synthetic fixture/disposable test remote only.

## Work: implement bounded, safe MANUAL_LOCAL code

Develop an *explicit operator-selected* `MANUAL_LOCAL` route reusing current transport, common strict dispatch validation, immutable prompt/branch checks, claim/checkpoint, existing Agent adapters and Git result semantics. Avoid cloned E2E stack, global mode relaxations and normal BRIDGE automatic selection. Keep BRIDGE auto-execute normalizer rejecting MANUAL_LOCAL. In a negative or stopped state `PAUSED`/ `stop_requested=true`, deny new claim/spawn. Do not bypass `honor_controls` or introduce a one-off "resume while paused" workaround. Only choose a design whose lease, permission, no-replay and durable claim are verifiable with current six-file scope; otherwise STOP at that blocker rather than edit shared unapproved modules. Never make real installed MANUAL_LOCAL/CANARY run from this offline test.

**Only change these six exact paths** (anything else is disallowed even if tests would be improved):
- `agent_bridge/src/fox2_agent_bridge/dispatch_normalizer.py`
- `agent_bridge/src/fox2_agent_bridge/e2e_runner.py`
- `agent_bridge/src/fox2_agent_bridge/app.py`
- `agent_bridge/src/fox2_agent_bridge/__main__.py`
- `agent_bridge/tests/test_project_dictionary.py`
- `agent_bridge/tests/test_e2e_runner.py`

Write only these result files:
- `reports/FOX2-BRIDGE-MANUAL-LOCAL-ADMISSION-DEV-20261019/report.md`
- `reports/FOX2-BRIDGE-MANUAL-LOCAL-ADMISSION-DEV-20261019/evidence_manifest.json`
- `reports/FOX2-BRIDGE-MANUAL-LOCAL-ADMISSION-DEV-20261019/test_summary.json`
- `reports/FOX2-BRIDGE-MANUAL-LOCAL-ADMISSION-DEV-20261019/diff_trace.json`

**No editing** `ledger.py`, `desktop.py`, `process_lock.py`, `ops_runner.py`, `dispatch_poller.py`, `project_dictionary.py`, generated Dictionary/schema, shared PreExec, Task/Prompt/old receipts, worktree Git configuration or unrelated files. If any is required, stop and submit a truthful blocked report describing exact dependency + K1 consumer case. Never add an external new dependency or config with unapproved manifest change.

**Acceptance tests (all on synthetic fixtures only):** existing auto BRIDGE selection unchanged + manual explicit opt-in; wrong mode/Owner/Policy/Dictionary/model/effort/prompt SHA/source SHA/branch/worktree; concurrent claim/race; pause/stop reject; consumed/current+legacy marker/status no replay; crash-before-claim, after durable claim, before/after spawn, after uncertain Git delivery; no extra Agent spawn, no false PASS; preserve v1 PreExec schema and legacy v0.6 Canary v3 compatibility. Run `pytest agent_bridge/tests/test_e2e_runner.py agent_bridge/tests/test_project_dictionary.py`, and relevant read-only regressions `agent_bridge/tests/test_desktop.py` and `agent_bridge/tests/test_ops_runner.py` when setup allows. Do not run any real Agent integration tests or installer. Test failures are FAIL/UNKNOWN, not passed-by-history.

**K1 impact trace:** for every material diff hunk record `REQUESTED`, `NECESSARY_DEPENDENCY` or `JUSTIFIED_GENERATED`, and exact requirement/consumer/test evidence. No drive-by refactor.

## Delivery and STOP

Deliver full `reports/FOX2-BRIDGE-MANUAL-LOCAL-ADMISSION-DEV-20261019/report.md`, `evidence_manifest.json` plus `test_summary.json`, `diff_trace.json` under source/result contract; include real commands/test exit status, summary of diff paths, fixed commit/blob provenance, unknown/fail/blocked counts, model/effort metadata only if observable (do not pretend observed just because requested). No raw credentials/log secrets. Preserve actual results/attempt history if blocked or interrupted.

Before commit/push, validate **only** ten exact changed-path allowlist entries (six code/test + four reports), `git diff --check`, tests/secret scan, and current remote expected HEAD, rejecting unrelated WIP. Commit/push only onto original non-main CODE_BRANCH, read back remote exact HEAD and actual result report/manifest. Return observed remote result SHA *outside* the committed report file to CHAT. Branch update or "DONE" alone is not CHAT ACCEPT. If publish blocked, report `DELIVERY_BLOCKED` with exact artifacts; do not force push or retry execution.

**STOP** for ambiguity in task/authority/one-writer, model capability/permission, source drift, previously started attempt, any required code beyond six paths, failure to prove atomic claim or pause semantics, real runtime interactions, diff secret, or false result publication. No code execution of protected COMPAT001/Canary009, no main/merge/deploy/installed runtime/Provider/Broker/LIVE. If early STOP before changes, produce honest blocking report only as permissions allow.

The only coding authorization is the pinned source-and-handoff route above **subject to CHAT final admission/readback**; never treat this artifact's mere publication as an independent authorization or instruction to self-start.
