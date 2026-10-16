# FOX2 Bridge RC1 — Desktop Implementation Specification

**State:** SOURCE_READY_SPEC / NON_EXECUTABLE  
**Target code root:** `agent_bridge/desktop_app/**`  
**Framework:** .NET 8 / WPF / MVVM  
**Purpose:** provide a Git-readable implementation contract for the RC1 coding Agent after fresh PreExec and CHAT assignment.

## 1. Product shell

Default window approximately 1180x760, resizable, minimum approximately 1040x680.

Navigation:
- Dashboard
- Activity
- Agents
- Diagnostics
- Artifacts
- Settings

Visual baseline:
- Background `#0B1017`
- Surface `#111923`
- Elevated `#17212D`
- Border `#263241`
- FOX Orange `#F59E0B`
- Info `#38BDF8`
- Success `#22C55E`
- Critical `#EF4444`
- Primary text `#F4F7FA`
- Secondary text `#9CA9B7`
- Muted text `#647383`
- Segoe UI Variable / Segoe UI
- restrained 8–12 px corner radius
- professional infrastructure-console presentation, not crypto/hacker styling.

## 2. Process topology

The WPF application is NOT the Worker owner.

Required topology:

```text
stable launcher
  +--> Python Worker
  +--> WPF Desktop App
```

The Worker retains Git mailbox polling, durable ledger, dispatch validation, replay protection, Agent invocation and delivery semantics.

The Desktop App is presentation/control only.

Desktop App failure or exit MUST NOT terminate the Worker.

## 3. Desktop single-instance

One interactive Windows user may have at most one active Desktop App instance.

Use a user-scoped named mutex or equivalent bounded Windows primitive.

Second launch behavior:
- do not spawn another polling/control process;
- bring/open the existing Dashboard if practical;
- otherwise exit harmlessly.

This is independent of Worker singleton enforcement.

## 4. Installation locator

Resolve the installed Bridge through:

`%LOCALAPPDATA%\FOX2\AgentBridge\current.json`

Validate `package_sha256` as lowercase 64-character SHA-256.

Resolve only:

`%LOCALAPPDATA%\FOX2\AgentBridge\versions\<package_sha256>\runtime\Scripts\python.exe`

Do not accept arbitrary runtime executable paths from UI/user input.

## 5. Fixed control client

The Desktop client may execute only:

```text
python -m fox2_agent_bridge control status
python -m fox2_agent_bridge control pause
python -m fox2_agent_bridge control resume
python -m fox2_agent_bridge control check-now
python -m fox2_agent_bridge control request-exit
python -m fox2_agent_bridge control open-logs
python -m fox2_agent_bridge control set-start-with-windows --enabled true|false
python -m fox2_agent_bridge diagnostics --output <exact-user-selected-path>
```

Process requirements:
- `UseShellExecute=false`
- `CreateNoWindow=true`
- bounded timeout
- stdout/stderr drained concurrently
- do not expose raw stderr to UI by default
- remove inherited `PYTHONPATH` and `PYTHONHOME`
- use `ArgumentList`, never shell-string concatenation.

Forbidden from Desktop code:
- `run-next`
- `poll-once`
- `e2e-once`
- Git execution
- SQLite direct access
- Codex/Copilot process launch
- prompt construction/execution
- routing decisions
- model/reasoning/permission override.

## 6. State mapping

```text
STARTING      -> Starting
RECONCILING   -> Recovering State
IDLE          -> Ready
POLLING       -> Checking
EXECUTING     -> Agent Running
PUBLISHING    -> Publishing
PAUSED        -> Paused
DEGRADED      -> Needs Attention
ERROR         -> Action Required
STOPPING      -> Stopping Safely
STOPPED       -> Offline
other         -> Unknown
```

PAUSED is neutral/amber, not critical.

While PAUSED:
- do not display a fake "next poll" countdown;
- show `Polling: Paused` or equivalent;
- Check now must not imply that pause is bypassed.

## 7. Dashboard

Dashboard must answer quickly:
1. Is Bridge healthy?
2. Is a task active?
3. What Agent/model/permission data is factually exposed?
4. What was the last result?

Cards:
- Bridge status
- Current task
- Worker status
- Agent/last execution
- Activity
- Last result

Do not expose invented global model/permission defaults.

## 8. Activity

V1 may display session-local transitions derived from Bridge status.

It MUST NOT query SQLite directly.

Suggested filters:
- All
- Tasks
- Worker
- Git
- Agent
- System

If the runtime does not expose durable event history through an approved control contract, label the list as session activity rather than fabricating history.

## 9. Agents

Display readiness/observed status for Codex and Copilot from data already exposed by Bridge Worker status.

