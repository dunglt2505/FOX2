# Shared PreExec rollout

Delivery remains `PUSHED_UNREVIEWED` until CHAT accepts this implementation.

The shared lifecycle lives in `fox2_agent_bridge.preexec`. Task profiles register
capability checks and exact routing candidates; PowerShell adapters only pass
configuration to `agent_bridge/scripts/preexec.py`. The former rollout-local
PowerShell lifecycle is retired by its thin adapter replacement.

Publication requires a clean, exclusively owned task worktree at the explicitly
supplied source head. That head must contain the pinned Dictionary v1.2 and the
exact Policy, Routing, Protocol and PreExec contract bytes represented by the
generated binding. The target remote branch must still equal that source head.
The runner stages only the configured receipt, checks the resulting commit,
pushes the exact task branch, then verifies remote SHA and receipt bytes.

Example after CHAT has reconciled a target's source and accepted the rollout:

```powershell
python agent_bridge/scripts/preexec.py --profile app --worktree C:\Projects\FOX2-worktrees\FOX2-M1-A-APP-BATCH-B --source-head <exact-source-sha> --publish
```

`--pinned-agent CODEX` or `--pinned-agent COPILOT` makes that candidate material.
Without a pin, candidates are alternatives and only `eligible_agent_route` is
material. Successful probes remain evidence for CHAT's final selection.

`--cleanup-stale-receipt` permits cleanup only after schema, task, branch, path
and source identity prove the sole dirty artifact belongs to this receipt.
Unrelated staged or unstaged WIP remains untouched and blocks publication.

`--snapshot-root` with `--snapshot-path reports/.../preexec/name.json` records
diagnostic evidence without publishing the target branch. A snapshot never
emits `RECEIPT_PUSHED` and never satisfies durable task-branch readiness by itself.
Unsafe source/worktree states can produce a sanitized Schema-v1 `INFRA_FAILED`
snapshot using the trusted generated schema; they do not run Agent probes or
publish to the unsafe target.

CLI exit codes are 0 for durably published PASS, 20 for durably published BLOCKED,
and 30 or greater for infrastructure failure or non-published diagnostics. Successful
snapshot generation returns 33, preserving 0/20 exclusively for publication.
For `--publish`, only exact successful remote readback emits
`RECEIPT_PUSHED`. Publication failure overrides the process exit code while
preserving an already observed material blocker in the receipt.

Both Batch-B worktrees and their checked remote tips currently lack the current
Dictionary. This recovery therefore records fresh `INFRA_FAILED` snapshots under
the rollout report scope. CHAT must reconcile their sources and separately run
task-branch publication before assigning either Batch-B implementation. This
rollout publishes only `work/FOX2-PREEXEC-ROLLOUT-V1`.
