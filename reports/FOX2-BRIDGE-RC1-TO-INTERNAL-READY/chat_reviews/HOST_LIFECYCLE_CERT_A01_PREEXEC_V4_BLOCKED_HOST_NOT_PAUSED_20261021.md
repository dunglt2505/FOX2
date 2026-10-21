# FOX2 — Host Lifecycle Cert A01 PreExec v4 Reconciliation

Date: 2026-10-21
Whole-WP: `FOX2-BRIDGE-RC1-TO-INTERNAL-READY`
Task: `FOX2-BRIDGE-RC1-HOST-LIFECYCLE-CERT-A01`

## Observed Owner-host run

PreExec publication:
`768b35164fd740bb6a455ee50fc4dcaae331fed8`

PreExec v4 blob:
`a2ac93b5d99e2817f1a777a02094a05811c46930`

Observed gates before failure:
- remote task branch head exact: PASS;
- accepted source ancestor: PASS;
- pre-start product drift: NONE;
- dedicated worktree created cleanly;
- local branch/head exact: PASS;
- task/prompt/blob identity: PASS;
- PreExec v4 started;
- installed Bridge `control status` command executed successfully.

Observed blocker:
`HOST_NOT_PAUSED`.

The PreExec stopped before build/package/install/update/uninstall/reinstall and before CODEX live route probe completion.

## Remote reconciliation

CHAT independently remote-read task branch after the Owner run:

- remote head remains `768b35164fd740bb6a455ee50fc4dcaae331fed8`;
- standard PreExec receipt `reports/FOX2-BRIDGE-RC1-TO-INTERNAL-READY/preexec/host_lifecycle_cert_a01.json` is absent;
- no executable Dispatch has been published for the host-lifecycle task;
- no implementation/host-cert Agent was started by this PreExec;
- no Bridge package lifecycle mutation occurred.

## Protocol classification

Under PreExec Evidence Protocol v1.1:
- this is a material prerequisite failure before Dispatch;
- no executable Dispatch exists;
- implementation Agent did not start;
- `dispatch_consumed=NO`;
- pre-start failure does not trigger Dispatch replay semantics.

Because the v4 runner threw before emitting a durable BLOCKED receipt, the observed blocker is preserved by this CHAT reconciliation record rather than rewritten as PASS.

## Verdict

`RECOVERED / PREEXEC_BLOCKED — HOST_NOT_PAUSED`

No blind rerun.

## Next safe action

Use the installed Bridge fixed control path only to establish a safe paused/non-running local state:

1. verify exact task branch/publication and absent PreExec receipt;
2. read current installed control state;
3. refuse recovery if state indicates active execution/publication/stop transition that cannot be safely reconciled;
4. issue official installed `control pause`;
5. if an installed Worker/Tray remains active, issue official `control request-exit` and wait for it to terminate;
6. verify `paused=true`, no active Worker/Tray, exact task branch still unchanged and no receipt exists;
7. rerun the same immutable PreExec v4.

This is a reconciled preflight retry, not a consumed Dispatch replay.

G3/G4/Canary remain HOLD.
