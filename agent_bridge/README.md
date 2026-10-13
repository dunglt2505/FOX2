# FOX2 Local Agent Bridge

The Bridge is the FOX2-only local relay between immutable Git dispatches and
supported local agents. The current Operational MVP supports Git-backed
dispatch discovery, exact worktree resolution, GitHub Copilot CLI execution,
single-use replay protection, result verification, durable execution status,
startup recovery of interrupted runs, and one-dispatch operational polling.

## Source and runtime model

GitHub `dunglt2505/FOX2` under `agent_bridge/**` is the source of truth.
Development happens in task worktrees under `C:\Projects\FOX2-worktrees`.
`C:\Projects\FOX2-AgentBridge` is runtime state only: Python environment,
SQLite ledger, logs, Git transport objects, lock file, and runtime result JSON.

Do not develop directly in `C:\Projects\FOX2` or treat the runtime folder as
authoritative source.

## Operational commands

From the Bridge source worktree:

```powershell
.\agent_bridge\scripts\bridge_ops.ps1 status
.\agent_bridge\scripts\bridge_ops.ps1 health
.\agent_bridge\scripts\bridge_ops.ps1 poll-once
.\agent_bridge\scripts\bridge_ops.ps1 run-next
```

`run-next` only executes a dispatch that explicitly opts in with:

```json
{
  "runtime_contract": {
    "auto_execute": true
  }
}
```

Historical canaries and normal dispatches without that flag are never selected
automatically. A selected dispatch remains single-use.

For one exact diagnostic dispatch, `e2e-once --dispatch-path ...` remains
available, but normal operation should use `run-next`.

## Execution states

The SQLite ledger persists dispatch and execution state. Typical terminal
states are:

- `PUSHED_UNREVIEWED`: agent result was committed, pushed, and verified.
- `FAILED`: execution or verification failed.
- `INTERRUPTED`: execution was interrupted locally or recovered on next
  Bridge startup after the previous Bridge process ended.

An interrupted single-use dispatch is not automatically retried. A new
dispatch id is required.

Detailed successful results and failure information are persisted in SQLite.
The Bridge also writes a best-effort runtime JSON snapshot under:

`C:\Projects\FOX2-AgentBridge\data\results\<dispatch_id>.json`

Use:

```powershell
.\agent_bridge\scripts\bridge_ops.ps1 status -DispatchId <dispatch_id>
```

to inspect one dispatch.

## Safety boundary

Operational MVP does not merge, open PRs, touch main, deploy, write to
provider/broker/LIVE systems, or reevaluate FOX2 governance. It executes only
an already-authorized immutable dispatch and verifies the result against the
dispatch branch/path constraints.

One writer owns one branch/worktree for one execution. VS Code Copilot,
Bridge Copilot CLI, and Codex must not write concurrently to the same worktree.
