# FOX2 — Agent Prompt Policy V1.2.7 — CLI-FIRST Effective Routing Index

**Document ID:** `FOX2-AGENT-PROMPT-ROUTING-INDEX`  
**Revision:** `V1.2.7`  
**Date:** 2026-10-14  
**Status:** `EFFECTIVE_DERIVATIVE_ROUTING_INDEX / NOT_SEPARATE_POLICY / NO_DEV_GRANT`  
**Supersedes for NEW/re-scoped prompts:** `V1.2.6`  
**Normative Policy:** `FOX2_POLICY_V1.8.6.md`  
**Bridge Technical:** `FOX2_LOCAL_AGENT_BRIDGE_TECHNICAL_SPEC_v0.7_CANDIDATE.md` REV6+  
**Scope:** FOX2 only.

## 1. Routing model

CHAT performs routing once and binds the complete immutable execution tuple.

```text
Owner
 -> CHAT
 -> COPILOT CLI or CODEX CLI
 -> optional Bridge transport/supervision
 -> exact non-main delivery
 -> CHAT remote readback/acceptance
```

Codex CLI and Copilot CLI are the primary implementation engines.

Bridge is optional transport/supervision and is not a routing authority.

## 2. Required routing order

Before a new/re-scoped executable assignment:

```text
POLICY_CHECK
-> TASK_STATE_CHECK
-> SOURCE_BINDING_CHECK
-> ROUTING_R0_R7
-> ASSIGNMENT_CHECK
-> MATERIAL_CAPABILITY_CHECK
-> BIND EXECUTION + DELIVERY
-> PUBLISH IMMUTABLE HANDOFF
```

Do not repeat these governance decisions inside Bridge.

## 3. Canonical execution tuple

Every executable handoff binds:

```text
Role
+ Agent Product
+ Model Policy
+ Model or Auto Tier
+ Reasoning / Thinking
+ Permission Profile
+ Execution Path
+ Delivery Owner
+ Worktree / Branch / Base SHA
+ Allowed Code Paths
+ Allowed Report Paths
+ Git Permissions
+ Required Tests
+ STOP Conditions
```

## 4. Primary Agent routing

Baseline guidance:

| Task profile | Primary route |
| --- | --- |
| docs/tests/simple/clear implementation | COPILOT CLI, Native Auto, CHAT-selected tier |
| repetitive/low-complexity coding | COPILOT CLI, efficiency/balance as CHAT selects |
| harder coding still suitable for Copilot | COPILOT CLI, intelligence as CHAT selects |
| concurrency/recovery/safety/complex implementation | CODEX CLI, pinned model, medium reasoning |
| race condition/hard debug/critical recovery | CODEX CLI, pinned model, high reasoning |

CHAT may override based on current evidence, capacity, cost, safety or task complexity.

No Bridge-side routing table may override CHAT.

## 5. Permission routing

Normal coding default:

```text
permission_profile = FULL_ACCESS
```

CHAT selects the profile. Bridge/CLI applies it exactly.

Codex intent:

```text
danger-full-access
approval_policy = never
```

Copilot intent:

```text
allow-all
```

If exact permission semantics cannot be applied, stop before launch with a permission-profile mismatch. Do not silently downgrade.

Autopilot remains a separate CHAT decision.

## 6. Git delivery routing

```text
git_code_push=YES + delivery_owner=AGENT
 -> Agent commits/pushes exact non-main task branch
 -> CHAT readback

git_code_push=YES + delivery_owner=BRIDGE
 -> Bridge commits/pushes exact non-main task branch
 -> CHAT readback

git_code_push=NO
 -> no code publication
```

Do not create a duplicate publication path.

Ordinary commits/pushes already authorized inside an exact WP do not require repeated Owner confirmation.

## 7. Material Tool Compatibility

Do not route on version strings alone.

```text
VERSION_MATCH != READINESS
```

Required capability available + required tests pass + task semantics correct -> continue.

Missing material capability -> block.

Unknown material capability -> hold.

Non-material version/capability/metadata deviation -> record and continue.

## 8. Usage/capacity routing

Before each new Agent assignment, CHAT reads the newest available usage/capacity evidence when material.

```text
POST-RUN USAGE SNAPSHOT
-> CHAT NORMALIZATION
-> NEXT ROUTING DECISION
```

Bridge may collect telemetry but does not auto-switch Agent/model/tier/reasoning or wait/relaunch.

Missing numeric quota alone is not a blocker when execution is demonstrably available and the missing value is non-material.

## 9. Runtime failure routing

Post-start non-zero/quota/auth/capacity uncertainty:

```text
NEEDS_RECONCILIATION
dispatch consumed
no blind replay
no automatic substitution
```

Proven pre-spawn failures may be terminal/actionable.

CHAT decides any replacement/retry dispatch.

## 10. Whole-WP and anti-fragmentation rule

One bounded WP should proceed continuously through implementation/test/evidence/publication until a genuine STOP or final delivery.

Operational reconciliation is not a new WP.

Systemic defects that affect shared components should be consolidated into the current dependency-safe batch rather than split into repeated micro-fixes.

## 11. In-flight source transition

A newer source release triggers material-impact evaluation, not automatic invalidation.

New/re-scoped WPs use Policy V1.8.6 and this Routing Index V1.2.7.

Historical immutable WPs keep their binding unless materially affected.

## 12. Non-effects

This derivative index grants no DEV authority by itself and creates no main push, PR creation, merge, deploy, Production/provider write, broker write or LIVE right.

`ROUTING_INDEX_STATUS=V1.2.7_EFFECTIVE / POLICY=V1.8.6 / CLI_FIRST=YES / FULL_ACCESS_DEFAULT=YES / DELIVERY_OWNER=EXPLICIT / CAPABILITY_BASED_READINESS=YES`
