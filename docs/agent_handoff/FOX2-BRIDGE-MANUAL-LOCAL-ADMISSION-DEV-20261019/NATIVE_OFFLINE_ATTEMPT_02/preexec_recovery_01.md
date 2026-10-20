# FOX2 — Native Offline Attempt 02 PreExec Recovery 01 (non-executable)

**Date:** 2026-10-20. **Owner:** CHAT. **Status:** `PREEXEC_BLOCKED_PRESERVED / SCRIPT_BINDING_BUG_CONFIRMED / RECOVERY_PREFLIGHT_NOT_RUN / CODEX_CODING_NOT_STARTED`.

## Immutable Git evidence
- **Attempt 02 code branch** `work/FOX2-BRIDGE-MANUAL-LOCAL-ADMISSION-DEV-20261019-NATIVE-ATTEMPT-02` receipt publication: `fb4b7818f7e55651c5dcdef1d19ae4164c9f3f84`; parent `23afe56675b9b3698d47c192d4e22b62c82be435`.
- Failed immutable receipt: `reports/FOX2-BRIDGE-MANUAL-LOCAL-ADMISSION-DEV-20261019/preexec/native_offline_attempt02_preflight.json` at `fb4b7818f7e55651c5dcdef1d19ae4164c9f3f84`, blob `4547f5e05b788f98bcb116b89ee0b99303a38d1e`. `status=BLOCKED`, `TASK_ROUTE_BINDING=FAIL` (`TASK_AUTHORITY_BINDING_MISSING`); `CODEX=NOT_RUN` (`UPSTREAM_CAPABILITY_NOT_READY`); `ELIGIBLE_AGENT_ROUTE=FAIL`. Git, Python, pwsh, deps, receipt slot and preflight worktree check PASS. `agent_execution_started=false`. No coding/Agent attempt consumed.
- Original Attempt 02 task: `fb809f77589d517a1133d40fdd0cf3fd90b5b322:docs/agent_handoff/FOX2-BRIDGE-MANUAL-LOCAL-ADMISSION-DEV-20261019/NATIVE_OFFLINE_ATTEMPT_02/task.md`; blob `a07d4c7dced8f38090dec0fb38217a0fd8b8daab`; raw SHA-256 `7111c5f2d4f49f740cc8e118081bf67f289603d508560485e18d71cb684e621e`.
- Historical Attempt 01 consumed: `252d5c78f8ffc1c7b177d028b8e0d3ffa9fb021e` on original infrastructure branch, four report files preserved; no source rebind/replay.
- Native original route PreExec PASS is separate historical snapshot; Bridge bootstrap receipt remains BLOCKED; COMPAT001 and Canary009 HOLD.

## Reproduced exact root cause

The one-time operator PowerShell script's `binding_check` incorrectly demanded all literal substrings `c23d28bd56d9d06d64561dcf255b2d94227f6acc`, `NATIVE-OFFLINE-ATTEMPT-02`, and `ATTEMPT_02` in the **content** of the authorized task. Actual published task includes Owner SHA and `NATIVE-OFFLINE-ATTEMPT-02`, but **does not contain** `ATTEMPT_02` (underscored spelling). Thus the homebuilt consistency check returned a false `TASK_AUTHORITY_BINDING_MISSING`; the genuine bounded CODEX model marker was intentionally skipped. This is not evidence of failed CODEX auth/quota/model, installed Bridge or source conflict.

## Authorized next gate — NEW independent assessment, not replay

- Preserve failed immutable receipt and code branch exactly, including source commit `fb4b7818f7e55651c5dcdef1d19ae4164c9f3f84` (until new receipt). Re-run only a **corrected fresh PreExec** on the **same isolated Attempt 02 worktree** with an **unused new receipt path** `reports/FOX2-BRIDGE-MANUAL-LOCAL-ADMISSION-DEV-20261019/preexec/native_offline_attempt02_preflight_recovery01.json`. This is a new preflight evidence observation after a prior non-Agent BLOCKED check, *not* a CODEX implementation attempt or blind retry of a consumed Dispatch.
- Bind the exact immutable task **by commit+path/blob SHA-1+SHA-256**, Owner SHA and exact attempt ID; do **not** demand arbitrary display-text spelling. The PreExec engine's `task_source` is the unchanged original whole-WP task on the isolated coding branch. The new scoped Attempt 02 task is separately verified in material custom `task_route_binding` capability from the immutable handoff commit. Explicitly retain these **two different** source roles in CHAT's receipt intake; a new task must not silently overwrite original.
- Source HEAD for new PreExec is current `fb4b7818f7e55651c5dcdef1d19ae4164c9f3f84` and branch `work/FOX2-BRIDGE-MANUAL-LOCAL-ADMISSION-DEV-20261019-NATIVE-ATTEMPT-02`; check clean worktree, exact remote HEAD, this immutable failed receipt blob, scoped Owner grant, active one-writer, Python/git/pwsh/deps, and unused recovery receipt slot. CODEX `gpt-6.1-sol / medium / FULL_ACCESS` marker may run only after real material static checks PASS, recording observed outcome. No ignored failed check, no synthetic PASS, no overwrite/cleanup, no Agent coding launch.
- After new receipt publication, CHAT must independently remote-readback **exact** commit/blob and all material capability statuses. Any BLOCKED/UNKNOWN remains HOLD. Prompt Builder's new immutable `prompt.md` and a separate CHAT final admission are **not published yet**; they are mandatory before any Attempt 02 coding Agent starts.
- Never modify historical Attempt 01 claim marker or worktree, old receipts, installed Worker, Canary009, COMPAT001, main, merge, provider/broker or LIVE.

**Next action:** FOXLE-PC only for the explicit new-route preflight; CHAT keeps receipt acceptance, prompt publication, assignment and result review. No claim of work occurring in the background.
