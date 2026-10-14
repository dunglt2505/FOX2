# FOX2 — BRIDGE-DESKTOP-01+02 Combined Source & Design Lock

**Date:** 2026-10-14  
**Combined WP:** `BRIDGE-DESKTOP-01-02`  
**Status:** `SOURCE_DESIGN_LOCKED / OWNER_DEV_AUTHORIZED / STOP_AT_PUSHED_UNREVIEWED`  
**Owner instruction:** combine `BRIDGE-DESKTOP-01` with next candidate `BRIDGE-DESKTOP-02` and execute now.

## 1. Immutable source authority

This task binds the following already-read-back Candidate source as executable by explicit Owner decision; it does not promote those source documents to RELEASED:

- `FOX2-BRD-09 v0.1 Candidate`
  - commit: `6062a3b3a9b1580181b0bfa4501cf04de5c2ddaf`
  - path: `docs/brd_mirror/FOX2-BRD-09_v0.1_CANDIDATE.md`
  - blob: `a525d55912935639fa317471f9b85cee6c42ceca`
- `FOX2 Local Agent Bridge Technical Specification v0.7 Candidate`
  - commit: `6062a3b3a9b1580181b0bfa4501cf04de5c2ddaf`
  - path: `docs/architecture/FOX2_LOCAL_AGENT_BRIDGE_TECHNICAL_SPEC_v0.7_CANDIDATE.md`
  - blob: `d5b576d0698c0c332a7d1c3819b7c10180f3deda`
- Candidate readback receipt
  - commit: `6062a3b3a9b1580181b0bfa4501cf04de5c2ddaf`
  - path: `docs/agent_handoff/BRIDGE/FOX2_BRIDGE_DESKTOP_SPEC_CANDIDATE_RECEIPT_20261014.json`
  - blob: `61c1120acef0ece1ded41afeb17e1604ef9f2620`

Released governance remains unchanged:
- FOX2 Policy V1.8.5
- Routing Index V1.2.6
- Bridge Technical Spec v0.6 released predecessor

Operational Bridge code base for this task is exactly:
`398bebf9c48e7694c69c3416a5780715f025e7b5`

This task does not merge the divergent Candidate-doc branch into the operational code branch. Source is bound by immutable commit/path/blob references.

## 2. Combined product outcome

Deliver Desktop-01 and Desktop-02 as one bounded implementation lane:

### Desktop-01
- continuous per-user background worker;
- healthy/idle polling loop;
- pause/resume/check-now control;
- bounded offline/error backoff;
- singleton worker;
- durable worker/recovery state;
- restart reconciliation;
- no blind replay after uncertain execution;
- diagnostic CLI commands.

### Desktop-02
- Windows System Tray control surface;
- Running/Paused/Degraded/Error/current-task/last-result visibility;
- Pause new tasks / Resume / Check now / Open logs / Start with Windows / Exit;
- Start-with-Windows per-user registration;
- graceful exit semantics;
- no visible PowerShell required for normal background use after bootstrap;
- no duplicate worker when launched twice.

Desktop-03 setup/installer packaging is NOT part of this task.

## 3. Agent routing and model policy lock

Bridge transports an already-authorized exact Agent. It never silently substitutes Agent products.

### 3.1 GitHub Copilot CLI

For eligible Copilot dispatches, support:

- `agent.product = COPILOT`
- `model_policy = NATIVE_AUTO | PINNED`
- default native auto policy:
  - `model = auto`
  - `auto_tier = balance`
- optional auto tiers: `efficiency | balance | intelligence`
- non-interactive execution:
  - exact worktree
  - `--model auto` for native Auto
  - `--no-ask-user`
  - `--output-format json` when supported
  - only explicit minimal `--allow-tool` / `--allow-url` grants
- never use `--allow-all`, `--yolo`, or unrestricted Autopilot in this WP.
- optional `max_ai_credits` may be accepted from dispatch only when the installed CLI supports it and the bound is explicit.
- the actual model selected by Copilot Auto is observed/reportable when the CLI exposes it; Bridge never fabricates it.

Official GitHub behavior considered in this lock:
- Copilot CLI accepts `--model auto`.
- Auto selection considers task complexity and current model availability.
- Auto tiers: efficiency / balance / intelligence.
- `--no-ask-user`, `--output-format=json`, `--allow-tool`, and `--max-ai-credits` are programmatic controls.
- minimal permissions are preferred for automation.

