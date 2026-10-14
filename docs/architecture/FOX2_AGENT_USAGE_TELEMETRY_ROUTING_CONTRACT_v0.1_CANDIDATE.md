# FOX2 — Agent Usage Telemetry & CHAT Routing Contract v0.1 Candidate

**Document ID:** `FOX2-AGENT-USAGE-TELEMETRY-01`  
**Version:** `0.1 Candidate REV4`  
**Status:** `CANDIDATE / SOURCE_CONTRACT / INTEGRATED_INTO_BRIDGE_DESKTOP_BATCH_A / NO_DEV_GRANT`  
**Project:** `FOX2 ONLY`  
**Date:** 2026-10-14  
**Governance:** `FOX2_POLICY_V1.8.6.md` + `FOX2_AGENT_PROMPT_POLICY_V1_2_7_EFFECTIVE_ROUTING_INDEX_20261014.md`  
**Bridge technical baseline:** `FOX2_LOCAL_AGENT_BRIDGE_TECHNICAL_SPEC_v0.7_CANDIDATE.md`  
**Execution mapping:** requirements are absorbed into `BRIDGE-DESKTOP-BATCH-A`; there is no standalone Usage DEV round. `BRIDGE-DESKTOP-01-02-FIX-01` must PASS before Batch A is dispatched.

## 1. Purpose

Use telemetry returned by each Agent execution as an input for the next CHAT routing decision, while keeping Bridge a transport/execution layer rather than a routing authority.

Core principle:

```text
POST-RUN USAGE SNAPSHOT -> NEXT-ROUTING INPUT
```

This contract also standardizes model selection:

```text
COPILOT = NATIVE_AUTO + CHAT-selected tier
CODEX   = CHAT-pinned model + reasoning effort
```

## 2. Authority boundary

### CHAT

CHAT is the sole owner of:

- task/risk/complexity evaluation;
- Agent Product selection;
- Model Policy selection;
- Copilot Auto tier selection;
- Codex model selection;
- Codex reasoning effort selection;
- Scope;
- HOLD / PUBLISH routing decision.

### Bridge

Bridge may only:

- receive an immutable dispatch;
- validate minimum runtime facts required for safe launch;
- invoke the exact requested Agent configuration;
- collect result + telemetry;
- persist and relay evidence;
- preserve replay/single-use/reconciliation safety.

Bridge MUST NOT:

- substitute Agent;
- change model policy;
- change Copilot Auto tier;
- change Codex model;
- change reasoning effort;
- retry quota failures blindly;
- wait for reset and relaunch autonomously;
- publish a replacement dispatch.

### System Tray

System Tray is display-only for routing/usage information. It MUST NOT make routing decisions or mutate dispatch configuration.

## 2A. Permission authority

CHAT is the sole authority that selects the Agent permission profile. For normal FOX2 coding execution the baseline is:

```text
permission_profile = FULL_ACCESS
```

Bridge does not decide whether Full Access is appropriate. Bridge receives the immutable choice, verifies that the installed CLI/host can honor it, maps it to exact CLI flags/config and launches the selected Agent.

Canonical mapping:

```text
CODEX FULL_ACCESS
= danger-full-access sandbox semantics
+ approval_policy = never

COPILOT FULL_ACCESS
= --allow-all semantics
= all tools + all paths + all URLs
```

If effective runtime permissions cannot match the requested profile, Bridge must stop before launch and return a permission-profile mismatch to CHAT. It MUST NOT silently downgrade, substitute another Agent, or rewrite the dispatch.

Full Access is technical execution permission only; immutable project authority and release restrictions remain separate.

## 2B. Git delivery authority

Git delivery follows released Policy V1.8.6 and must be bound in the immutable handoff.

```text
git_code_push=YES + delivery_owner=AGENT
=> selected Agent may commit/push exact authorized non-main task branch

git_code_push=YES + delivery_owner=BRIDGE
=> Bridge may commit/push exact authorized non-main task scope

git_code_push=NO
=> no code-result publication
```

CHAT performs independent remote readback and semantic acceptance in all cases. Bridge MUST NOT create a duplicate publication path after an Agent-owned delivery already exists.

## 3. Canonical routing tuple

Every executable Agent dispatch must bind:

```text
Role
+ Agent Product
+ Model Policy
+ Model or Auto Tier
+ Reasoning / Thinking
+ Permission Profile
+ Scope
```

### Copilot

Default strategy:

```text
product = COPILOT
model_policy = NATIVE_AUTO
auto_tier = balance
model = null
reasoning_effort = null
```

Allowed Auto tiers:

```text
efficiency
balance
intelligence
```

CHAT chooses the tier. GitHub Copilot chooses the concrete model.

### Codex

Strategy:

```text
product = CODEX
model_policy = PINNED
auto_tier = null
model = <CHAT-selected exact model>
reasoning_effort = low | medium | high
```

Bridge must pass the pinned model/reasoning values from the immutable dispatch rather than falling back silently to user-global defaults.

## 4. Dispatch contract

