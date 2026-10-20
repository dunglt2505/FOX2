# FOX2 — CODEX Native Offline Manual Local Admission: Attempt 02

**Role:** CODEX coding Agent · **Engine/Model:** OpenAI CODEX CLI, PINNED `gpt-6.1-sol` · **Thinking:** `medium` · **Permission:** `FULL_ACCESS` (`danger-full-access`, approval `never`) bounded by exact paths · **Scope:** FOX2 only, Whole-WP `FOX2-BRIDGE-RC1-TO-INTERNAL-READY`, existing implementation WP `FOX2-BRIDGE-MANUAL-LOCAL-ADMISSION-DEV-20261019`, new isolated Attempt 02 · **Delivery:** AGENT Git result; CHAT independently reviews · **RUNS:** one coding invocation maximum; no retry or agent delegation.

## Exact task and host admission

1. The authoritative **new route task** is the immutable `docs/agent_handoff/FOX2-BRIDGE-MANUAL-LOCAL-ADMISSION-DEV-20261019/NATIVE_OFFLINE_ATTEMPT_02/task.md` at commit `fb809f77589d517a1133d40fdd0cf3fd90b5b322`, Git blob `a07d4c7dced8f38090dec0fb38217a0fd8b8daab`, SHA-256 `7111c5f2d4f49f740cc8e118081bf67f289603d508560485e18d71cb684e621e`. Read and comply in full; do not reinterpret this as a new Whole-WP.
2. This exact `prompt.md` must be bound by its immutable Git commit/blob/SHA-256 in a **separate CHAT final-admission receipt** issued **after** prompt Git publication. The real host launcher must validate that receipt and provide the verified admission text plus the pinned task/prompt to you. **Do not infer CHAT admission merely from a published prompt**.
3. Native offline PreExec Recovery 01 at code commit `65c50f7831722300a5418d0e9bc21f9f95988147:reports/FOX2-BRIDGE-MANUAL-LOCAL-ADMISSION-DEV-20261019/preexec/native_offline_attempt02_preflight_recovery01.json`, blob `df39ab6e42c03e9a10683141099720fd19b03b32`, is `PASS` with nine material capabilities `PASS`, no blockers; source_head in receipt `fb4b7818f7e55651c5dcdef1d19ae4164c9f3f84`. Earlier Attempt 02 receipt `native_offline_attempt02_preflight.json` stays `BLOCKED` for a proven string-guard bug; it is not edited, promoted or replayed. The original Bridge bootstrap receipt stays `BLOCKED`.
4. **Code branch:** `work/FOX2-BRIDGE-MANUAL-LOCAL-ADMISSION-DEV-20261019-NATIVE-ATTEMPT-02`; **worktree:** `C:\Projects\FOX2-worktrees\FOX2-BRIDGE-MANUAL-LOCAL-ADMISSION-DEV-20261019-NATIVE-ATTEMPT-02`; **expected code HEAD and remote:** `65c50f7831722300a5418d0e9bc21f9f95988147`. No reset, rebase, force-push, branch-switch or inherited dirty WIP. Original Attempt 01 branch is a separate historical record at `252d5c78f8ffc1c7b177d028b8e0d3ffa9fb021e`, and its host marker must not be touched.
5. Owner authorization for six primary code/test files: `c23d28bd56d9d06d64561dcf255b2d94227f6acc:docs/governance/releases/FOX2_MANUAL_LOCAL_ADMISSION_OWNER_EXECUTION_AUTHORIZATION_20261019.json`. Human governance Registry `d34da1e3b4918a902646621b487ca8ad3e05b0e0` selects scoped Policy 2.0.0/CODE-FIRST, Dictionary v1.3, Routing v1.4.0 and Git-first Protocol v12 for new coordination; frozen installed Bridge RC1 source `f3d6468fedb553ba6c6192ba5811cb1b26a11ab9` stays immutable. This is **not** adoption of installed machine runtime.

## Mandatory pre-code decision, corrected from Attempt 01

The verified host wrapper—not CODEX chat text—is responsible for (a) checking remote/local branch and pristine source, immutable task/prompt/final-admission hashes, (b) confirming fresh process observation and holding a named exclusive Windows mutex through the entire Agent invocation, (c) atomically creating the unique durable Attempt 02 marker immediately before starting the CLI, (d) launching with explicit `--model gpt-6.1-sol`, `-c model_reasoning_effort="medium"`, `--sandbox danger-full-access`, approval never and no fallback. The fresh PreExec marker gives bounded evidence of service availability, not unlimited quota. Exact model/effort telemetry may be `NOT_EXPOSED`; report actual telemetry if provided, but **do not require inaccessible observed_model or observed_effort values as a second redundant launch gate** after host-verified pinned CLI arguments/PreExec and CHAT receipt. Explicit runtime mismatch, invalid model, exhaustion/quota failure, or altered launch configuration => STOP.

