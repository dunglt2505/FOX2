# FOX2 Local Agent Bridge

The Bridge is the FOX2-only local relay between immutable Git dispatches and
supported local agents. The current Operational MVP supports Git-backed
dispatch discovery, exact worktree resolution, selected local Agent CLI execution
(Codex CLI for current DEV tasks; Copilot CLI retained for historical compatibility),
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

`run-next` only auto-executes a **Codex** dispatch that explicitly opts in with:

```json
{
  "runtime_contract": {
    "auto_execute": true
  }
}
```

Copilot dispatches are no longer selected by `run-next`; they remain available only through explicit diagnostic execution if needed. Dispatches without the opt-in flag are never selected automatically. A selected dispatch remains single-use.

For one exact diagnostic dispatch, `e2e-once --dispatch-path ...` remains
available, but normal operation should use `run-next`.


## Codex CLI DEV execution

New DEV dispatches can use `agent.product=CODEX`,
`agent.interface=OPENAI_CODEX_CLI`, and
`execution_path=BRIDGE_DIRECT_CODEX_CLI`.

The Bridge launches `codex exec` non-interactively with `workspace-write` and
`--ask-for-approval never`. Codex is instructed to edit/test only; it does not
need Git push authority. After Codex exits, the Bridge verifies that Codex did
not change Git history, validates every dirty path against the immutable
dispatch allowlist, validates required result files/markers, then the Bridge
itself stages, commits and pushes the authorized result branch. Main/merge,
provider, broker and LIVE rights remain false unless separately authorized.

The historical Copilot path remains available for already-published dispatches.

## Bounded DEV shell capabilities (Copilot compatibility)

Real coding WPs may need deterministic test commands in addition to Git.
A dispatch can opt into a Bridge-owned capability name:

```json
{
  "runtime_contract": {
    "auto_execute": true,
    "dev_shell_capabilities": ["PYTEST"]
  }
}
```

`PYTEST` maps only to a small exact command catalog: `python -m pytest --version`,
`python -m pytest -q`, and `python -m pytest tests/m1_p2_01 -q`. The Bridge does
not grant `shell(python:*)` or arbitrary pytest arguments. The Bridge rejects
unknown capability names and the Copilot adapter independently rejects raw
shell patterns outside its safe catalog. Arbitrary shell, PowerShell, package
installation, provider/network tooling, broker commands, and LIVE operations
are not granted by this capability.

The Bridge prepends the directory containing its own runtime Python executable
to the child `PATH`, so `python -m pytest` resolves to the controlled Bridge
runtime environment rather than an arbitrary system Python.

## Execution states

The SQLite ledger persists dispatch and execution state. Typical terminal
states are:

- `PUSHED_UNREVIEWED`: agent result was committed, pushed, and verified.
- `FAILED`: execution or verification failed.
- `INTERRUPTED`: execution was interrupted locally or recovered on next
  Bridge startup after the previous Bridge process ended.

An interrupted single-use dispatch is not automatically retried. A new
dispatch id is required.

Detailed successful results and failure information are persisted in SQLite. When the selected Agent exits but result verification fails, its captured stdout/stderr is also persisted so the next diagnosis does not lose the Agent's explanation.
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
Bridge Copilot CLI, Codex CLI, and Codex desktop/IDE sessions must not write
concurrently to the same worktree.
