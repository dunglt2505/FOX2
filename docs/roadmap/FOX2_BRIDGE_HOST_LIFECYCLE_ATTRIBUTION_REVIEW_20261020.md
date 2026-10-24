# FOX2 — CHAT Host Lifecycle Attribution Review (Read-only, 2026-10-20)

**Whole-WP:** `FOX2-BRIDGE-RC1-TO-INTERNAL-READY` · **Feature:** `FOX2-BRIDGE-MANUAL-LOCAL-ADMISSION` · **Stage/Status:** `BUILD/BLOCKED`. **Source:** owner-supplied direct PowerShell 7 JSON, schema `FOX2_HOST_LIFECYCLE_ATTRIBUTION_V1`, observed `2026-10-20T07:17:06.0715120Z`; this is a point-in-time **host observation**, not a Git Result from the consumed Agent audit. No raw host command lines, SID, personal host path or registry value stored in this report. CHAT cannot independently read the local process table. `errors=[]`, `mode=READ_ONLY_NO_AGENT`, `replay_permitted=false`.

## Immutable source and prior gates

- Baseline governance / Feature Registry before review: `89eb879a687aab6d695d929215e04040c4d3e38a:docs/roadmap/FOX2_FEATURE_STATUS.json`; source-code forensic readback: `a3ad10d490993fb4ed4ccfd7d1a73f74cc465581:agent_bridge/src/fox2_agent_bridge/{desktop.py,paths.py}` and `agent_bridge/scripts/{desktop_startup.ps1,desktop_launcher.ps1}`. These are Git source bytes, not independently attested installed binary version.
- Previous CHAT bounded observation: `1c210139cad1f09b59ec4f1c728f00e929de57dc:docs/roadmap/FOX2_BRIDGE_HOST_LIFECYCLE_PARTIAL_OBSERVATION_REVIEW_20261020.md`.
- Previous CODEX host-audit attempt marker `VALID_RESERVATION_CONSUMED` per owner PowerShell log (reconciliation report `c6e9966eed688bb8b3286e1a2feda5acd129b5cd`), no Agent report/result, `NO_REPLAY`. Attempt01–03 coding also consumed. Git-only host evidence cannot retroactively certify agent startup.
- Six cross-root no-replay fixture tests FAIL under Attempt03 report-only result `a3ad10d490993fb4ed4ccfd7d1a73f74cc465581`. No actual installed legacy writer runtime evidence from that fixture. No CANARY/COMPAT001 deployment.

## Actual host process attribution

| PID | executable | executable root class | command root class | parent | strict conclusion |
|---|---|---|---|---|---|
| 16056 | python.exe | CURRENT_REFERENCE | CURRENT_REFERENCE | 17036 | currently running Python from a current-root executable; cannot infer ledger claim or Worker PAUSED state |
| 10940 | python.exe | OTHER | CURRENT_REFERENCE | 16056 | child of current-root Python and references current root; exact script/mode not visible; not proof of a legacy writer |
| 10476 | FOX2.Bridge.Desktop.exe | CURRENT_REFERENCE | CURRENT_REFERENCE | 17036 | installed/current-root desktop process observed; Desktop UI existence is not proof Worker claim/dispatch or readiness |
| 20300 | codex.exe | OTHER | OTHER | 18720 | FOX2 command signature NOT_OBSERVED; does not prove no in-memory FOX2 work |
| 25096 | codex.exe | OTHER | OTHER | 18720 | same limitation |

The **three previously unattributed FOX2 process candidates** are now identified at least to root class and parent relationship. Parent PID `17036` and `18720` were not themselves classified in this output; they are **UNATTRIBUTED_PARENT_PROCESSES**, not automatically legacy/current. `ONE_WRITER=UNKNOWN` remains because current Bridge process state/ledger ownership and host process attribution do not establish a protected exclusive operational writer.

## Startup and retirement boundaries

