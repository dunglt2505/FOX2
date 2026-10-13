# FOX2-BRD-09 — AgentBridge Desktop & Local Orchestration

**Version:** `0.1 Candidate`  
**Status:** `CANDIDATE / OWNER_REVIEW / NO_DEV_GRANT`  
**Project:** FOX2 initially; product direction supports a later generic AgentBridge distribution  
**Date:** 2026-10-14  
**Owner direction:** continue Bridge productization in parallel with FOX2 application development.  
**Technical counterpart:** `FOX2_LOCAL_AGENT_BRIDGE_TECHNICAL_SPEC_v0.7_CANDIDATE.md`  
**Governance:** FOX2 Policy V1.8.5 + Routing Index V1.2.6  
**Current runtime evidence:** Bridge Core is assessed `OPERATIONAL_MVP`; direct Copilot CLI and Codex CLI canaries have immutable Git result evidence.  
**Non-effect:** this Candidate creates no DEV, merge, deployment, provider, broker or LIVE authority.

## 1. Purpose and ownership

BRD-09 owns the **product requirements and user experience** of AgentBridge as a local desktop orchestration utility.

The product exists so the Owner can use CHAT as the coordination/control surface while approved coding work is executed locally by supported Agent CLIs without repeatedly opening PowerShell, manually navigating worktrees, or keeping VS Code open.

BRD-09 defines **what AgentBridge must do for the user**. It does not define Python classes, Windows APIs, SQLite schema, polling implementation, packaging framework or command syntax. Those HOW decisions belong to the Technical Specification.

Bridge remains a transport/launcher for already-authorized work. CHAT remains responsible for project requirements, routing and semantic review.

## 2. Product vision

Target experience:

```text
Owner talks to CHAT
    -> CHAT prepares/authorizes exact task
    -> Git dispatch becomes available
    -> AgentBridge is already running in Windows background
    -> AgentBridge discovers the task
    -> launches exact approved Copilot CLI or Codex CLI
    -> supervises the task in the exact isolated worktree
    -> publishes authorized Git result
    -> CHAT reads back and reviews
```

The normal Owner experience must not require:

- opening PowerShell for every task;
- keeping VS Code running;
- manually copying prompts after initial setup when Bridge transport is selected;
- manually creating worktrees for routine eligible Bridge tasks;
- manually checking whether an already-completed dispatch should be replayed.

PowerShell/CLI remains available for diagnostics and development but is not the normal product UX.

## 3. Primary users and operating assumptions

### 3.1 Primary user

A single Windows user who:

- owns or has authorized access to one or more development repositories;
- already has their own GitHub and Agent CLI access;
- wants CHAT to coordinate tasks while local machine resources execute them;
- may be away from the development PC and expect the Bridge to remain available while Windows is logged in.

### 3.2 Credentials and subscriptions

AgentBridge never provides or shares OpenAI, GitHub Copilot or GitHub subscriptions.

Each installation uses the **current Windows user's own authenticated Git/Agent CLI sessions**. The product must not embed the Owner's tokens, passwords or subscription credentials in distributable source, config or logs.

### 3.3 Initial platform

Windows is the first supported desktop platform. Multi-platform support is a later product decision and is not required for the initial FOX2 release.

## 4. Product requirements

