# FOX2 — Agent Prompt Policy V1.4.0 CANDIDATE — Dictionary-Resolved Alternative-Route Routing Index

**Document ID:** `FOX2-AGENT-PROMPT-ROUTING-INDEX`  
**Revision:** `V1.4.0`  
**Date:** 2026-10-14  
**Status:** `CANDIDATE_DERIVATIVE_ROUTING_INDEX / NOT_EFFECTIVE / NO_NEW_DEV_GRANT`  
**Normative Policy:** resolved from `FOX2_PROJECT_DICTIONARY_v1.json` -> Policy V1.9.0 CANDIDATE  
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

`ROUTING_INDEX_STATUS=V1.4.0_CANDIDATE / POLICY=V1.8.9 / PROJECT_DICTIONARY=V1.2 / AGENT_ROUTE_MATERIALITY=AGGREGATE / IDENTITY_RESOLUTION=DICTIONARY_FIRST`


## 10. Direct CHAT first route — candidate

The routing precheck begins with `CHAT_DIRECT_CAPABILITY_CHECK`: verify actual tool operation, requested result, Owner operation grant, exact source, destination conflicts/readback and whether a separate execution-host or independent-audit capability is material. When direct feasible, CHAT MUST execute and verify; do not create a prompt or handoff. When partial, CHAT finishes direct subset before routing residual tasks.

For Agent work, preserve Dictionary -> Policy -> TASK_STATE -> SOURCE_BINDING -> R0-R7 -> PreExec receipt -> CHAT Intake -> final assignment -> immutable Dispatch. CHAT direct documentation operations use permission/source/write/readback checks but do not produce a fake Agent dispatch. WORK only for demonstrably needed independent audit; CODEX/COPILOT for demonstrably required coding host. Preserve pinned model and eligible-route aggregation for actual Agent tasks. Do not redirect to another Agent without CHAT analysis of evidence and source state.

`ROUTE_FIRST=CHAT_DIRECT / DELEGATION_REASON=REQUIRED / PREEXEC_AGENT_ONLY_WHEN_AGENT_EXECUTION / POLICY_CANDIDATE=V1.9.0`

## Git latest-at-execution — Phase A prospective candidate integration

Status: CANDIDATE_NOT_EFFECTIVE. Applies prospectively only after the required authority and compatibility gates; this amendment grants no runtime/DEV, merge, release or LIVE permission.

1. **Historical references remain valid.** Old version numbers in BRDs, Policy, Specs, Protocols, templates and reports are historical references, not execution pins. Do not rewrite them in bulk merely because a newer version exists.
2. **Refresh live Git before every execution.** At CHAT direct actionable admission, Agent PreExec and dequeue before first claim, automatically contact authenticated GitHub at the authorized Registry location; read current Registry, manifests, publication and supersession metadata and newly published versions. Record observation time, Registry ref/commit and all relevant candidates. If the trusted Registry location or live access is unavailable, record SOURCE_UNVERIFIED / AUTHORITY_UNVERIFIED / GIT_UNAVAILABLE and HOLD dependent execution; cache or Library must never silently substitute.
3. **Choose newest applicable.** Evaluate scope, owning authority, release approval, compatibility and target environment; distinguish LATEST_GIT_OBSERVED from LATEST_APPLICABLE. Record selected and rejected versions with reasons. A newer unqualified version is LATEST_PRESENT_BUT_BLOCKED and goes through the applicable gate; do not silently promote it or downgrade to the version in authored text. A qualified older source requires an explicit, evidenced applicability decision under the gate.
4. **Lock before claim/effect.** Recheck material Registry/source-head drift immediately before first claim or side effect. Drift invalidates affected stale PreExec/routing and requires permitted revalidation before start. Freeze repository, Registry and manifest commits, source path/commit, Git blob and SHA-256 of exact bytes, scope/compatibility verdict and approval evidence into the attempt source lock. Refresh/lock is not a release approval.
5. **Preserve running Dispatches.** Consumed/started Dispatches retain their original immutable source locks; no hot-swap, mutation or automatic replay. Newer sources affect subsequent work or explicit governed stop/reconciliation. Queued unstarted work refreshes and rebinds only before claim, within existing permissions.

Evidence must distinguish REFRESH_PASS, APPLICABILITY_PASS, RELEASE_AUTHORITY_PASS, EXECUTION_PASS and EFFECTIVE_RELEASE_PASS. Static document verification proves none of the runtime or release claims. CHAT result intake compares actual execution to its frozen lock; live discovery for follow-up does not retroactively rebind that execution.

Normative candidate detail: `docs/governance/FOX2_GIT_LATEST_AT_EXECUTION_CONTRACT_v1_CANDIDATE.md`. Source commit/hash must be resolved at execution; this path/reference is not proof that this Candidate is EFFECTIVE.
