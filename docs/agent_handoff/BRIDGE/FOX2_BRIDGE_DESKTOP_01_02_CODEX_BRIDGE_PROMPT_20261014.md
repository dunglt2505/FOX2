# FOX2 Bridge Desktop-01+02 — Codex execution

Execute the already-authorized combined work package `BRIDGE-DESKTOP-01-02`.

Before editing, read these local immutable task documents completely:

1. `docs/agent_handoff/BRIDGE/FOX2_BRIDGE_DESKTOP_01_02_SOURCE_DESIGN_LOCK_20261014.md`
2. `docs/agent_handoff/BRIDGE/FOX2_BRIDGE_DESKTOP_01_02_CODEX_EXECUTE_20261014.md`

Implement the complete bounded combined Desktop-01 + Desktop-02 scope.

Rules:

- Edit only `agent_bridge/**` and `reports/BRIDGE-DESKTOP-01-02/**`.
- Do not modify the two immutable task documents.
- Preserve FOX2 application/backend/frontend/governance/provider paths.
- No package installation unless the handoff explicitly allows it; this handoff prefers no new third-party runtime dependency.
- No provider, broker, Production, LIVE, merge, PR, deployment or main changes.
- Do not run `git add`, `git commit`, `git push`, merge, or PR. FOX2 Bridge owns Git commit/push after you exit.
- Reuse the current Operational MVP rather than rewriting it.
- Implement continuous worker + reconciliation + pause/resume/check-now + dual Agent routing/model policy + local control plane + PowerShell/.NET tray + per-user Start-with-Windows support.
- Keep Copilot CLI permissions minimal; never use `--allow-all` or `--yolo`.
- Preserve Codex workspace-write/approval-never safety boundary.
- Run all existing Bridge tests plus new Desktop tests.
- Produce `reports/BRIDGE-DESKTOP-01-02/report.md` and `reports/BRIDGE-DESKTOP-01-02/evidence_manifest.json`.
- Distinguish unit/simulated acceptance from NOT_RUN real logon/tray/manual canaries and Desktop-03 installer/community obligations.
- If a required change falls outside scope or a platform behavior cannot be safely proven, stop with a precise blocker instead of bypassing it.

When implementation, tests, result evidence, scope verification, diff check and secret scan are complete, end your final response with exactly:

`FOX2_BRIDGE_DESKTOP_01_02_DELIVERY_READY`
