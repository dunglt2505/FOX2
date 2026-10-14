# FOX2 — BRIDGE-DESKTOP-01 Background Worker & Reconciliation — Codex Execution

**WP:** `FOX2-BRIDGE-DESKTOP-01`
**Date:** 2026-10-14
**Status:** `EXECUTABLE / OWNER_AUTHORIZED / ONE_WHOLE_WP / STOP_AT_PUSHED_UNREVIEWED`

## 0. Source binding

Repository:
`dunglt2505/FOX2`

Task branch:
`work/FOX2-BRIDGE-DESKTOP-01-worker-codex`

Base SHA:
`308edc7bdabbc541216a97318590d2394acc9096`

Exact worktree:
`C:\Projects\FOX2-worktrees\FOX2-BRIDGE-DESKTOP-01-CODEX`

Normative product sources:
- BRD-09 v0.1 Candidate REV2, blob `c6f3cafd7c9bdba97fd413c6a9a891bde82d0699`
- Bridge Technical Spec v0.7 Candidate REV2, blob `dc4b28e12a7824771c22733682c8409e67127701`
- Desktop-01 Source/Design Lock, blob `df3a9c112d03635f561791ea5fc538d5f93abea6`
- Simplified Desktop-01 Implementation Plan, blob `e9d67896cc6192087ed37b40dc553a7c09ea53ab`
- Accepted Delivery Hotfix 01 result, commit `308edc7bdabbc541216a97318590d2394acc9096`

The Agent must implement the already-decided design. Do not reopen architecture or governance.

## 1. Execution model

This is **one whole WP**, not multiple gated phases.

Internal order only:

```text
A. Make existing Bridge tests Codex-sandbox compatible
B. Worker + GitHub mailbox signal
C. Durable state + pause/backoff
D. Restart/recovery + single instance
E. CLI integration + one final regression/evidence cycle
```

Do not stop between A-E unless a genuine STOP condition occurs.

There is no intermediate CHAT/WORK review.

## 2. Local preflight only

Before editing verify only:
- cwd is exact task worktree;
- branch is exact task branch;
- local HEAD equals exact base SHA;
- worktree/index is clean.

Allowed examples:
- `git rev-parse HEAD`
- `git branch --show-current`
- `git status --short`

Do NOT run remote Git preflight or host process inspection:
- no `git ls-remote/fetch/pull/push`
- no `Get-CimInstance`
- no competing-process scan.

CHAT/Bridge own remote/writer preflight.

If local exact checks fail, print only the blocked summary and final marker:
`FOX2_BRIDGE_DESKTOP_01_BLOCKED`

## 3. Writable scope

Writable:
- `agent_bridge/src/fox2_agent_bridge/**`
- `agent_bridge/tests/**`
- `agent_bridge/scripts/**` only when genuinely needed for Worker diagnostic/control
- `reports/FOX2-BRIDGE-DESKTOP-01/**` for final evidence only

Read-only:
- FOX2 product backend/frontend
- governance/docs except final report path above
- root project files unless absolutely required and STOPped for approval
- provider/broker/LIVE areas
- main

No package installation.

Codex edits/tests only. Bridge owns final commit/push.

## 4. Step A — fix Bridge test sandbox compatibility first

The previous hotfix implementation proved a test-harness portability defect inside Codex Windows sandbox.

Observed legacy issues:
1. adapter tests create synthetic worktrees under fixed `bridge_config.worktree_root` paths outside the task sandbox, e.g. `CODEX-E2E`, `COPILOT-SMOKE`, `COPILOT-E2E`, `COPILOT-PYTEST`, `COPILOT-UNSAFE`, causing permission errors;
2. `test_dispatch_poller.py` uses local Git remote setup/push in a way that invokes Git for Windows `sh.exe` signal-pipe behavior denied by the sandbox.

Fix test infrastructure, not production semantics.

Requirements:
- synthetic adapter worktrees live under pytest `tmp_path` or another task-worktree-local temp tree;
- preserve adapter path validation semantics;
- local Git fixture must remain an actual deterministic local Git test but avoid the sandbox-hostile shell path;
- prefer Git plumbing/direct bare-ref manipulation or another sandbox-safe local transport over external/network behavior;
- no Internet/GitHub dependency;
- no weakening/skipping/xfailed tests merely to obtain green;
- no broad monkeypatch that bypasses the production behavior under test;
- cleanup remains under sandbox-writable temp paths.

**Mandatory gate before Worker coding continues:**

`python -m pytest agent_bridge/tests -q`

must PASS **inside Codex sandbox** from this exact worktree.

If this cannot be achieved with bounded test-harness changes, STOP and return BLOCKED. Do not continue Worker implementation on an ungreen baseline.

## 5. Step B — Worker + GitHub mailbox signal

Implement a long-running per-user background Worker using existing Bridge Core.

V1 flow:

```text
CHAT immutable dispatch on configured Git control ref
 -> Worker lightweight remote-ref SHA probe
 -> unchanged SHA: no full fetch, no dispatch scan, no Agent call
 -> changed SHA: fetch exact control ref and discover immutable dispatch delta
 -> eligible auto_execute task: existing Bridge execution route
```

Requirements:
- outbound Git/HTTPS only;
- no inbound Internet listener/server;
- healthy poll candidate default ~30 seconds;
- immediate local `check-now` wake;
- one iteration independently testable;
- fake clock/sleeper/wake primitive in tests; no real 30/60/120/300 second waits.

Reuse existing `dispatch_poller.py`, `ops_runner.py`, `e2e_runner.py`, ledger and app composition. A small `worker.py` / `background_worker.py` is acceptable.

