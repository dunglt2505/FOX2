# FOX2 Local Agent Bridge

BRG-010/020 provide the FOX2-specific local foundation: typed TOML
configuration, structured redacted logs, a versioned SQLite ledger, a process
singleton lock, runtime executable discovery, a health command, and read-only
discovery of candidate dispatch files from the fixed FOX2 control branch.
Discovered files remain unvalidated candidates; no agent is executed.

## Environment

Use only the project virtual environment:

```powershell
C:\Projects\FOX2-AgentBridge\.venv\Scripts\python.exe -m pip install -e "C:\Projects\FOX2-AgentBridge[dev]"
C:\Projects\FOX2-AgentBridge\.venv\Scripts\python.exe -m pytest "C:\Projects\FOX2-AgentBridge\tests"
C:\Projects\FOX2-AgentBridge\.venv\Scripts\python.exe -m fox2_agent_bridge health
C:\Projects\FOX2-AgentBridge\.venv\Scripts\python.exe -m fox2_agent_bridge poll-once
```

The optional configuration file can be copied from `config\bridge.example.toml`
to `config\bridge.toml`, then supplied with `health --config <path>`. Do not put
credentials or other secrets in configuration.

`poll-once` performs a read-only poll of
`dunglt2505/FOX2` branch `work/FOX2-LOCAL-DISPATCH-chat`. Git objects and poll
observations are stored under the Bridge `data` directory, not in the FOX2
working tree. A missing branch is reported as `CONTROL_BRANCH_UNAVAILABLE`;
the command does not create it.

## Scope boundary

This is a FOX2-only package. Project identity and repository are fixed to
`FOX2` and `dunglt2505/FOX2`. Polling only inventories candidate paths and
records immutable Git object identities; it does not validate dispatch
authorization or content. Prompt execution, worktree creation, result pushes,
and review events are not implemented.
