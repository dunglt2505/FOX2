# FOX2-PREEXEC-ROLLOUT-V1 — Project-Wide Shared PreExec Implementation

**Status:** SOURCE_READY / PREEXEC_HOLD  
**Project:** FOX2  
**Class:** SYSTEMIC_SHARED_INFRASTRUCTURE / WHOLE_WP / NO_MICRO_FIXES  
**Authority:** Owner-authorized Project-Wide PreExec Implementation Mandate v1  
**Governance:** Project Dictionary v1.2 -> Policy V1.8.9 -> Routing Index V1.3.0  
**Lifecycle:** PreExec Evidence Protocol v1.1 -> Receipt Schema v1 -> CHAT Preflight Intake v1.1 -> Dispatch Schema v3 -> Protocol v12  
**CODE_ALLOWED:** YES_FOR_THIS_BOUNDED_ROLLOUT  
**Final implementation Agent:** NOT_ASSIGNED — R3/R5 HOLD

## 1. Source binding

Task branch:
`work/FOX2-PREEXEC-ROLLOUT-V1`

Accepted Bridge code base:
`3013f34d7ad91d1462e44495c873a84c41297b6b`

Aggregate-route governance/source sync head before this task rebind:
`336d621b8781fe8f7f22f1ed8fd51b5fdedcbc63`

Coordinated governance release branch/head:
`work/FOX2-AGENT-USAGE-TELEMETRY-01-chat@dc3fc5ea7e952fb377d6625885a1a078842328ee`

Normative/current sources:
- `docs/governance/FOX2_PROJECT_DICTIONARY_v1.json` — Dictionary v1.2;
- `docs/governance/FOX2_POLICY_V1.8.9.md`;
- `docs/governance/FOX2_AGENT_PROMPT_POLICY_V1_3_0_EFFECTIVE_ROUTING_INDEX_20261014.md`;
- `docs/agent_handoff/FOX2_PREEXEC_EVIDENCE_PROTOCOL_v1.1.md`;
- `docs/agent_handoff/FOX2_PREFLIGHT_RECEIPT_SCHEMA_v1.json`;
- `docs/agent_handoff/FOX2_CHAT_PREFLIGHT_INTAKE_CHECKLIST_v1.1.md`;
- `docs/agent_handoff/FOX2_GIT_FIRST_TASK_RESULT_PROTOCOL_v12.md`;
- `docs/architecture/FOX2_LOCAL_AGENT_BRIDGE_TECHNICAL_SPEC_v0.7_CANDIDATE.md` REV10;
- `docs/governance/FOX2_PROJECT_WIDE_PREEXEC_IMPLEMENTATION_MANDATE_v1.1.md`;
- `docs/governance/FOX2_AGENT_ROUTE_MATERIALITY_RELEASE_MANIFEST_20261014.json`.

No Library mirror/readback is asserted by this task.

## 2. Objective

Implement the released FOX2-wide PreExec lifecycle once as reusable orchestration infrastructure. Remove the need for independent APP/Bridge-specific lifecycle logic.

One shared engine must support:

```text
task-specific material check registration
 -> shared worktree/source checks
 -> shared capability/Agent probes
 -> PASS | BLOCKED | INFRA_FAILED
 -> Receipt Schema v1
 -> canonical sanitized artifact
 -> exact task-branch commit/push/readback
```

The implementation must remain pre-dispatch. It must never publish an executable Dispatch or start an implementation Agent.

## 3. Architecture decision

Implement the common engine inside the existing FOX2 orchestration package:

`agent_bridge/src/fox2_agent_bridge/preexec/**`

Expose one script/CLI entry under:

`agent_bridge/scripts/**`

Task-specific APP/Bridge PowerShell wrappers become thin adapters/configuration only and MUST NOT retain a competing state machine.

Agent readiness semantics are project-wide:
- Copilot/Codex candidate probes are alternative routing evidence and are normally `material=false`;
- one `eligible_agent_route` capability is `material=true`;
- aggregate PASS requires at least one allowed candidate PASS;
- CHAT chooses the final Agent after Intake; no runner silently substitutes;
- if this or a future task explicitly pins one Agent as required, that candidate becomes material and alternatives cannot satisfy it.

Rationale:
- reuses the already-proven Python/pytest/orchestration environment;
- keeps governance tooling outside business runtime;
- avoids creating a second standalone execution framework;
- allows Bridge and non-Bridge FOX2 WPs to invoke the same project-level preflight engine without importing it into application business code.

## 4. Required implementation

At minimum:

1. load/validate Dictionary-resolved PreExec identities;
2. validate produced receipt against `FOX2_PREFLIGHT_RECEIPT_SCHEMA_v1.json`;
3. common status model `PASS/BLOCKED/INFRA_FAILED`;
4. common blocker classes from Dictionary;
5. exact branch/worktree/source-head verification;
6. competing-writer/WIP fail-closed checks;
7. stale-receipt-only safe cleanup;
8. task-material capability registration/configuration;
9. safe CODEX/COPILOT minimal execution probe interface;
10. alternative-route materiality: individual candidate probes non-material by default, aggregate `eligible_agent_route` material;
11. support a task-pinned Agent override that makes the pinned candidate material;
12. sanitized failure classification — no raw unrestricted stdout/stderr in receipt;
13. canonical UTF-8/LF JSON output;
14. exact staged receipt allowlist;
15. commit -> push -> exact remote SHA readback before `RECEIPT_PUSHED`;
16. explicit:
    - `executable_dispatch_published=false`;
    - `dispatch_consumed=false`;
    - `agent_execution_started=false`;
17. no silent Agent/model/tier/reasoning/permission substitution;
18. shared CLI exit contract:
    - 0 = PASS receipt published/read back;
    - 20 = BLOCKED receipt published/read back;
    - 30+ = INFRA_FAILED / publication infrastructure failure;
19. migrate current APP-BATCH-B and BRIDGE-BATCH-B preflight wrappers to thin adapters;
20. regenerate Dictionary binding from v1.2 and prove drift;
21. remove/retire duplicated transitional lifecycle code once equivalent coverage exists.

## 5. Writable scope

Allowed implementation:
- `agent_bridge/**`;
- `docs/agent_handoff/FOX2-PREEXEC-ROLLOUT-V1/**`;
- current APP-BATCH-B / BRIDGE-BATCH-B preflight wrapper files only when converting them to thin adapters;
- `reports/FOX2-PREEXEC-ROLLOUT-V1/**`;
- generated Dictionary/runtime binding files owned by the existing generator.

Normative governance/BRD/Data Contract/Acceptance semantics are READ-ONLY during implementation.

Do not modify:
- `backend/**`;
- `frontend/**`;
- market-data/business contracts;
- provider/broker/LIVE behavior.

## 6. Required acceptance

At minimum all must PASS:

- `PROJECT_DICTIONARY_BINDING`
- `PREFLIGHT_RECEIPT_SCHEMA`
- `ALTERNATIVE_AGENT_ROUTE_MATERIALITY`
- `PINNED_AGENT_MATERIALITY`
- `PREFLIGHT_PASS_DURABLE`
- `PREFLIGHT_BLOCKED_DURABLE`
- `PREFLIGHT_INFRA_FAILED_SAFE`
- `NO_DISPATCH_BEFORE_PASS`
- `PRESTART_DISPATCH_NOT_CONSUMED`
- `NO_IMPLEMENTATION_AGENT_START`
- `NO_AGENT_SUBSTITUTION`
- `SANITIZED_FAILURE_CLASSIFICATION`
- `CANONICAL_RECEIPT_TEXT`
- `STALE_RECEIPT_ONLY_CLEANUP`
- `NO_FALSE_PUSHED_MARKER`
- `REMOTE_READBACK_REQUIRED`
- `APP_THIN_ADAPTER`
- `BRIDGE_THIN_ADAPTER`
- `FULL_SHARED_PREEXEC_TESTS`
- `CHANGED_PATH_ALLOWLIST`
- `SECRET_SCAN`
- `GIT_DIFF_CHECK`

Then generate fresh Schema-v1 receipts for APP-BATCH-B and BRIDGE-BATCH-B using the shared engine. Those receipts remain separate CHAT Preflight Intake decisions; this rollout must not self-authorize their executable Dispatches.

## 7. Routing candidates

No final Agent is assigned by this task document.

Current live evidence before aggregate-route rebind:
- rollout preflight proved CODEX PASS with pinned `gpt-6.1-sol` and FULL_ACCESS;
- COPILOT remained `AUTH_REQUIRED`;
- the prior receipt is historical because it predates the aggregate-route semantic release;
- a fresh receipt from this re-bound source is required before final assignment.

Preferred route after recovery:
1. **COPILOT / NATIVE_AUTO / balance / FULL_ACCESS** if authentication + minimal probe PASS; this is a clear bounded implementation with favorable cost.
2. **CODEX / PINNED / gpt-6.1-sol / Medium / FULL_ACCESS** if Copilot remains unavailable and Codex probe PASS.
3. Codex High only if concurrency/recovery semantics become materially difficult.

No silent fallback.

## 8. Git / protected authority

Future executable Dispatch may authorize exact non-main task-branch commit/push only.

No:
- main push;
- PR;
- merge;
- deploy;
- Production provider;
- broker write;
- LIVE.

## 9. STOP

STOP for:
- source-sync/branch/worktree mismatch;
- competing material writer;
- no eligible Agent execution proof;
- implementation requires business-runtime changes;
- receipt schema/Dictionary drift;
- secret exposure;
- required test failure;
- unexpected write outside allowlist;
- push/readback failure.

## 10. Exit

`FOX2_PREEXEC_ROLLOUT_V1=SHARED_IMPLEMENTATION_ACCEPTED`

Only after CHAT acceptance may current/future FOX2 WPs use the shared engine as the project-wide preflight implementation.

