# CODEX REWORK — BRIDGE-DESKTOP-BATCH-A — DISPATCH V2 RUNTIME COMPATIBILITY

This is a material correction inside the SAME `BRIDGE-DESKTOP-BATCH-A` whole WP. It is not a new WP and does not reopen already-passing Batch A areas.

## CHAT finding

Remote result `26fdc0af7317a675b618982575f3ee64429a991f` passes the reported Batch A test suite, but independent CHAT readback found that:

`agent_bridge/src/fox2_agent_bridge/e2e_runner.py::_validate_dispatch`

still requires:

`schema_version == "0.6"`

and validates the legacy 0.6 dispatch shape directly.

FOX2 Policy V1.8.6 + Routing Index V1.2.7 + Git-first Protocol v9 require all NEW/re-scoped WPs to use:

`FOX2_LOCAL_AGENT_DISPATCH_SCHEMA_v2.json`

with:

`schema_version = "2.0"`.

Therefore current Bridge Batch A cannot consume the current FOX2 dispatch format and is REWORK_REQUIRED.

## Required correction

Implement one compatibility boundary that accepts the current Dispatch Schema v2 and normalizes it into the Bridge's internal execution payload without weakening validation.

Dispatch v2 materially binds, among other fields:

- `target_agent`
- `policy`
- `task`
- `prompt`
- `source`
- `routing.model_policy`
- `routing.auto_tier`
- `routing.model`
- `routing.reasoning_effort`
- `routing.permission_profile`
- `execution_path`
- `delivery_owner`
- `permissions`
- `decision_receipt`
- `runtime_contract.repo`
- `runtime_contract.branch`
- `runtime_contract.worktree`
- `runtime_contract.base_sha`
- `runtime_contract.allowed_code_paths`
- `runtime_contract.allowed_report_paths`
- `runtime_contract.required_capabilities`
- `runtime_contract.stop_conditions`
- `required_tests`
- `max_runs=1`.

Bridge must enforce the current v2 semantics and must not silently substitute Agent/model/reasoning/permission/delivery owner/scope.

Preserve backward compatibility for already-bound legacy `0.6` dispatches. Legacy support is historical compatibility only; v2 is the current format for new/re-scoped FOX2 work.

Do not maintain two divergent execution implementations. Normalize both supported external schemas into one internal validated representation and reuse existing execution logic.

## Mandatory tests

Add regression coverage proving:

1. an actual shape-equivalent Dispatch Schema v2 payload is accepted and normalized correctly;
2. exact CODEX v2 routing tuple is preserved;
3. exact COPILOT Native Auto/tier v2 routing tuple is preserved;
4. v2 FULL_ACCESS permission profile is enforced;
5. v2 `delivery_owner=AGENT|BRIDGE` is preserved and only one publication path executes;
6. v2 runtime branch/worktree/base/allowed paths map exactly;
7. v2 denied main/merge/provider/broker/LIVE rights remain denied;
8. v2 malformed/missing/materially inconsistent fields fail closed before Agent spawn;
9. v2 Agent mismatch/model mismatch/permission mismatch fail closed;
10. legacy 0.6 dispatches still pass their existing regression suite;
11. full Bridge suite PASS;
12. canonical artifact/text hygiene and `git diff --check` remain PASS.

Use the real repository schema document as a read-only contract source if available in the worktree. Do not alter Policy/governance docs or the schema itself.

## Scope

Writable scope remains unchanged:

- `agent_bridge/**`
- `reports/BRIDGE-DESKTOP-BATCH-A/**`

Do not modify application/backend/frontend/governance.

## Git / delivery

- delivery_owner = AGENT
- git_code_push = YES
- same task branch
- no PR/main/merge/deploy/provider/broker/LIVE.

Update the existing Batch A report/evidence to include:

`DISPATCH_V2_RUNTIME_COMPATIBILITY=PASS`
`LEGACY_V06_COMPATIBILITY=PASS`

Run the full required validation, stage only allowed paths, commit once, push this exact branch and remote-readback.

Finish only after remote publication with:

`FOX2_BRIDGE_DESKTOP_BATCH_A_REWORK_V2_PUSHED_UNREVIEWED`