| Requirement | Normative outcome | Priority | State | Acceptance |
|---|---|---:|---|---|
| `FOX2-09-R01` | One user action launches AgentBridge into a usable background state without requiring a visible PowerShell console. | P0 | SPECIFIED_CANDIDATE | T01 |
| `FOX2-09-R02` | User can enable/disable **Start with Windows**; when enabled, AgentBridge starts after that user's Windows logon. | P0 | SPECIFIED_CANDIDATE | T02 |
| `FOX2-09-R03` | AgentBridge exposes a Windows System Tray status/control surface showing Running/Paused/Error and relevant current/last task information. | P0 | SPECIFIED_CANDIDATE | T03 |
| `FOX2-09-R04` | Tray provides Pause new tasks, Resume, Sync/Check now, Open logs/status, Settings and Exit controls without creating new task authority. | P0 | SPECIFIED_CANDIDATE | T03,T04 |
| `FOX2-09-R05` | Background operation discovers only configured immutable dispatches and launches only explicitly eligible already-authorized tasks. | P0 | SPECIFIED_CANDIDATE | T05,T06 |
| `FOX2-09-R06` | Restart/crash/logoff recovery never blindly duplicates a task whose Agent execution or Git publication may already have occurred. | P0 | SPECIFIED_CANDIDATE | T07,T08 |
| `FOX2-09-R07` | Dispatch remains single-use; AgentBridge reconciles durable local state with remote Git evidence before any retry after uncertain execution. | P0 | SPECIFIED_CANDIDATE | T07,T08 |
| `FOX2-09-R08` | Exact authorized Agent product is used with no silent substitution. Initial supported adapters are Codex CLI and Copilot CLI. | P0 | SPECIFIED_CANDIDATE | T09 |
| `FOX2-09-R09` | VS Code is optional for human inspection and never a mandatory execution dependency for normal Bridge CLI operation. | P0 | SPECIFIED_CANDIDATE | T10 |
| `FOX2-09-R10` | Every execution is bound to the exact repository, branch/base, worktree, prompt/source identity and allowed write paths supplied by the authorized handoff. | P0 | SPECIFIED_CANDIDATE | T06,T11 |
| `FOX2-09-R11` | Bridge never grants DEV, merge, deployment, provider, broker or LIVE authority; it transports an authority already decided outside Bridge. | P0 | SPECIFIED_CANDIDATE | T11 |
| `FOX2-09-R12` | Pause blocks **new** Agent launches while preserving already-running work by default; Resume does not replay completed work. | P0 | SPECIFIED_CANDIDATE | T04,T12 |
| `FOX2-09-R13` | Missing CLI, expired login, offline Git, rejected dispatch, path conflict or failed task is visible as an actionable status instead of an uncontrolled retry loop. | P0 | SPECIFIED_CANDIDATE | T13 |
| `FOX2-09-R14` | Background network retries are bounded and back off when offline; simple Bridge polling must not consume Agent credits. | P1 | SPECIFIED_CANDIDATE | T14 |
| `FOX2-09-R15` | Auto-start does not mean auto-spending: only dispatches explicitly marked eligible for automatic execution may start an Agent. | P0 | SPECIFIED_CANDIDATE | T05,T15 |
| `FOX2-09-R16` | One user/profile has only one active worker for the same Bridge profile; duplicate launches do not create competing pollers/writers. | P0 | SPECIFIED_CANDIDATE | T16 |
| `FOX2-09-R17` | Product preserves safe, user-readable local logs/status while redacting secrets, credentials and unneeded Agent output. | P0 | SPECIFIED_CANDIDATE | T17 |
| `FOX2-09-R18` | First-run onboarding verifies repository/worktree locations and installed Agent CLIs, explains missing login/tool state, and does not ask the user to paste secrets into Bridge. | P1 | SPECIFIED_CANDIDATE | T18 |
| `FOX2-09-R19` | Installation/update/uninstall preserves user project repositories/worktrees by default and never deletes them as application cleanup. | P1 | SPECIFIED_CANDIDATE | T19 |
| `FOX2-09-R20` | Core orchestration remains usable from a diagnostic CLI even when Tray/UI is unavailable. | P1 | SPECIFIED_CANDIDATE | T20 |
| `FOX2-09-R21` | Architecture supports project profiles so a later generic AgentBridge Core can serve projects other than FOX2 without embedding FOX2 business rules in Core. | P1 | SPECIFIED_CANDIDATE | T21 |
| `FOX2-09-R22` | Initial FOX2 build may remain project-bound; multi-project simultaneous scheduling is not required until separately accepted. | P2 | SPECIFIED_CANDIDATE | T21 |
| `FOX2-09-R23` | A future community/open-source distribution must separate generic Bridge Core/adapters from FOX2-specific policies/configuration and remove owner paths, credentials and private/proprietary content. | P1 | SPECIFIED_CANDIDATE | T22 |
| `FOX2-09-R24` | Public/community release requires an explicit software license and release-sanitization decision; current public visibility alone is not that decision. | P1 | SPECIFIED_CANDIDATE | T22 |

