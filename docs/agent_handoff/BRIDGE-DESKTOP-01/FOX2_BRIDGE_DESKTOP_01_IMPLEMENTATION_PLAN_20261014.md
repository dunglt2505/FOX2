# FOX2 — BRIDGE-DESKTOP-01 Background Worker & Reconciliation — Simplified Implementation Plan

**WP:** `FOX2-BRIDGE-DESKTOP-01`  
**Date:** 2026-10-14  
**Status:** `DEV_PLAN_SIMPLIFIED / OWNER_AUTHORIZED / EXECUTION_PENDING_HOTFIX_BASE`  
**Owner authorization:** "thực hiện dev luôn ha"  
**Primary implementer after dependency closure:** CODEX via Bridge CLI  
**Execution stop:** `PUSHED_UNREVIEWED`

## 1. Operating rule

This is **one whole WP**, not eight sub-WPs.

CODEX receives one prompt, owns one branch/worktree and continues from start to final delivery unless a genuine STOP condition occurs.

Internal implementation order is only:

```text
1. Worker loop + GitHub mailbox poll
2. Durable state + pause/backoff
3. Restart/recovery + single instance
4. CLI integration + full regression
```

There is:
- no Owner review between these blocks;
- no new CHAT handoff between these blocks;
- no separate commit/push per block;
- no WORK audit per block;
- no new Agent assignment per block.

The previous D01-D21 items remain **final acceptance assertions only**, not execution gates.

## 2. Dependency/base

Mandatory predecessor:

`FOX2-BRIDGE-DELIVERY-HOTFIX-01`

Desktop-01 starts from the **independently accepted remote SHA** of that hotfix.

Until that SHA exists:

```text
OWNER_AUTHORIZATION = YES
DESIGN = LOCKED
PLAN = READY
CODE_EXECUTION = WAIT_HOTFIX_ONLY
```

After hotfix acceptance CHAT only:
1. binds exact hotfix SHA;
2. verifies no writer/worktree collision;
3. creates Desktop-01 branch;
4. publishes executable prompt + immutable dispatch;
5. starts the one whole WP.

No additional Owner approval is required if scope/Agent stay unchanged.

## 3. Exact product behavior to implement

V1 remains deliberately small:

```text
CHAT
 -> immutable GitHub control-ref dispatch
 -> local Worker polls remote ref
 -> if SHA unchanged: sleep
 -> if SHA changed: fetch + discover
 -> if eligible auto_execute task: existing Bridge execution route
 -> Git result
 -> CHAT review
```

Normal V1 requires:
- outbound Git/HTTPS only;
- no static/public IP;
- no inbound port/server;
- no ngrok/Tailscale/cloud relay;
- no Agent call while idle.

## 4. Code ownership

Writable:

- `agent_bridge/src/fox2_agent_bridge/**`
- `agent_bridge/tests/**`
- `agent_bridge/scripts/**` only if required for Worker diagnostic/control
- `reports/FOX2-BRIDGE-DESKTOP-01/**` only for final evidence

Reuse existing modules first:

- `dispatch_poller.py`
- `ops_runner.py`
- `e2e_runner.py`
- `ledger.py`
- `process_lock.py`
- `app.py`
- `__main__.py`

A small `worker.py` / `background_worker.py` may be added if it keeps the loop isolated.

Do not rewrite proven Bridge Core merely to create a new framework.

## 5. Four implementation blocks

### Block 1 — Worker + mailbox signal

Implement the long-running Worker and lightweight remote-ref probe.

Required:
- one iteration testable independently;
- healthy poll target ~30s;
- unchanged control SHA => no full fetch, no dispatch scan, no Agent call;
- changed SHA => fetch/discover using existing Git transport;
- `check-now` can wake the poll immediately;
- no inbound listener.

### Block 2 — Durable state + pause/backoff

Persist only what restart correctness needs:
- pause state;
- last observed/processed control SHA or equivalent existing cursor;
- poll/backoff state if required.

Required:
- offline/error backoff `30 -> 60 -> 120 -> 300s max`;
- successful Git contact resets healthy cadence;
- Pause blocks new task launches;
- Resume does not replay terminal dispatches;
- tests use fake time, never real multi-minute waits.

Use existing ledger structure where sufficient. Schema bump only if actually necessary.

### Block 3 — Restart/recovery + single instance

Reuse the accepted delivery-hotfix behavior.

Required:
- completed task never reruns after restart;
- post-Agent delivery failure remains delivery recovery, not Agent rerun;
- task published while Worker was stopped is found after restart;
- one Worker/profile only;
- second Worker cannot become competing poller/writer;
- no second recovery framework.

### Block 4 — CLI integration + final tests

