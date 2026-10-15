# FOX2 Bridge Desktop App v1

Native Windows control center for the existing FOX2 Bridge Worker.

## Product boundary

The Desktop App is presentation and fixed-control only. It MUST NOT:

- poll Git to discover work;
- claim dispatches;
- run Codex or Copilot directly;
- mutate the Bridge SQLite ledger;
- select or override model / reasoning / permission;
- merge, deploy, access provider/broker write surfaces, or grant LIVE authority.

All execution authority remains in the existing Python Bridge Worker.

## Technology

- .NET 8
- WPF
- MVVM
- built-in Windows tray integration
- no Electron
- no WebView
- no third-party UI framework

## Screens

- Dashboard
- Activity
- Agents
- Diagnostics
- Settings

Visual baseline: dark navy / graphite surfaces, FOX orange accents, compact professional infrastructure-console density.

## Build

From this directory on Windows with .NET 8 SDK:

    pwsh -NoProfile -File .\build.ps1

The script restores, builds Release, runs the no-dependency smoke harness, and publishes a framework-dependent win-x64 build into `artifacts\publish`.

## Install the Desktop App only

    pwsh -NoProfile -File .\install_desktop.ps1 -PublishDirectory .\artifacts\publish -Launch

This does not install, update, pause, resume, or mutate the Python Bridge Worker.

## Uninstall the Desktop App only

    pwsh -NoProfile -File .\uninstall_desktop.ps1

Settings are preserved by default.

## Runtime integration

The app resolves the installed Bridge Python from:

    %LOCALAPPDATA%\FOX2\AgentBridge\current.json
      -> versions\<package_sha256>\runtime\Scripts\python.exe

It calls only fixed existing commands:

    python -m fox2_agent_bridge control status
    python -m fox2_agent_bridge control pause
    python -m fox2_agent_bridge control resume
    python -m fox2_agent_bridge control check-now
    python -m fox2_agent_bridge control request-exit
    python -m fox2_agent_bridge control open-logs
    python -m fox2_agent_bridge control set-start-with-windows --enabled true|false
    python -m fox2_agent_bridge diagnostics --output <path>

The UI never reads or writes Git for task selection and never edits the ledger directly.
