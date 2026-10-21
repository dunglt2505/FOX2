# FOX2 G2 — Dictionary 1.2 machine-binding compatibility with Governance Dictionary 1.3

Date: 2026-10-21  
Whole-WP: `FOX2-BRIDGE-RC1-TO-INTERNAL-READY`  
Task: `FOX2-BRIDGE-RC1-G2-A01`

## Boundary

Governance source selection for this new task is Dictionary 1.3 / Policy 2.0.0 / Routing 1.4.0.

The source branch's generated Bridge machine binding remains Dictionary 1.2:
- `agent_bridge/src/fox2_agent_bridge/project_dictionary.py`
- `DICTIONARY_VERSION = 1.2`
- source path `docs/governance/FOX2_PROJECT_DICTIONARY_v1.json`.

This receipt does NOT claim machine migration to Dictionary 1.3. It answers only whether the shared PreExec v1.1 machinery bound to 1.2 is materially compatible for the G2 MANUAL_LOCAL CODEX readiness check.

## Exact comparison

Dictionary 1.2 source on G2 branch compared with Dictionary 1.3 @ `b25f7f728de67cf8595bf24f22fcbd79ef50babc`.

The following task-material machine identities are EXACTLY EQUAL:

- Dispatch Schema: 3.0 / same path.
- Git-first Protocol: 12 / same path.
- Result Schema: v2 / same path.
- Result Template: v4 / same path.
- CHAT Result Intake: v9 / same path.
- PreExec Evidence Protocol: v1.1 / same path.
- Preflight Receipt Schema: v1 / same path.
- CHAT Preflight Intake: v1.1 / same path.
- Agent products: CODEX, COPILOT.
- Model policy enum.
- CODEX reasoning efforts: low, medium, high.
- Permission profiles and normal coding permission: FULL_ACCESS.
- Execution paths including MANUAL_LOCAL.
- Delivery-owner enum.
- max parallel material writers = 2.
- Preflight statuses/capability statuses/blocker classes.
- Agent-route materiality rule and aggregate capability.

Known DIFFERENCES:
- Dictionary 1.2 human Policy pointer = 1.8.9; Dictionary 1.3 = 2.0.0.
- Dictionary 1.2 Routing pointer = 1.3.0; Dictionary 1.3 = 1.4.0.

Those human-governance differences are bound independently in G2 task.md to the current Owner-approved Registry/Source Resolution and are not delegated to the old generated machine binding.

## Verdict

`MACHINE_PREEXEC_COMPATIBILITY=PASS_SCOPED`

Meaning:
- shared PreExec v1.1 from the G2 branch may be used for task-specific machine readiness evidence;
- its receipt remains a Dictionary-1.2 machine compatibility receipt, not proof that runtime adopted Dictionary 1.3;
- CHAT must combine that machine receipt with the separately verified Dictionary-1.3 governance source binding before assignment;
- any material field drift discovered at runtime => HOLD, not PASS.

No Agent execution or Dispatch is authorized by this receipt.
