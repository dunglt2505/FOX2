# FOX2 — Package Lifecycle A01 PreExec Recovery

Date: 2026-10-21
Whole-WP: `FOX2-BRIDGE-RC1-TO-INTERNAL-READY`
Task: `FOX2-BRIDGE-RC1-PACKAGE-LIFECYCLE-A01`
Recovery method: `fox2-execution-recovery`

## Observed failed invocation

Owner launched task-specific PreExec tooling at publication head:
`14f46f7d5f38cff617d78db14b33275738adf15e`.

Observed:
- worktree created successfully;
- exact branch/head verified;
- original script blob `1d06a66a249b8e4a9c222c50713624fe6df99195` verified;
- PreExec script entered;
- then failed with `Index was outside the bounds of the array`;
- launcher exit 1.

The implementation Agent did not start. No Dispatch was published or consumed. No host lifecycle mutation occurred.

## Durable reconciliation

CHAT remote-read:
- task branch remained exactly `14f46f7d5f38cff617d78db14b33275738adf15e`;
- `reports/FOX2-BRIDGE-RC1-TO-INTERNAL-READY/preexec/package_lifecycle_a01.json` did not exist;
- therefore no PreExec PASS receipt or Git-side execution state was created.

## Root cause

The PreExec PowerShell helper declared:

`function Git([string[]]$Args)`

PowerShell variable names are case-insensitive and `$args` is an automatic variable. The helper therefore collided with the automatic argument variable. Its error path indexed `$Args[0]`, producing the observed array-bounds exception before material PreExec checks/live admission.

This was a CHAT tooling defect, not an Agent/task/product failure.

## Recovery patch

Patched only the versioned PreExec script:
- commit `b8dbf2a709f58efdab654cc0e12ba738ceaabb21`;
- script blob `c353fedab620b7dd5dbd4763be796c35a616b4e3`;
- change: rename helper argument to `$GitArgs`, require at least one Git argument, and use `$GitArgs[0]` in diagnostics.

Compare `14f46f7d… → b8dbf2a…`: one file only; 4 additions / 3 deletions.

## Verdict

`RECOVERED_TOOLING_FAILURE`.

Old failed PreExec invocation is not relabeled PASS. It did not consume an Agent attempt or Dispatch because neither existed yet.

Next safe action: fast-forward the clean local task worktree to `b8dbf2a…`, verify exact script blob, and run the corrected task-specific PreExec once. If any receipt or WIP is present, STOP and reconcile rather than rerun.
