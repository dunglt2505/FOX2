# FOX2 — Legacy/Current Host Lifecycle Inventory Contract (READ-ONLY CANDIDATE)

**Date:** 2026-10-20 · **Reviewer/owner:** CHAT · **Whole-WP:** FOX2-BRIDGE-RC1-TO-INTERNAL-READY · **Existing feature:** FOX2-BRIDGE-MANUAL-LOCAL-ADMISSION.
**Action classification:** READ_ONLY host evidence, not Agent assignment, PreExec, runtime adoption, or release. No coding Attempt 04 issued. Previous Attempts 01, 02, 03 are consumed / no replay.

## Verified starting evidence

- CODEX Attempt03 report-only result `work/FOX2-BRIDGE-MANUAL-LOCAL-ADMISSION-DEV-20261019-NATIVE-ATTEMPT-03@a3ad10d490993fb4ed4ccfd7d1a73f74cc465581`, `BLOCKED`; six cross-root no-replay negative tests remain FAIL, standalone current-then-legacy process restart fixture returned duplicate claim. No production change. CHAT-owned review `c659100b785ee75fdbe12b851ee30ec1d3aaf352:docs/roadmap/FOX2_BRIDGE_MANUAL_LOCAL_ATTEMPT03_CHAT_RESULT_REVIEW_20261020.md`; Feature Registry `95d528b130909de44774deb69207ec4bd59f82e4:docs/roadmap/FOX2_FEATURE_STATUS.json` is `BUILD/BLOCKED`.
- Immutable code `a3ad10d490993fb4ed4ccfd7d1a73f74cc465581:agent_bridge/src/fox2_agent_bridge/desktop.py` specifies `LEGACY_ROOT=C:\Projects\FOX2-AgentBridge` and `BRIDGE_ROOT=Path.home()/AppData/Local/FOX2/AgentBridge`. These are source-default claims, not observed installed locations.
- `agent_bridge/scripts/desktop_startup.ps1` blob `543f9b93e6257eb03e876da78d50d6e41a756faa`: exact SID-qualified task name `FOX2Bridge-` + current user SID, triggered at logon, limited interactive principal, action runs `pwsh.exe` and an installed `%LOCALAPPDATA%\FOX2\AgentBridge\launch.ps1` (fallback scripts/desktop_launcher.ps1).
- `agent_bridge/scripts/desktop_launcher.ps1` blob `1db524e98324893076322fc1b87a59972998a4c8`: reads `current.json` package pointer and per-version isolated payload. Local source does not prove this launcher or its installed version is running.
- `agent_bridge/src/fox2_agent_bridge/startup.py` blob `c1dc5757117698403d843e7c313e2398fe7bdf59` uses a current-user startup task. Further startup routes, per-user Run/RunOnce registry, startup shortcuts, old Windows tasks/services and externally owned schedulers **may exist** and are not excluded by these files.

## Read-only evidence collection requirements

Use PowerShell 7 only for host read-only enumeration; never execute launcher, import/snapshot SQLite data, open/change durable claim, stop processes, disable tasks, delete registry value or modify installed directories. The Owner runs a complete inline script in CHAT (not an Agent Dispatch).

Collect UTC timestamp / OS and current-user scope; exact intended root existence and directory metadata (legacy and current), installed pointer FILE PRESENCE AND HASH only (do not collect file contents, credential material or private user config); file identities/hashes for known launchers; inspect reparse/symlink state. Record local presence of data/bridge.db and data/manual_consumption.json only as metadata (size and existence; do not disclose their bytes). Detect processes whose executable path/command has FOX2/AgentBridge signatures, redact all full command-line content and environmental secrets. Detect current-user scheduled tasks especially `FOX2Bridge-<SID>` and any FOX2-related task/action; report task state, principal scope, trigger type, executable basename and whether arguments reference relevant launcher patterns. Inspect HKCU/HKLM Run and RunOnce key names and presence of FOX2-looking values only, not raw value strings. Inspect user/common Startup shortcuts only for FOX2-linked metadata, not full target argv. Optionally inspect Windows services matching FOX2 and source paths, read-only. All errors/privilege-denied probes remain UNKNOWN, not FALSE.

Keep any host export **local/private** until CHAT review; DO NOT automatically push to public Git, include raw command lines, usernames/SIDs, registry value content, credentials, binary packages, SQLite bytes or token-bearing config. A ZIP with sanitized JSON and SHA-256 can be attached privately to CHAT; CHAT verifies bytes, assesses gaps and publishes only a separately reviewed redacted decision/receipt to non-main Git if allowed.

## Review matrix

- `LEGACY_WRITER_PRESENT`: process/task/startup or eligible executable found; NOT a claim it is actively trading. No new Manual Local claims; assess source/exit/restart and explicit host-only retirement proposal under fresh authority.
- `NO_LEGACY_ENTRYPOINT_OBSERVED_IN_SCOPED_INVENTORY`: limited negative observation; **NOT** `LEGACY_DURABLY_RETIRED`. Must prove all authorized startup surfaces, old binary/aliases and durable fencing before positive claim.
- `UNKNOWN/INCOMPLETE`: incomplete enumeration, hidden scheduler, reparse alias, privilege issue, absent logs or unknown installer/supervisor; FAIL CLOSED.
- `DURABLE_RETIREMENT_VERIFIED` is NOT available from the inventory alone. Requires a distinct decision: exact old binaries and their launchers, disabled/replaced entrypoints, immutable evidence of authority/supervisor controls, restart behavior and rollback/no-replay tests, with installed version provenance. This inventory NEVER grants that state.
- If a jointly honored old/new identity authority is shown by both executable implementations, CHAT may evaluate a separate migration design. Do not infer old binary recognizes new fence.

## Gates and continuation

`READ_ONLY/HOST_DATA_COLLECTION`: source Git readback = verified; Owner host execution = PENDING. No coding agent, task prompt or PreExec is required for this **read-only** inventory. A task-specific agent PreExec will be mandatory for any subsequent executable DEV/release task. No Agent attempts, no main, no merge, no installed Worker resume, no Canary009/COMPAT001, no provider/broker/LIVE.

**Next safe action:** receive sanitized actual host inventory; CHAT audit against this contract and detect exact legacy lifecycle gap. If host evidence remains insufficient, preserve `BUILD/BLOCKED` and create a candidate fail-closed design rather than burning another Agent invocation.
