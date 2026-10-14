# FOX2 — BRIDGE-DESKTOP-01 Background Worker & Reconciliation — Source / Design Lock

**WP:** `FOX2-BRIDGE-DESKTOP-01`  
**Date:** 2026-10-14  
**Status:** `AUTHORIZED_PENDING_DEPENDENCY / CODE_ALLOWED=NO_UNTIL_HOTFIX_ACCEPTED`  
**Owner decision:** "thực hiện dev luôn ha"  
**Project:** FOX2  
**Execution target:** CODEX via Bridge CLI after delivery hotfix acceptance  
**No new Owner confirmation required** if the dependency and scope below remain unchanged.

## 1. Routing result

- **R0 — TASK/EVIDENCE:** PASS. Bridge Relay MVP already proven; BRD-09/Tech v0.7 REV2 are current Candidate sources for this WP. Do not rebuild Relay MVP.
- **R1 — ACTUAL STAGE:** Desktop productization implementation, WP 01.
- **R2 — RISK/AUTHORITY:** Offline/local Bridge only. No merge/Production/provider/broker/LIVE. Restart/reconciliation and process ownership are safety-critical.
- **R3 — AGENT:** CODEX CLI is proven usable. Exact current model/thinking/quota may be NOT_EXPOSED. Copilot eligibility is not freshly proven and prior quota pressure exists.
- **R4 — ROUTING:** CODEX preferred for worker state/restart/concurrency implementation; CHAT owns source/spec/review; WORK not needed pre-code; COPILOT not selected.
- **R5 — WRITER:** BLOCKED until `FOX2-BRIDGE-DELIVERY-HOTFIX-01` closes because both WPs write `agent_bridge/**`.
- **R6 — HANDOFF:** This document freezes scope now. Executable dispatch is created only after the hotfix remote result is accepted and exact base SHA is pinned.
- **R7 — DECISION:** Owner authorization is recorded. Transition automatically to DEV when dependency closes and race-sensitive local writer checks pass.

## 2. Normative source binding

Governance:
- FOX2 Policy V1.8.5
- Routing Index V1.2.6
- Bridge Technical Spec v0.6 released predecessor

Desktop product source:
- BRD-09 `v0.1 Candidate REV2`
  - path: `docs/brd_mirror/FOX2-BRD-09_v0.1_CANDIDATE.md`
  - blob: `c6f3cafd7c9bdba97fd413c6a9a891bde82d0699`
- Bridge Technical Spec `v0.7 Candidate REV2`
  - path: `docs/architecture/FOX2_LOCAL_AGENT_BRIDGE_TECHNICAL_SPEC_v0.7_CANDIDATE.md`
  - blob: `dc4b28e12a7824771c22733682c8409e67127701`
- Candidate receipt
  - blob: `104079980557da04bc177f38263789004d7a6125`
  - signaling: `GITHUB_DURABLE_MAILBOX_LOCAL_OUTBOUND_PULL`

Operational predecessor:
- Bridge Relay MVP source before delivery hotfix:
  `398bebf9c48e7694c69c3416a5780715f025e7b5`

Mandatory dependency:
- `FOX2-BRIDGE-DELIVERY-HOTFIX-01`
- Desktop-01 base MUST be the independently accepted remote result SHA of that hotfix.
- Do not base Desktop-01 on `398bebf9...` after the hotfix completes.
- Do not cherry-pick around an unreviewed hotfix result merely to start early.

## 3. Product objective

Turn the command-driven Bridge Core into an always-running Windows background Worker that receives CHAT task signals indirectly through the configured GitHub control ref.

V1 signal architecture:

```text
CHAT
 -> immutable dispatch on GitHub control ref
 -> local Worker lightweight outbound remote-ref poll
 -> fetch only on SHA change
 -> validate immutable dispatch
 -> claim only eligible auto_execute task
 -> existing Codex/Copilot relay
 -> authorized Git result
 -> CHAT remote review
```

No public/static IP, inbound port, ngrok, Tailscale or cloud relay is required.

## 4. Exact WP scope

Desktop-01 owns:

1. **Background Worker loop**
   - long-running per-user Worker process;
   - healthy idle polling;
   - graceful stop;
   - responsive local control state.

2. **GitHub mailbox signal probe**
   - lightweight remote-ref SHA query;
   - durable last-seen / last-processed control SHA;
   - no full fetch when SHA unchanged;
   - no Agent invocation when no eligible new dispatch exists.

3. **Polling policy**
   - candidate healthy interval: 30 seconds;
   - immediate `check-now` / equivalent internal trigger;
   - offline/error backoff: 30 -> 60 -> 120 -> 300 seconds max;
   - successful Git contact resets healthy cadence.

4. **Pause/Resume**
   - Pause prevents claiming/launching new tasks;
   - currently running Agent remains supervised by default;
   - Resume never replays a terminal dispatch.

5. **Restart/reconciliation**
   - startup inspects durable non-terminal execution state;
   - completed dispatch remains terminal;
   - uncertain post-Agent/delivery state must be reconciled, not blindly rerun;
   - integrate/reuse the delivery-recovery semantics from the accepted hotfix.

6. **Single instance / writer ownership**
   - one Worker per profile/user;
   - duplicate Worker launch must not create competing pollers or task writers.

7. **CLI control for Desktop-01**
   - expose Worker/watch mode and bounded local controls necessary to test start/stop/pause/resume/check-now/status;
   - no Tray/UI in this WP.

8. **Durable worker state**
   - persist pause state and the minimum poll/reconciliation metadata necessary for restart correctness;
   - schema migration if needed, with migration tests.

## 5. Out of scope

Not in Desktop-01:
- System Tray UI;
- Start with Windows / Task Scheduler registration;
- installer/packaging;
- first-run GUI wizard;
- cloud relay/webhook implementation;
- VS Code session injection;
- generic multi-project scheduling beyond avoiding FOX2 hardcoding where practical;
- semantic code review/auto-rework;
- auto-merge/deploy;
- provider/broker/LIVE;
- product backend/frontend.

These belong to later Desktop WPs.

## 6. V1 signaling invariants

### 6.1 Outbound-only

Normal Worker networking is outbound Git/HTTPS to the configured repository.

No inbound Internet listener.

### 6.2 Remote SHA is only a hint

A control-ref SHA change means "Git content changed", not "execute this task".

Every candidate still requires immutable dispatch validation, exact project/repo/worktree/branch/base/source binding, permission checks, replay protection and `auto_execute=true`.

### 6.3 Idle polling spends zero Agent credits

Unchanged control-ref polls and ordinary health/status checks must not call Codex/Copilot prompts.

### 6.4 Fetch on change

When remote control SHA equals the durable last-seen SHA:
- do not full-fetch control content;
- do not scan unchanged dispatch content;
- do not call Agent.

When it differs:
- fetch exact control ref;
- discover/record delta safely;
- process only eligible tasks.

### 6.5 Offline/sleep durability

If local machine is offline/asleep, dispatch remains on GitHub.

After Worker restart/wake:
- recover ledger;
- reconcile execution;
- probe control ref;
- discover pending eligible dispatch;
- execute at most once.

## 7. Writer and Git plan

Future task branch:
`work/FOX2-BRIDGE-DESKTOP-01-worker-codex`

Preferred local worktree:
`C:\Projects\FOX2-worktrees\FOX2-BRIDGE-DESKTOP-01-CODEX`

Writable code:
- `agent_bridge/src/fox2_agent_bridge/**`
- `agent_bridge/tests/**`
- `agent_bridge/scripts/**` only if needed for Worker diagnostic/control launch

Allowed task result:
- `reports/FOX2-BRIDGE-DESKTOP-01/report.md`
- `reports/FOX2-BRIDGE-DESKTOP-01/evidence_manifest.json`
- `reports/FOX2-BRIDGE-DESKTOP-01/evidence/**`

Everything else read-only.

The final executable dispatch must use the accepted delivery-hotfix SHA as `base_sha`.

## 8. Required implementation behavior

### Worker lifecycle

At minimum support:

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

Existing dispatch execution states remain distinct.

### Poll algorithm

Conceptually:

