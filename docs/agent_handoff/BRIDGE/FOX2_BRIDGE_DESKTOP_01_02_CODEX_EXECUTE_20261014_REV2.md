# FOX2 — BRIDGE-DESKTOP-01+02 Replacement Execution Handoff REV2

**Date:** 2026-10-14  
**Combined WP:** `BRIDGE-DESKTOP-01-02`  
**Replacement dispatch:** `FOX2-BRIDGE-DESKTOP-01-02-CODEX-002`  
**Status:** `EXECUTABLE_REPLACEMENT / OWNER_DEV_AUTHORIZED / STOP_AT_PUSHED_UNREVIEWED`

## 0. Why this replacement exists

Dispatch `FOX2-BRIDGE-DESKTOP-01-02-CODEX-001` was consumed and reached terminal FAILED/WORKSPACE_BLOCKED before implementation. It MUST NOT be replayed because `max_runs=1`.

The failure was caused by two pre-edit checks that were incorrectly delegated to the CODEX sandbox:
- live remote branch verification through `git ls-remote`;
- process inventory verification through `Get-CimInstance Win32_Process`.

Those checks belong to CHAT/Bridge trust and writer-control responsibilities, not to the implementation Agent.

This REV2 corrects that handoff defect without changing BRD-09, Tech Spec v0.7 Candidate, the combined implementation scope, or the Owner's DEV authorization.

## 1. Source authority

Normative source remains unchanged:

- Source/design lock commit: `1ca353efc2ffc2f6d7eaacccac11d48897ba09ac`
- Source/design lock path: `docs/agent_handoff/BRIDGE/FOX2_BRIDGE_DESKTOP_01_02_SOURCE_DESIGN_LOCK_20261014.md`
- Source/design lock blob: `6683781beb03a9c7deea9260c2d6553798e298ad`
- BRD-09 v0.1 Candidate / Tech Spec v0.7 Candidate / readback receipt bound exactly as in that lock.
- Operational Bridge base remains `398bebf9c48e7694c69c3416a5780715f025e7b5`.

CHAT has independently verified through GitHub that the replacement task branch exists at the expected source lineage before this REV2 handoff is published.

## 2. Trust / responsibility correction

### CHAT owns
- source provenance and immutable GitHub readback;
- exact branch/base/prompt/dispatch publication;
- semantic task authorization;
- post-delivery immutable-SHA review.

### Bridge owns BEFORE Agent launch
- ledger lookup;
- replay detection;
- atomic claim;
- exact branch remote-head/base verification;
- exact worktree creation/binding;
- dirty-worktree rejection;
- singleton execution ownership / no competing Bridge execution for the same dispatch/worktree;
- immutable prompt verification.

If any Bridge prelaunch check fails, Bridge blocks before launching CODEX.

### CODEX owns
- implementation and tests inside the already-claimed exact worktree;
- result/evidence generation;
- no Git commit/push.

CODEX MUST NOT repeat Bridge/CHAT authority checks that depend on:
- outbound GitHub network access;
- Windows global process enumeration;
- administrator/elevated privileges.

Specifically, CODEX must NOT call `git ls-remote` merely to re-prove the task branch and must NOT call `Get-CimInstance Win32_Process` or equivalent global process inventory merely to re-prove writer exclusivity.

## 3. CODEX local pre-edit gate

After Bridge has launched CODEX in the exact worktree, CODEX only needs to verify:

1. current directory is exactly the dispatched worktree;
2. `git rev-parse HEAD` equals the dispatch `base_sha`;
3. `git status --porcelain` is clean at start;
4. the immutable local source/design lock blob hashes to `6683781beb03a9c7deea9260c2d6553798e298ad`;
5. allowed write scope is exactly:
   - `agent_bridge/**`
   - `reports/BRIDGE-DESKTOP-01-02/**`

These local checks are sufficient for CODEX because Bridge has already completed claim/worktree/remote validation before launch.

## 4. Combined implementation scope

Implement the same Desktop-01 + Desktop-02 scope already authorized:

- continuous per-user background Worker;
- pause/resume/check-now;
- bounded backoff;
- durable worker state;
- restart/reconciliation without blind replay;
- exact CODEX/COPILOT routing;
- Copilot native Auto / pinned model policy with minimal permissions;
- Codex pinned model/reasoning support while preserving workspace-write and approval-never;
- local fixed-command control plane;
- PowerShell 7 / .NET System Tray;
- per-user Start-with-Windows registration;
- full existing Bridge regression + new Desktop tests;
- report/evidence manifest.

Desktop-03 installer/setup/community extraction remains out of scope.

## 5. Exact write scope

Allowed:
- `agent_bridge/**`
- `reports/BRIDGE-DESKTOP-01-02/**`

Everything else read-only.

No package installation unless already available runtime tooling is used. No PR, merge, main, deployment, provider, broker or LIVE.

## 6. Testing requirements

Run all existing Bridge tests plus new deterministic Desktop-01+02 tests.

Required evidence includes:
- idle polling causes no Agent invocation;
- pause/resume/check-now;
- singleton worker;
- bounded backoff/reset;
- recovery at pre-Agent/RUNNING/AGENT_EXITED/PUBLISHING;
- published result reconciliation without replay;
- uncertain execution never blind-replays;
- exact CODEX/COPILOT routing;
- no silent substitution;
- Copilot Auto and pinned-model command construction;
- Codex model/reasoning command construction;
- control commands while worker is alive;
- Tray fixed-action mapping;
- Task Scheduler command generation/idempotence in mocked/dry-run tests;
- log/secret redaction;
- changed-path allowlist;
- `git diff --check`.

## 7. Branch / worktree

Replacement task branch:
`work/FOX2-BRIDGE-DESKTOP-01-02-R2-codex`

Replacement worktree:
`C:\Projects\FOX2-worktrees\FOX2-BRIDGE-DESKTOP-01-02-R2-CODEX`

Single writer:
CODEX via Bridge after successful claim.

The old worktree `C:\Projects\FOX2-worktrees\FOX2-BRIDGE-DESKTOP-01-02-CODEX` contains terminal blocker-report WIP from dispatch 001 and MUST NOT be reused or cleaned by this replacement task.

## 8. Result Contract

Required:
- `reports/BRIDGE-DESKTOP-01-02/report.md`
- `reports/BRIDGE-DESKTOP-01-02/evidence_manifest.json`
- optional evidence below `reports/BRIDGE-DESKTOP-01-02/evidence/**`

Final required marker:
`FOX2_BRIDGE_DESKTOP_01_02_DELIVERY_READY`

Stop at:
`PUSHED_UNREVIEWED`

## 9. Gate snapshot

```text
DISPATCH_001=TERMINAL_FAILED_DO_NOT_REPLAY
REPLACEMENT=FOX2-BRIDGE-DESKTOP-01-02-CODEX-002
CHAT_SOURCE_PROVENANCE=VERIFIED
BRIDGE_PRELAUNCH_REMOTE_CHECK=REQUIRED
BRIDGE_LEDGER_CLAIM=REQUIRED
BRIDGE_SINGLETON_OWNERSHIP=REQUIRED
CODEX_REMOTE_RECHECK=NOT_REQUIRED
CODEX_GLOBAL_PROCESS_ENUMERATION=NOT_REQUIRED
OWNER_DEV_AUTHORIZATION=YES
CODE_ALLOWED=YES_TASK_ONLY
MERGE_ALLOWED=NO
PRODUCTION_PROVIDER=NO
BROKER_WRITE=NO
LIVE=NO
```
