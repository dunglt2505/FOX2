# FOX2 — BRIDGE-DESKTOP-01 Background Worker & Reconciliation — Implementation Plan

**WP:** `FOX2-BRIDGE-DESKTOP-01`  
**Date:** 2026-10-14  
**Status:** `DEV_PLAN_LOCKED / OWNER_AUTHORIZED / EXECUTION_PENDING_HOTFIX_BASE`  
**Owner authorization:** "thực hiện dev luôn ha"  
**Primary implementer after dependency closure:** CODEX via Bridge CLI  
**Execution stop:** `PUSHED_UNREVIEWED`

## 1. Purpose

This plan translates BRD-09 v0.1 Candidate REV2 + Bridge Technical Spec v0.7 Candidate REV2 + the Desktop-01 Source/Design Lock into one bounded implementation sequence.

The Agent must not redesign product behavior. It implements the already-frozen V1 model:

```text
CHAT
 -> immutable GitHub dispatch
 -> local outbound Git control-ref poll
 -> fetch only when remote SHA changes
 -> validate/claim eligible dispatch
 -> existing Agent relay
 -> authorized Git result
 -> CHAT remote review
```

No inbound Internet endpoint is introduced.

## 2. Dependency and base rule

Mandatory predecessor:

`FOX2-BRIDGE-DELIVERY-HOTFIX-01`

Desktop-01 implementation MUST start from the **independently accepted remote SHA** of that hotfix.

Until that SHA exists:

```text
OWNER_AUTHORIZATION = YES
DESIGN = LOCKED
IMPLEMENTATION_PLAN = LOCKED
CODE_EXECUTION = WAIT_DEPENDENCY
```

After hotfix acceptance, CHAT only substitutes the exact accepted SHA into the executable handoff and creates the task branch/dispatch. No additional Owner approval is required if scope and Agent remain unchanged.

## 3. Planned code ownership

Expected writable areas:

- `agent_bridge/src/fox2_agent_bridge/**`
- `agent_bridge/tests/**`
- `agent_bridge/scripts/**` only if needed for local Worker diagnostics/control
- `reports/FOX2-BRIDGE-DESKTOP-01/**` for final evidence only

Expected existing modules to reuse/extend:

- `dispatch_poller.py` — current immutable control-ref/discovery transport
- `ops_runner.py` — current eligible-dispatch selection and one-task execution
- `e2e_runner.py` — exact selected-Agent execution/delivery path
- `ledger.py` — durable dispatch/execution state
- `process_lock.py` — single-instance foundation
- `app.py` — application composition
- `__main__.py` — diagnostic/control CLI

Likely new module:

- `worker.py` or `background_worker.py` — long-running Worker state machine

Agent may choose the exact module name if it preserves clear ownership and tests. It must not move/rewrite unrelated proven Bridge Core code without necessity.

## 4. Implementation phases

### Phase D01 — Worker state/control foundation

Implement a Worker abstraction with deterministic injected dependencies.

Minimum Worker states:

```text
STARTING
RECONCILING
IDLE
POLLING
EXECUTING
PUBLISHING
PAUSED
DEGRADED
STOPPING
STOPPED
```

Required behavior:

- no real sleep in unit tests; inject clock/sleeper/wake primitive;
- start in reconciliation before ordinary polling;
- Pause affects only new claims/launches;
- Stop is graceful;
- Check-now wakes polling immediately;
- one iteration is independently testable without running an infinite loop.

**Gate D01**
- state-transition tests PASS;
- pause/resume/check-now/stop deterministic;
- no Agent adapter invoked by Worker construction or idle state.

### Phase D02 — Lightweight GitHub mailbox signal probe

Implement a remote-ref signal probe using current Git transport or a small transport extension.

Required semantics:

```text
remote_sha = query configured control ref

same SHA:
    no full fetch
    no dispatch scan
    no Agent call

changed SHA:
    fetch exact control ref
    discover/persist delta
    only then evaluate eligible dispatch
```

Prefer the existing Git transport and `ls-remote` behavior; do not create a second network stack.

Persist enough distinction between:
- last remote SHA observed;
- last control SHA safely fetched/processed.

**Gate D02**
- repeated unchanged SHA => zero fetch;
- changed SHA => one fetch/discovery;
- remote SHA is treated as signal only, not authority;
- no inbound listener/server/socket binding exists.

### Phase D03 — Durable polling state + backoff

Extend ledger only as necessary.

Persist minimum:
- Worker pause state;
- last observed control SHA;
- last safely processed control SHA/cursor if not already represented sufficiently;
- last poll timestamp/state;
- backoff attempt/state;
- last transport error category.

Candidate timing policy:

```text
healthy = 30s
offline/error = 30s -> 60s -> 120s -> 300s max
successful Git contact = reset to healthy
```

Tests use fake time; no test waits real wall-clock intervals.

If schema migration is needed:
- bump schema once;
- migration must preserve existing dispatch/execution rows;
- future-schema refusal behavior remains safe.

