# FOX2 — CHAT Execution Recovery — CLAIMED empty-string normalization

Date: 2026-10-22
Whole-WP: `FOX2-BRIDGE-RC1-TO-INTERNAL-READY`
Task: `FOX2-BRIDGE-RC1-HOST-LIFECYCLE-CERT-A02`
Dispatch: `FOX2-DISPATCH-BRIDGE-RC1-HOST-LIFECYCLE-CERT-A02-CODEX-001`

## Verdict

**RECOVERED — EXISTING CLAIM REMAINS PRE-CONSUME**

The first recovery continuation stopped before consume because it required `result_sha == null`, while the existing `CLAIMED` record stores that unset string field as an empty string.

Observed stop:
`NO_REPLAY_STOP: result_sha already populated.`

The continuation had already passed:
- exact task/control remote heads;
- clean worktree / no product drift;
- immutable task/prompt/Dispatch binding;
- claim identity;
- `state=CLAIMED`;
- `dispatch_consumed=false`;
- no `spawn_attempted_at`;
- no `running_at`;
- no `process_id`;
- no `exited_at`;
- no `exit_code`.

It stopped at the first string-unset validation before writer/host/capacity/consume steps.

## Root cause

The original launcher used optional typed PowerShell parameters such as:

`[AllowNull()][string]$ResultSha = $null`

and then tested `$null -ne $ResultSha`.

PowerShell string binding may normalize an unset/null string value to an empty string. The original claim writer therefore serialized semantically unset string fields as `""`.

For recovery, `result_sha`, `delivery`, and `detail` must be treated as unset only when `[string]::IsNullOrWhiteSpace(...)` is true.

Any non-empty value remains a no-replay stop.

## Git reconciliation

CHAT independently verified after the stop:
- task branch remains exactly `76913f36b461689a84e8b4acf57a9ef83a98828d`;
- control branch remains exactly `8dceb41112d8240ec579ddede23b8ae6a9d06662`;
- no result branch advance exists.

Therefore no Git evidence supports Agent start or result delivery.

## Safe continuation

Resume the same existing claim only.

Before consume, require:
- exact claim identity and `state=CLAIMED`;
- `dispatch_consumed=false`;
- lifecycle timestamp/PID/exit fields absent;
- `result_sha`, `delivery`, `detail` null or whitespace only;
- no task-scoped writer;
- exact task/control heads;
- clean worktree;
- safe Owner-host state;
- current pinned CODEX route/capacity.

At the consume transition, normalize semantically unset string fields back to JSON null and atomically update the same claim to `SPAWN_ATTEMPTED`.

Do not delete/recreate the claim and do not publish a new Dispatch.

G3 remains false.
