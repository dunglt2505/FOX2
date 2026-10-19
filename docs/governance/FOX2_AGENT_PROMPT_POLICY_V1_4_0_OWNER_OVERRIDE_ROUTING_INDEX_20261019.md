# FOX2 — Agent Routing Index V1.4.0 — Owner Override · CODE-FIRST · CHAT-FIRST

**Document ID:** `FOX2-AGENT-PROMPT-ROUTING-INDEX`  
**Revision:** `V1.4.0`  
**Date:** 2026-10-19  
**Status:** `OWNER_APPROVED_MIGRATION_CANDIDATE / NOT_INSTALLED_EFFECTIVE / NO_DEV_GRANT`  
**Normative Policy:** resolved from `FOX2_PROJECT_DICTIONARY_v1.json` -> Policy V2.0.0  
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

Default: a candidate route is not a final executable assignment until CHAT has remote-read the task's Preflight Receipt. Owner may explicitly override named internal preflight/assignment gates per Policy v2.0.0, without relabeling failed/unrun checks PASS.

Required behavior:

- bind the material capability/worktree checks first;
- run a non-implementation preflight using the project-wide PreExec Evidence Protocol;
- `PASS` may close R3/R5;
- `BLOCKED` keeps normal assignment/executable dispatch on HOLD and must identify sanitized material blocker classes; an explicit Owner override may separately record AUTHORIZED_BY_OWNER_OVERRIDE for a bounded action, never PASS;
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

`ROUTING_INDEX_STATUS=V1.4.0_MIGRATION_CANDIDATE / POLICY=V2.0.0 / PROJECT_DICTIONARY=V1.3 / AGENT_ROUTE_MATERIALITY=AGGREGATE / IDENTITY_RESOLUTION=DICTIONARY_FIRST`

## 11. Owner override lane and DEV product-first routing — 2026-10-19

The Owner is the project's highest **internal** decision authority and can expressly waive/replace a named FOX2 internal gate without fabricating a technical PASS. CHAT records the directive, scope, historical failure and residual controls in the existing Whole-WP; no micro-WP solely for an exception.

**Route A — READ_ONLY or authorized CHAT candidate/release documentation:** CHAT acts directly through accessible tools; no host PreExec or WORK is required simply to compare source/Git/Library/metadata.

**Route B — offline product DEV:** CLI-first Copilot or CODEX if demonstrably supported and independently admitted. Only task-material prerequisites are checked; a Bridge worker PAUSED state is not material if the DEV route does not touch installed Bridge, its worker or its ledger. Normal flow is route-bound PreExec PASS and CHAT R0–R7; an explicit Owner Override may waive a named internal gate and must yield `AUTHORIZED_BY_OWNER_OVERRIDE`, never synthetic PASS. Maintain task/branch/path ownership, honest evidence and no unauthorized actions.

**Route C — Bridge installed execution / Canary / real side effects:** apply real singleton, claim/no-replay, provenance, capacity, recovery and external-access controls. An Owner Override can supersede an internal approval step, not an OS lock, a consumed dispatch, unavailable code or an external entitlement. Never silently replay Dispatch001 or Canary009.

**Implementation boundary:** this derivative routing document updates source semantics, not the installed runtime. If current Dispatch v3 schema or Bridge Python code does not accept an Owner override status as a machine field, DO NOT place it into existing PASS-only fields or launch through unsupported paths. Update versioned consumers/tests before effective machine adoption. In-flight immutable WPs keep their own bound versions until explicitly rebased or superseded.
