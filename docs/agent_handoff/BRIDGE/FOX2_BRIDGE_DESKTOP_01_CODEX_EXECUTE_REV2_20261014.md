# FOX2 — BRIDGE-DESKTOP-01 Background Worker & Reconciliation — Codex Execution REV2

**WP:** `FOX2-BRIDGE-DESKTOP-01`
**Date:** 2026-10-14
**Status:** `EXECUTABLE / OWNER_AUTHORIZED / ONE_WHOLE_WP / STOP_AT_PUSHED_UNREVIEWED`

## 0. Why REV2 exists

Dispatch `FOX2-BRIDGE-DESKTOP-01-CODEX-001` was blocked before mutation because Codex tried to verify source blobs that live on the dedicated docs branch and therefore are not present in the local task branch object database.

That verification responsibility belongs to CHAT, not Codex.

CHAT has freshly verified on GitHub before publishing this REV2:
- Desktop task branch remote HEAD = `308edc7bdabbc541216a97318590d2394acc9096`
- BRD-09 v0.1 Candidate REV2 blob = `c6f3cafd7c9bdba97fd413c6a9a891bde82d0699`
- Bridge Technical Spec v0.7 Candidate REV2 blob = `dc4b28e12a7824771c22733682c8409e67127701`
- Desktop-01 Source/Design Lock blob = `df3a9c112d03635f561791ea5fc538d5f93abea6`
- Simplified Desktop-01 Implementation Plan blob = `e9d67896cc6192087ed37b40dc553a7c09ea53ab`

These blob IDs are **provenance only**.

Codex MUST NOT attempt to:
- `git cat-file` these blobs;
- fetch the docs branch;
- verify these off-branch blobs locally;
- perform any remote Git access for source verification.

This executable prompt is self-contained and is the exact implementation instruction for the Agent.

## 1. Exact task binding

Repository:
`dunglt2505/FOX2`

Task branch:
`work/FOX2-BRIDGE-DESKTOP-01-worker-codex`

Base SHA:
`308edc7bdabbc541216a97318590d2394acc9096`

Exact worktree:
`C:\Projects\FOX2-worktrees\FOX2-BRIDGE-DESKTOP-01-CODEX`

Accepted predecessor:
`FOX2-BRIDGE-DELIVERY-HOTFIX-01 @ 308edc7bdabbc541216a97318590d2394acc9096`

## 2. Execution model

This is **one whole WP**.

Internal order only:

```text
A. Make existing Bridge tests Codex-sandbox compatible
B. Worker + GitHub mailbox signal
C. Durable state + pause/backoff
D. Restart/recovery + single instance
E. CLI integration + one final regression/evidence cycle
```

Do not stop between A-E unless a genuine STOP condition occurs.

There is no intermediate Owner/CHAT/WORK checkpoint.

## 3. Local preflight only

Before editing verify only:
- cwd is exact task worktree;
- current branch is exact task branch;
- local HEAD equals exact base SHA;
- worktree and index are clean.

Allowed examples:
- `git rev-parse HEAD`
- `git branch --show-current`
- `git status --short`

Do NOT run:
- `git ls-remote`
- `git fetch`
- `git pull`
- `git push`
- `git cat-file` for the docs/source blobs above
- `Get-CimInstance`
- competing-process discovery.

CHAT/Bridge own remote/source/writer preflight.

If local branch/HEAD/status fail, STOP without mutation and end with:
`FOX2_BRIDGE_DESKTOP_01_BLOCKED`

## 4. Writable scope

Writable:
- `agent_bridge/src/fox2_agent_bridge/**`
- `agent_bridge/tests/**`
- `agent_bridge/scripts/**` only if genuinely required for Worker diagnostic/control
- `reports/FOX2-BRIDGE-DESKTOP-01/**` for final evidence only

Read-only:
- FOX2 product backend/frontend
- governance/docs outside final report path
- root project files unless a genuine STOP is required
- provider/broker/LIVE areas
- main

No package installation.

Codex edits/tests only. Bridge owns final commit/push.

## 5. Step A — make full Bridge tests sandbox-compatible

A prior hotfix run exposed a test-harness portability defect inside Codex Windows sandbox.

Observed legacy problems:
1. adapter tests create synthetic worktrees below fixed `bridge_config.worktree_root` paths outside the task sandbox, such as `CODEX-E2E`, `COPILOT-SMOKE`, `COPILOT-E2E`, `COPILOT-PYTEST`, `COPILOT-UNSAFE`;
2. `test_dispatch_poller.py` uses local Git remote setup/push in a way that invokes sandbox-hostile Git-for-Windows shell/signal-pipe behavior.

Fix test infrastructure only; do not weaken production semantics.

Requirements:
- synthetic adapter worktrees must live under pytest `tmp_path` or another task-worktree-local sandbox-writable temp tree;
- preserve adapter path-validation semantics;
- local Git poller fixture remains a deterministic local Git test but must avoid sandbox-hostile shell behavior;
- prefer direct Git plumbing / bare-ref manipulation / sandbox-safe local transport;
- no Internet/GitHub dependency;
- no skip/xfail merely to make suite green;
- no broad monkeypatch that bypasses the actual production behavior under test;
- temp cleanup remains inside sandbox-writable paths.

Mandatory gate before Worker implementation continues:

`python -m pytest agent_bridge/tests -q`