Copilot example:

```json
{
  "agent": {
    "product": "COPILOT",
    "model_policy": "NATIVE_AUTO",
    "auto_tier": "balance",
    "model": null,
    "reasoning_effort": null
  },
  "execution_budget": {
    "max_ai_credits": 60
  }
}
```

Codex example:

```json
{
  "agent": {
    "product": "CODEX",
    "model_policy": "PINNED",
    "auto_tier": null,
    "model": "gpt-6.1-sol",
    "reasoning_effort": "medium"
  }
}
```

`max_ai_credits`, when present, is a CHAT-issued task execution bound. It is not derived automatically by Bridge from account credits remaining.

## 5. Result and telemetry contract

Each execution SHOULD return the newest machine-readable telemetry exposed by the Agent CLI.

Minimum logical fields:

```text
requested_agent
requested_model_policy
requested_auto_tier
requested_model
requested_reasoning_effort

observed_agent
observed_model_policy
observed_auto_tier
observed_model
observed_reasoning_effort

five_hour_remaining_percent
five_hour_reset_at
weekly_remaining_percent
weekly_reset_at

credits_remaining
session_credits_used
ordinary_usage_allowed

observed_at
source
freshness
state
```

Unknown or unexposed values remain:

```text
null
UNKNOWN
NOT_EXPOSED
```

They MUST NOT be converted into guessed percentages, guessed model names or guessed availability.

Preferred structured output:

- Copilot CLI: machine-readable JSON output when supported.
- Codex CLI: structured output schema / last-message output when supported.

## 6. CHAT pre-routing usage gate

Before each new Agent assignment/dispatch:

```text
TASK_STATE_CHECK
    -> READ_LAST_AGENT_USAGE
    -> NORMALIZE_USAGE
    -> ROUTING_R0_R7
    -> SELECT AGENT PRODUCT
    -> SELECT MODEL POLICY
    -> SELECT TIER or MODEL+REASONING
    -> PUBLISH IMMUTABLE DISPATCH or HOLD
```

Usage is an input to CHAT routing only. It is not Bridge routing logic.

Normalized states:

```text
AVAILABLE
LOW
EXHAUSTED
CAPACITY_THROTTLED
AUTH_REQUIRED
UNKNOWN
STALE
```

Semantics:

```text
UNKNOWN != AVAILABLE
UNKNOWN != EXHAUSTED
NOT_EXPOSED != EXHAUSTED
CAPACITY_THROTTLED != EXHAUSTED
```

Materiality remains governed by Policy V1.8.6: missing numeric quota alone does not block a launch if the selected Agent can actually execute and the missing field is non-material.

Tool/runtime compatibility follows the Bridge Technical Spec REV7 Material Tool Compatibility Rule. Exact version mismatch alone MUST NOT alter routing, HOLD, or launch eligibility when the capabilities required by the current immutable task are available and required validation passes. Missing or unknown capability blocks only when that capability is material to correctness, safety, compatibility, or execution. If materiality is not bound clearly enough for Bridge to decide technically, Bridge returns the ambiguity to CHAT.

## 7. Codex reset normalization

If a known five-hour reset time has passed:

```text
if now >= five_hour_reset_at:
    five_hour_remaining_percent = 100
    five_hour_usage_source = DERIVED_RESET
else:
    keep last observed value
```

No Codex run is required solely to confirm the reset.

A later real Codex execution replaces the derived value with observed telemetry.

Five-hour reset MUST NOT reset or override weekly state.

Example:

```text
5h = 100% DERIVED_RESET
weekly = 0%
=> CODEX remains HOLD for ordinary usage
```

An explicit CLI field such as `ordinary_usage_allowed=false` overrides a derived percentage.

## 8. Runtime quota race and reconciliation

A previous snapshot cannot guarantee that capacity remains available at runtime.

If:

```text
CHAT routes Agent
-> Bridge claims dispatch
-> Agent starts
-> Agent hits quota/login/capacity failure
```

then:

```text
execution = NEEDS_RECONCILIATION
dispatch = consumed
no blind replay
no automatic Agent substitution
```

If failure output exposes quota/reset information, Bridge persists that telemetry with the failure result for the next CHAT routing cycle.

## 9. Copilot runtime profile rule

Bridge MUST NOT mutate the user's normal global Copilot settings per task.

Candidate implementation may use process-scoped runtime profiles:

```text
copilot_profiles/
  efficiency/
  balance/
  intelligence/
```

with a process-local `COPILOT_HOME` or another officially supported isolation mechanism.

This remains subject to a dedicated canary on the actual FOX2 host before it is trusted, because auth/session/config behavior must be proven.

Copilot Full Access permission is allowed when selected by CHAT through the immutable permission profile. Autopilot remains a separate execution-mode decision and is not implied by Full Access.

## 10. Tray display

Tray may show, when available:

```text
CODEX
- normalized state
- 5h remaining/reset/source
- weekly remaining/reset
- requested/observed model
- reasoning
- last observed time

COPILOT
- normalized state
- credits remaining
- Auto tier
- observed concrete model if exposed
- last observed time
```

