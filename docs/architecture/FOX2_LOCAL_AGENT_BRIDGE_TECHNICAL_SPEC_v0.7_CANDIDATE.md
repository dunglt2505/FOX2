# FOX2 — Local Agent Bridge Technical Specification v0.7 Candidate

**Document ID:** `FOX2-LOCAL-AGENT-BRIDGE-SPEC`  
**Version:** `0.7 Candidate`  
**Status:** `CANDIDATE / DESKTOP_BACKGROUND_PRODUCTIZATION / NO_DEV_GRANT`  
**Date:** 2026-10-14  
**Predecessor:** v0.6 `RELEASED_EFFECTIVE / SIMPLIFIED_RELAY_MVP`  
**Product owner BRD:** `FOX2-BRD-09_v0.1_CANDIDATE.md`  
**Governance:** FOX2 Policy V1.8.5 + Routing Index V1.2.6  
**Purpose:** evolve the already-proven Bridge Relay MVP into a reliable Windows background utility with Tray, Start-with-Windows, restart reconciliation and product packaging while preserving the simple transport/launcher boundary.

> This Candidate does not reopen proven Relay MVP work. It specifies the next productization layer and reuses existing `agent_bridge/**` core/adapters/ledger/E2E evidence.

## 1. Current baseline

Current observed Bridge source/evidence establishes:

- Git-backed dispatch discovery;
- immutable dispatch/prompt verification;
- exact worktree/branch/base/path validation;
- durable SQLite execution ledger;
- single-use/replay protection;
- interrupted-run recovery path;
- Copilot CLI adapter;
- Codex CLI adapter;
- direct Copilot CLI E2E result;
- direct Codex CLI E2E result;
- Bridge-controlled commit/push verification on the Codex route;
- diagnostic commands including `health`, `status`, `poll-once`, `run-next`;
- current normal `run-next` selection policy auto-executes eligible CODEX dispatches.

Therefore v0.7 is **not** a rewrite of v0.6. Existing safe modules are reused and wrapped by background/product UX components.

## 2. Target runtime architecture

```text
                       GitHub / configured Git remote
                                  |
                         immutable dispatch ref
                                  |
                     +------------v-------------+
                     | AgentBridge Worker        |
                     | per-user background proc  |
                     |                           |
                     | DispatchWatcher           |
                     | DispatchValidator         |
                     | ReplayGuard / Ledger      |
                     | WorkspaceResolver         |
                     | RuntimeAttestor           |
                     | AgentAdapterRegistry      |
                     |  - CodexAdapter           |
                     |  - CopilotAdapter         |
                     | ExecutionSupervisor       |
                     | ResultPublisher           |
                     | RecoveryReconciler        |
                     +------+--------------------+
                            |
                    local-user IPC
                            |
                     +------v--------------------+
                     | AgentBridge Tray          |
                     | status / pause / resume   |
                     | check-now / settings      |
                     | logs / startup toggle     |
                     +---------------------------+

Agent execution:
Worker -> exact isolated worktree -> selected CLI -> tests/edit
       -> Worker validates diff/result -> non-main commit/push -> CHAT readback
```

VS Code remains optional and outside the required normal execution path.

## 3. Process model

### 3.1 Per-user execution

Default runtime executes under the **interactive Windows user account**, not SYSTEM.

Reason:

- Git credentials belong to the user;
- Copilot/Codex CLI login belongs to the user;
- project/worktree ACLs belong to the user;
- SYSTEM execution can silently lose access to the authenticated CLI context.

### 3.2 Two-process target

Target productization uses:

1. **AgentBridge Worker** — hidden/background process owning Git polling, ledger, recovery, Agent CLI processes and result publication.
2. **AgentBridge Tray** — thin interactive shell owning status display and user controls.

Tray MUST NOT reimplement dispatch, Git, replay or Agent execution logic.

Closing the Tray UI does not have to terminate an already-running Worker unless the user explicitly selects Exit Bridge. A later implementation may initially ship a combined process if it passes the same behavior tests, but component boundaries must remain separable.

### 3.3 Single instance

Each Bridge profile has one Worker owner enforced by an OS/user-scoped singleton plus the existing durable process lock.

Second launch:

- detects existing Worker;
- opens/focuses Tray or requests status;
- never starts a second poller for the same profile.

## 4. Runtime directories

### 4.1 Development source

Git source remains:

```text
<FOX2 repo>/agent_bridge/**
```

### 4.2 Product runtime target

Preferred per-user installed/runtime layout:

