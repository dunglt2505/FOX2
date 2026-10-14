# FOX2 — Local Agent Bridge Technical Specification v0.7 Candidate

**Document ID:** `FOX2-LOCAL-AGENT-BRIDGE-SPEC`  
**Version:** `0.7 Candidate REV3`  
**Status:** `CANDIDATE / DESKTOP_BACKGROUND_PRODUCTIZATION / NO_DEV_GRANT`  
**Date:** 2026-10-14  
**Predecessor:** v0.6 `RELEASED_EFFECTIVE / SIMPLIFIED_RELAY_MVP`  
**Product owner BRD:** `FOX2-BRD-09_v0.1_CANDIDATE.md`  
**Governance:** FOX2 Policy V1.8.5 + Routing Index V1.2.6  
**Purpose:** evolve the already-proven Bridge Relay MVP into a reliable Windows background utility with Tray, Start-with-Windows, restart reconciliation, deterministic dual-Agent execution, usage telemetry and product packaging while preserving the simple transport/launcher boundary. REV2 locked GitHub-as-durable-mailbox + local outbound pull as the V1 signaling model. REV3 integrates Agent model-policy and usage telemetry into the normal Desktop implementation batches so they are built once with the same adapters, ledger, recovery and Tray surfaces rather than as a later standalone feature.

> This Candidate does not reopen proven Relay MVP work. It specifies the next productization layer and reuses existing `agent_bridge/**` core/adapters/ledger/E2E evidence. The normative routing/telemetry requirements are defined by `FOX2_AGENT_USAGE_TELEMETRY_ROUTING_CONTRACT_v0.1_CANDIDATE.md`; that contract is integrated into the Desktop plan and is **not** a separate DEV round.

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
                     durable control-ref mailbox
                                  ^
                                  | outbound Git/HTTPS only
                                  | lightweight remote-ref poll
                                  |
                     +------------+-------------+
                     | AgentBridge Worker        |
                     | per-user background proc  |
                     |                           |
                     | GitSignalWatcher          |
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

Per-task Agent/model selection is **dispatch-owned**, not global-config-owned. Global config may enable/locate an Agent, but MUST NOT silently choose or override a task's `model_policy`, Copilot `auto_tier`, Codex `model`, or Codex `reasoning_effort`.

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

## 7. GitHub mailbox signaling and local pull protocol

### 7.1 Authority model

GitHub is the V1 durable task mailbox. The configured control ref is the only signal source that can lead to dispatch discovery.

CHAT publishes:

```text
immutable prompt/source
+ immutable dispatch JSON
+ control-ref commit
```

The local Worker **pulls outward** to GitHub. There is no direct CHAT-to-PC socket and no inbound AgentBridge network listener in V1.

Required V1 network shape:

```text
Local Windows PC
      |
      | outbound Git/HTTPS
      v
GitHub configured repository/control ref
```

Normal operation must work behind NAT and with dynamic IP.

### 7.2 Lightweight signal probe

The Worker maintains a durable `last_seen_control_sha`.

Healthy loop:

```text
remote_sha = query configured remote control-ref SHA

if remote_sha == last_seen_control_sha:
    no full fetch
    no dispatch parse
    no Agent call
    sleep healthy interval
else:
    fetch exact configured control ref at remote_sha
    discover immutable dispatch delta
    validate candidate(s)
    persist new observation/cursor
    execute only eligible auto_execute dispatch
```

Implementation may use `git ls-remote --refs origin refs/heads/<control-branch>` or an equivalent remote-ref query that does not update the worktree.

The signal probe must not require Codex/Copilot invocation.

### 7.3 Poll intervals and backoff

Candidate defaults:

```text
healthy idle: 30 seconds
manual Check now: immediate one-shot signal probe
offline/error: 30s -> 60s -> 120s -> 300s max
successful Git contact: reset to 30s
```

Add bounded jitter only if it materially reduces synchronized polling; it must never exceed configured safe bounds.

The Worker must remain responsive to local Pause/Resume/Check-now/Exit while waiting.

### 7.4 Durable cursor semantics

Persist at minimum:

- configured repository/project profile;
- control ref;
- last successfully observed remote SHA;
- last successfully fetched/processed control SHA;
- last poll timestamp;
- current backoff state;
- last transport error code.

A remote SHA change is only a **hint that Git content changed**. It is not task authority by itself. Dispatch JSON still requires normal immutable identity, scope, replay and eligibility validation.

Do not advance the durable processed cursor past an unprocessed control commit if doing so would make a valid dispatch unreachable. Poll/discovery and cursor persistence must remain transactionally consistent enough to survive Worker crash/restart.

