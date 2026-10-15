# FOX2 Bridge Desktop App v1

Native Windows control center for the existing FOX2 Bridge Worker.

## Product boundary

The Desktop App is presentation and fixed-control only. It MUST NOT poll Git to discover work, claim dispatches, run Codex or Copilot directly, mutate the Bridge SQLite ledger, override model / reasoning / permission, or grant main / merge / deploy / provider / broker / LIVE authority.

## Distribution

The ready-built Windows artifact is self-contained win-x64. No separate .NET installation is required.

After extracting the artifact, install and launch with:

    pwsh -NoProfile -File .\install_desktop.ps1 -Launch

Verify passive integration with the existing Bridge using:

    pwsh -NoProfile -File .\verify_desktop.ps1

Uninstall only the Desktop App using:

    pwsh -NoProfile -File .\uninstall_desktop.ps1

The installer writes only under %LOCALAPPDATA%\FOX2\BridgeDesktop and creates a Start Menu shortcut. It does not install, update, pause, resume, or mutate the Python Bridge Worker.

## Runtime integration

The app resolves installed Bridge Python from %LOCALAPPDATA%\FOX2\AgentBridge\current.json and calls only the existing fixed control/status/diagnostics CLI contract.

The UI never reads or writes Git for task selection and never edits the ledger directly.
