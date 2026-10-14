# FOX2 — CODEX EXECUTION HANDOFF — BRIDGE-DESKTOP-01+02

**Date:** 2026-10-14  
**Combined WP:** `BRIDGE-DESKTOP-01-02`  
**Status:** `EXECUTABLE / DEV_AUTHORIZED_TASK_BOUND / STOP_AT_PUSHED_UNREVIEWED`  
**Owner direction:** combine `BRIDGE-DESKTOP-01` and `BRIDGE-DESKTOP-02` and execute now.

## 0. Role · Engine · Thinking · Scope

- **Role:** CODEX implementation Agent through FOX2 Bridge
- **Engine/Model:** current configured Codex CLI model; target policy for this task is GPT-6.1 Sol if available
- **Thinking:** High preferred because this task contains restart/replay recovery, concurrency/singleton semantics, local control boundaries and Windows background behavior. If exact effort is not exposed, report `NOT_EXPOSED`; do not fabricate.
- **Scope:** one whole combined Bridge Desktop-01+02 WP
- **Stop boundary:** `PUSHED_UNREVIEWED`

No additional Owner confirmation is required for implementation/test checkpoints that remain inside this immutable handoff.

## 1. Base and immutable source

Repository:
`dunglt2505/FOX2`

Task branch:
`work/FOX2-BRIDGE-DESKTOP-01-02-codex`

Operational Bridge base:
`398bebf9c48e7694c69c3416a5780715f025e7b5`

Normative combined source/design lock:
- commit: `1ca353efc2ffc2f6d7eaacccac11d48897ba09ac`
- path: `docs/agent_handoff/BRIDGE/FOX2_BRIDGE_DESKTOP_01_02_SOURCE_DESIGN_LOCK_20261014.md`
- blob: `6683781beb03a9c7deea9260c2d6553798e298ad`

Read the source/design lock completely before editing.

Bound Candidate product source is immutable by explicit Owner decision:
- BRD-09 v0.1 Candidate @ `6062a3b3a9b1580181b0bfa4501cf04de5c2ddaf`
- Bridge Tech Spec v0.7 Candidate @ same commit
- Candidate receipt @ same commit

Do not modify those source documents.

## 2. Exact Agent write scope

Allowed:
- `agent_bridge/**`
- `reports/BRIDGE-DESKTOP-01-02/**`

Do not modify:
- application backend/frontend;
- BRD/Technical Candidate source;
- governance;
- provider/broker/LIVE code;
- unrelated docs;
- `.github/**`.

The two CHAT-authored handoff files already present on the task branch are immutable source. Do not edit them.

## 3. Required implementation

Implement the combined source lock fully enough to make the normal Owner experience:

```text
Owner -> CHAT -> immutable dispatch
             -> background AgentBridge worker
             -> exact Copilot/Codex CLI
             -> verify/commit/push
             -> CHAT review
```

No recurring PowerShell step should be needed after initial bootstrap.

### 3A. Background Worker

Add a long-running per-user worker around the existing Operational MVP:
- continuous poll loop;
- `poll_interval_seconds` healthy cadence;
- bounded offline/error backoff 30/60/120/300;
- pause/resume/check-now;
- graceful exit;
- one worker singleton/profile;
- worker state persisted;
- worker heartbeat/state visible to control/status;
- polling with no eligible dispatch invokes no Agent.

Do not busy-loop.

### 3B. Recovery/Reconciliation

Upgrade stale execution handling so restart does not blindly mark/replay uncertain work.

Persist execution stage sufficiently to distinguish:
- claimed but Agent not started;
- Agent started/running;
- Agent exited;
- verifying/publishing;
- terminal result.

At startup:
- reconcile non-terminal rows;
- inspect exact remote target branch/result evidence using current dispatch identity;
- recover proven published result to `PUSHED_UNREVIEWED`;
- never blindly launch a second Agent after uncertain RUNNING/AGENT_EXITED/PUBLISHING;
- use `NEEDS_RECONCILIATION` / terminal interrupted state where proof is insufficient;
- only safely reconsider pre-Agent stale claim when non-execution is proven.

Do not infer replay permission from elapsed time.

### 3C. Exact dual-Agent routing

Generalize normal automatic dispatch selection from CODEX-only to exact authorized `CODEX | COPILOT`.

No silent substitution.

Dispatch eligibility still requires explicit `runtime_contract.auto_execute=true`.

Bridge should understand a bounded Agent model policy object while remaining backward compatible with existing dispatches.

#### Copilot CLI

Support:
- `model_policy=NATIVE_AUTO` with `--model auto`;
- optional `auto_tier=efficiency|balance|intelligence`;
- default desired policy `auto/balance`;
- `model_policy=PINNED` with exact `--model`;
- `--no-ask-user`;
- `--output-format json` if installed CLI supports it;
- optional explicit `max_ai_credits` only when supported;
- existing bounded tool permissions; never `--allow-all` / `--yolo`.