Per-task auto-tier configuration must not mutate the Owner's global Copilot settings. If the installed CLI exposes no direct tier flag, use an isolated Bridge-owned Copilot runtime profile/config outside Git, feature-detect behavior, and keep auth credentials in the user's normal supported credential mechanism. If this cannot be proven safely, default to native `--model auto` without forcing a tier and report `AUTO_TIER_NOT_ENFORCED`; do not rewrite global settings.

### 3.2 OpenAI Codex CLI

For eligible Codex dispatches, support:

- `agent.product = CODEX`
- `model_policy = PINNED | CURRENT_CONFIG`
- preferred task fields:
  - `model`
  - `reasoning_effort = low | medium | high`
- current Windows safety baseline remains:
  - approval `never`
  - sandbox `workspace-write`
  - Windows sandbox fallback `unelevated` where required by installed CLI
  - prefer MSI/WiX PowerShell at `C:\Program Files\PowerShell\7\pwsh.exe`
- Bridge remains Git commit/push owner after Codex exits.
- model/effort requested by immutable dispatch must be passed to the CLI when supported; actual observed model/effort is recorded when exposed.
- do not loosen to danger/full-access sandbox in this WP.

### 3.3 Selection ownership

CHAT chooses:
- exact Agent product;
- Copilot Auto tier or pinned model policy;
- Codex model/reasoning policy.

Bridge only validates and executes the immutable selection.

Agent unavailable/quota/login failure is terminal/actionable for that dispatch. No COPILOT<->CODEX silent fallback.

## 4. Worker architecture lock

Add a background worker loop around current Operational MVP, reusing existing poller/ledger/E2E runner.

Required state semantics:

```text
STOPPED
STARTING
RECONCILING
IDLE
POLLING
EXECUTING
PUBLISHING
PAUSED
DEGRADED
ERROR
STOPPING
```

Loop:
```text
start
-> acquire one per-user worker singleton
-> initialize/migrate ledger
-> reconcile non-terminal prior executions
-> discover tools
-> idle
-> poll control branch
-> if paused: no new claim
-> if eligible: execute exact dispatch
-> verify/publish
-> idle
-> repeat
```

Healthy default poll target: 30s.  
Offline/error backoff target: 30s -> 60s -> 120s -> 300s max, reset after successful Git contact.

Polling alone must not invoke an Agent.

## 5. Recovery lock

Current v0.6 behavior that blindly terminalizes any stale RUNNING execution as INTERRUPTED is insufficient for Desktop-01 certification.

On worker start:
- inspect non-terminal execution stage;
- reconcile local ledger with exact target branch and expected result state;
- if remote authorized result is already present and validates, recover as `PUSHED_UNREVIEWED`;
- if evidence proves the Agent never started, claim may be safely reconsidered under exact immutable identity;
- if Agent may have started or workspace/result state is uncertain, enter `NEEDS_RECONCILIATION` / `INTERRUPTED` and do NOT blindly launch a second Agent;
- retry requires explicit safe recovery evidence or a fresh dispatch according to current governance.

Do not use elapsed time alone as replay permission.

## 6. Durable worker/control state

Extend the ledger with a versioned migration rather than replacing current evidence.

Minimum durable state:
- worker generation/start/heartbeat/stop;
- pause state;
- check-now request generation;
- graceful-stop request;
- last poll/backoff;
- current dispatch/execution stage;
- recovery/reconciliation outcome;
- remote result SHA when known;
- requested Agent/model policy and observed Agent/model metadata where safely available.

Migrations must preserve current dispatch/execution evidence.

## 7. Local control plane and Tray lock

Use a local-user control mechanism that does not expose a TCP listener and does not accept arbitrary shell strings.

For this combined task, a Bridge-owned local control plane backed by the durable runtime DB/status files and fixed command enums is acceptable if:
- it is under the current user's Bridge runtime directory;
- control commands are enumerated and validated;
- the worker singleton does not block read/control operations;
- no arbitrary command/prompt payload can be injected through the Tray control path.

Required commands:
- status
- pause
- resume
- check-now
- request-exit
- set-start-with-windows
- open-logs

Tray may invoke these fixed Bridge control commands.

### Windows Tray implementation

Prefer no new third-party runtime dependency for Desktop-01+02.