```text
while not stopping:
    if paused:
        wait for resume/check/status/stop
        continue

    remote_sha = lightweight_query(control_ref)

    if transport_error:
        persist degraded/backoff state
        wait bounded backoff
        continue

    reset backoff

    if remote_sha == durable_last_seen_sha:
        wait healthy interval
        continue

    fetch exact control ref
    discover/validate/persist candidates
    update safe cursor
    execute at most the next eligible dispatch
```

Do not hold long SQLite write transactions while performing Git or Agent operations.

### Check-now

A local control action may wake the Worker immediately to perform one signal probe. It does not alter authorization or bypass Pause unless the command is explicitly defined to perform a poll-only check.

## 9. Required tests

At minimum:

1. unchanged remote SHA repeatedly => zero full fetch;
2. unchanged remote SHA => zero Agent adapter invocation;
3. changed remote SHA => fetch once and discover expected immutable dispatch;
4. changed SHA with no eligible dispatch => no Agent invocation;
5. eligible dispatch => existing execution route called exactly once;
6. healthy cadence defaults/config bounds;
7. transport failure backoff sequence 30/60/120/300 max;
8. successful contact resets backoff;
9. Check-now wakes without waiting full cadence;
10. Pause blocks new claim/launch;
11. Resume does not replay completed dispatch;
12. worker restart preserves/reloads pause/cursor state as specified;
13. task published while Worker stopped is discovered after restart;
14. non-terminal pre-Agent claim recovery is safe;
15. post-Agent/delivery-recovery-required state is not auto-rerun;
16. single-instance contention prevents second Worker;
17. crash/restart around poll cursor update does not lose a valid dispatch;
18. dynamic IP/NAT has no inbound dependency in architecture/import/runtime tests;
19. no Internet listener/socket server introduced;
20. full existing `agent_bridge/tests` regression suite passes;
21. no main/merge/Production/provider/broker/LIVE authority introduced.

Use deterministic fake transport/clock/sleeper/process fixtures for timing and failure tests. Do not make tests wait real 30/60/120/300 seconds.

## 10. Acceptance mapping

Desktop-specific scenarios:
- BRD-09 T23 — outbound mailbox works behind NAT/dynamic IP;
- T24 — unchanged SHA avoids full fetch/Agent; Check now immediate;
- T25 — idle Worker consumes zero Agent prompts;
- T26 — bounded backoff/recovery;
- T27 — IP change irrelevant to correctness;
- T28 — offline/asleep publication recovered after startup;
- relevant existing T04/T07/T08/T12/T13/T16 — pause/restart/error/single-instance semantics.

All remain NOT_RUN until runtime evidence exists.

## 11. STOP conditions

STOP and preserve WIP if:
- delivery hotfix has not been remotely accepted;
- exact hotfix result SHA/base cannot be pinned;
- Bridge code writer conflict exists;
- target worktree has unreviewed WIP;
- required change expands outside Bridge code/test/script/report scope;
- current hotfix API/state semantics make Desktop-01 design materially incompatible;
- required tests cannot pass without package install or out-of-scope mutation;
- Agent actually unavailable/quota exhausted;
- secret/path/authority safety regression;
- push/readback fails.

## 12. Activation state

Current:

```text
OWNER_AUTHORIZATION=YES
SOURCE_DESIGN=LOCKED_REV2
DEPENDENCY_HOTFIX=OPEN
CODE_ALLOWED=NO_UNTIL_DEPENDENCY_ACCEPTED
DISPATCH=NOT_YET_CREATED
MERGE=NO
PRODUCTION=NO
BROKER_WRITE=NO
LIVE=NO
```

Once the hotfix result is independently accepted:
1. pin its exact remote SHA;
2. verify no Bridge writer collision;
3. create Desktop-01 task branch from that SHA;
4. create executable prompt + immutable dispatch;
5. set `CODE_ALLOWED=YES_FOR_BRIDGE_DESKTOP_01_ONLY`;
6. execute through Bridge/Codex CLI;
7. stop at `PUSHED_UNREVIEWED`;
8. CHAT reviews remote evidence.

No additional Owner approval is required if nothing material changes.
