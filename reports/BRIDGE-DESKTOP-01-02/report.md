# BRIDGE-DESKTOP-01+02 replacement delivery

Dispatch: `FOX2-BRIDGE-DESKTOP-01-02-CODEX-002`. Delivery is local, uncommitted,
and ready for Bridge-owned Git publication and CHAT immutable-SHA review.
This report does **not** claim `PUSHED_UNREVIEWED` has already been reached.

## Local execution gate

- Exact worktree: `C:\Projects\FOX2-worktrees\FOX2-BRIDGE-DESKTOP-01-02-R2-CODEX`.
- Initial HEAD and locally cached dispatch base both:
  `4778d78a11e844b6938157fcb0532664169a68d3`.
- Initial `git status --porcelain`: empty.
- Local source/design lock blob: `6683781beb03a9c7deea9260c2d6553798e298ad`.
- Both named handoffs were read completely before editing. Dispatch 002 was
  read from Bridge's existing local Git cache to obtain its base and exact scope.
- Write allowlist: `agent_bridge/**`, `reports/BRIDGE-DESKTOP-01-02/**`.

Source provenance/readback remains CHAT-owned. Claim, replay, remote branch HEAD,
worktree binding and writer exclusivity remain prelaunch Bridge responsibilities.
No remote task-HEAD recheck, global process inventory, elevation, control relaxation,
package installation, or old terminal-worktree cleanup was performed.
The operational base is `398bebf9c48e7694c69c3416a5780715f025e7b5`; dispatch base
includes the source-lock and replacement handoff lineage. Candidate source remains
Owner-bound Candidate, with released governance unchanged.

## Implementation

The continuous per-user Worker reuses the poller, immutable dispatch validator,
atomic ledger claim, selected Agent adapters, and result publication verifier.
It persists generation, start/heartbeat/stop, pause, check-now generations, stop
request, last poll/backoff/result/error, current dispatch, recovery, tool discovery,
execution stage and requested/observed Agent metadata. Healthy polling defaults
to 30 seconds. Failure backoff is 30/60/120/300 seconds, capped at 300, with reset
after successful Git contact. Idle polling does not call an Agent.

The Worker and one-shot runners share the OS-backed singleton. Fixed SQLite
controls remain accessible while that lock is held; there is no TCP listener or
arbitrary shell/prompt IPC. Pause/exit also gate the atomic claim transaction, so
a request arriving during discovery prevents new execution. Check-now is durable;
pause preserves it. Graceful exit lets the active task finish. Heartbeats continue
during long Agent execution. Error state and its diagnostic survive shutdown.

Runtime defaults to `%USERPROFILE%\AppData\Local\FOX2\AgentBridge`. First use
snapshots an existing legacy ledger read-only under its legacy singleton before
polling, preserving all previously consumed identities. If the legacy supervisor
still runs, bootstrap blocks. Schema 4 adds durable worker/checkpoint data without
discarding earlier dispatches, results, cursors or review evidence. The shared
existing Python runtime is reused; no environment or package is installed.

Recovery distinguishes CLAIMED, RUNNING, AGENT_EXITED, PUBLISHING and old UNKNOWN
checkpoints. Proven pre-launch claims become SAFE_NOT_STARTED with the original
single-use identity retained. Uncertain execution becomes NEEDS_RECONCILIATION.
No timeout or age grants replay. Post-Agent recovery verifies exact worktree
branch, cleanliness, base ancestry, authorized remote branch HEAD, changed-path
scope and required result/marker evidence. When recorded, the expected publication
SHA must match. Validated remote results recover as PUSHED_UNREVIEWED without an
Agent call. Unpublished/dirty/offline cases require explicit safe review or a fresh
dispatch; this implementation deliberately does not resume publishing uncertain WIP.

CODEX and COPILOT routing is exact, including continuous auto-execute selection.
Missing/login/quota/nonzero failures never invoke the other product. Definitive
pre-spawn capability/tool failures are terminal; ambiguous spawn/execution or
publication failures retain reconciliation evidence. Copilot supports native
`--model auto` and pinned models, requires non-interactive support, uses JSON output
when exposed, and permits only explicit write/catalogued shell grants. Dispatched
Copilot receives no Git wildcard permission; Bridge publishes both products'
uncommitted results. Prompts must leave Git publication to Bridge. No allow-all,
yolo, unrestricted Autopilot, or global Copilot settings mutation is used.

Copilot Auto defaults to balance. Task-local tier enforcement is conservatively
`AUTO_TIER_NOT_ENFORCED`; no speculative tier flag or unsafe profile/auth handling
is introduced. Explicit credit bounds fail closed if the CLI cannot enforce them.
Codex supports CURRENT_CONFIG, PINNED model and low/medium/high reasoning while
retaining approval-never, workspace-write and the existing unelevated Windows
fallback. The existing dispatch spelling PINNED_PREFERRED is treated as an exact
pin; unsupported pins fail rather than falling back. CLI capabilities are checked
through help, with no paid discovery invocation. Observed model/effort comes only
from explicit structured output; missing observations remain unknown. Quota
NOT_EXPOSED is not interpreted as exhausted. Adapter streams, ledger/checkpoints,
runtime reports and logs are redacted.

