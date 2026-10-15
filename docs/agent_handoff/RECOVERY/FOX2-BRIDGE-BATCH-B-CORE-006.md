# FOX2 Bridge Desktop Batch B — Core continuation 006

**Status:** SOURCE_READY / WAIT_CURRENT_PREEXEC / NON_EXECUTABLE (not an Agent dispatch)
**Owner decision:** Uninstall deferred. Focus on making Bridge Core usable; no more uninstall recovery micro-dispatches.
**WP:** `FOX2-BRIDGE-DESKTOP-BATCH-B` — single whole-WP continuation; preserve all prior code.
**Source:** `work/FOX2-BRIDGE-DESKTOP-BATCH-B` @ `e8598a1a2933fe3c640bfb4c34c3cbfd59b37ed2`.
**Policy:** Project Dictionary v1.2 -> FOX2 Policy V1.8.9 -> Routing Index V1.3.0 -> PreExec v1.1 -> Dispatch v3 -> Git-first Protocol v12.
**Owner decision authority:** `docs/agent_handoff/RECOVERY/FOX2-BRIDGE-BATCH-B-OWNER-DEFER-UNINSTALL-20261015.md` @ `de406f2d2f29a8b349151813482609758f693e0c`.

## Preserve state — zero rediscovery
- Dispatches 001–005 CONSUMED; NEVER replay. The 005 report-only commit is `e8598a1a`; no source code changed in 005.
- Recovered 17 code files are saved; 354 tests PASS before 004. In 004, repaired Tray graceful exit, 5/5 focused regressions PASS, real worker shutdown/lock release PASS; retain as historical evidence, not current full-certification PASS.
- Current per-user installation is quarantined: its pointed version is partially uninstalled (10 receipt payload files + installed module missing); retained data/config/ledger/reports. NEVER launch, uninstall, reinstall, modify pointer, delete or kill processes in this compromised root without a distinct safe recovery authorization.
- `UNINSTALL_PATH=DEFERRED_OWNER_PRIORITY`, previous failure remains factual. Do NOT label this PASS. `INTERNAL_FOX2_BRIDGE_READY=NO` until the normative 24-gate acceptance/approved scope change is resolved.

## One bounded execution package; no fragments
After fresh PREEXEC PASS + CHAT readback, the single selected Agent runs the following **in ONE Dispatch**:

1. Use the existing source as-is first; do not rewrite previously working subsystems, Batch A or Shared PreExec.
2. Establish a **separate disposable Windows user profile/runtime root** (must not resolve to the existing `%LOCALAPPDATA%\FOX2\AgentBridge` path). Record both resolved roots before tests. Fail closed on overlap. Run Python/Pwsh inside isolated profile with pinned source and only test assets.
3. Test CORE, not uninstall: source-config/setup and per-user installation in isolation; deterministic package/install/update; Worker/Tray healthy PAUSED mode, exactly one Worker, heartbeat and graceful exit, shutdown/lock release; source-current Dictionary/Dispatch-v3/legacy compatibility, eligible safe fixture dispatch, selected Agent route and Full Access, Git non-main result/readback, usage snapshot, restart/no replay, sanitized diagnostics.
4. Reuse a valid targeted PASS if code inputs are unchanged; otherwise run targeted regressions. Run full pytest **once** after substantive code changes, not multiple times for tracing.
5. Fix only confirmed CORE defects affecting these gates, within `agent_bridge/**`. If no defect is found, do not churn source. NEVER change core trading/provider/broker code or send LIVE instructions.
6. Record a per-gate status for the **existing 24 identities**, distinguishing verified fresh PASS, historical evidence, deferred uninstall, NOT_RUN, and FAIL. `UNINSTALL_PATH=DEFERRED_OWNER_PRIORITY` is NOT a release PASS.
7. Publish one report and provenance/evidence under `reports/BRIDGE-DESKTOP-BATCH-B/**`, source code within `agent_bridge/**` only if needed, one final Git non-main commit/push/readback. Result `BRIDGE_CORE_VALIDATED / PUSHED_UNREVIEWED` ONLY if core tests really passed; never `INTERNAL_FOX2_BRIDGE_READY` unless all normative release gates are formally satisfied and CHAT accepts.

## Safety and STOP boundary
- PreExec/Agent permission/Current quota, exclusive worktree owner, source HEAD and clean Git, toolchain and pinned Agent route must be proven at launch. No concurrent writer; CODE_ALLOWED requires a separate valid executable Dispatch.
- Stop only for a **material** problem: source drift/writer collision, Agent auth or quota, core test failure needing a real fix, no safe disposable runtime, data/ledger/replay compromise, out-of-scope mutations, secrets, or remote publication failure. A damaged quarantined install alone must not stop isolated core DEV.
- Git scope is exactly `work/FOX2-BRIDGE-DESKTOP-BATCH-B` worktree `C:\Projects\FOX2-worktrees\FOX2-BRIDGE-DESKTOP-BATCH-B`, writable paths `agent_bridge/**` and `reports/BRIDGE-DESKTOP-BATCH-B/**`. No PR/main/merge/deploy/provider/broker/LIVE.
- This file is a prepared source contract ONLY. Publish a new single-use Dispatch 006 **after** fresh current-source PreExec receipt is published and independently verified by CHAT. Do not replay 005.

## Single current PREEXEC gate (Windows)
```powershell
$ErrorActionPreference="Stop"
$wt="C:\Projects\FOX2-worktrees\FOX2-BRIDGE-DESKTOP-BATCH-B"
$sha="e8598a1a2933fe3c640bfb4c34c3cbfd59b37ed2"
if ((git -C $wt rev-parse HEAD).Trim() -ne $sha) { throw "STOP: local HEAD mismatch" }
if (@(git -C $wt status --porcelain=v1 --untracked-files=all).Count) { throw "STOP: dirty worktree" }
python -B "$wt\agent_bridge\scripts\preexec.py" --profile bridge --worktree $wt --source-head $sha --publish
if ($LASTEXITCODE) { throw "STOP: preexec failed" }
```
