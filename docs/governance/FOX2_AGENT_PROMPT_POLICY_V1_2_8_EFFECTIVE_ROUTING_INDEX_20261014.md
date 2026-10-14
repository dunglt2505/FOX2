# FOX2 — Agent Prompt Policy V1.2.8 — Dictionary-Resolved Routing Index

**Document ID:** `FOX2-AGENT-PROMPT-ROUTING-INDEX`  
**Revision:** `V1.2.8`  
**Date:** 2026-10-14  
**Status:** `EFFECTIVE_DERIVATIVE_ROUTING_INDEX / NOT_SEPARATE_POLICY / NO_DEV_GRANT`  
**Normative Policy:** resolved from `FOX2_PROJECT_DICTIONARY_v1.json` -> Policy V1.8.7  
**Scope:** FOX2 only.

## 1. Routing source order

Before every new/re-scoped executable assignment:

```text
PROJECT_DICTIONARY_CHECK
-> POLICY_CHECK
-> TASK_STATE_CHECK
-> SOURCE_BINDING_CHECK
-> ROUTING_R0_R7
-> ASSIGNMENT_CHECK
-> MATERIAL_CAPABILITY_CHECK
-> BIND EXECUTION + DELIVERY
-> PUBLISH IMMUTABLE HANDOFF
```

CHAT MUST NOT independently hard-code a competing "current Policy/Dispatch/Protocol" identity.

## 2. Canonical execution tuple

Resolve allowed machine identifiers from the Dictionary, then bind:
- Role;
- Agent Product;
- Model Policy;
- Model/Auto Tier;
- Reasoning;
- Permission Profile;
- Execution Path;
- Delivery Owner;
- Worktree/Branch/Base SHA;
- Allowed Code/Report Paths;
- Git Permissions;
- Required Capabilities/Tests;
- STOP Conditions.

## 3. Routing baseline

Current routing guidance remains:
- clear/repetitive coding: Copilot CLI Native Auto, CHAT-selected tier when capacity is usable;
- complex implementation: Codex CLI pinned model, medium;
- concurrency/recovery/safety/race/hard debug: Codex CLI pinned model, high.

CHAT may route differently based on current evidence/capacity/risk.

Bridge never routes.

## 4. Permission and Git

Normal coding permission profile is resolved from Dictionary and currently `FULL_ACCESS`.

Git delivery remains explicit:
- AGENT owner -> Agent commit/push exact non-main scope;
- BRIDGE owner -> Bridge commit/push exact non-main scope;
- no permission -> no publication.

No repeated Owner approval for already-bound ordinary commits/pushes inside the same WP.

## 5. Compatibility routing

Exact tool/runtime version equality is not readiness.

Dispatch schema/control path compatibility comes from Dictionary. Unsupported schema/control identity is a pre-launch technical block, not a reason to guess or silently convert.

Supported schemas normalize to one internal execution path.

## 6. Whole-WP anti-fragmentation

Operational reconciliation is not a new WP.

Dictionary drift or a systemic shared binding defect is corrected once at the shared layer and propagated by generated bindings/tests, rather than patched independently in every consumer.

## 7. Usage routing

Post-run usage telemetry remains next-routing input only.

Unknown/non-exposed non-material numeric usage does not block when execution is demonstrably available.

Bridge does not auto-switch Agent/model/tier/reasoning.

## 8. In-flight transition

New Dictionary/source release triggers material-impact analysis, not automatic cancellation of in-flight work.

## 9. Non-effects

This index grants no DEV/main/PR/merge/deploy/Production/provider/broker/LIVE authority.

`ROUTING_INDEX_STATUS=V1.2.8_EFFECTIVE / POLICY=V1.8.7 / PROJECT_DICTIONARY=V1 / IDENTITY_RESOLUTION=DICTIONARY_FIRST`
