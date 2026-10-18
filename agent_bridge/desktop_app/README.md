# FOX2 Bridge Desktop RC1

Native .NET 8 WPF/MVVM presentation and fixed local controls. Worker and Desktop are independent siblings started by the installed stable launcher. Closing X hides Desktop to Tray; only explicit graceful exit requests Worker shutdown.

Build: `dotnet build agent_bridge/desktop_app/FOX2.Bridge.Desktop.sln -c Release`.

Contract checks: set `FOX2_TEST_PYTHON` to a local Python interpreter and run `dotnet run --project agent_bridge/desktop_app/tests/FOX2.Bridge.Desktop.ContractTests -c Release`.

`build_user_package.py` publishes a self-contained win-x64 Desktop with the offline Python wheel package. Install with the existing Bridge `install --package <zip> --sha256 <independently-verified-sha256>` command, run `setup`, then use `%LOCALAPPDATA%/FOX2/AgentBridge/launch.ps1`. Existing completed setups can start offline. The pointer switches only after a complete runtime is verified. Startup is current-user, limited and interactive.

Desktop resolves only the fixed installed pointer and permits seven control actions plus bounded support export. It never opens the Bridge ledger or invokes Git or Agents. Desktop has both a user singleton and a presentation lock; uninstall refuses live mapped Desktop binaries before deleting any version. Stop via Exit after current task before uninstalling. Updates retain old versions until uninstall and preserve config, data, logs, reports and the separate Artifact Vault.

Artifact Vault stores explicit local selections up to 100 MiB at `%LOCALAPPDATA%/FOX2/BridgeDesktop/Artifacts`. Objects and their SHA-256 are verified before atomic index replacement. RC1 implements LOCAL_SAVED only; Git synchronization and release transitions are absent.

No authorized FOX2 icon exists in the bound source tree. A generic Windows application icon is used; the branded icon remains an explicit acceptance item for CHAT/independent audit.

Runtime certification: `certify_rc1_installed.py` requires an already paused installed profile. It tests real UI automation, lifecycle, startup, support export, explicit artifact selection, safe installed polling with Worker stopped, uninstall and reinstall. It never invokes an Agent or Canary. Partial attempt receipts remain evidence; rerunning operational checks is not replaying an Agent Dispatch.

Current RC1 WIP is STOPPED_NEEDS_RECONCILIATION: a fresh save through the final installed UI was not established after bounded native-picker automation repair. Core checks pass, but existing Vault records are not fresh UI evidence. The certifier now rejects stale/unverified manual receipts before mutation. Independent audit and branded icon acceptance remain open. Do not replay Dispatch RC1-CODEX-003.
