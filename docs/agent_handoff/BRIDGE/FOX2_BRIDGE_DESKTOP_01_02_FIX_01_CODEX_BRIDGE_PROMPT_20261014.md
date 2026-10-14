# FOX2 Bridge Desktop-01+02 FIX-01 — CODEX corrective prompt

Execute corrective WP `BRIDGE-DESKTOP-01-02-FIX-01` only when this prompt is reached through its future executable Bridge dispatch.

Read completely before editing:

1. `docs/agent_handoff/BRIDGE/FOX2_BRIDGE_DESKTOP_01_02_FIX_01_SOURCE_LOCK_20261014.md`
2. `docs/agent_handoff/BRIDGE/FOX2_BRIDGE_DESKTOP_01_02_FIX_01_CODEX_EXECUTE_20261014.md`
3. parent `docs/agent_handoff/BRIDGE/FOX2_BRIDGE_DESKTOP_01_02_SOURCE_DESIGN_LOCK_20261014.md`

Correct only the locked CHAT findings:

- post-launch/non-zero Agent exit must conservatively become `NEEDS_RECONCILIATION`, retain consumed identity, never auto-replay, never substitute Agent;
- preserve proven pre-spawn terminal/actionable failures;
- add regression tests for the quota-stop/non-zero-after-start path;
- fix all `git diff --check` defects;
- successfully regenerate `evidence_manifest.json` and `evidence/verification.json`;
- update `report.md` to the true recovery-published history and FIX-01 lineage;
- rerun the full Bridge suite and validator.

Exact write scope:

- `agent_bridge/**`
- `reports/BRIDGE-DESKTOP-01-02/**`

Everything else is read-only.

Do not redesign Desktop Worker/Tray/Startup except where the narrow recovery bug requires a code change. Do not expand Desktop-03, packaging, generic/community extraction, application code, governance, provider, broker, Production or LIVE.

Do not run git add/commit/push. Bridge owns publication.

Mandatory final gates:

- full Bridge pytest PASS;
- new post-launch non-zero recovery test PASS;
- same dispatch replay blocked;
- no Agent substitution;
- pre-spawn failure semantics retained;
- `git diff --check` PASS;
- delivery validator PASS;
- evidence manifest PRESENT + valid;
- verification JSON PRESENT + valid;
- changed paths exact allowlist;
- report secret scan PASS.

Do not use a paid nested Agent canary merely for this corrective patch.

When all corrective implementation and local evidence are complete, end the response with exactly:

`FOX2_BRIDGE_DESKTOP_01_02_FIX_01_DELIVERY_READY`
