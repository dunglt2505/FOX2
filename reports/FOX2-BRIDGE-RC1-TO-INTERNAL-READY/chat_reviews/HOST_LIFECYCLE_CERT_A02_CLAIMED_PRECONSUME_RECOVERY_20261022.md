# FOX2 — CHAT Execution Recovery — Host Lifecycle A02 CLAIMED / PRE-CONSUME

Date: 2026-10-22
Whole-WP: `FOX2-BRIDGE-RC1-TO-INTERNAL-READY`
Feature: `FOX2-BRIDGE-RC1`
Task: `FOX2-BRIDGE-RC1-HOST-LIFECYCLE-CERT-A02`
Dispatch: `FOX2-DISPATCH-BRIDGE-RC1-HOST-LIFECYCLE-CERT-A02-CODEX-001`

## Verdict

**RECOVERED — PRE-CONSUME CLAIM EXISTS / SAFE TO RESUME SAME ATTEMPT ONLY**

Do not delete or recreate the durable claim. Do not publish a new Dispatch. Do not rerun the original launcher from the beginning.

## Observed execution timeline

Owner-host launcher passed all pre-start material checks:
- task branch exact runtime base;
- control branch exact Dispatch;
- no product drift;
- task/prompt/receipt binding PASS;
- Dispatch blob/SHA binding PASS;
- no prior claim;
- host safe control PASS;
- exactly one hidden/minimized exact-current WPF process;
- Worker/legacy count zero;
- build environment PASS;
- CODEX route/capacity PASS;
- exclusive writer lease acquired.

The launcher then durably wrote the attempt claim as:

`state=CLAIMED`

and printed:

`FOX2_ATTEMPT_STATE=CLAIMED`

The next transition attempted to save `SPAWN_ATTEMPTED`, but the launcher-local state variable was not updated after the first create. The second save therefore incorrectly used `FileMode.CreateNew` against the already-created claim path and failed with "file already exists".

The output then correctly reported:
- `FOX2_DISPATCH_CONSUMED=FALSE`;
- `FOX2_AGENT_STARTED=FALSE`;
- `FOX2_NEXT=CHAT_PRESTART_INTAKE`.

No `Process.Start()` for CODEX was reached.

## Root cause

Launcher vehicle defect in claim persistence state tracking:

The first successful claim create set `$script:ClaimCreated = $true`, while subsequent logic/catch tested the invocation-scope `$ClaimCreated`. The invocation-scope value remained false, so the second `Save-Claim` attempted another create-new operation.

This defect is outside task/prompt/Dispatch semantics.

## Remote reconciliation

CHAT independently verified after the failure:
- task branch remains exactly `76913f36b461689a84e8b4acf57a9ef83a98828d`;
- control branch remains exactly `8dceb41112d8240ec579ddede23b8ae6a9d06662`;
- no result branch advance occurred.

## Recovery boundary

Before continuing, the Owner-host recovery launcher must read the existing claim and require:
- exact Dispatch/task/prompt/runtime/source bindings;
- `state=CLAIMED`;
- `dispatch_consumed=false`;
- no spawn/running/exit/result fields populated;
- no task-scoped CODEX writer;
- task/control remote heads unchanged;
- clean worktree;
- current host safe state still compatible;
- current CODEX route/capacity PASS.

Only then may the same claim be atomically updated to `SPAWN_ATTEMPTED` and the same Dispatch be consumed exactly once immediately before CODEX process start.

Any different/unknown claim state => `NO_REPLAY_STOP`.

## Forbidden

- no claim deletion;
- no claim recreation;
- no new Dispatch;
- no replay of old Host A01 or Lifecycle/WPF Dispatches;
- no product/source/test write;
- no G3/G4/Canary/main/merge/provider/broker/LIVE.

G3 remains false.