## 5. System Tray UX

Minimum Tray presentation:

```text
AgentBridge
Status: Running | Paused | Error
Git: Connected | Offline
Codex CLI: Ready | Login required | Missing
Copilot CLI: Ready | Login required | Missing
Current task: <WP/dispatch or Idle>
Last result: <status + time>

[Pause new tasks / Resume]
[Check now]
[Open status/logs]
[Settings]
[Start with Windows ✓]
[Exit]
```

Status must be communicated with text, not color alone.

Tray controls do not alter task scope, permissions or acceptance. They control only local execution availability.

## 6. First-run experience

A first-run setup flow must:

1. identify or create the local Bridge runtime directory;
2. discover Git and supported Agent CLIs;
3. identify the FOX2 repository/local source location;
4. identify the worktree root;
5. read/validate the configured dispatch control source;
6. show Agent login state when supported without using a paid prompt merely as a health probe;
7. allow enabling Start with Windows;
8. run a read-only health check;
9. show a clear Ready / Degraded / Blocked result.

The flow must not require a user to paste account passwords or long-lived secrets into a project file.

## 7. Background/recovery user semantics

### 7.1 Normal operation

When Running, AgentBridge checks the configured dispatch source periodically. Polling alone does not launch an Agent or consume Agent credits.

### 7.2 Pause

Pause means:

- do not claim/launch a new Agent task;
- continue to supervise an Agent process that was already running unless the Owner explicitly cancels it;
- retain durable queue/execution status.

### 7.3 Restart

After restart:

- previously completed dispatches remain completed;
- a dispatch whose execution outcome is uncertain enters a reconciliation state;
- Bridge checks durable local ledger and remote Git result state;
- Bridge must not automatically execute a second copy merely because the old process disappeared.

### 7.4 Offline

When Git/network is unavailable:

- Bridge remains running;
- status becomes Offline/Degraded;
- retry uses bounded backoff;
- no Agent is started from stale/unverified new dispatch data.

## 8. Resource and credit behavior

AgentBridge must not fabricate an exact token/credit balance if the Agent product does not expose one.

It must distinguish:

- Agent CLI executable available;
- Agent session/login usable;
- quota/model data exposed;
- quota/model data `NOT_EXPOSED`;
- actual launch rejected because quota/access is exhausted.

A missing numeric quota display is not itself a failure when the Agent can execute.

No background test prompt may be sent solely to estimate quota unless explicitly requested and authorized.

## 9. Security and privacy requirements

- Operate under the interactive Windows user's identity by default.
- Do not default to SYSTEM/service-account execution where user Git/Agent credentials may not be available.
- Secrets are never committed to Git.
- Logs redact credentials and unsafe URL auth fragments.
- Bridge accepts only the configured repository/control source and bounded worktree roots.
- Writable paths come from an immutable authorized dispatch.
- Arbitrary shell/package/provider/broker commands are not implicitly granted.
- Tray/IPC/control surfaces are local-user scoped.
- Public FOX2 bootstrap trust may use current pinned-Git development rules, but hardened publisher/control-ref trust is required before a later confidential/private/Production operation if that operation depends on it.

## 10. Generic/community direction

The desired long-term product shape is:

```text
AgentBridge Core
  + Git dispatch transport
  + durable ledger/recovery
  + worktree supervisor
  + Agent adapter interface
      + Codex CLI adapter
      + Copilot CLI adapter
  + Windows background/tray shell
  + project profile/config
```

FOX2-specific requirements, policy texts, trading logic and proprietary project sources are **not** part of generic Core.

A later standalone repository should be created from a sanitized product boundary rather than automatically publishing FOX2 Git history.

## 11. Acceptance scenarios

These are BRD-09-specific acceptance IDs. They do **not** modify or mark PASS in the existing M1 Market Acceptance Matrix.

