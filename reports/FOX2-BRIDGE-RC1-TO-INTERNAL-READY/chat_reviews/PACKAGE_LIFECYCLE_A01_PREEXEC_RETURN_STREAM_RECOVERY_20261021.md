# FOX2 — Package Lifecycle A01 PreExec Return-Stream Recovery

Date: 2026-10-21
Whole-WP: `FOX2-BRIDGE-RC1-TO-INTERNAL-READY`
Task: `FOX2-BRIDGE-RC1-PACKAGE-LIFECYCLE-A01`
Method: `fox2-execution-recovery`

## Observed invocation

PreExec tooling at `42ef88352e24d675a2ed3f9cd352c1785b3b4a22` entered successfully and stopped with:

`The property 'Code' cannot be found on this object.`

Launcher facts:
- exact task branch/head verified;
- exact script blob verified;
- implementation Agent not started;
- Dispatch not published or consumed;
- host lifecycle mutation false.

## Durable reconciliation

CHAT remote-read:
- task branch remained exactly `42ef88352e24d675a2ed3f9cd352c1785b3b4a22`;
- task-specific PreExec receipt remained absent.

Therefore no PreExec PASS, Dispatch or implementation attempt was created.

## Root cause

`Run-Tool` emitted stage telemetry using:

`Write-Output ('FOX2_PREEXEC_STAGE=' + $Stage)`

In PowerShell, function success-stream output participates in the function return value. Therefore callers such as:

`$r = Run-Tool ...`

received both the telemetry string and the intended PSCustomObject, so `$r` became a collection and `$r.Code` was not a valid scalar property.

This failure occurred on the first helper call, before CODEX login/help/live-probe execution.

## Recovery patch

Commit:
`d55c0c79349f3f7e1e42cd6f60a942b5934de9e1`

Script blob:
`e528ee4724a4676be9d841ee6050c2d34fa227eb`

Change:
- stage telemetry moved from success stream to host stream using `Write-Host`;
- intended PSCustomObject remains the only success-stream return value.

Compare `42ef8835… → d55c0c79…`: exactly one file, one line replacement.

## Verdict

`RECOVERED_PREEXEC_RETURN_STREAM_TOOLING`.

Historical tooling failures remain factual and are not relabeled PASS.

Next safe action: with clean task worktree and no receipt, fast-forward to `d55c0c79…`, verify script blob `e528ee47…`, and run the corrected task-specific PreExec once. If receipt/WIP/process ambiguity exists, STOP and reconcile instead of rerunning.