Do not build a second transport/governance engine.

## 6. Step C — durable state + pause/backoff

Persist only what restart correctness needs:
- pause state;
- last observed control SHA;
- last safely processed control SHA/cursor or equivalent existing durable cursor;
- poll/backoff state only if needed for correct restart/status.

Timing:
- healthy: 30s candidate default;
- error/offline: 30 -> 60 -> 120 -> 300s max;
- successful Git contact resets healthy cadence.

Pause:
- blocks new claim/Agent launch;
- does not abandon supervision of a task already running.

Resume:
- must not replay terminal dispatch.

Schema bump only if necessary. Preserve existing ledger rows and future-schema refusal behavior.

## 7. Step D — restart/reconciliation + single instance

Reuse accepted Hotfix 01 delivery recovery.

On Worker startup:
1. acquire existing process/single-instance lock;
2. open/migrate ledger;
3. reconcile non-terminal state;
4. never blindly rerun a successful Agent whose delivery is unresolved;
5. then enter mailbox polling.

Required:
- terminal/pushed dispatch never reruns;
- `DELIVERY_RECOVERY_REQUIRED` never relaunches Agent;
- task published while Worker was stopped is found after restart;
- crash around control-SHA/cursor persistence does not lose a valid dispatch;
- one Worker/profile only;
- second Worker cannot become a competing poller/writer.

Do not create a second delivery-recovery framework.

## 8. Step E — minimal CLI controls

Add only what is needed before Tray/Desktop-02.

Target behavior, names may follow existing CLI style:
- start/watch Worker;
- pause;
- resume;
- check-now;
- status;
- graceful stop if needed.

Controls are local operational controls only. They create no DEV/merge/Production/LIVE authority.

Do not implement Tray, Task Scheduler/autostart, installer, onboarding GUI, cloud relay, webhook, remote desktop, or multi-user service in this WP.

## 9. Final acceptance assertions

These are final checks, not intermediate gates:

- D01 Worker state/control deterministic
- D02 unchanged remote SHA => zero full fetch
- D03 unchanged remote SHA => zero Agent call
- D04 changed SHA => exact fetch/discovery
- D05 changed SHA/no eligible dispatch => zero Agent call
- D06 eligible dispatch executes once
- D07 healthy cadence deterministic
- D08 backoff 30/60/120/300 capped
- D09 successful contact resets backoff
- D10 check-now wakes promptly
- D11 Pause blocks new launch
- D12 Resume does not replay terminal dispatch
- D13 required durable state survives restart
- D14 offline-published task discovered after restart
- D15 pre-Agent interruption reconciled safely
- D16 delivery-recovery state never relaunches Agent
- D17 one Worker/profile enforced
- D18 crash around cursor handling loses no valid dispatch
- D19 no inbound Internet listener/server
- D20 full existing Bridge suite PASS inside Codex sandbox
- D21 no main/merge/Production/provider/broker/LIVE authority

BRD mapping:
- T23 -> D02/D04/D19
- T24 -> D02/D03/D10
- T25 -> D03
- T26 -> D08/D09
- T27 -> D19
- T28 -> D14
- T29 remains future push-hint only, not implemented.

## 10. Required tests

At final:
1. focused Desktop-01 tests;
2. full `python -m pytest agent_bridge/tests -q` inside Codex sandbox;
3. accepted Hotfix 01 regression tests;
4. migration tests if ledger schema changes;
5. syntax/import checks;
6. `git diff --check`;
7. changed-path scope check;
8. obvious-secret scan.

Do not require GitHub connectivity from Codex tests.

## 11. Final evidence

Create once at end:
- `reports/FOX2-BRIDGE-DESKTOP-01/report.md`
- `reports/FOX2-BRIDGE-DESKTOP-01/evidence_manifest.json`
- `reports/FOX2-BRIDGE-DESKTOP-01/evidence/**`

Report must include:
- base SHA;
- changed paths;
- focused/full test commands and results;
- sandbox-baseline fix summary;
- D01-D21 verdict;
- BRD T23-T29 mapping;
- restart/recovery proof;
- idle-zero-Agent proof;
- no-inbound-listener proof;
- scope/diff/secret checks;
- NOT_RUN/open gates.

Do not create intermediate report packages.

## 12. STOP conditions

STOP, preserve WIP and print BLOCKED marker if:
- local branch/HEAD/worktree exactness fails;
- sandbox baseline suite cannot be made PASS with bounded test-harness changes;
- implementation requires out-of-scope root/product files;
- frozen interface/source conflict appears;
- package install is required;
- safety/security regression;
- final required tests fail;
- Codex becomes unavailable;
- required evidence cannot be produced.

Do not STOP for routine internal implementation choices.

## 13. Git ownership

Codex MUST NOT:
- `git add`
- `git commit`
- `git push`

Bridge performs final verification, commit, push, and remote readback.

If delivery fails after successful implementation, use accepted delivery-recovery semantics; do not rerun Codex merely to repeat Git delivery.

## 14. Final response contract

On success summarize compactly:
- sandbox baseline fix;
- Worker/mailbox implementation;
- durable/restart/single-instance behavior;
- CLI controls;
- focused/full test results;
- D01-D21;
- changed paths;
- report/evidence paths;
- limitations/NOT_RUN.

Then end exactly:

`FOX2_BRIDGE_DESKTOP_01_DELIVERY_READY`

If blocked, end exactly:

`FOX2_BRIDGE_DESKTOP_01_BLOCKED`