Expose only the minimum local controls needed before Tray:

- Worker/watch start;
- Pause;
- Resume;
- Check now;
- Status;
- graceful stop if needed.

Exact command names may follow the existing CLI style.

Then run one final validation cycle:
- focused Desktop-01 tests;
- full `agent_bridge/tests`;
- delivery-hotfix regressions;
- migration tests if schema changed;
- scope/diff/secret checks.

Only after this final cycle create the evidence package and deliver once.

## 6. Final acceptance checklist

The following are assertions checked at final delivery, **not separate phase gates**:

| ID | Final proof |
|---|---|
| D01 | Worker state/control deterministic |
| D02 | unchanged remote SHA => zero full fetch |
| D03 | unchanged remote SHA => zero Agent call |
| D04 | changed SHA => correct fetch/discovery |
| D05 | changed SHA with no eligible task => zero Agent call |
| D06 | eligible task executes once |
| D07 | healthy cadence deterministic |
| D08 | backoff 30/60/120/300 capped |
| D09 | success resets backoff |
| D10 | Check-now wakes promptly |
| D11 | Pause blocks new launch |
| D12 | Resume does not replay terminal dispatch |
| D13 | required durable state survives restart |
| D14 | offline-published task discovered after restart |
| D15 | pre-Agent interruption handled safely |
| D16 | delivery-recovery state never relaunches Agent |
| D17 | one Worker/profile enforced |
| D18 | crash around cursor handling loses no valid dispatch |
| D19 | no inbound Internet listener/server |
| D20 | full existing Bridge suite PASS |
| D21 | no main/merge/Production/provider/broker/LIVE authority |

BRD mapping remains:
- T23 -> D02/D04/D19
- T24 -> D02/D03/D10
- T25 -> D03
- T26 -> D08/D09
- T27 -> D19
- T28 -> D14
- T29 -> future push hint remains out of this WP

## 7. Final evidence only

Produce once, at the end:

- `reports/FOX2-BRIDGE-DESKTOP-01/report.md`
- `reports/FOX2-BRIDGE-DESKTOP-01/evidence_manifest.json`
- `reports/FOX2-BRIDGE-DESKTOP-01/evidence/**`

No intermediate report package per block.

Report only needs:
- exact base/result SHA;
- changed paths;
- test commands/results;
- D01-D21 final verdict;
- BRD T23-T29 mapping;
- restart/recovery proof;
- idle-zero-Agent proof;
- no-inbound-listener proof;
- scope/secret/diff checks;
- limitations/NOT_RUN.

## 8. Final Agent Result Contract

CODEX returns one result:

```text
FOX2 BRIDGE-DESKTOP-01 DELIVERY RESULT

EXECUTION_STATE:
BASE_SHA:
BRANCH:
WORKTREE:
FINAL_LOCAL_HEAD:
REMOTE_HEAD:

CHANGED_PATHS:
FOCUSED_TESTS:
FULL_BRIDGE_REGRESSION:
DELIVERY_HOTFIX_REGRESSION:
MIGRATION_TESTS:
D01_D21:
BRD_T23_T29:
NOT_RUN:
OPEN_GATES:
STOP_REASON:

FOX2_BRIDGE_DESKTOP_01_DELIVERY_READY
```

Do not require verbose reporting when a compact exact result is sufficient.

## 9. STOP conditions

Only genuine material STOPs:

- hotfix accepted SHA unavailable/mismatched;
- writer/worktree collision;
- frozen source/interface conflict;
- required out-of-scope file change;
- required package install not authorized;
- safety/security regression;
- required final tests fail;
- Agent actually unavailable;
- push/readback failure.

Do **not** stop for:
- internal block completion;
- routine implementation choices inside allowed scope;
- NOT_EXPOSED model/quota fields when Agent is actually running;
- need for another governance/review checkpoint.

## 10. Activation

After hotfix acceptance:

```text
CHAT bind exact SHA
 -> create one Desktop-01 branch/worktree
 -> publish one prompt + one dispatch
 -> CODEX implements all four blocks continuously
 -> one final test/evidence cycle
 -> Bridge commit/push
 -> CHAT remote review
```

No intermediate CHAT/WORK/CODEX handoff.

Current:

```text
BRD_09_REV2 = READY
TECH_V0_7_REV2 = READY
SOURCE_LOCK = READY
SIMPLIFIED_IMPLEMENTATION_PLAN = READY
OWNER_AUTHORIZATION = YES
HOTFIX_DEPENDENCY = OPEN
EXECUTABLE_PROMPT = WAIT_EXACT_BASE
DISPATCH = WAIT_EXACT_BASE
CODE_EXECUTION = WAIT_HOTFIX_ONLY
```
