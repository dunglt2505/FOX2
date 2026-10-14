# FOX2 — Project-Wide PreExec Evidence Implementation Mandate v1

**Status:** OWNER_AUTHORIZED / PROJECT_WIDE / SOURCE_READY  
**Date:** 2026-10-14  
**Project:** FOX2 only  
**Authority:** Owner direction + Policy V1.8.8 + Routing Index V1.2.9  
**Machine source:** Project Dictionary v1.1  
**Execution state:** CODE_ALLOWED=YES_FOR_BOUNDED_ROLLOUT / FINAL_AGENT_ASSIGNMENT=HOLD_R3_R5

## 1. Objective

Implement the released FOX2 PreExec Evidence Protocol once as shared project infrastructure and make every new/re-scoped executable FOX2 WP consume that common behavior.

This is one systemic rollout, not a collection of task-local fixes.

## 2. Required shared outcome

FOX2 must have one reusable pre-execution implementation that provides:

- common PASS/BLOCKED/INFRA_FAILED lifecycle;
- Preflight Receipt Schema v1 validation;
- material capability observation;
- exact task branch/worktree/writer checks;
- safe Agent execution probe;
- sanitized blocker classification;
- canonical UTF-8/LF receipt writer;
- exact staged allowlist;
- commit/push/remote-readback before success marker;
- safe stale-receipt-only cleanup;
- no executable Dispatch publication from the preflight layer;
- no dispatch consumption and no implementation Agent start during preflight.

Task-specific checks are registered/configured into the common layer; they do not duplicate the lifecycle.

## 3. Project application

Applies prospectively to:
- application/frontend/backend executable WPs;
- AgentBridge/Desktop WPs;
- provider-adjacent read-only WPs;
- source/release automation WPs;
- research/tooling WPs;
- future FOX2 executable WPs.

Already completed immutable work remains history.

In-flight work with an already-published executable Dispatch retains its frozen binding unless materially re-scoped.

Source-ready work without executable Dispatch — including current APP-BATCH-B and BRIDGE-BATCH-B — rebinds to this project-wide protocol before final assignment.

## 4. Authorized implementation scope

Owner authorizes bounded implementation of the project-wide rollout in shared orchestration/tooling surfaces, including as materially required:

- `agent_bridge/**`;
- shared FOX2 handoff/preflight tooling under `docs/agent_handoff/**`;
- generated Dictionary/runtime bindings;
- tests for shared pre-execution behavior;
- `reports/**/preexec/**` receipts/evidence;
- task-local preflight wrappers only as thin adapters to the shared implementation.

Business application/domain behavior is not authorized for modification merely to implement this protocol.

Do not alter:
- BRD business semantics;
- Market Data Contract semantics;
- M1 Acceptance semantics;
- provider/broker/LIVE rights.

## 5. Required tests

At minimum:

- `PREFLIGHT_RECEIPT_SCHEMA=PASS`
- `PREFLIGHT_PASS_DURABLE=PASS`
- `PREFLIGHT_BLOCKED_DURABLE=PASS`
- `PREFLIGHT_INFRA_FAILED_SAFE=PASS`
- `NO_DISPATCH_BEFORE_PASS=PASS`
- `PRESTART_DISPATCH_NOT_CONSUMED=PASS`
- `NO_IMPLEMENTATION_AGENT_START=PASS`
- `NO_AGENT_SUBSTITUTION=PASS`
- `SANITIZED_FAILURE_CLASSIFICATION=PASS`
- `CANONICAL_RECEIPT_TEXT=PASS`
- `STALE_RECEIPT_ONLY_CLEANUP=PASS`
- `NO_FALSE_PUSHED_MARKER=PASS`
- `REMOTE_READBACK_REQUIRED=PASS`
- `PROJECT_DICTIONARY_BINDING=PASS`
- `CHANGED_PATH_ALLOWLIST=PASS`
- `SECRET_SCAN=PASS`
- `GIT_DIFF_CHECK=PASS`

## 6. Routing / execution

This mandate grants CODE_ALLOWED for the bounded project-wide rollout, but does not select an implementation Agent by itself.

Before execution CHAT still performs the current R3/R5 preflight for the rollout worktree and compares:
- Copilot CLI;
- Codex CLI;
- CHAT direct changes only when suitable and bounded;
- WORK only for independent audit/readiness, not primary coding.

No silent fallback.

## 7. Delivery / protected authority

Implementation may publish only the exact authorized non-main rollout branch/result according to its future executable Dispatch.

This mandate grants no:
- main push;
- PR creation;
- merge;
- deploy;
- Production provider access;
- broker write;
- LIVE.

## 8. Exit

Project-wide rollout is complete only when shared implementation and tests are accepted and current source-ready WPs consume it without retaining independent competing lifecycle logic.

`FOX2_PREEXEC_ROLLOUT_V1=OWNER_AUTHORIZED / PROJECT_WIDE=YES / CODE_ALLOWED=BOUNDED / MICRO_FIXES=NO / MERGE=NO / LIVE=NO`