Tray MUST NOT:

```text
auto-route
auto-switch Agent
auto-change tier/model/reasoning
auto-retry quota
auto-publish dispatch
```

## 11. Baseline routing guidance

This is CHAT guidance, not a Bridge routing table:

| Task profile | Agent | Model policy | Tier / reasoning |
| --- | --- | --- | --- |
| docs, tests, simple fix, clear implementation | COPILOT | NATIVE_AUTO | Balance |
| very simple/repetitive task | COPILOT | NATIVE_AUTO | Efficiency |
| harder coding still appropriate for Copilot | COPILOT | NATIVE_AUTO | Intelligence |
| concurrency/recovery/safety/complex implementation | CODEX | PINNED | Medium |
| race condition/hard debugging/critical recovery | CODEX | PINNED | High |

CHAT may choose differently when current task evidence, capacity, cost or safety requires it.

## 12. Acceptance

Required acceptance set:

```text
COPILOT_NATIVE_AUTO_SUPPORTED=PASS
COPILOT_AUTO_TIER_FROM_DISPATCH=PASS
COPILOT_DEFAULT_AUTO_BALANCE=PASS

CODEX_PINNED_MODEL_FROM_DISPATCH=PASS
CODEX_PINNED_REASONING_FROM_DISPATCH=PASS

MODEL_POLICY_IMMUTABLE_AFTER_PUBLISH=PASS
BRIDGE_DOES_NOT_SUBSTITUTE_AGENT=PASS
BRIDGE_DOES_NOT_CHANGE_AUTO_TIER=PASS
BRIDGE_DOES_NOT_CHANGE_MODEL=PASS
BRIDGE_DOES_NOT_CHANGE_REASONING=PASS
GIT_DELIVERY_POLICY_ALIGNED=PASS
NO_DUPLICATE_PUBLICATION_PATH=PASS

REQUESTED_CONFIGURATION_RECORDED=PASS
OBSERVED_CONFIGURATION_RECORDED_WHEN_EXPOSED=PASS
UNEXPOSED_VALUES_REMAIN_UNKNOWN=PASS

CODEX_RESULT_CAN_CAPTURE_USAGE=PASS
COPILOT_RESULT_CAN_CAPTURE_USAGE=PASS
FIVE_HOUR_RESET_DERIVATION=PASS
FIVE_HOUR_RESET_DOES_NOT_RESET_WEEKLY=PASS

CHAT_READS_USAGE_BEFORE_ROUTING=PASS
CHAT_OWNS_ROUTING_DECISION=PASS

POST_START_QUOTA_FAILURE=NEEDS_RECONCILIATION
NO_BLIND_REPLAY=PASS
NO_AUTOMATIC_AGENT_SUBSTITUTION=PASS

COPILOT_MAX_AI_CREDITS_ENFORCED_IF_DISPATCHED=PASS
COPILOT_GLOBAL_USER_CONFIG_NOT_MUTATED=PASS
COPILOT_PROFILE_CANARY_REQUIRED=PASS

MATERIAL_TOOL_COMPATIBILITY_RULE=PASS
NON_MATERIAL_VERSION_MISMATCH_CONTINUES=PASS
MATERIAL_CAPABILITY_MISSING_BLOCKS=PASS
UNKNOWN_MATERIAL_CAPABILITY_HOLDS=PASS
FULL_ACCESS_PROFILE_FROM_DISPATCH=PASS
CODEX_FULL_ACCESS_EFFECTIVE=PASS
COPILOT_FULL_ACCESS_EFFECTIVE=PASS
PERMISSION_PREFLIGHT=PASS
NO_PERMISSION_DOWNGRADE=PASS
PERMISSION_MISMATCH_BLOCKS_PRELAUNCH=PASS
TRAY_USAGE_DISPLAY_ONLY=PASS
COPILOT_AUTOPILOT_NOT_ENABLED=PASS
FULL_ACCESS_PERMISSION_FROM_DISPATCH=PASS
```

## 13. Non-effects

This Candidate:

- does not modify released Policy V1.8.6;
- does not modify released Routing Index V1.2.7;
- does not modify or expand `BRIDGE-DESKTOP-01-02-FIX-01`;
- grants no DEV permission by itself;
- grants no main push, merge, deploy, Production/provider/broker write or LIVE;
- does not create a separate Usage Governor service;
- does not create a separate standalone Usage DEV work package;
- does not allow Bridge to become a routing authority.

`CONTRACT_STATUS=CANDIDATE_REV4_SOURCE / GOVERNANCE=POLICY_V1.8.6_ROUTING_V1.2.7 / BASELINE=CLI_FIRST_FULL_ACCESS_DEFAULT / TOOL_COMPATIBILITY=BRIDGE_SPEC_REV7 / EXECUTION=BATCH_A / STANDALONE_DEV=NO / DEV_ALLOWED=NO_FROM_THIS_DOCUMENT`.