```text
%LOCALAPPDATA%\AgentBridge\
    config\
    data\
    logs\
    run\
```

Development runtime `C:\Projects\FOX2-AgentBridge` remains a valid current bootstrap/dev installation but is not the long-term product location.

Migration from the existing path must be explicit and backup-safe. Do not silently relocate or delete source/worktrees.

### 4.3 Worktrees

Project worktrees stay under the project/profile-defined root, for FOX2 currently:

```text
C:\Projects\FOX2-worktrees\
```

Bridge installation/uninstall never owns deletion of project worktrees by default.

## 5. Configuration model

Use typed local configuration. Proposed logical structure:

```toml
[bridge]
profile_id = "default"
poll_interval_seconds = 30
start_paused = false
start_with_windows = true

[[projects]]
project_id = "FOX2"
repository = "dunglt2505/FOX2"
local_repo = "C:\\Projects\\FOX2"
worktree_root = "C:\\Projects\\FOX2-worktrees"
control_branch = "work/FOX2-LOCAL-DISPATCH-chat"
enabled = true

[agents.codex]
enabled = true
executable = "auto"

[agents.copilot]
enabled = true
executable = "auto"
```

Exact file format may remain TOML to reuse current code.

Configuration must not contain passwords, access tokens or embedded Agent subscription credentials.

Initial v0.7 only needs **one actively scheduled project profile at a time**. Data structures should avoid hardcoding FOX2 so a later generic Core can enable additional profiles.

## 6. Background watcher

### 6.1 Polling loop

Worker owns a continuous loop:

```text
START
 -> load config
 -> acquire singleton
 -> open/migrate ledger
 -> recover/reconcile interrupted state
 -> discover local tools
 -> IDLE
 -> poll Git
 -> validate discoveries
 -> if paused/no eligible task: IDLE
 -> if eligible: claim -> execute -> verify -> publish -> IDLE
 -> repeat
```

### 6.2 Poll cadence

Candidate defaults:

- healthy/idle poll: 30 seconds;
- manual **Check now** bypasses wait;
- offline/error backoff: 30s -> 60s -> 120s -> 300s maximum;
- successful Git contact resets backoff.

These are implementation defaults, not product semantics. They must be configurable within safe bounds.

Polling Git alone must never launch an Agent without an explicitly eligible dispatch.

### 6.3 No hidden Agent health prompts

Tool health checks use non-billable/non-task mechanisms where supported, such as executable discovery/version/auth-status commands.

Do not send a real Agent prompt merely to determine whether quota remains unless an explicit task authorizes that probe.

## 7. Worker state model

Worker state:

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

Dispatch lifecycle remains distinct:

```text
DISCOVERED
CLAIMED
AGENT_STARTING
RUNNING
AGENT_EXITED
VERIFYING
PUBLISHING
PUSHED_UNREVIEWED
BLOCKED
FAILED
INTERRUPTED
NEEDS_RECONCILIATION
```

Tray displays the user-level Worker state plus current dispatch state when relevant.

## 8. Pause, Resume and Exit semantics

### Pause

Pause prevents claiming/launching **new** dispatches.

Default behavior for an already-running Agent is **finish current task**. Worker continues supervising it and can publish its authorized result.

### Resume

Resume returns to polling. ReplayGuard and ledger remain authoritative, so Resume never re-runs a completed dispatch.

### Exit

If no task is running, Exit stops Worker and Tray cleanly.

If a task is active, UI should offer:

- `Exit after current task` — recommended;
- `Cancel active task and exit` — only where adapter/process cancellation is safely supported.

No abrupt silent process kill.

## 9. Restart/recovery reconciliation

This is the highest-priority v0.7 reliability addition.

At Worker startup, inspect durable non-terminal executions.

### 9.1 Safe automatic recovery

If ledger proves the Agent had **not yet started**, a stale claim may be released/re-evaluated if remote dispatch identity is still exact and the task is still eligible.

### 9.2 Uncertain execution

If an Agent process may have started before crash:

```text
RUNNING/AGENT_EXITED/PUBLISHING observed after restart
 -> mark NEEDS_RECONCILIATION
 -> inspect target branch/ref/result path
 -> compare immutable dispatch/result expectations
```

Never automatically start a second Agent process merely because the original PID is gone.

### 9.3 Remote result exists

If authorized remote result commit exists and validates against the dispatch:

- record recovered result identity;
- mark terminal `PUSHED_UNREVIEWED`;
- do not replay.

### 9.4 Remote result absent

If execution outcome cannot be proven and remote result does not exist:

- mark `INTERRUPTED` / `NEEDS_RECONCILIATION`;
- require a new explicit retry/recovery decision or dispatch generation unless the implementation can prove the Agent never mutated the workspace.

Avoid heuristic replay based solely on elapsed time.

## 10. Agent Adapter Registry

Core exposes a common adapter boundary:

```python
AgentAdapter:
    discover()
    inspect_readiness()
    launch(worktree, prompt, runtime_contract)
    stream_status()
    cancel()
    collect_result()
```

No requirement that every adapter exposes identical model/quota details.

### 10.1 Codex

Current proven path is preserved:

- direct Codex CLI;
- exact worktree;
- non-interactive prompt input;
- bounded timeout;
- workspace-write;
- current Windows sandbox workaround where still required by installed CLI;
- Bridge owns path/result/history verification and task-branch commit/push.

Do not freeze current Codex CLI version/flag workarounds forever; adapter feature-detects supported behavior and tests changes.

### 10.2 Copilot

Current direct Copilot CLI E2E evidence is preserved.

Normal `run-next` may remain CODEX-only until an explicit product routing decision enables Copilot automatic selection. Explicit diagnostics/historical dispatch remain supported.

No silent fallback from CODEX to COPILOT or vice versa.

## 11. Worktree ownership and Git behavior

Before Agent launch:

1. resolve exact repository;
2. verify branch remote head/base;
3. create/attach only the authorized worktree when permitted;
4. detect conflicting registered worktree;
5. detect material WIP/lock/active writer;
6. bind allowed write paths.

After Agent exit:

1. verify Git history was not rewritten unexpectedly;
2. inspect all dirty paths;
3. reject out-of-scope changes;
4. validate required result artifacts;
5. run configured final checks;
6. stage only allowed paths;
7. commit only task branch;
8. push and remote-readback full SHA.

No main push or merge in Bridge v0.7.

## 12. Tray technical behavior

### 12.1 Required status

Tray obtains local state through a user-scoped IPC contract and displays:

- Worker state;
- Git connection state;
- selected project;
- Codex availability;
- Copilot availability;
- current dispatch/WP;
- current Agent;
- elapsed task time;
- last result;
- last material error;
- Start-with-Windows state.

### 12.2 Actions

IPC operations:

```text
GET_STATUS
PAUSE
RESUME
CHECK_NOW
OPEN_LOG_DIRECTORY
SET_START_WITH_WINDOWS
REQUEST_EXIT
REQUEST_CANCEL_ACTIVE
```

IPC never carries project secrets or arbitrary shell strings.

### 12.3 IPC security

Preferred Windows mechanism: local Named Pipe or equivalent user-local IPC.

Requirements:

- ACL restricted to current user/session;
- no TCP listener required for Tray;
- validate protocol version and command enum;
- no arbitrary code execution payload.

## 13. Start with Windows

Preferred initial mechanism:

**Windows Task Scheduler — At logon of current user**, or another per-user startup facility with equivalent behavior.

Do not default to a Windows Service running as SYSTEM.

Registration requirements:

- per-user;
- points to installed/signed launcher;
- no stored plaintext password;
- idempotent enable/disable;
- survives app update;
- removal on uninstall;
- startup failure becomes visible in Tray next run/log.

A simple Startup shortcut may be fallback if Task Scheduler proves unnecessarily brittle.

## 14. First-run onboarding

First launch enters Setup when required config is absent.

Wizard stages:

1. **Runtime** — choose/confirm local runtime location.
2. **Repository** — locate FOX2 repository.
3. **Worktrees** — confirm worktree root.
4. **Git** — executable/version/read access.
5. **Codex** — discovered / auth state if supported.
6. **Copilot** — discovered / auth state if supported.
7. **Dispatch** — read configured control branch, no write.
8. **Startup** — Start with Windows toggle.
9. **Health** — read-only final validation.

No package installation or credential login is silently performed. The wizard may guide the user to the official Agent login flow.

## 15. Logs and diagnostics

Use structured, bounded local logging.

Required redaction:

- userinfo in URLs;
- GitHub tokens;
- API keys;
- private keys;
- Authorization headers;
- obvious credential CLI output.

Do not persist full Agent conversation output by default. Persist only what is needed for execution diagnosis and result traceability.

Rotation is bounded by file count/size or time.

Diagnostic export, if added, must sanitize before packaging.

## 16. Durable ledger extensions

Existing SQLite ledger remains the durable source for runtime state.

v0.7 additions may include:

- worker heartbeat/start/stop metadata;
- pause state;
- restart generation;
- reconciliation outcome;
- task attempt generation;
- Agent PID/process identity where safe;
- remote result SHA;
- last poll/backoff state;
- user-visible error code.

Schema migrations must preserve current execution evidence.

## 17. Error taxonomy

Minimum user-facing categories:

```text
GIT_OFFLINE
GIT_ACCESS_DENIED
DISPATCH_INVALID
DISPATCH_REPLAYED
WORKTREE_CONFLICT
WRITER_COLLISION
AGENT_MISSING
AGENT_LOGIN_REQUIRED
AGENT_ACCESS_DENIED
AGENT_QUOTA_EXHAUSTED
AGENT_FAILED
AGENT_TIMEOUT
RESULT_SCOPE_VIOLATION
RESULT_MISSING
PUSH_FAILED
RECOVERY_REVIEW_REQUIRED
CONFIG_INVALID
INTERNAL_ERROR
```

Errors are actionable but sanitized.

Do not invent `QUOTA_EXHAUSTED` from `NOT_EXPOSED`; use it only when the Agent/platform actually reports such failure.

## 18. Packaging

### 18.1 Desired user artifact

Target distribution:

- per-user Windows installer, plus optionally a portable diagnostic package;
- no console window for normal Tray/Worker startup;
- Start Menu entry;
- Tray;
- Start-with-Windows support;
- clean uninstall.

Exact bundler/installer technology is an implementation choice to evaluate during packaging WP.

### 18.2 Upgrade behavior

Upgrade preserves:

- config;
- ledger;
- logs as configured;
- project repository/worktrees.

Perform schema migration before normal polling begins.

Failed upgrade/migration must fail closed without destroying prior data.

## 19. Security boundary

v0.7 keeps v0.6's intentionally small authority model.

Bridge:

- consumes an already-authorized immutable dispatch;
- validates minimum runtime identity;
- launches exact Agent;
- supervises;
- enforces local scope;
- publishes allowed task result;
- replay-protects.

Bridge does **not**:

- perform R0-R7;
- reinterpret BRD/Policy;
- create new code authority;
- change Agent merely because one is unavailable;
- auto-rework;
- auto-merge;
- deploy;
- enable provider/broker/LIVE.

### 19.1 Current public bootstrap

Current pinned-Git bootstrap trust may continue for public/offline FOX2 development.

The existing GitHub ruleset configuration observed in October 2026 is not treated as hardened trust because its ref uses a Unicode dash mismatch and its bypass actor is DeployKey.

This does not block v0.7 offline productization under current released bootstrap rules.

Before confidential/private/Production use where trusted publisher enforcement is required, create and certify a hardened publisher/control-ref design.

## 20. Community/open-core separation

Do not mechanically publish the FOX2 repository as the standalone product.

Future extraction boundary:

```text
agentbridge-core/
    transport/
    ledger/
    workspace/
    supervisor/
    adapters/
    tray/
    installer/

project profiles/config:
    FOX2-specific config stays outside generic distribution
```

Before standalone public release:

- remove owner/local paths;
- remove FOX2 policy/business requirements;
- remove synthetic credential-shaped fixtures;
- scan Git history/source package;
- choose software license;
- confirm third-party redistribution/licensing;
- document supported Agent CLI versions.

## 21. Acceptance test plan

BRD-09 acceptance IDs map to implementation tests.

### Background / Tray

- `FOX2-09-T01`: packaged launch produces Worker+Tray without console requirement.
- `T02`: logon starts one instance.
- `T03`: status accurately tracks IDLE/EXECUTING/PAUSED/ERROR.
- `T04`: pause/resume blocks only new launches.
- `T16`: second launch attaches to existing instance.

### Dispatch / spend guard

- `T05`: ineligible dispatch does not launch Agent.
- `T06`: exact project/worktree/branch/prompt/scope.
- `T15`: idle auto-start consumes no Agent invocation.

### Recovery

- `T07`: completed task survives restart without replay.
- `T08`: crash at CLAIMED, RUNNING, AGENT_EXITED, PUBLISHING stages; reconcile correctly.
- Kill Worker at deterministic fault-injection checkpoints and restart using same ledger.

### Agent adapters

- `T09`: explicit CODEX and COPILOT canaries, no substitution.
- `T10`: VS Code closed; CLI route still works.
- Missing executable/login states map to T13 without paid health prompts.

### Safety

- `T11`: rejected merge/main/Production/broker/LIVE permission expansion.
- `T17`: log redaction.
- worktree/path traversal, dirty writer collision and out-of-scope result tests.

### Setup/package

