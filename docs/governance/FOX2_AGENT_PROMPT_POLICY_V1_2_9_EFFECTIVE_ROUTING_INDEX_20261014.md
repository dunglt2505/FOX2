# FOX2 — Agent Prompt Policy V1.2.9 — Dictionary-Resolved Routing Index

**Document ID:** `FOX2-AGENT-PROMPT-ROUTING-INDEX`  
**Revision:** `V1.2.9`  
**Date:** 2026-10-14  
**Status:** `EFFECTIVE_DERIVATIVE_ROUTING_INDEX / NOT_SEPARATE_POLICY / NO_DEV_GRANT`  
**Normative Policy:** resolved from `FOX2_PROJECT_DICTIONARY_v1.json` -> Policy V1.8.8  
**Scope:** FOX2 only.

## 1. Routing source order

Before every new/re-scoped executable assignment:

```text
PROJECT_DICTIONARY_CHECK
-> POLICY_CHECK
-> TASK_STATE_CHECK
-> SOURCE_BINDING_CHECK
-> ROUTING_R0_R7
-> PREEXEC_REQUIREMENTS_BIND
-> MATERIAL_PREFLIGHT_RUN
-> PREFLIGHT_EVIDENCE_CHECK
-> ASSIGNMENT_CHECK
-> BIND EXECUTION + DELIVERY
-> PUBLISH IMMUTABLE HANDOFF
```

CHAT MUST NOT independently hard-code a competing "current Policy/Dispatch/Protocol" identity.

## 2. Project-wide pre-execution gate

A candidate route is not a final executable assignment until CHAT has remote-read the task's Preflight Receipt.

Required behavior:

- bind the material capability/worktree checks first;
- run a non-implementation preflight using the project-wide PreExec Evidence Protocol;
- `PASS` may close R3/R5;
- `BLOCKED` keeps assignment/executable dispatch on HOLD and must identify sanitized material blocker classes;
- `INFRA_FAILED` distinguishes the evidence pipeline itself from Agent/tool capacity;
- preflight failures occur before implementation dispatch publication and therefore do not consume a dispatch;
- do not silently switch Agent because a probe failed; CHAT re-routes only after reading the receipt;
- never treat missing numeric quota telemetry as exhaustion when execution is otherwise demonstrated.

The same rule applies to application, Bridge, provider-adjacent, research/tooling and future FOX2 WPs. A task-local script may implement the checks but may not redefine the state model.

## 3. Canonical execution tuple

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

## 4. Routing baseline

Current routing guidance remains:
- clear/repetitive coding: Copilot CLI Native Auto, CHAT-selected tier when capacity is usable;
- complex implementation: Codex CLI pinned model, medium;
- concurrency/recovery/safety/race/hard debug: Codex CLI pinned model, high.

CHAT may route differently based on current evidence/capacity/risk.

Bridge never routes.

## 5. Permission and Git

Normal coding permission profile is resolved from Dictionary and currently `FULL_ACCESS`.

Git delivery remains explicit:
- AGENT owner -> Agent commit/push exact non-main scope;
- BRIDGE owner -> Bridge commit/push exact non-main scope;
- no permission -> no publication.

No repeated Owner approval for already-bound ordinary commits/pushes inside the same WP.

## 6. Compatibility routing

Exact tool/runtime version equality is not readiness.

Dispatch schema/control path compatibility comes from Dictionary. Unsupported schema/control identity is a pre-launch technical block, not a reason to guess or silently convert.

Supported schemas normalize to one internal execution path.

## 7. Whole-WP anti-fragmentation

Operational reconciliation is not a new WP.

Dictionary drift or a systemic shared binding defect is corrected once at the shared layer and propagated by generated bindings/tests, rather than patched independently in every consumer.

## 8. Usage routing

Post-run usage telemetry remains next-routing input only.

Unknown/non-exposed non-material numeric usage does not block when execution is demonstrably available.

Bridge does not auto-switch Agent/model/tier/reasoning.

## 9. In-flight transition

New Dictionary/source release triggers material-impact analysis, not automatic cancellation of in-flight work.

## 10. Non-effects

This index grants no DEV/main/PR/merge/deploy/Production/provider/broker/LIVE authority.

`ROUTING_INDEX_STATUS=V1.2.9_EFFECTIVE / POLICY=V1.8.7 / PROJECT_DICTIONARY=V1 / IDENTITY_RESOLUTION=DICTIONARY_FIRST`