Rules:
- no routing controls;
- no global default Agent selector;
- no direct auth command or paid health prompt from the UI;
- `NOT_EXPOSED` becomes user-readable text such as "Not provided by CLI";
- do not interpret missing numeric quota as exhaustion.

## 10. Diagnostics

Display:
- Worker state
- heartbeat
- installed package SHA
- installed source SHA if exposed
- runtime tool availability
- tool auth state when exposed
- last sanitized error

Controls:
- Open Logs
- Save Support Bundle
- Copy Diagnostic Summary

No secrets, raw credential-bearing URLs or unrestricted process stderr.

## 11. Settings

RC1 settings:
- Start with Windows
- Start minimized
- close hides app / Worker remains running
- notification preference if implemented safely
- paths/version/support information

Do NOT add:
- model selector
- reasoning selector
- permission selector
- Git delivery authority
- merge/deploy/LIVE switches.

## 12. Tray

Tray is secondary control surface.

Left-click:
- open Dashboard

Context:
- Open Dashboard
- Pause/Resume Bridge
- Check now
- Open Logs
- Exit after current task

Closing the window hides to Tray.

Only explicit graceful exit requests Worker shutdown.

## 13. Notifications

Notify only meaningful events:
- task starts
- task result pushed for CHAT review
- Bridge enters DEGRADED/ERROR
- recovery/action required

Do not notify on every idle poll.

## 14. Artifact Vault v1

Storage root:

`%LOCALAPPDATA%\FOX2\BridgeDesktop\Artifacts`

Required object flow:

```text
user selects local file
 -> validate file + size bound
 -> compute SHA-256
 -> copy to objects/<sha256>/<sanitized-name>
 -> compute SHA-256 of copied object
 -> require exact match
 -> atomic index update
 -> LOCAL_SAVED
```

Suggested index fields:
- artifact_id = `sha256:<digest>`
- file_name
- sha256
- size_bytes
- saved_at_utc
- state
- vault_path

V1 state:
- `LOCAL_SAVED`

Reserved only, not implemented as automatic transitions:
- `GIT_SYNCED`
- `RELEASED`

Artifact Vault MUST NOT:
- run Git
- mutate Bridge SQLite
- invoke Agents
- change Source Authority
- mark an artifact RELEASED
- grant DEV/merge/LIVE authority.

## 15. Project layout

Recommended:

```text
agent_bridge/desktop_app/
├─ FOX2.Bridge.Desktop.sln
├─ src/
│  └─ FOX2.Bridge.Desktop/
│     ├─ App.xaml
│     ├─ MainWindow.xaml
│     ├─ Models/
│     ├─ Services/
│     │  ├─ BridgeInstallationLocator.cs
│     │  ├─ BridgeProcessRunner.cs
│     │  ├─ BridgeControlClient.cs
│     │  ├─ ArtifactVaultService.cs
│     │  └─ TrayService.cs
│     ├─ ViewModels/
│     ├─ Views/
│     └─ Resources/
└─ tests/
   └─ FOX2.Bridge.Desktop.ContractTests/
```

## 16. Packaging integration

RC1 must integrate Desktop App into the existing verified per-user package lifecycle.

Required:
- deterministic app build/package inputs;
- stable package-relative Desktop App location;
- launcher resolves the atomic installed version;
- update switches to the complete new version, not mixed old/new binaries;
- failed update retains previous valid pointer/runtime;
- uninstall removes owned Desktop binaries but preserves intended durable user data/artifacts;
- repositories/worktrees remain untouched.

## 17. Launcher behavior

The launcher must start Worker and UI independently.

Required semantics:
- Worker launch does not depend on successful UI startup;
- UI launch does not spawn a second Worker;
- no visible console;
- duplicate launch does not create duplicate Worker/Desktop instances;
- Start with Windows invokes the stable launcher, not a version-specific mutable path where avoidable.

## 18. Tests required before pre-Canary

At minimum:
- WPF solution build PASS
- fixed-control contract tests PASS
- forbidden execution surface scan PASS
- Desktop single-instance PASS
- Worker/UI separation PASS
- close/hide-to-tray PASS
- graceful exit PASS
- installed pointer validation PASS
- support bundle PASS
- artifact SHA/copy/index PASS
- artifact isolation PASS
- package determinism PASS
- update rollback PASS
- uninstall preservation PASS
- startup single-instance PASS
- full Python Bridge regression PASS
- secret scan PASS
- diff check PASS

## 19. STOP

STOP implementation for:
- need to bypass fixed Bridge control contract;
- need for direct Git/SQLite/Agent execution from UI;
- Worker lifecycle regression;
- change outside allowed scope;
- source/task/worktree mismatch;
- secret exposure;
- inability to package/update/uninstall safely.

This spec is implementation guidance only. It is not CODE_ALLOWED and does not select an Agent. Fresh PreExec + CHAT intake remain mandatory before executable RC1 implementation.