### 7.5 Offline, sleep and wake

If the PC is offline/asleep:

- GitHub retains the dispatch;
- Worker sends no Agent prompt;
- no inbound wake path is required.

After wake/login/start:

```text
startup
 -> recover ledger
 -> reconcile non-terminal execution
 -> signal probe
 -> fetch changed control ref
 -> process still-eligible pending dispatch
```

Wake-on-LAN/remote wake is outside v0.7 V1.

### 7.6 Push/webhook future option

Webhook/cloud relay is **not required** for Desktop-01.

A later push path may emit only a wake/check hint:

```text
GitHub webhook -> optional relay -> local hint -> perform normal Git signal probe
```

It must not carry executable authority that bypasses the configured Git control ref, immutable dispatch validation or ReplayGuard.

### 7.7 No inbound exposure in V1

Do not require or expose:

- public/static IP;
- router port forwarding;
- inbound HTTP server;
- public WebSocket listener;
- ngrok tunnel;
- Tailscale/VPN dependency.

Local Tray IPC remains local-user-only as defined separately and is not an Internet signaling endpoint.

## 8. Worker state model

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

## 9. Pause, Resume and Exit semantics

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

## 10. Restart/recovery reconciliation

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

## 11. Agent Adapter Registry

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

Bridge executes the exact immutable Agent configuration supplied by CHAT. It does not decide routing.

Canonical dispatch-owned execution tuple:

```text
Agent Product
+ Model Policy
+ Model or Auto Tier
+ Reasoning / Thinking
+ Scope
```

No silent substitution is allowed between CODEX and COPILOT, and Bridge must not change tier/model/reasoning based on quota, cost or runtime conditions.

### 11.1 Codex

Current proven direct Codex CLI path is preserved, with the Desktop completion adding deterministic dispatch-owned model configuration:

- exact worktree;
- non-interactive prompt input;
- bounded timeout;
- workspace-write;
- current Windows sandbox workaround where still required by installed CLI;
- `model_policy = PINNED`;
- exact `model` from dispatch;
- exact `reasoning_effort` from dispatch;
- structured result output when supported;
- usage/quota extraction when officially exposed;
- Bridge-owned path/result/history verification and authorized task-branch commit/push.

Codex must not fall back silently to a user-global model/reasoning setting when the immutable dispatch requires explicit values.

### 11.2 Copilot

Current direct Copilot CLI E2E evidence is preserved and generalized for normal exact-product execution.

Default model strategy:

```text
model_policy = NATIVE_AUTO
auto_tier = balance
```

CHAT may choose `efficiency`, `balance` or `intelligence`; GitHub Copilot selects the concrete model. Bridge does not emulate its own Auto router.

Required Desktop completion behavior:

- exact worktree;
- bounded programmatic prompt;
- `--no-ask-user` where supported;
- machine-readable JSON result where supported;
- dispatch-owned Auto tier;
- optional dispatch-owned `max_ai_credits` execution bound;
- usage/credit extraction when officially exposed;
- no mutation of normal user-global Copilot settings per task;
- process-scoped profile/isolation mechanism only after a host canary proves auth/session behavior;
- existing bounded `--allow-tool` safety retained.

Copilot Autopilot/YOLO/full-permission mode remains out of scope.

### 11.3 Usage snapshot and runtime failure

After either Agent exits, Bridge stores the newest usage/capacity information actually exposed by that CLI together with the execution result.

Unknown/unexposed data remains `UNKNOWN` / `NOT_EXPOSED`; Bridge does not guess quota, model or availability.

If quota/login/capacity failure occurs after Agent start:

```text
dispatch remains consumed
-> NEEDS_RECONCILIATION
-> no blind replay
-> no automatic Agent substitution
```

The persisted snapshot becomes an input for the **next CHAT routing decision**. CHAT, not Bridge, performs reset normalization and routing/HOLD decisions.

## 12. Worktree ownership and Git behavior

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

## 13. Tray technical behavior

### 13.1 Required status

Tray obtains local state through a user-scoped IPC contract and displays:

- Worker state;
- Git connection state;
- selected project;
- Codex availability and latest usage snapshot when exposed;
- Codex requested/observed model + reasoning and 5h/weekly reset state when available;
- Copilot availability, credits, Auto tier and observed concrete model when exposed;
- current dispatch/WP;
- current Agent;
- elapsed task time;
- last result;
- last material error;
- Start-with-Windows state.

### 13.2 Actions

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

### 13.3 IPC security

Preferred Windows mechanism: local Named Pipe or equivalent user-local IPC.