A PowerShell 7 / .NET `System.Windows.Forms.NotifyIcon` tray host is allowed and preferred for this internal FOX2 build because PowerShell 7 MSI is already present and avoids adding GUI Python packages. It must:
- run without a visible console in normal use;
- display textual state;
- invoke only fixed Bridge control commands;
- not embed credentials;
- not become an authority source;
- exit cleanly.

If implementation proves this approach unreliable under tests, STOP with evidence rather than adding an unapproved dependency.

## 8. Start with Windows lock

Initial implementation:
- per-user Windows Task Scheduler at current-user logon, or equivalent per-user startup facility;
- never SYSTEM by default;
- no plaintext password;
- idempotent enable/disable;
- task points to installed/current internal launcher location;
- disabling removes only Bridge startup registration;
- never deletes project repositories/worktrees.

No installer is required in this WP. Desktop-03 owns packaged installer/update/uninstall.

## 9. Combined exact write scope

Allowed:
- `agent_bridge/**`
- `reports/BRIDGE-DESKTOP-01-02/**`

The CHAT-authored source-lock and executable handoff files created before Agent execution are immutable source, not Agent write targets.

Forbidden:
- FOX2 application backend/frontend/data-contract/BRD implementation paths;
- governance source changes;
- provider/broker/LIVE code;
- main branch;
- auto-merge/deploy;
- unrelated docs.

Do not modify BRD-09 or Tech Spec v0.7 Candidate in this implementation task.

## 10. Mandatory implementation evidence

### Worker/recovery
- singleton worker;
- idle polling consumes zero Agent invocations;
- pause blocks new claim but keeps worker alive;
- resume does not replay completed dispatch;
- check-now wakes poll loop;
- bounded backoff;
- crash/restart at deterministic stages:
  - before Agent start
  - RUNNING
  - AGENT_EXITED
  - PUBLISHING
- completed remote result is reconciled without replay;
- uncertain execution never blind-replays.

### Agent routing
- CODEX dispatch selects Codex only;
- COPILOT dispatch selects Copilot only;
- no silent substitution;
- Copilot Auto produces command/config policy consistent with native Auto;
- Copilot pinned model supported;
- Codex pinned model/reasoning passed when supported;
- actual model metadata is observational, not fabricated;
- quota NOT_EXPOSED is not treated as exhausted.

### Tray/control/startup
- tray status maps worker state;
- Pause/Resume/Check-now fixed commands;
- duplicate tray/worker start does not create a second worker;
- Start-with-Windows registration command is idempotent in mocked/dry-run tests;
- startup runs under current user, not SYSTEM;
- no arbitrary shell IPC;
- no visible console requirement in the normal launcher/tray design;
- Open logs uses only configured local log path.

### Safety
- all existing Bridge tests pass;
- new Desktop tests pass;
- secrets/logs redacted;
- no provider/broker/LIVE behavior;
- no main/merge/deploy;
- changed paths exact allowlist;
- `git diff --check`.

## 11. Acceptance mapping

Combined implementation should produce evidence for BRD-09:

- T01/T02/T03/T04
- T05/T06/T07/T08/T09/T10/T11/T12/T13/T14/T15/T16/T17/T20

T18/T19 setup/installer acceptance remains Desktop-03.  
T21/T22 generic/community extraction remains later scope.

Do not mark packaging/install/uninstall or community release PASS.

## 12. Branch / worktree / stop

Task branch:
`work/FOX2-BRIDGE-DESKTOP-01-02-codex`

Preferred worktree:
`C:\Projects\FOX2-worktrees\FOX2-BRIDGE-DESKTOP-01-02-CODEX`

Single writer:
CODEX CLI via current Bridge.

Final boundary:
`PUSHED_UNREVIEWED`

No PR, merge, main push, deployment, provider, broker or LIVE.

## 13. Gate snapshot

```text
BRD09_SOURCE=CANDIDATE_BOUND_BY_OWNER
TECH_V07_SOURCE=CANDIDATE_BOUND_BY_OWNER
BRIDGE_CORE_BASE=398bebf9c48e7694c69c3416a5780715f025e7b5
DESKTOP_01_02_OWNER_DEV_AUTHORIZATION=YES
CODE_ALLOWED=YES_TASK_ONLY
GIT_CODE_PUSH=YES_TASK_BRANCH_ONLY
PR_CREATE=NO
MERGE_ALLOWED=NO
PRODUCTION_PROVIDER=NO
BROKER_WRITE=NO
LIVE=NO
```