- `T18`: first-run degraded setup with one missing CLI.
- `T19`: uninstall leaves repository/worktrees.
- `T20`: diagnostic CLI still operates independently of Tray.

### Generic boundary

- `T21`: project profile switches repository/worktree/control config without Core source edit.
- `T22`: standalone package scan/license/sanitization gate.

## 22. Productization work packages

Recommended sequence, runnable in parallel with FOX2 application work when writer paths are disjoint:

### `BRIDGE-DESKTOP-01 — Background Worker & Reconciliation`

Scope:
- continuous watcher loop;
- pause state;
- bounded backoff;
- restart/crash reconciliation;
- single-instance worker;
- relevant ledger migration;
- CLI commands for `start/stop/pause/resume/watch`.

Exit:
- restart/no-replay fault tests pass;
- no Tray required yet.

### `BRIDGE-DESKTOP-02 — System Tray & Startup`

Depends on Desktop-01 interfaces.

Scope:
- local IPC;
- Tray states/actions;
- Start with Windows;
- notifications;
- graceful exit.

Exit:
- T01/T02/T03/T04/T13/T16.

### `BRIDGE-DESKTOP-03 — Setup & Packaging`

Scope:
- first-run setup;
- installed per-user runtime layout;
- installer/update/uninstall;
- sanitized logs/support bundle if needed.

Exit:
- T18/T19/T20.

### `BRIDGE-DESKTOP-04 — Real FOX2 WP Certification`

Use a real, independently eligible FOX2 WP rather than another trivial canary.

Prove:
- CHAT dispatch;
- background Worker discovery;
- real selected Agent CLI;
- tests;
- non-main Git result;
- CHAT readback;
- restart does not replay.

Do not force a currently in-progress manually-owned WP to switch execution path mid-flight.

### `BRIDGE-DESKTOP-05 — Standalone/Community Extraction`

Only after FOX2 workflow is stable.

Scope:
- generic project profile;
- sanitized repo/package;
- license decision;
- public docs;
- installer release process.

## 23. Parallelism and writer boundaries

Current FOX2 Policy permits up to two independent material writers.

Bridge Desktop work can run in parallel with application P2-02 only if:

- Bridge lane writes only `agent_bridge/**`, dedicated `tests/reports` if defined, and Bridge docs;
- application lane remains within its own backend/test/result allowlist;
- worktrees/branches differ;
- no shared packaging/root file requires concurrent edits.

Technical Spec Candidate itself grants no writer.

## 24. Definition of Ready for Desktop-01 implementation

Before coding:

1. BRD-09 and v0.7 source are Owner-approved/released or explicitly bound as executable Candidate by Owner decision.
2. exact `agent_bridge/**` base commit chosen;
3. existing Bridge WIP/branch landscape checked;
4. one dedicated writer/worktree reserved;
5. exact allowed code/test/report paths defined;
6. latest Operational MVP tests/evidence reused; no BRG-003 reimport;
7. Python/runtime/Agent tool availability checked only as materially needed;
8. no overlap with active FOX2 application writer;
9. STOP conditions and result paths bound.

## 25. Definition of Done for v0.7 productization

v0.7 may be considered product-ready for the Owner's normal Windows use when:

- Worker stays running in background after normal launch;
- Start with Windows works under user session;
- Tray controls/status work;
- Pause/resume semantics are correct;
- completed dispatch survives reboot/restart without replay;
- uncertain crash is reconciled without blind duplicate launch;
- Codex direct route remains E2E functional;
- Copilot direct route remains supported/tested or explicitly classified degraded;
- no visible PowerShell is required for normal operation;
- first-run setup reports Ready/Degraded accurately;
- secrets/logging/path boundaries pass;
- one real FOX2 WP completes through the background Bridge path and CHAT independently reads back result.

Installer/community extraction is a separate release boundary and need not block internal FOX2 v0.7 use if the local installed bundle is otherwise reliable.

## 26. Non-effects

This Candidate does not:

- modify Policy V1.8.5;
- modify Routing Index V1.2.6;
- change FOX2 M1 market-data BRDs;
- change existing accepted P2 application interfaces;
- authorize Bridge code;
- authorize a third parallel writer beyond Policy limit;
- merge to main;
- enable provider/broker/LIVE;
- declare hardened publisher trust PASS;
- declare BRD-09 acceptance tests PASS.

`TECH_V0_7_STATUS=CANDIDATE / CODE_ALLOWED=NO_FROM_THIS_DOCUMENT / ACCEPTANCE=NOT_RUN`.
