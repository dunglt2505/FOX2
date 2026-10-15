# FOX2 Bridge Batch B — Tray/Lifecycle Recovery Intake 004

**Status:** PREEXEC_REQUIRED / NON_EXECUTABLE / NOT_AN_AGENT_ASSIGNMENT
**Prepared by:** CHAT
**WP:** FOX2-BRIDGE-DESKTOP-BATCH-B (same WP; no micro-WP split)
**Source branch:** `work/FOX2-BRIDGE-DESKTOP-BATCH-B`
**Source HEAD checked:** `7f027d4f8e1346ebc13a3d4f3e5b299f4d870a0c`
**Control branch:** `work/FOX2-DISPATCH-chat`
**Policy:** FOX2 Policy V1.8.9; Project Dictionary v1.2; project-wide PreExec v1.1
**Safety:** No PR, merge, main, deploy, provider/broker writes or LIVE.

## R0 / R1 — evidence reconciled

- Dispatch 001, 002 and 003 are CONSUMED; **never replay**.
- Dispatch 003 STOP report on the task branch: previously 352 pytest PASS / 2 FAIL due missing Shared PreExec thin adapters, and separately Tray graceful exit failed.
- Exact accepted upstream thin adapters were copied into task branch at `f3c0f0b795d9adf7012b08f6f1727c925f218e2e`; owner reports targeted `test_thin_adapters` = 3 PASS.
- Owner recovered Dispatch 003 authored code from `%LOCALAPPDATA%\FOX2\recovery\003-stopped-draft`, preserving `agent_bridge/.gitignore`, and reports local pytest = **354 PASS / 0 FAIL**. This is operator-reported Windows evidence, *not* installed-runtime certification.
- The recovered 17 code files were pushed as WIP checkpoint `7f027d4f8e1346ebc13a3d4f3e5b299f4d870a0c`; CHAT verified remote HEAD and exact changed path list. Do not redo or overwrite recovered implementation.
- Remain: Tray shutdown/lifecycle diagnosis, verified correction, installed packaging/update/uninstall/restart certification, and 24 acceptance gates.

## Root-cause investigation boundary

Code examined:
- `agent_bridge/scripts/desktop_tray.ps1`: 2-second UI timer polls fixed `control status`; Tray exits only after `stop_requested && state == STOPPED`. Exit menu sends `request-exit`. Installed Tray starts Worker subprocess.
- `agent_bridge/src/fox2_agent_bridge/desktop.py`: Worker tests stop request before pause, enters STOPPING, then updates STOPPED in finalization.
- `agent_bridge/scripts/certify_user_lifecycle.py`: real installed test requests exit, polls Tray process count for up to 30 seconds, then raises `tray did not finish graceful exit`.

**Not yet proven:** Whether the Tray UI event loop is blocked, Worker is delayed, subprocess control query hangs, exit condition is missed, or a launch/context/config discrepancy causes the timeout. Do not report a guessed root cause as confirmed.

**Narrow code change** only after evidence: graceful shutdown of Tray and Worker, worker/process disposal, bounded diagnostic/termination behavior without unsafe kill of unrelated process; add deterministic regression tests. No business logic or Agent dispatch/replay changes unless proven necessary.

## R2–R7 gate before assignment

1. **R2 Source authority:** task branch current HEAD must exactly match above checkpoint; Task Spec + Policy V1.8.9 remain authority; do not modify released governance or accepted Batch A.
2. **R3 Agent access/quota:** publish/read the source-current PreExec v1.1 receipt for the exact worktree and source. Check both permitted alternatives. Previously Copilot AUTH_REQUIRED and Codex PASS are *historical*, not current proofs.
3. **R4 Routing:** compare COPILOT CLI / Native Auto Balance for small deterministic scripts against CODEX CLI / gpt-6.1-sol Medium for Windows process-shutdown/concurrency. CHAT handles intake; WORK only when independent final audit is warranted. Pick only after current PASS and cost/safety comparison.
4. **R5 Exclusive writer:** real local Windows worktree/branch CLEAN, ownership verified; no uncoordinated writer. `git` worktree is `C:\Projects\FOX2-worktrees\FOX2-BRIDGE-DESKTOP-BATCH-B`.
5. **R6 Bound handoff:** publish a **new** single-use Dispatch only after durable PreExec PASS and independent CHAT Git readback. Bind exact source, Agent/model/permission, authorized code `agent_bridge/**`, reports `reports/BRIDGE-DESKTOP-BATCH-B/**`, and all STOP/gates. Treat Dispatch 001–003 consumed; no replay or reinterpretation of ledger.
6. **R7 STOP:** missing/UNKNOWN material capability, nonexclusive writer, unexpected code changes, install-risk or safety failure, unproven replay protection, test failure, leak or out-of-scope diff.

## Acceptance and delivery

- Repair only the demonstrated Tray graceful-exit and installed lifecycle problem; preserve previously recovered code and test behavior.
- First run narrow deterministic shutdown regression; then installed lifecycle / packaging checks on Windows, then full pytest **once when changes warrant it**.
- Certify the current task's all **24 gates**, including dispatch-v3 Dictionary binding, legacy compatibility, real eligible canary, exact Agent parameters and permissions, result remote readback, usage snapshot, replay prevention, full suite, allowlist, secret scan, diff check.
- Publish only `work/FOX2-BRIDGE-DESKTOP-BATCH-B`, include verified evidence and independent remote readback. Output `PUSHED_UNREVIEWED`; **only CHAT** can subsequently accept `INTERNAL_FOX2_BRIDGE_READY`.
- If certification incomplete, publish truthful WIP/evidence only, explicitly `BRIDGE_READY=NO`.

## Immediate next operational gate (not DEV)

In the clean correct Windows worktree, use the existing canonical preexec CLI:
```powershell
python -B agent_bridge/scripts/preexec.py --profile bridge --worktree "C:\Projects\FOX2-worktrees\FOX2-BRIDGE-DESKTOP-BATCH-B" --source-head 7f027d4f8e1346ebc13a3d4f3e5b299f4d870a0c --publish
```
A receipt's `PASS` or `BLOCKED` only counts if commit/push/readback succeeds. CHAT then independently checks latest branch HEAD, receipt status, eligible route, and writer facts before any execution Dispatch 004.