PowerShell 7/.NET NotifyIcon provides Running/Paused/Degraded/Error visibility,
current task and last result, Pause/Resume/Check now/Open logs/Start with Windows/
Exit. The normal launcher and child processes use hidden windows. A SID-qualified
Tray mutex and shared Worker lock prevent duplicate hosts/execution. Open logs
uses only the configured local directory. Startup registration is a SID-qualified
current-user interactive logon task with Limited privileges, no password, idempotent
enable/disable, and removal limited to its named Bridge registration. The internal
source/launcher location must remain available; packaging belongs to Desktop-03.

## Evidence and verification

`evidence/pytest.xml` and `evidence/pytest.txt` record the full Bridge suite and new
deterministic Desktop tests. Final outcome: **120 passed**. New Desktop coverage:
43 tests, including parameterized cases. No paid Agent, broker or provider is used.

| Evidence | Classification | Outcome |
| --- | --- | --- |
| Existing config/path/hash/logging/health/ledger/adapters/poller/runner regressions | Unit/local regression | PASS |
| Idle, pause/resume/check-now, atomic paused claim, controls with singleton held | Deterministic unit/local SQLite and OS lock | PASS |
| Backoff bounds/reset, graceful active-task exit, durable pause/lifecycle | Deterministic unit | PASS |
| CLAIMED/RUNNING/AGENT_EXITED/PUBLISHING/UNKNOWN recovery and completed result without replay | Simulated result verifier plus real ledger | PASS |
| Exact result branch, ancestry, remote SHA, scope, required artifact/marker verification | Mocked Git responses with local artifacts | PASS |
| Legacy snapshot and versioned migration preserve consumed claims/results | Real local SQLite and OS locks | PASS |
| Exact Agent routing, no failure fallback, Auto/pinned/reasoning/credits/unknown quota metadata | Fake Agents and CLI capability fixtures | PASS |
| PowerShell script parsing and NotifyIcon/Timer construction/disposal without visible icon | Actual installed PowerShell/.NET, headless | PASS |
| Tray action/state/hidden-launch mapping and singleton design | Static contract plus OS singleton tests | PASS |
| Startup repeated enable and repeated disable | Actual PowerShell execution with mocked scheduler cmdlets | PASS |
| Changed paths, diff whitespace and report secret scan | Local verification script | PASS; see evidence/verification.json |

The original poller fixture's Git file transport hit managed-sandbox MSYS signal
pipe denial. The final fixture simulates only local remote transport using native
object/ref plumbing. Commit histories, blob identities, ancestry queries, discovery
and SQLite transactions remain real. Fixture generation uses update-index,
write-tree, commit-tree and update-ref in isolated test repositories. This is
**simulated transport evidence**, not a GitHub/network canary. Preliminary fixture
runs exercised the original temporary-repository seed helpers; the dispatched
task index/HEAD and all remote task branches were never published or changed by CODEX.
Windows pytest mode-0700 temporary directories were also inaccessible; fixtures
now inherit workspace ACLs under ignored `agent_bridge/test_artifacts`, without
changing permissions or sandbox controls. Preliminary failures were environmental;
the final full run has no failures or skips.

## Acceptance boundary and remaining obligations

The source lock's Desktop-01+02 mapping covers T01/T02/T03/T04 and
T05/T06/T07/T08/T09/T10/T11/T12/T13/T14/T15/T16/T17/T20. The implementation and
unit/simulated evidence above support that mapping. **This is not blanket real-world
acceptance certification.** Real Windows logon/startup, manual Tray interaction,
normal hidden-launch usability, actual installed-CLI policy behavior and paid Agent
canaries are **NOT_RUN** and require authorized manual/canary evidence. Actual
Auto-selected model/tier/credit enforcement is not claimed from fake CLI fixtures.

T18/T19 setup/installer/update/uninstall obligations remain **Desktop-03 / NOT_RUN**.
T21/T22 generic/community extraction remains later scope. No packaging, install,
uninstall, community release, provider/broker/Production/LIVE, PR, merge, deployment
or main change is claimed. No task Git add/commit/push was performed. Bridge owns
publication; CHAT owns post-delivery review. The old terminal worktree is untouched.

Reproduce with existing tooling, from this worktree:

```powershell
$env:PYTHONPATH = Join-Path $PWD 'agent_bridge/src'
python -m pytest agent_bridge/tests -q -p no:cacheprovider --junitxml reports/BRIDGE-DESKTOP-01-02/evidence/pytest.xml
python agent_bridge/scripts/validate_desktop_delivery.py
```