On intake, confirm the injected `FINAL_CHAT_ADMISSION` document explicitly matches the actual prompt SHA, task SHA, code branch/source commit and PreExec commit, and is a conditional PASS_TO_ASSIGN under host checks. Fail closed on absent/altered admission, source drift, competing writer, or consumed marker; no self-relaunch or nested Agents. If host evidence is present and internally consistent, proceed with the authorized implementation rather than repeating Attempt 01's self-block.

## Exact allowed diff

**Code and tests, ONLY six paths:**
- `agent_bridge/src/fox2_agent_bridge/dispatch_normalizer.py`
- `agent_bridge/src/fox2_agent_bridge/e2e_runner.py`
- `agent_bridge/src/fox2_agent_bridge/app.py`
- `agent_bridge/src/fox2_agent_bridge/__main__.py`
- `agent_bridge/tests/test_project_dictionary.py`
- `agent_bridge/tests/test_e2e_runner.py`

**Delivery artifacts, ONLY four paths:**
- `reports/FOX2-BRIDGE-MANUAL-LOCAL-ADMISSION-DEV-20261019/report.md`
- `reports/FOX2-BRIDGE-MANUAL-LOCAL-ADMISSION-DEV-20261019/evidence_manifest.json`
- `reports/FOX2-BRIDGE-MANUAL-LOCAL-ADMISSION-DEV-20261019/test_summary.json`
- `reports/FOX2-BRIDGE-MANUAL-LOCAL-ADMISSION-DEV-20261019/diff_trace.json`

Do NOT modify `agent_bridge/src/fox2_agent_bridge/{ledger.py,desktop.py,process_lock.py,ops_runner.py,dispatch_poller.py,project_dictionary.py}`, config, Policy/Dictionary/Registry/schema, generated code, any receipt, task/handoff, `.git`, README or other file. If a necessary shared-layer dependency is proved, **STOP the implementation at that boundary** and deliver the exact evidence/K1 justification, not a speculative workaround or broad permission expansion.

## Engineering objective and gates

Implement an explicit human-operator-selected `MANUAL_LOCAL` path using the existing shared dispatch validation, durable atomic claim, adapter/checkpoint and no-replay pipeline without cloning the Bridge E2E engine. Existing automatic `BRIDGE` dispatches must never accidentally admit MANUAL_LOCAL. Preserve `PAUSED` and `stop_requested` denial of new claims; do NOT toggle PAUSED, bypass `honor_controls`, edit installed SQLite or interact with Worker/scheduler/real protected Dispatch. If shared ledger cannot ensure once-only claim/crash semantics with the six permitted paths, STOP with a genuine dependency report instead of shipping unsafe semantics.

Run focused fixture-only tests for `test_e2e_runner.py` and `test_project_dictionary.py`, then applicable `test_desktop.py` and `test_ops_runner.py` regressions. Test source drift, Owner/permission/schema/model mismatch, explicit manual vs BRIDGE auto, paused/stop, duplicate/current+legacy markers, concurrency, claim-before-spawn crash windows and ambiguous delivery. No live Agent execution test, no actual Dispatch001 or Canary009 claim, no installed Bridge activation. FAIL/UNKNOWN/NOT_RUN remain truthful. Trace every changed diff hunk to `REQUESTED/NECESSARY_DEPENDENCY/JUSTIFIED_GENERATED` with specific consumer and test evidence.

## Result contract, Git delivery and STOP

Write **real** `reports/FOX2-BRIDGE-MANUAL-LOCAL-ADMISSION-DEV-20261019/report.md` and `reports/FOX2-BRIDGE-MANUAL-LOCAL-ADMISSION-DEV-20261019/evidence_manifest.json` conforming to Dictionary-selected `docs/agent_handoff/FOX2_AGENT_RESULT_SCHEMA_v2.json`, plus `test_summary.json` and `diff_trace.json`. A local stopped/partial result remains `BLOCKED`/ `PARTIAL` and test `NOT_RUN` if applicable; never invent PASS. Record source locks, changed-path list, actual test commands and exit codes, model requested vs observed separately, quota as `NOT_EXPOSED` when appropriate. Use Git result commit SHA **outside** committed manifest to avoid self-reference.

Before commit/push: check no unexpected changed/untracked files, only ten exact allowed paths, no secrets, `git diff --check`, remote expected-parent/fast-forward and report integrity. Commit/push only onto the isolated non-main code branch; recheck origin HEAD and exact remote report bytes. Return actual remote result SHA to CHAT. Report-only BLOCKED result is permitted when appropriate, but does not accept BUILD. If Git push fails, export actual files to Owner/CHAT with truthful `DELIVERY_BLOCKED`; never force or retry Agent.

**STOP:** incompatible immutable task/admission, writer/attempt already consumed, unsupported model/effort/permission, branch/source drift, excluded dependency, atomic/no-replay uncertainty, unexpected remote status, secrets, protected Worker/Canary interaction, or inability to validate claimed tests. Never merge/main/install/runtime adopt/Canary/COMPAT001/provider/broker/LIVE. Do not claim completion before CHAT independent Git Result Review.

**HANDOFF STATUS:** executable prompt published only after CHAT Git verification; no self-start from Git. The separate subsequent CHAT admission and verified host wrapper are mandatory.
