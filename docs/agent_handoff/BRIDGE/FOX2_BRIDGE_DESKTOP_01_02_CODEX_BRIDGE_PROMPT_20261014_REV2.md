# FOX2 Bridge Desktop-01+02 — CODEX replacement execution REV2

Execute the already-authorized combined work package `BRIDGE-DESKTOP-01-02` under replacement dispatch `FOX2-BRIDGE-DESKTOP-01-02-CODEX-002`.

Read completely before editing:

1. `docs/agent_handoff/BRIDGE/FOX2_BRIDGE_DESKTOP_01_02_SOURCE_DESIGN_LOCK_20261014.md`
2. `docs/agent_handoff/BRIDGE/FOX2_BRIDGE_DESKTOP_01_02_CODEX_EXECUTE_20261014_REV2.md`

Important responsibility correction:

- CHAT already owns source provenance and GitHub readback.
- Bridge owns ledger/replay/atomic claim/remote branch-head verification/worktree binding/single-writer enforcement before CODEX launch.
- Do NOT call `git ls-remote` merely to re-prove remote task HEAD.
- Do NOT call `Get-CimInstance Win32_Process` or any equivalent global process inventory merely to re-prove writer exclusivity.
- Do NOT escalate privileges or relax sandbox/network controls to perform those checks.

Your local pre-edit checks are only:
- exact current directory equals dispatched worktree;
- `git rev-parse HEAD` equals the dispatch base SHA;
- `git status --porcelain` is clean;
- local immutable source/design lock blob matches the bound blob;
- write scope is exactly `agent_bridge/**` and `reports/BRIDGE-DESKTOP-01-02/**`.

Then implement the full combined Desktop-01+02 scope:

- continuous per-user Worker;
- pause/resume/check-now;
- bounded backoff;
- durable worker state;
- restart/reconciliation with no blind replay;
- exact CODEX/COPILOT routing and no silent substitution;
- Copilot native Auto / pinned model support with minimal permissions;
- Codex model/reasoning support preserving workspace-write + approval-never;
- fixed local control plane;
- PowerShell 7/.NET System Tray;
- per-user Start-with-Windows;
- full existing Bridge regression plus new deterministic Desktop tests.

Rules:

- Edit only `agent_bridge/**` and `reports/BRIDGE-DESKTOP-01-02/**`.
- Do not modify BRD/Tech Spec/governance/application/provider/frontend/.github paths.
- Do not clean/reset/stash the old terminal worktree.
- No package installation unless already authorized by the handoff.
- No provider, broker, Production, LIVE, PR, merge, deployment or main changes.
- Do not run `git add`, `git commit`, or `git push`; Bridge owns Git publication.
- Produce:
  - `reports/BRIDGE-DESKTOP-01-02/report.md`
  - `reports/BRIDGE-DESKTOP-01-02/evidence_manifest.json`
- Distinguish simulated/unit evidence from NOT_RUN real logon/manual paid Agent canaries and Desktop-03 obligations.

When implementation, tests, scope verification, diff check, and report secret scan are complete, end your final response with exactly:

`FOX2_BRIDGE_DESKTOP_01_02_DELIVERY_READY`
