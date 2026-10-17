# FOX2 — Agent Prompt Policy V1.3.0 — Dictionary-Resolved Alternative-Route Routing Index

**Document ID:** `FOX2-AGENT-PROMPT-ROUTING-INDEX`  
**Revision:** `V1.3.0`  
**Date:** 2026-10-14  
**Status:** `EFFECTIVE_DERIVATIVE_ROUTING_INDEX / NOT_SEPARATE_POLICY / NO_DEV_GRANT`  
**Normative Policy:** resolved from `FOX2_PROJECT_DICTIONARY_v1.json` -> Policy V1.8.9  
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

Alternative-route materiality:
- Copilot/Codex candidate probes are compared, not AND-gated, unless the task explicitly pins one Agent as required;
- each alternative candidate probe is normally `material=false` routing evidence;
- one aggregate `eligible_agent_route` capability is `material=true`;
- aggregate PASS = at least one allowed candidate probe PASS;
- aggregate FAIL/BLOCKED = no allowed candidate can currently execute;
- preferred-route failure never authorizes silent fallback: CHAT reads the receipt and selects the final route;
- a task-pinned Agent is an exception: its probe is material and no alternative route may satisfy that requirement.

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

`ROUTING_INDEX_STATUS=V1.3.0_EFFECTIVE / POLICY=V1.8.9 / PROJECT_DICTIONARY=V1.2 / AGENT_ROUTE_MATERIALITY=AGGREGATE / IDENTITY_RESOLUTION=DICTIONARY_FIRST`


## CHAT-FIRST execution — Owner-approved operating addendum (candidate, 2026-10-17)

For FOX2 task intake, CHAT is the default DIRECT EXECUTION OWNER. Before routing to WORK, CODEX or COPILOT, CHAT MUST test current actual tool availability, scope, authority, evidence and whether an independent auditor or execution host is materially required. CHAT directly completes every authorized and technically supported step, with exact readback and evidence. Multiple steps, document volume or project complexity alone do not justify delegation. If execution is partially possible, perform that portion directly and hand off ONLY the bounded residual work, explaining the material reason. WORK is not a routine proxy for CHAT source inspection, documentation editing, Git comparisons or reports. Agent prompting is not task completion when CHAT can execute.

This operating addendum preserves Dictionary-first source identity, pinned Agent/model/permission, project-wide PreExec before final Agent assignment, durable receipts, source lock, exact non-main Git grants, safety/release approval and no-replay. It grants no authority to self-certify EFFECTIVE, alter protected governance semantics without owning approval, merge, deploy or LIVE. The existing document's current release identity remains historical; this branch edit is a candidate revision pending governed publication.