must PASS inside Codex sandbox.

If bounded test-harness changes cannot make this baseline green, STOP with BLOCKED marker and do not proceed to Worker coding.

## 6. Step B — Worker + GitHub durable mailbox signal

Implement a long-running per-user Worker using existing Bridge Core.

V1 behavior:

```text
CHAT immutable dispatch on configured Git control ref
 -> Worker lightweight remote-ref SHA probe
 -> unchanged SHA: no full fetch, no dispatch scan, no Agent call
 -> changed SHA: fetch exact control ref and discover immutable dispatch delta
 -> eligible auto_execute task: invoke existing Bridge execution route
```

Requirements:
- outbound Git/HTTPS only;
- no inbound Internet listener/server;
- healthy poll candidate default ~30 seconds;
- immediate local check-now wake;
- one iteration independently testable;
- fake clock/sleeper/wake primitive in tests;
- no real 30/60/120/300 second waits.

Reuse current `dispatch_poller.py`, `ops_runner.py`, `e2e_runner.py`, ledger and app composition. A small `worker.py` or `background_worker.py` is acceptable.

Do not create a second transport or governance engine.

## 7. Step C — durable state + pause/backoff

Persist only what restart correctness needs:
- pause state;
- last observed control SHA;
- last safely processed control SHA/cursor or equivalent existing durable cursor;
- poll/backoff state only where needed for correct restart/status.

Timing:
- healthy: 30s candidate default;
- error/offline: 30 -> 60 -> 120 -> 300s max;
- successful Git contact resets healthy cadence.

Pause:
- blocks new task claim/Agent launch;
- does not abandon an already running task.

Resume:
- must not replay terminal dispatch.

Schema bump only if necessary. Preserve existing ledger rows and future-schema refusal semantics.

## 8. Step D — restart/reconciliation + single instance

Reuse accepted Hotfix 01 delivery recovery.

On Worker startup:
1. acquire existing process/single-instance lock;
2. open/migrate ledger;
3. reconcile non-terminal state;
4. never blindly rerun a successful Agent whose delivery is unresolved;
5. enter mailbox polling.

Required:
- terminal/pushed dispatch never reruns;
- `DELIVERY_RECOVERY_REQUIRED` never relaunches Agent;
- task published while Worker was stopped is found after restart;
- crash around control-SHA/cursor persistence does not lose a valid dispatch;
- one Worker/profile only;
- second Worker cannot become competing poller/writer.

Do not create a second recovery framework.

## 9. Step E — minimal CLI controls

Add only what is needed before Desktop-02 Tray:
- Worker/watch start;
- pause;
- resume;
- check-now;
- status;
- graceful stop if required by the Worker lifecycle.

Exact command names may follow existing CLI style.

Do not implement:
- Tray;
- Start-with-Windows / Task Scheduler;
- installer;
- onboarding GUI;
- webhook/cloud relay;
- remote desktop;
- multi-user service.

## 10. Final acceptance assertions

These are final assertions, not intermediate gates:

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
- T29 remains future push-hint only and is not implemented here.

## 11. Required final validation

Run:
1. focused Desktop-01 tests;
2. full `python -m pytest agent_bridge/tests -q` inside Codex sandbox;
3. accepted Hotfix 01 regression tests;
4. migration tests if schema changes;
5. syntax/import checks;
6. `git diff --check`;
7. changed-path scope check;
8. obvious-secret scan.

Do not require GitHub connectivity from Codex tests.

## 12. Final evidence

Create once, at the end:
- `reports/FOX2-BRIDGE-DESKTOP-01/report.md`
- `reports/FOX2-BRIDGE-DESKTOP-01/evidence_manifest.json`
- `reports/FOX2-BRIDGE-DESKTOP-01/evidence/**`

Report must include:
- base SHA;
- changed paths;
- sandbox-baseline compatibility fix summary;
- focused/full test commands/results;
- D01-D21 verdict;
- BRD T23-T29 mapping;
- restart/recovery proof;
- idle-zero-Agent proof;
- no-inbound-listener proof;
- scope/diff/secret checks;
- NOT_RUN/open gates.

No intermediate report packages.

## 13. STOP conditions

STOP and preserve WIP only for genuine material blockers:
- local branch/HEAD/worktree exactness fails;
- sandbox baseline suite cannot be made PASS with bounded test-harness changes;
- implementation requires out-of-scope root/product files;
- frozen interface conflict appears;
- package installation is required;
- safety/security regression;
- final required tests fail;
- Codex becomes unavailable;
- required evidence cannot be produced.

Do not STOP for routine internal implementation choices.

## 14. Git ownership

Codex MUST NOT:
- `git add`
- `git commit`
- `git push`

Bridge performs final verification, commit, push and remote readback.

If delivery fails after successful implementation, use the accepted delivery-recovery path. Do not rerun Codex merely to repeat Git delivery.

## 15. Final response contract

On success summarize compactly:
- sandbox baseline fix;
- Worker/mailbox implementation;
- durable/restart/single-instance behavior;
- CLI controls;
- focused/full tests;
- D01-D21;
- changed paths;
- report/evidence paths;
- limitations/NOT_RUN.

Then end exactly:

`FOX2_BRIDGE_DESKTOP_01_DELIVERY_READY`

If blocked, end exactly:

`FOX2_BRIDGE_DESKTOP_01_BLOCKED`
