# FOX2 — Package Lifecycle A01 PreExec Timeout Recovery

Date: 2026-10-21
Whole-WP: `FOX2-BRIDGE-RC1-TO-INTERNAL-READY`
Task: `FOX2-BRIDGE-RC1-PACKAGE-LIFECYCLE-A01`
Method: `fox2-execution-recovery`

## Observed invocation

Corrected PreExec tooling at `b8dbf2a709f58efdab654cc0e12ba738ceaabb21` entered successfully, then terminated with:
`TOOL_TIMEOUT:codex.exe`.

Observed launcher facts:
- task worktree exact head verified;
- corrected script blob verified;
- implementation Agent not started;
- Dispatch not published or consumed;
- host lifecycle mutation false.

## Durable reconciliation

CHAT remote-read:
- branch remained exactly `b8dbf2a709f58efdab654cc0e12ba738ceaabb21`;
- task-specific PreExec receipt remained absent;
- no Git-side PASS or assignment state was created.

Therefore this invocation is not a task/Agent failure and is not a consumed implementation attempt.

## Tooling defect / ambiguity

The versioned helper redirected CODEX stdout/stderr but waited for process exit before draining those pipes. A sufficiently chatty child process can block on a full pipe while the parent waits, producing a synthetic timeout. The tooling also did not emit a stage identifier before CODEX login/help/live-probe calls, so the historical timeout stage is not defensibly recoverable from the old log.

Do not relabel that timeout as model/quota/runtime failure.

## Recovery patch

New PreExec tooling commit:
`42ef88352e24d675a2ed3f9cd352c1785b3b4a22`

Script blob:
`5f86f2b85cf0c580f4474f2d32ec8ade2e390b6b`

Changes:
- start async stdout/stderr drain immediately after process start;
- on timeout, kill process tree, wait, drain bounded output, then classify;
- emit `FOX2_PREEXEC_STAGE` for CODEX login status, exec help and live probe;
- use 60s / 60s / 240s stage-specific timeouts;
- reject any lingering process command line carrying `FOX2-package-lifecycle-preexec-` before another live probe.

Compare `b8dbf2a… → 42ef8835…`: one file only, the versioned PreExec script.

## Verdict

`RECOVERED_PREEXEC_TIMEOUT_TOOLING`.

The prior timeout remains historical and is not changed to PASS.

Next safe action: with a clean task worktree and no receipt, fast-forward to `42ef8835…`, verify exact script blob, then run the corrected task-specific PreExec once. If a receipt/WIP/lingering probe process is observed, STOP and reconcile instead of rerunning.