| ID | Scenario | Expected |
|---|---|---|
| `FOX2-09-T01` | User launches installed AgentBridge | Background Bridge becomes usable with no visible PowerShell requirement |
| `FOX2-09-T02` | Start with Windows enabled, user logs in | Bridge starts once under that user session |
| `FOX2-09-T03` | Tray opened | Accurate Running/Paused/Error, Agent readiness, current/last task shown |
| `FOX2-09-T04` | Pause then Resume | No new launch while paused; no duplicate on resume |
| `FOX2-09-T05` | New dispatch lacks explicit auto-execute eligibility | Agent is not launched |
| `FOX2-09-T06` | Eligible immutable dispatch | Correct repo/worktree/branch/prompt/path scope is used |
| `FOX2-09-T07` | Reboot after completed dispatch | Completed dispatch is not executed again |
| `FOX2-09-T08` | Crash while Agent outcome uncertain | Reconciliation occurs; no blind second launch |
| `FOX2-09-T09` | CODEX dispatch then COPILOT dispatch | Exact requested adapter used; no silent substitution |
| `FOX2-09-T10` | VS Code closed | Direct CLI task remains runnable when Agent CLI supports it |
| `FOX2-09-T11` | Dispatch requests main/merge/Production/LIVE beyond grant | Bridge rejects/blocks affected action |
| `FOX2-09-T12` | Pause while Agent already running | Existing execution remains supervised; no second task starts |
| `FOX2-09-T13` | CLI missing/auth expired/Git denied | Visible actionable status; bounded retry, no retry storm |
| `FOX2-09-T14` | Network unavailable for extended period | Backoff occurs; Bridge remains responsive; no Agent spend |
| `FOX2-09-T15` | Bridge auto-starts at login with no eligible task | No Agent prompt/credit usage occurs |
| `FOX2-09-T16` | User launches AgentBridge twice | Single active worker/profile; second launch attaches/opens Tray |
| `FOX2-09-T17` | Logs include failing Git/CLI errors | No credential/token/private-key value is emitted |
| `FOX2-09-T18` | Fresh install missing one CLI | Setup completes as Degraded with clear remediation |
| `FOX2-09-T19` | Uninstall AgentBridge | Application removed; repositories/worktrees remain intact unless explicitly selected |
| `FOX2-09-T20` | Tray process unavailable | Diagnostic CLI can still health/status/start worker as supported |
| `FOX2-09-T21` | Project profile configuration changes | Core behavior uses profile data without FOX2 business logic hardcoding |
| `FOX2-09-T22` | Standalone/community release candidate | Sanitization/license review proves no FOX2-specific secret/proprietary baggage is implicitly published |

All scenarios are `NOT_RUN` until implementation evidence exists.

## 12. Out of scope for BRD-09 v0.1

- semantic code review or acceptance inside Bridge;
- automatic task decomposition/prioritization;
- auto-rework loops;
- auto-merge/deployment;
- production market-data operations;
- broker/order/cash/margin actions;
- remote desktop control;
- mobile AgentBridge client;
- multi-user server mode;
- macOS/Linux release;
- guaranteed real-time webhook delivery;
- simultaneous arbitrary multi-project scheduling;
- automatic purchase of Agent credits/subscriptions.

## 13. Current evidence and product gap

Observed Bridge development evidence already demonstrates:

- immutable Git dispatch;
- isolated worktree resolution;
- direct Copilot CLI canary result;
- direct Codex CLI canary result;
- Bridge-owned verification/commit/push on the Codex path;
- durable ledger/replay/recovery implementation paths;
- command-line `status/health/poll-once/run-next`.

This means BRD-09 starts from **Operational MVP Core**, not from a greenfield prototype.

The remaining primary product gap is the desktop operational shell:

```text
continuous background watcher
-> restart reconciliation certification
-> Tray
-> Start with Windows
-> first-run setup
-> packaging/installer
```

## 14. Revision disposition

This is a **new BRD Candidate**. It does not supersede BRD-00/06/08 and does not change market-data/product semantics.

Owner approval/publication may later promote BRD-09 to a released version. Until then:

`BRD09_STATUS=CANDIDATE / ACCEPTANCE=NOT_RUN / CODE_ALLOWED=NO_FROM_THIS_DOCUMENT`.
