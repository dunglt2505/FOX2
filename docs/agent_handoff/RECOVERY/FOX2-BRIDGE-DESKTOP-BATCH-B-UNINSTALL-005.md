# FOX2 Bridge Batch B — Uninstall Recovery Intake 005 (NON-EXECUTABLE)

**Status:** PREEXEC_REQUIRED / HOLD_DEV / SOURCE_READY / NOT_A_DISPATCH
**Project:** FOX2 only; same Bridge Batch B WP; no new feature work.
**Source task head:** `6a31409e0f3d46d4f2b2fc2bc48464ecff86e257`
**Control preceding head:** `056fd4f4a2f1d99355d78f7ebf8cdc4b13109c29`
**Policy:** FOX2 Policy V1.8.9 / Dictionary v1.2 / project-wide PreExec v1.1.
**Safety:** Dispatches 001–004 CONSUMED, never replay. No PR/main/merge/deploy/provider/broker/LIVE.

## R0, R1 — verified status, do not redo completed work

CHAT independently read back Dispatch 004 WIP code and evidence at task head `6a31409e`, publication = PUSHED_UNREVIEWED, not accepted. Five focused Tray regressions PASS. Tray graceful exit, stopped Worker, released worker lock, limited per-user startup, 1 Tray/Worker after 2 launches, deterministic package builds, update, setup, diagnostics PASS. 10/24 acceptance PASS; UNINSTALL_PATH FAIL; 8 NOT_CERTIFIED and 5 NOT_RUN_AFTER_MATERIAL_STOP. Previously recovered 17 files remain preserved. Full 354-test suite previously passed before 004, not rerun after 004 material STOP.

Dispatch 004 installed lifecycle called `python -I -m fox2_agent_bridge uninstall` using the currently installed per-version interpreter; returned exit code 2. Captured stderr was discarded by the harness; detailed failing exception unknown. After STOP, read-only evidence found both versions and `current.json` still present, worker STOPPED, task scheduler startup not registered, dispatches 001–004 in NEEDS_RECONCILIATION. Runtime integrity UNKNOWN; do not retry destructive uninstall, relaunch Bridge, cleanup or restart without reconciliation.

## Static code review — high-confidence causal defect; host traceback still unavailable

`agent_bridge/src/fox2_agent_bridge/installation.py::uninstall`:
1. Runs from an interpreter at `%LOCALAPPDATA%/FOX2/AgentBridge/versions/<SHA>/runtime/Scripts/python.exe`.
2. Detects the executable inside `versions` and synchronously launches `sys._base_executable -I -c <uninstall>` using `_run`.
3. Parent installed interpreter **waits synchronously** for child completion.
4. Child attempts `shutil.rmtree(path)` for every owned version, including its *still-running parent's executable on Windows*.
5. Windows executable-file deletion/share rules make this design unsafe; it provides a strong plausible root cause of the exit-2 wrapper error. Exact exception and any additional defects are still UNKNOWN, not claimed confirmed.

Potential separate failure: the base interpreter with `-I` and only the installed package path injected may lack installed wheel dependencies. Prove this with safe read-only subprocess import probes, not a second uninstall attempt.

## Correct fix (narrow, host-safety first)

- Provide an external uninstaller/bootstrap **outside the version tree**. Never synchronously wait in an installed interpreter while trying to remove that interpreter's executable. Use a two-stage exit/acknowledgement protocol: installed owner requests uninstall, releases its own executable; external helper waits for that exact PID to exit before deletion.
- Helper verifies current-user root, exact package hashes and ownership receipts for all version directories, symlink/junction guards, locks and worker STOPPED, no foreign processes using owned runtime; no arbitrary paths. Fail closed preserving all data and versions on uncertain ownership.
- Use deterministic result/receipt in *preserved* `reports`, distinguish `UNINSTALL_REQUESTED` vs `UNINSTALLED_VERIFIED`. Never report success before externally verified removal. Preserve config, SQLite ledger/dispatch claims, logs, reports and FOX2 project worktrees. No startup creation/privilege elevation.
- On uncertain runtime state, add diagnostic read-only code that classifies errors without logging raw subprocess stderr/tokens/paths outside allowed sanitized evidence. Specifically prove launched interpreter identity, current pointer, owned receipts, binary/process ownership and missing dependencies without mutating the install.
- Extend deterministic regression tests: Windows parent/child executable lock race, exact PID ack, timeout, interrupted helper, locked version, unowned dir, junction/symlink, partial failure preservation, no secrets, ledger no replay, verified uninstall + exact reinstall. Keep Tray fix unchanged.
- Verify owned installed-runtime lifecycle and 24 mandatory acceptance gates once, with focused tests first and full pytest only after code changes. No repeated Batch A or accepted Shared PreExec.
- Bounded code scope: `agent_bridge/src/fox2_agent_bridge/installation.py`, `agent_bridge/scripts/certify_user_lifecycle.py`, narrowly needed resource/entrypoint(s), relevant regression tests; reports under `reports/BRIDGE-DESKTOP-BATCH-B/**`. If systemic change outside scope is necessary, STOP to CHAT rather than broad edits.

## Governance R2–R7 (currently not closed for execution)

- **R2:** Released governance and task source remain semantic authority. This is read-only intake, **not CODE_ALLOWED/DEV grant**.
- **R3:** Last Codex PASS and Copilot AUTH_REQUIRED came from preexec on prior source `7f027d4f` (receipt commit `9bb217d1`); now stale for code head `6a31409e`. Current auth, quota, capability and root cleanup safety UNKNOWN until fresh Windows evidence.
- **R4:** CHAT does source binding and intake. COPILOT / Native Auto Balance only if fresh auth becomes PASS; CODEX / gpt-6.1-sol Medium if process/uninstall concurrency and Windows lifecycle are material. WORK only independent safety audit if needed. No selection yet.
- **R5:** Source worktree `C:\Projects\FOX2-worktrees\FOX2-BRIDGE-DESKTOP-BATCH-B`; remote head confirmed but local current head, dirty state and exclusive writer must be rechecked at launch.
- **R6:** Fresh durable current-source PreExec receipt -> CHAT Git readback -> single-use authorized Dispatch 005 -> Agent code/retests/certification -> Agent remote result -> CHAT intake. No reuse of consumed 004.
- **R7 STOP:** source mismatch, missing/UNKNOWN material capabilities, privilege change, competing writer, unowned or active executable deletion, non-atomic unsafe uninstall, secret exposure, unauthorized path mutation, test failures, remote readback mismatch, provider/broker/LIVE touch.

## Single no-agent operational preflight (after fast-forward, on clean worktree)

```powershell
$wt="C:\Projects\FOX2-worktrees\FOX2-BRIDGE-DESKTOP-BATCH-B"
git -C $wt fetch --no-tags origin work/FOX2-BRIDGE-DESKTOP-BATCH-B
git -C $wt merge --ff-only FETCH_HEAD
python -B agent_bridge/scripts/preexec.py --profile bridge --worktree $wt --source-head 6a31409e0f3d46d4f2b2fc2bc48464ecff86e257 --publish
```

Never treat a PASS as durable until commit/push and independent remote receipt readback. Source HEAD moves only by receipt-only commit; future executable dispatch must bind actual updated head. No Agent is yet assigned.