Do not mutate the Owner's global Copilot settings. For auto tier, use Bridge-owned isolated runtime config only if it can be feature-detected and tested safely; otherwise use native `--model auto` and report tier not enforced. Never break authentication by assuming config-home behavior.

Capture actual selected model only if CLI exposes it.

#### Codex CLI

Support dispatch fields:
- model policy/current config;
- exact model where supported;
- reasoning effort low/medium/high where supported.

Preserve:
- `workspace-write`;
- approval `never`;
- Windows unelevated sandbox fallback where current installed CLI requires it;
- MSI/WiX PowerShell preference;
- Bridge-owned Git commit/push.

No dangerous/full-access elevation.

### 3D. Local Control Plane

Add fixed local control commands that can work while Worker owns the singleton:
- `worker-status`
- `pause`
- `resume`
- `check-now`
- `request-exit`
- `startup-status`
- `startup-enable`
- `startup-disable`

Control plane must not accept arbitrary shell/prompt text.

Avoid a TCP listener.

Use durable runtime DB/control state under the current user's Bridge root so control commands remain local-user scoped. Do not make normal read/control commands contend on the worker singleton lock.

### 3E. System Tray

Implement internal FOX2 tray host without adding a new third-party runtime dependency.

Preferred:
- PowerShell 7 + .NET `System.Windows.Forms.NotifyIcon`;
- hidden/no visible console in normal use;
- text status for Running/Paused/Degraded/Error;
- current task / last result summary;
- fixed menu actions:
  - Pause new tasks / Resume
  - Check now
  - Open logs
  - Start with Windows toggle
  - Exit after current / Request exit

Tray may invoke only fixed Bridge control commands.

No arbitrary command input, secrets or authority creation.

### 3F. Start with Windows

Implement per-user idempotent enable/disable using Windows Task Scheduler or equivalent current-user startup mechanism.

Requirements:
- at current-user logon;
- never SYSTEM by default;
- no plaintext password;
- hidden background worker/tray startup;
- disable removes only AgentBridge startup registration;
- project repo/worktrees untouched;
- test implementation with command/mock/dry-run evidence rather than modifying the Owner's real Task Scheduler during unit tests.

Desktop-03 packaging/installer remains outside scope.

## 4. Tests / evidence

Add deterministic tests under existing `agent_bridge/tests/**`.

Minimum required:
- worker idle poll/no Agent spend;
- pause/resume/check-now;
- single-worker lock;
- bounded backoff/reset;
- restart at pre-Agent, RUNNING, AGENT_EXITED, PUBLISHING;
- published remote result recovery;
- uncertain execution no replay;
- CODEX exact routing;
- COPILOT exact routing;
- no substitution;
- Copilot native auto command policy;
- Copilot pinned model;
- Codex pinned model/reasoning;
- backward compatibility with old dispatches;
- control commands while worker is running;
- Tray fixed action mapping;
- Task Scheduler current-user/idempotent command behavior;
- log/secret redaction;
- all current Operational MVP tests remain passing.

No paid Copilot/Codex task invocation is required merely to test model-policy command construction. Use mocks/fakes for adapter command generation and startup registration.

A real post-implementation Codex/Copilot canary belongs to validation after unit/restart evidence.

## 5. Result Contract

Write:
- `reports/BRIDGE-DESKTOP-01-02/report.md`
- `reports/BRIDGE-DESKTOP-01-02/evidence_manifest.json`
- optional sanitized evidence below `reports/BRIDGE-DESKTOP-01-02/evidence/**`

Report:
- exact source/base/branch/worktree;
- changed paths;
- ledger schema version/migrations;
- worker/recovery semantics;
- dual-Agent/model-policy behavior;
- Tray/startup implementation;
- exact tests/results;
- BRD-09 acceptance subcases supported;
- NOT_RUN Desktop-03 installer/community extraction;
- actual model/thinking/quota if exposed;
- final local/remote SHA.

## 6. Git boundary

Preferred worktree:
`C:\Projects\FOX2-worktrees\FOX2-BRIDGE-DESKTOP-01-02-CODEX`

Before mutation verify:
- remote task branch exact HEAD equals this handoff commit;
- no attached conflicting worktree;
- no WIP at destination;
- no active Bridge Desktop writer.

Do not reset/stash/clean another worktree.

Commit/push only task branch.

Final:
`PUSHED_UNREVIEWED`

No PR, merge, main, deployment, provider, broker, LIVE or Desktop-03 packaging.

## 7. Required final marker

End the Codex response with exactly:

`FOX2_BRIDGE_DESKTOP_01_02_DELIVERY_READY`