1. **Scheduled Tasks:** `CURRENT_SID_FOX2BRIDGE` Ready/enabled, `MSFT_TaskLogonTrigger`, action `pwsh.exe`, `CURRENT_REFERENCE`. Another `OTHER_FOX2_CANDIDATE` is Disabled, `MSFT_TaskTimeTrigger`, action `pwsh.exe` and `FOX2_OTHER_REFERENCE`. The second is **not proven** to target the exact legacy Bridge binary/root. A disabled one-time task alone does not durably block an executable, manual restart, scripts or other schedulers.
2. **User/common Startup folder:** 0/4 shortcuts inspected, no FOX2 target match, no unreadable shortcut. `INSPECTED_NEGATIVE` for only those shortcut surfaces.
3. **WOW6432Node Run:** HKLM Run/RunOnce each inspected, 0 match; HKCU counterpart keys absent. Earlier normal HKLM/HKCU Run/RunOnce likewise had 0 matches. Does not prove absence of other supervisors.
4. **Source semantics:** `desktop_startup.ps1` defines SID-qualified scheduled task enabled at user logon; `desktop_launcher.ps1` chooses current installed package and starts Python Bridge launcher process. Current processes and current logon task are consistent with this code, but exact installed binary provenance/controls and Worker PAUSED flag have NOT been read. `desktop.py::initialize_runtime` copies legacy DB only when current missing and holds legacy lock temporarily; `ledger.claim_dispatch` locks only one SQLite DB. The six tests still demonstrate a source-level safety contract gap.
5. **Legacy root:** known to exist from prior observation; exact `launch.ps1` absent at that root, **not** equivalent to a durable retirement/deny-all-start guard. Currently observed process list has no `LEGACY_REFERENCE`; an old writer can be invoked or resurrect after snapshot. Do not mark `DURABLE_LEGACY_RETIREMENT_VERIFIED`.

## Next actionable distinction and gating

**Current bounded success:** `PROCESS_ATTRIBUTION_COMPLETED_FOR_FIVE_OBSERVED_PROCESSES` and `STARTUP_SHORTCUTS_CHECKED`. This narrows administrative uncertainty without spending a new coding Agent attempt.

**What matters for the design now:**
- Capture read-only root category and executable basenames for parent PIDs 17036/18720 **and** the current Bridge runtime control **without invoking `fox2_agent_bridge control status`** if status command would initialize/mutate runtime; prefer passive recorded log/state if proven safe. Do not read or publish SQLite rows or tokens.
- Inspect whether the non-current disabled time-trigger task's *action* actually references `LEGACY_ROOT`, another non-current installation or a harmless unrelated FOX2 workflow; and identify other authorized launchers (old worktrees/manual invocation/reparse aliases). An `OTHER_FOX2_REFERENCE` value alone is insufficient to retire old code.
- **Independent durable fencing decision:** even if observed legacy processes=0, a restartable old executable may ignore all new current-root fences. Safe feature design requires old-binary retirement/authoritative deny-and-restart prevention or a truly jointly honored atomic identity authority. Until then, fail closed at every claim route. Future positive Manual Local/Worker admission must not be enabled by this observation.

**CHAT verdict:** `ACCEPT_PARTIAL_HOST_OBSERVATION_ONLY / HOST_RETIREMENT_NOT_VERIFIED / ONE_WRITER_UNKNOWN / BUILD_BLOCKED`. `CANARY009=HOLD`, `COMPAT001=PUBLISHED_HOLD`, `INTERNAL_READY=NOT_ATTESTED`, no merge/main, Broker/Provider/LIVE, installed Worker mutation, replay or new CODEX Agent until an independently valid new task route is bound.

**Skills:** `fox2-execution-recovery=APPLIED`, `fox2-result-review=APPLIED` as bounded evidence intake, `fox2-source-resolver=APPLIED`, `fox2-governance-preflight=APPLIED`, `fox2-status-roadmap=APPLIED`, `fox2-agent-route-runtime=APPLIED`, `fox2-feature-certification=APPLIED` for stage gates. `fox2-agent-prompt-builder=NOT_APPLICABLE` for Owner-supplied PowerShell direct observation; REQUIRED for future new Agent assignment.

**GOAL partial:** Host process/startup attribution achieved for observed scope; durable no-replay and installed retirement **not** verified. **NEXT_SAFE_ACTION:** prepare bounded passive host lineage/launcher evidence without creating a new Agent attempt, then decide an authorized durable retirement/claim-fence route. No background work.
