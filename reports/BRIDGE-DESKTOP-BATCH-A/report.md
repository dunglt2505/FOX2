# BRIDGE-DESKTOP-BATCH-A

Implemented as one work package on `work/FOX2-BRIDGE-DESKTOP-BATCH-A-codex`, based on accepted FIX-01 `ef9f290e73c4f4500900528656212c38acf43a4f`.
Execution start HEAD: `efdf1f53f83a8eac3251660a588a447f50908fef`. Delivery owner: AGENT.
State: VALIDATED_FOR_AGENT_PUBLICATION_UNREVIEWED.

Final full-suite outcome: **164 passed** on Python 3.13.15.

The background Worker retains its Git durable mailbox, pause/resume/check-now,
bounded backoff and singleton. Recovery requires an explicit zero exit and valid
recorded configuration; it only verifies remote results. Consumed claims survive
restart, races and quota failures without replay or Agent substitution.

Exact adapters persist the immutable tuple and requested/applied/observed model,
reasoning, permission, usage and capacity metadata in SQLite checkpoints, runtime
reports and Tray status. Structured counters survive stdout truncation. Codex uses
danger-full-access/never. Copilot uses allow-all tools/paths/URLs and task-local
Native Auto tier. Missing material capabilities and permission mismatch block
before launch. Versions are recorded without equality gates.

Dispatch delivery_owner selects AGENT verification or one BRIDGE publication.
Four real local Git regressions cover both owners and both products, proving one
result commit, remote SHA equality and replay rejection. Existing schema 0.6
legacy dispatches retain BRIDGE ownership when delivery_owner is absent.

Generated text uses a shared atomic UTF-8/LF helper, deterministic JSON, trailing
whitespace removal and post-write hygiene. Runtime logs use the shared canonical
text routine. Tray model/permission/usage/capacity entries are disabled read-only
items. Fixed controls and per-user startup remain covered by headless PowerShell.

- WORKER_RECOVERY=PASS
- CODEX_EXACT_CONFIG=PASS
- COPILOT_EXACT_POLICY=PASS
- USAGE_PERSISTENCE=PASS
- POST_START_QUOTA_RECONCILIATION=PASS
- NO_REPLAY=PASS
- NO_AGENT_SUBSTITUTION=PASS
- GIT_DELIVERY_POLICY_ALIGNED=PASS
- NO_DUPLICATE_PUBLICATION_PATH=PASS
- FULL_ACCESS_CODEX=PASS
- FULL_ACCESS_COPILOT=PASS
- PERMISSION_PREFLIGHT=PASS
- MATERIAL_TOOL_COMPATIBILITY=PASS
- NON_MATERIAL_VERSION_MISMATCH_CONTINUES=PASS
- MATERIAL_CAPABILITY_MISSING_BLOCKS=PASS
- CANONICAL_GENERATED_ARTIFACT_PIPELINE=PASS
- TRAY_READ_ONLY_USAGE_DISPLAY=PASS
- TEXT_ARTIFACT_HYGIENE=PASS
- FULL_BRIDGE_TESTS=PASS
- SECRET_SCAN=PASS
- CHANGED_PATH_ALLOWLIST=PASS
- GIT_DIFF_CHECK=PASS

Evidence: evidence/pytest.xml, evidence/pytest.txt, evidence/cli_capabilities.json,
evidence/verification.json and SHA-256 entries in evidence_manifest.json.

Tests use fake Agents, real local child failure fixtures and actual local Git
publication; CLI help/version probes are real and harmless. Startup is mocked in
PowerShell; no paid Agent invocation, manual Tray interaction, real Windows logon,
PR/main/merge/deploy/provider/broker/LIVE was performed. Actual live model, usage
and quota remain unknown; fixture observations are not live account telemetry.

Task source authority was accepted as CHAT-verified. The two candidate spec paths
were absent at the task-cited commit; implementation follows the executable task's
explicit contracts and accepted code base without source-release rediscovery.

Agent will publish only allowed paths to this task branch and verify the remote
SHA after commit. This pre-publication manifest excludes its own hash and does
not claim a post-commit SHA before Git creates it.
