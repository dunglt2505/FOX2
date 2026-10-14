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

The Bridge launches Codex non-interactively as `codex -c windows.sandbox="unelevated" --ask-for-approval never exec --sandbox workspace-write -`. The approval flag is global and must appear before the `exec` subcommand. FOX2 pins the Windows sandbox implementation to `unelevated` because the installed Codex CLI 0.162.1 can fail its elevated sandbox setup refresh before any command starts; the outer Codex policy remains `workspace-write` with approval `never`. On Windows, the Bridge also prefers the MSI/WiX PowerShell host at `C:\\Program Files\\PowerShell\\7\\pwsh.exe` ahead of WindowsApps/MSIX PowerShell when that executable exists. Codex is instructed to edit/test only; it does not
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
- `FAILED`: a definitive pre-spawn failure proves the Agent never started.
- `NEEDS_RECONCILIATION`: execution started or is uncertain, including an Agent
  returning non-zero after launch. The consumed dispatch cannot be replayed and
  another Agent is never substituted.
- `SAFE_NOT_STARTED`: restart recovery found a proven pre-launch claim.

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
# Desktop-01+02 internal runtime

Run `agent_bridge/scripts/desktop_launcher.ps1` with PowerShell 7 to start the
hidden .NET System Tray host. It uses the existing Bridge Python runtime at
`C:\Projects\FOX2-AgentBridge\.venv\Scripts\python.exe`; no dependency installation
is performed. The source worktree must remain available at this internal launcher
location. This is an internal launcher, not Desktop-03 installer packaging.

Worker/control state is per user at `%USERPROFILE%\AppData\Local\FOX2\AgentBridge`.
On first use, an existing legacy ledger is snapshotted read-only while holding its
singleton lock; consumed dispatch identities are preserved. If the old supervisor
still owns that lock, bootstrap blocks. The old worktrees are never changed.
SQLite schema 4 preserves earlier execution/result/cursor evidence and adds
worker state and execution checkpoints. One-shot execution shares the Worker lock;
status and fixed controls remain available while it is held.

With `PYTHONPATH` pointing to `agent_bridge/src`, diagnostic commands are:

```powershell
python -m fox2_agent_bridge worker
python -m fox2_agent_bridge status
python -m fox2_agent_bridge status --dispatch-id EXACT_ID
python -m fox2_agent_bridge control pause
python -m fox2_agent_bridge control resume
python -m fox2_agent_bridge control check-now
python -m fox2_agent_bridge control open-logs
python -m fox2_agent_bridge control set-start-with-windows --enabled true
python -m fox2_agent_bridge control set-start-with-windows --enabled false
python -m fox2_agent_bridge control request-exit
```

Pause blocks new claims, including a control request during discovery. Check-now
is durable and waits while paused or executing. Exit finishes the current task
before stopping. Healthy polling defaults to 30 seconds; failures back off through
30/60/120/300 seconds. Heartbeats continue during Agent execution. No TCP listener
or arbitrary shell/prompt IPC exists. Start-with-Windows uses a SID-qualified
current-user interactive logon task with Limited privileges and no password.

Recovery never grants replay based on age. A pre-launch checkpoint becomes
`SAFE_NOT_STARTED` with the original claim retained. Uncertain execution becomes
`NEEDS_RECONCILIATION`; use a fresh authorized dispatch or explicit safe recovery
review, never delete the ledger or reuse a consumed identity. Non-zero exits retain
stdout, stderr, exit code, metadata and worktree identity in the checkpoint/result;
quota diagnostics grant neither replay nor Agent substitution. After a zero exit,
recovery verifies the exact branch, local cleanliness, base ancestry, remote HEAD,
write scope and acceptance evidence. A durable expected publication SHA must match.

CODEX accepts exact PINNED model and low/medium/high reasoning (legacy CURRENT_CONFIG
remains supported). Normal coding always requests FULL_ACCESS, sandbox
danger-full-access and approval never. COPILOT uses task-local Native Auto with
CHAT-selected efficiency/balance/intelligence tier, or an exact pin. The adapters
preflight the required CLI flags before spawning. Missing/unknown capabilities
and permission mismatches fail closed; versions are recorded without equality gates.
Copilot receives allow-all tools, paths and URLs. Technical access grants no
PR/main/merge/deploy/provider/broker/LIVE authority. Global settings are not changed.

Dispatch `delivery_owner` selects AGENT or BRIDGE. AGENT commits/pushes and Bridge
only verifies; BRIDGE requires uncommitted results and publishes once. Legacy
schema 0.6 dispatches without this field retain BRIDGE ownership. An immutable
execution tuple binds routing, permissions, prompt digest, worktree, branch and
delivery owner in SQLite. Requested/applied configuration and explicit structured
model, reasoning, usage and capacity observations survive restart. Missing actual
fields remain null/NOT_EXPOSED. Post-start quota/auth/capacity and configuration
mismatch require reconciliation even on exit zero. Claims are never replayed and
no alternate Agent is selected. Tray model/permission/usage/capacity entries are
read-only. Status reads do not mutate worker controls.

Generated runtime JSON and logs use the shared canonical UTF-8/LF pipeline.
Batch evidence generation uses the same helper and checks hygiene after writing.
Raw/binary evidence has a separate byte-preservation contract.

Deterministic tests use fake Agents and mocked startup registration. Poller tests
use real local Git histories with simulated file-remote transport in the managed
Windows sandbox. Manual Tray usability, real Windows logon and paid Agent canaries
must be recorded separately; these unit tests do not certify them.
