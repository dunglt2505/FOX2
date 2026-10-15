# FOX2 — Owner Direction: Defer Uninstall, Resume Core DEV
**Date:** 2026-10-15 (Asia/Ho_Chi_Minh)
**Status:** OWNER_PRIORITY_DECISION / NON_EXECUTABLE
**Scope:** FOX2 Bridge Desktop Batch B only.
**Controlling policy:** Dictionary v1.2, Policy V1.8.9, PreExec v1.1, Dispatch v3. Does not silently override mandatory release safety gates.

## Decision

Owner instruction: "Uninstall lỗi thì kệ đi ... tập trung vào vấn đề chính". Interpret as **DEFER UNINSTALL FIX**, not as a false PASS and not as permission for destructive cleanup. The earlier 005 evidence-only stop correctly preserved work. No new uninstall recovery task, no chain of micro-dispatches.

- `UNINSTALL_PATH=DEFERRED_OWNER_PRIORITY`, previous failure remains factual evidence.
- `INTERNAL_FOX2_BRIDGE_READY=NO` until required acceptance is satisfied or a formally approved, policy-valid changed release criterion is bound. Do not falsely report all 24 gates PASS.
- Do NOT fix, retry, kill, switch pointer, delete, repair or launch the existing partially uninstalled `%LOCALAPPDATA%\FOX2\AgentBridge` runtime.
- Dispatches 001–005 CONSUMED; NEVER replay.
- Preserve all existing code, restored 17 files, Tray graceful exit fix, tests, source branches, SQLite ledger, manual consumption evidence and data.
- Stop any matching FOX2-owned process **only if demonstrably active and blocking a permitted isolated test**, with exact PID/ownership verification; never globally kill `python.exe`, `pwsh.exe`, `codex.exe` or unrelated process.

## ONE next whole-WP execution, NOT another uninstall microtask

Goal: continue FOX2 Bridge core product development and evidence on **fresh, isolated runtime**, away from corrupted installation. No live provider/broker/trading writes.

1. Use latest task branch HEAD and current source; make only necessary minimal code changes for isolated install/startup/worker/Tray/dispatch, no uninstall fix. Avoid full repository rediscovery.
2. Run bounded targeted tests against clean disposable profiles/paths and existing source; prove core Bridge starts, stops gracefully, has single Worker, exact agent routing/dispatch v3/dictionary binding, durable no-replay, remote result readback, logs/usage snapshot with privacy hygiene.
3. Reuse historical evidence transparently. Re-run full pytest only once when there are substantive code changes; avoid repetitive testing.
4. Record 24 gates honestly: new PASS for actual tested gates, `UNINSTALL_PATH=DEFERRED_OWNER_PRIORITY`, unaffected historical gates `HISTORICAL_PASS` where applicable, remaining `NOT_CERTIFIED`. Never claim full release readiness.
5. Publish one integrated result/evidence from the same authorized work package; report `BRIDGE_CORE_VALIDATED` only when validated, and `INTERNAL_FOX2_BRIDGE_READY=NO` until formal release gate resolution.
6. Only after the Bridge core is proven, resume website according to the Owner priority and current policy/roadmap. Do not silently treat a damaged production/user runtime as acceptable.

## Routing gate and agent scope

This is a CHAT source/priority update, **not executable Dispatch, not CODE_ALLOWED**. Before Agent assignment: POLICY_CHECK → TASK_STATE_CHECK → ROUTING_R0_R7 → ASSIGNMENT_CHECK; one source-current PreExec PASS and readback for Agent candidate and exclusive writer. Compare COPILOT (prior AUTH_REQUIRED) and CODEX (prior eligible but current quota UNKNOWN), plus CHAT/WORK. An eligible Agent may be chosen only after gates are met. Keep worktree `C:\Projects\FOX2-worktrees\FOX2-BRIDGE-DESKTOP-BATCH-B`, task branch `work/FOX2-BRIDGE-DESKTOP-BATCH-B`, code `agent_bridge/**`, reports `reports/BRIDGE-DESKTOP-BATCH-B/**`. No main/PR/merge/deploy/provider/broker/LIVE.

**Single STOP boundary:** source/writer/authority mismatch; risk to user data, installation, ledger/no-replay, credentials or release-gate truthfulness. A known failed uninstall on the quarantined runtime is NOT by itself a STOP for isolated source core DEV.