Requirements:

- ACL restricted to current user/session;
- no TCP listener required for Tray;
- validate protocol version and command enum;
- no arbitrary code execution payload.

## 14. Start with Windows

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

## 15. First-run onboarding

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

## 16. Logs and diagnostics

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

## 17. Durable ledger extensions

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
- user-visible error code;
- requested Agent/model-policy/tier/model/reasoning tuple;
- observed Agent/model/reasoning fields when exposed;
- latest Agent usage/capacity snapshot, observation time, source and freshness.

Schema migrations must preserve current execution evidence.

## 18. Error taxonomy

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

## 19. Packaging

### 19.1 Desired user artifact

Target distribution:

- per-user Windows installer, plus optionally a portable diagnostic package;
- no console window for normal Tray/Worker startup;
- Start Menu entry;
- Tray;
- Start-with-Windows support;
- clean uninstall.

Exact bundler/installer technology is an implementation choice to evaluate during packaging WP.

### 19.2 Upgrade behavior

Upgrade preserves:

- config;
- ledger;
- logs as configured;
- project repository/worktrees.

Perform schema migration before normal polling begins.

Failed upgrade/migration must fail closed without destroying prior data.

## 20. Security boundary

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

### 20.1 Current public bootstrap

Current pinned-Git bootstrap trust may continue for public/offline FOX2 development.

The existing GitHub ruleset configuration observed in October 2026 is not treated as hardened trust because its ref uses a Unicode dash mismatch and its bypass actor is DeployKey.

This does not block v0.7 offline productization under current released bootstrap rules.

Before confidential/private/Production use where trusted publisher enforcement is required, create and certify a hardened publisher/control-ref design.

## 21. Community/open-core separation

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

## 22. Acceptance test plan

BRD-09 acceptance IDs map to implementation tests.

### Git mailbox signaling

- `T23`: local PC behind NAT/dynamic IP discovers CHAT-published dispatch using outbound Git only.
- `T24`: repeated unchanged remote-ref probes cause no full fetch and no Agent invocation; Check now probes immediately.
- `T25`: sustained idle Worker generates zero Codex/Copilot task prompts.
- `T26`: simulated Git offline state exercises 30/60/120/300 bounded backoff and resets after recovery.
- `T27`: changing local IP does not change control-mailbox correctness.
- `T28`: publish dispatch while Worker stopped; restart/reconcile then discovers and processes it once.
- `T29`: optional push hint cannot bypass exact Git dispatch validation/replay guard.

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

### Agent adapters / routing / usage

- `T09`: explicit CODEX and COPILOT canaries, no substitution.
- `T10`: VS Code closed; CLI route still works.
- Missing executable/login states map to T13 without paid health prompts.
- Copilot dispatch `NATIVE_AUTO / balance` executes without Bridge selecting a concrete model.
- Copilot `efficiency|balance|intelligence` tier is taken from immutable dispatch.
- Codex exact model + reasoning effort are taken from immutable dispatch.
- requested configuration is persisted; observed configuration is persisted only when exposed.
- unexposed model/quota fields remain UNKNOWN/NOT_EXPOSED.
- success and quota-failure results persist available usage telemetry.
- Codex known five-hour reset is normalized by CHAT without resetting weekly state.
- post-start quota failure becomes NEEDS_RECONCILIATION with no blind replay/substitution.
- Tray renders usage/model state read-only and contains no routing logic.
- Copilot process-scoped profile behavior passes one real-host canary before trusted use.
- Copilot Autopilot/YOLO/full-permission mode remains disabled.

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

## 23. Productization execution plan — consolidated batches

The historical Desktop IDs remain useful for traceability, but implementation is intentionally batched to avoid repeated edits to the same adapters, ledger, worker and Tray code.

### Gate — `BRIDGE-DESKTOP-01-02-FIX-01`

This is the current corrective task only.

- keep its frozen corrective scope unchanged;
- do not inject routing/usage features into the in-flight fix;
- require PASS/readback before rebasing the next Bridge implementation batch.

### Batch A — `BRIDGE-DESKTOP-BATCH-A: CORE + ROUTING + USAGE + TRAY`

This is **one implementation round** after FIX-01 PASS. It absorbs the remaining related scope of historical Desktop-01, Desktop-02 and `FOX2-AGENT-USAGE-TELEMETRY-01`.

Implement together because these features share the same runtime paths:

- background Worker / Git mailbox polling;
- single-instance, pause/resume/check-now;
- restart/crash reconciliation and no-replay semantics;
- AgentAdapterRegistry generalized for exact CODEX or COPILOT dispatch;
- immutable routing tuple;
- Copilot `NATIVE_AUTO` + dispatch-owned Auto tier;
- Codex pinned model + reasoning effort;
- structured requested/observed execution result;
- usage/quota extraction when exposed;
- ledger migration for routing + usage snapshots;
- post-start quota/login failure reconciliation;
- CHAT-readable status surface;
- Tray IPC/status/startup behavior;
- Tray read-only usage/model display;
- Copilot runtime-profile canary;
- bounded permissions, no Autopilot/YOLO.

Exit Batch A only when Worker/recovery, both Agent paths, model policy, telemetry persistence and Tray status pass together. Do not close only the UI while adapter/ledger behavior remains pending.

### Batch B — `BRIDGE-DESKTOP-BATCH-B: SETUP + PACKAGE + REAL CERTIFICATION`

This is the second and final internal-productization round. It absorbs historical Desktop-03 and Desktop-04:

- first-run setup;
- installed per-user runtime layout;
- installer/update/uninstall;
- sanitized logs/support bundle if needed;
- one real eligible FOX2 WP through the background Bridge;
- real selected Agent/model-policy execution;
- result push/readback;
- usage snapshot available for next CHAT routing;
- restart proves no replay.

Exit Batch B when the installed Bridge is usable for normal FOX2 operation and one real WP has passed end-to-end CHAT readback.

### Later only — `BRIDGE-DESKTOP-05: Standalone/Community Extraction`

Keep this outside internal FOX2 readiness. Start only after the internal Bridge is stable.

Scope:
- generic project profile;
- sanitized repo/package;
- license decision;
- public docs;
- installer release process.

## 24. Parallelism and writer boundaries

Current FOX2 Policy permits up to two independent material writers.

Bridge Desktop work can run in parallel with application P2-02 only if:

- Bridge lane writes only `agent_bridge/**`, dedicated `tests/reports` if defined, and Bridge docs;
- application lane remains within its own backend/test/result allowlist;
- worktrees/branches differ;
- no shared packaging/root file requires concurrent edits.

Technical Spec Candidate itself grants no writer.

## 25. Definition of Ready for Batch A

Before Batch A coding:

1. `BRIDGE-DESKTOP-01-02-FIX-01` is PASS and its immutable remote result is read back.
2. BRD-09, v0.7 REV3 and the Agent Usage/CHAT Routing Contract are Owner-approved/released or explicitly bound as executable Candidates.
3. exact post-FIX `agent_bridge/**` base commit is chosen.
4. one dedicated writer/worktree is reserved.
5. exact allowed code/test/report paths are defined.
6. latest Relay/Desktop evidence is reused; no already-proven work is reimplemented.
7. Python/runtime/Agent tool availability is checked only as materially needed.
8. no overlap with another active Bridge writer.
9. STOP conditions and result paths are bound.

The intent is one whole Batch A assignment, not a chain of micro-WPs.

## 26. Definition of Done for v0.7 productization

v0.7 may be considered product-ready for the Owner's normal Windows use when:

- Worker stays running in background after normal launch;
- Start with Windows works under user session;
- Tray controls/status work;
- Pause/resume semantics are correct;
- completed dispatch survives reboot/restart without replay;
- uncertain crash is reconciled without blind duplicate launch;
- Codex direct route remains E2E functional with dispatch-pinned model/reasoning;
- Copilot direct route remains E2E functional with dispatch-owned Native Auto tier or is explicitly classified degraded;
- requested/observed Agent configuration is persisted correctly;
- available usage telemetry is persisted for both Agent result paths;
- post-start quota failure reconciles without replay/substitution;
- Tray shows model/usage state read-only without routing authority;
- no visible PowerShell is required for normal operation;
- first-run setup reports Ready/Degraded accurately;
- secrets/logging/path boundaries pass;
- one real FOX2 WP completes through the background Bridge path and CHAT independently reads back result.

Installer/community extraction is a separate release boundary and need not block internal FOX2 v0.7 use if the local installed bundle is otherwise reliable.

## 27. Non-effects

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
- declare BRD-09 acceptance tests PASS;
- create a separate DEV round for `FOX2-AGENT-USAGE-TELEMETRY-01`; its requirements are absorbed into Batch A.

`TECH_V0_7_STATUS=CANDIDATE_REV3 / EXECUTION_PLAN=FIX01_THEN_BATCH_A_THEN_BATCH_B / SIGNALING=GITHUB_MAILBOX_LOCAL_PULL / CODE_ALLOWED=NO_FROM_THIS_DOCUMENT / ACCEPTANCE=NOT_RUN`.