**Gate D03**
- backoff sequence exact and capped;
- success resets backoff;
- restart reloads persisted state;
- migration regression PASS.

### Phase D04 — Poll-to-execution integration

Connect Worker polling to current `BridgeOps`/eligible-dispatch path without duplicating governance.

Rules:
- at most one selected task per execution slot;
- unchanged control SHA never invokes Agent;
- changed SHA with no eligible `auto_execute=true` dispatch invokes no Agent;
- eligible dispatch calls existing exact execution route;
- CODEX-only current `run-next` selection remains unchanged unless separately authorized;
- no silent Agent substitution.

**Gate D04**
- eligible task invoked exactly once;
- ineligible task zero invocation;
- replayed/known dispatch skipped;
- existing `run-next` behavior regression PASS.

### Phase D05 — Restart and reconciliation

On Worker startup:

1. open/migrate ledger;
2. acquire process/single-instance lock;
3. inspect non-terminal/recovery states;
4. reuse accepted delivery-hotfix semantics;
5. do not blindly rerun a previously successful Agent execution;
6. then enter mailbox polling.

Required classifications:

- pre-Agent stale claim: recover only when existing semantics prove safe;
- Agent may have run / delivery uncertain: preserve WIP and require/reuse delivery recovery;
- already pushed/terminal: never replay.

Desktop-01 MUST consume the hotfix's recovery semantics rather than creating a second competing recovery path.

**Gate D05**
- completed dispatch survives restart without rerun;
- delivery-recovery-required survives restart without Agent relaunch;
- task published while Worker stopped is discovered after restart;
- fault-injection around polling/cursor persistence does not lose a valid dispatch.

### Phase D06 — Single Worker instance

Reuse `process_lock.py` or equivalent existing lock.

Rules:
- one active Worker/profile;
- second Worker cannot become a competing poller/writer;
- diagnostic status may still inspect persisted state safely if architecture permits;
- no SYSTEM/service requirement.

**Gate D06**
- simultaneous second Worker attempt rejected/attached safely;
- lock cleanup after graceful stop;
- stale-lock behavior safe and tested.

### Phase D07 — CLI operational controls

Add only the CLI needed to operate/test Worker before Tray exists.

Target commands/behavior may be:

```text
fox2-bridge watch
fox2-bridge pause
fox2-bridge resume
fox2-bridge check-now
fox2-bridge status
```

Equivalent names are acceptable if clear and tested.

Do not implement Tray, Task Scheduler or installer here.

Controls must be local-user operations and must not grant new task authority.

**Gate D07**
- watch starts Worker;
- pause/resume/check-now observable;
- status exposes safe Worker state;
- existing CLI commands remain compatible.

### Phase D08 — Full regression/evidence

Run:
- all new Desktop-01 focused tests;
- full existing `agent_bridge/tests`;
- delivery-hotfix regressions;
- syntax/import checks;
- Git diff checks;
- allowed-path check;
- obvious-secret scan.

Produce final task evidence only after code is stable.

**Gate D08**
- all required tests PASS;
- no expected test left silently unrun;
- any NOT_RUN explicitly listed;
- no provider/broker/LIVE activity.

## 5. Required acceptance matrix

| ID | Required proof |
|---|---|
| D01 | Worker state machine deterministic |
| D02 | unchanged remote SHA => zero fetch |
| D03 | unchanged remote SHA => zero Agent invocation |
| D04 | changed SHA => exact fetch/discovery |
| D05 | changed SHA/no eligible task => zero Agent invocation |
| D06 | eligible task executes exactly once |
| D07 | healthy timing policy deterministic |
| D08 | backoff 30/60/120/300 capped |
| D09 | successful contact resets backoff |
| D10 | Check-now wakes immediately |
| D11 | Pause blocks new claim/launch |
| D12 | Resume does not replay terminal dispatch |
| D13 | pause/cursor state survives restart as designed |
| D14 | offline-published task discovered after restart |
| D15 | pre-Agent interruption reconciled safely |
| D16 | post-Agent delivery recovery never relaunches Agent |
| D17 | one Worker/profile enforced |
| D18 | poll/cursor crash injection loses no valid dispatch |
| D19 | no inbound Internet listener/server introduced |
| D20 | full existing Bridge suite PASS |
| D21 | no main/merge/Production/provider/broker/LIVE authority |

BRD-09 mapping:
- T23 -> D02/D04/D19
- T24 -> D02/D03/D10
- T25 -> D03
- T26 -> D08/D09
- T27 -> D19
- T28 -> D14
- T29 -> future push hint remains out of implementation scope; architecture must not preclude validation boundary.

## 6. Required final evidence package

Paths:

- `reports/FOX2-BRIDGE-DESKTOP-01/report.md`
- `reports/FOX2-BRIDGE-DESKTOP-01/evidence_manifest.json`
- `reports/FOX2-BRIDGE-DESKTOP-01/evidence/**`

Report must contain:

- exact source/base SHA;
- exact changed files;
- Agent/model/thinking/quota truthfully reported or NOT_EXPOSED;
- Python/Git/runtime versions relevant to execution;
- all test commands + exit codes;
- acceptance D01-D21 status;
- BRD T23-T29 mapping;
- restart/reconciliation proof;
- zero-Agent-call idle proof;
- zero inbound-listener proof;
- changed-path allowlist result;
- secret scan;
- final local commit;
- pushed remote SHA;
- limitations/NOT_RUN.

Evidence manifest must hash exact evidence files and avoid self-hash recursion.

## 7. Agent final Result Contract

The coding Agent must end with:

```text
FOX2 BRIDGE-DESKTOP-01 DELIVERY RESULT

EXECUTION_STATE:
  PUSHED_UNREVIEWED
  | BLOCKED_SOURCE
  | BLOCKED_WORKTREE
  | BLOCKED_WRITER
  | BLOCKED_INTERFACE_CONFLICT
  | BLOCKED_TEST
  | BLOCKED_SCOPE
  | BLOCKED_PUSH
  | BLOCKED_OTHER

BASE_SHA:
WORKTREE:
BRANCH:
INITIAL_REMOTE_HEAD:
FINAL_LOCAL_HEAD:
REMOTE_HEAD:

AGENT:
MODEL:
THINKING:
QUOTA:

CHANGED_CODE_PATHS:
REPORT_PATHS:

FOCUSED_TESTS:
FULL_BRIDGE_REGRESSION:
DELIVERY_HOTFIX_REGRESSION:
MIGRATION_TESTS:
RESTART_RECONCILIATION:
IDLE_ZERO_AGENT_CALL:
MAILBOX_FETCH_ON_CHANGE:
BACKOFF_POLICY:
PAUSE_RESUME:
CHECK_NOW:
SINGLE_INSTANCE:
NO_INBOUND_LISTENER:
SECRET_SCAN:
DIFF_CHECK:

ACCEPTANCE_D01_D21:
BRD_T23_T29:
NOT_RUN:
COMMIT:
PUSH:
RESULT_REPORT:
EVIDENCE_MANIFEST:
OPEN_GATES:
STOP_REASON:
```

Final success marker:

`FOX2_BRIDGE_DESKTOP_01_DELIVERY_READY`

## 8. Git delivery ownership

Preferred after the delivery hotfix:

- CODEX edits/tests only;
- Bridge verifies scope/acceptance and owns commit/push;
- if post-Agent delivery fails, use delivery-only recovery; never rerun the Agent merely to repeat Git delivery.

If the accepted hotfix changes this contract materially, CHAT performs a bounded delta rebind before dispatch.

## 9. Exact activation checklist after hotfix

CHAT performs only:

1. verify hotfix remote result and acceptance;
2. set `DESKTOP_01_BASE_SHA=<accepted hotfix SHA>`;
3. verify no active Bridge writer;
4. create `work/FOX2-BRIDGE-DESKTOP-01-worker-codex` from that exact SHA;
5. verify worktree target is safe;
6. publish executable prompt derived from this plan/source lock;
7. publish immutable dispatch with `auto_execute=true`;
8. set:
   - `CODE_ALLOWED=YES_FOR_BRIDGE_DESKTOP_01_ONLY`
   - `GIT_CODE_PUSH=YES_OWN_TASK_BRANCH_ONLY`
   - `GIT_REPORT_WRITE=YES_TASK_RESULT_ONLY`
   - `GIT_REPORT_PUSH=YES_TASK_BRANCH_ONLY`
   - `MERGE=NO`
   - `PRODUCTION=NO`
   - `BROKER_WRITE=NO`
   - `LIVE=NO`
9. execute through Bridge/Codex CLI;
10. CHAT independently reviews immutable pushed result.

## 10. STOP conditions

STOP without widening scope when:
- accepted hotfix SHA cannot be verified;
- Bridge writer/worktree collision exists;
- executable handoff source differs materially from this plan;
- hotfix recovery semantics are incompatible and need architecture review;
- out-of-scope root/project files are required;
- package install is required but not explicitly approved;
- required regression fails and cannot be resolved in scope;
- secret/credential exposure occurs;
- inbound listener becomes required;
- Git delivery/push/readback fails.

## 11. Readiness disposition

```text
BRD_09_REV2 = READY
TECH_V0_7_REV2 = READY
DESKTOP_01_SOURCE_LOCK = READY
DESKTOP_01_IMPLEMENTATION_PLAN = READY
OWNER_AUTHORIZATION = YES
HOTFIX_DEPENDENCY = OPEN
EXACT_DESKTOP_BASE_SHA = PENDING_HOTFIX_ACCEPTANCE
EXECUTABLE_PROMPT = WAIT_EXACT_BASE
IMMUTABLE_DISPATCH = WAIT_EXACT_BASE
CODE_EXECUTION = WAIT_HOTFIX_ONLY
```

The only intentionally missing execution artifacts are the exact-base executable prompt and dispatch. Creating them before the hotfix is accepted would violate source binding.
