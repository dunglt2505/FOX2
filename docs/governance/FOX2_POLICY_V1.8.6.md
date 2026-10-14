# FOX2 — POLICY V1.8.6 | CLI-FIRST EXECUTION + DISPATCH-OWNED DELIVERY

**Document ID:** `FOX2-POLICY-V1`  
**Version:** `1.8.6`  
**Status:** `RELEASED_EFFECTIVE`  
**Project:** `FOX2 ONLY`  
**Date:** 2026-10-14  
**Released predecessor:** `FOX2_POLICY_V1.8.5.md`  
**Purpose:** preserve the simplified FOX2 routing model while making Codex CLI and Copilot CLI the primary implementation engines, binding technical permission and Git delivery authority explicitly in each immutable handoff, and replacing version-string gating with task-material capability checks.

> **Owner release decision 2026-10-14:** “triển khai các tài liệu và policy liên quan đi, để áp dụng cho dự án FOX2”. This release supersedes V1.8.5 for new or re-scoped FOX2 work. Existing in-flight immutable work keeps its frozen binding unless a material impact requires transition.

## 1. FOX2 operating model

```text
Owner
  -> CHAT decides/decomposes/binds exact WP
  -> up to two independent implementation lanes
       -> Copilot CLI
       -> Codex CLI
  -> optional Local Bridge transport/supervision
  -> selected Agent implements/tests in isolated worktree/branch
  -> authorized delivery owner publishes exact non-main result
  -> CHAT independently reads back and reviews immutable remote result
```

Codex CLI and Copilot CLI are the primary implementation engines.

CHAT remains the routing, source-binding and acceptance authority.

Bridge is an optional local transport/supervision component. It is not a second governance engine and does not replace CHAT or the selected Agent.

## 2. Parallel lane control

FOX2 may keep up to:

```text
MAX_PARALLEL_MATERIAL_WRITERS = 2
```

when:

- WPs are dependency-safe for concurrent work;
- shared interfaces required by both lanes are frozen enough for the planned scope;
- branches/worktrees are distinct;
- writable file paths do not overlap;
- each lane has one accountable writer and its own tests/evidence.

A blocked lane does not freeze an unrelated safe lane.

## 3. CHAT-FIRST assignment and whole-WP continuity

Before executable assignment, CHAT performs the applicable governance/routing checks once and binds an exact WP.

A bounded WP continues through its internal implementation/test/evidence checkpoints without repeated Owner confirmation unless a material execution input changes.

Do not fragment one engineering objective into repeated Owner-facing micro-WPs merely because an internal test, evidence file, Git state or tool condition needs reconciliation.

Create a new WP only at a genuine ownership, dependency, authority, safety, architecture or review boundary.

## 4. Minimum immutable executable handoff

Every executable coding handoff must bind at least:

```yaml
wp_id: <exact>
source_lock: <immutable refs>

role: <implementation role>
agent:
  product: COPILOT|CODEX
  model_policy: <NATIVE_AUTO|PINNED|other approved exact policy>
  auto_tier: <efficiency|balance|intelligence|null>
  model: <exact|null>
  reasoning_effort: <low|medium|high|null>
  permission_profile: <FULL_ACCESS|other explicitly approved profile>

execution_path: BRIDGE|MANUAL_LOCAL|VSCODE_ONE_CLICK
delivery_owner: AGENT|BRIDGE

worktree: <exact>
branch: <exact non-main>
base_sha: <full SHA>

allowed_code_paths: [...]
allowed_report_paths: [...]

permissions:
  code_allowed: YES|NO
  git_code_push: YES|NO
  git_report_write: YES|NO
  git_report_push: YES|NO
  pr_create: NO
  merge_allowed: NO
  production_provider: NO
  broker_write: NO
  live: NO

required_tests: [...]
stop_if:
  - material_source_drift
  - writer_collision
  - scope_violation
  - required_test_failure
  - secret_exposure
  - denied_required_access
  - material_required_capability_missing
```

An omitted field must not be guessed when material to the operation.

## 5. CLI-FIRST permission baseline

For normal FOX2 coding execution:

```text
permission_profile = FULL_ACCESS
```

CHAT owns the permission decision.

The selected local execution layer applies the exact permission profile. Bridge may translate and verify the profile when Bridge is in the execution path, but Bridge must not invent, broaden, reduce or substitute it.

Canonical intent:

```text
CODEX FULL_ACCESS
= danger-full-access sandbox semantics
+ approval_policy = never

COPILOT FULL_ACCESS
= allow-all semantics
= all required tools + paths + URLs
```

Full Access is technical execution permission. It does not create project authority for main push, merge, deploy, Production/provider access, broker write or LIVE.

Autopilot is a separate execution-mode decision and is not implied by Full Access.

If the requested permission profile cannot be applied exactly, fail before Agent execution and return a permission-profile mismatch. Do not silently downgrade.

## 6. Dispatch-owned Git delivery

Git publication authority follows the immutable handoff.

```text
git_code_push = YES
+ delivery_owner = AGENT
=> selected Agent may stage/commit/push the exact authorized non-main task branch
=> CHAT performs independent remote readback and acceptance

git_code_push = YES
+ delivery_owner = BRIDGE
=> Bridge may stage/commit/push only the exact authorized non-main task scope
=> CHAT performs independent remote readback and acceptance

git_code_push = NO
=> neither Agent nor Bridge may publish code-result changes
```

Bridge is not the default Git owner merely because it launched an Agent.

CHAT must not create a duplicate publication path after an authorized result has already been published.

Once a WP has `git_code_push=YES`, ordinary commits/pushes within that exact WP do not require repeated Owner approval. New approval is required only for a material authority change.

## 7. Material Tool Compatibility Rule

Version equality is not readiness.

```text
VERSION_MATCH != READINESS

REQUIRED_CAPABILITIES_SUFFICIENT
+ REQUIRED_TESTS_PASS
+ TASK_SEMANTICS_CORRECT
= READY
```

A tool/runtime version, optional capability, UI state, quota detail or metadata field becomes a hard gate only when it materially affects correctness, safety, compatibility or executability of the current immutable task.

Examples:

- Python/Node/runtime differs from a declared/preferred version, but the current task does not rely on version-specific behavior and required tests pass -> record deviation and continue;
- Git/Codex/Copilot version differs, but all dispatch-required capabilities are available -> continue;
- required syntax/ABI/protocol/permission/model/output/authentication/safety capability is absent -> block;
- capability state is unknown and that capability is material -> hold and return to CHAT;
- unknown/non-exposed information that is non-material -> record and continue.

Do not create a STOP solely because a version string differs.

## 8. UNKNOWN / NOT_EXPOSED materiality

`UNKNOWN`, `NOT_EXPOSED`, `STALE` and missing numeric telemetry block only when material to the operation being performed.

Missing quota percentage alone does not block a launch if the selected Agent can actually execute and no material capacity restriction is observed.

A known explicit restriction may block even when a derived percentage appears available.

## 9. Bridge governance boundary

For Policy purposes Bridge may:

1. receive an immutable dispatch already authorized by CHAT/Owner;
2. verify transport identity and minimum task-material runtime facts;
3. apply/verify the exact dispatch-owned permission profile when Bridge launches the Agent;
4. invoke the exact selected Agent without silent substitution;
5. supervise observable process state;
6. collect/persist result and telemetry;
7. preserve single-use/replay/reconciliation safety;
8. publish the result only when the dispatch explicitly assigns `delivery_owner=BRIDGE`.

Bridge MUST NOT:

- rerun CHAT governance decisions;
- reinterpret requirements or scope;
- change Agent/model/tier/reasoning/permission profile;
- decide semantic acceptance;
- create new authority;
- silently downgrade permissions;
- blind-retry a consumed dispatch;
- substitute Agents after runtime failure;
- auto-merge/deploy;
- grant Production/provider/broker/LIVE rights.

## 10. Post-start failure and reconciliation

If an Agent has started and then returns non-zero due to quota, authentication, capacity or another execution-uncertain condition:

```text
execution = NEEDS_RECONCILIATION
dispatch = consumed
no blind replay
no automatic Agent substitution
```

Preserve observable exit/checkpoint/WIP evidence.

Proven pre-spawn failures may remain terminal/actionable when non-execution is established.

## 11. Agent usage telemetry and next routing

Usage/capacity telemetry is an input to the next CHAT routing decision.

Bridge may collect and persist telemetry but must not route, switch Agent, wait for reset and relaunch, or rewrite the dispatch based on usage.

CHAT selects Agent/model/tier/reasoning for the next task using current evidence, materiality, cost and risk.

## 12. Source transition

A newer released Policy/Technical source appearing after a WP started does not automatically invalidate the in-flight WP.

```text
NEW_RELEASE
  -> MATERIAL_TO_THIS_WP ?
       NO  -> keep frozen binding and continue
       YES -> preserve WIP/evidence and rebind only affected assumptions
```

New or re-scoped WPs use the newest applicable released source.

## 13. Evidence and systemic-vs-operational fixes

Required task evidence must be complete enough for CHAT remote readback and acceptance.

Operational state reconciliation such as staging/index cleanup, stale local metadata or a non-material version deviation does not by itself justify a new corrective WP.

A reproducible systemic defect that affects a shared generator, adapter, ledger, permission path or evidence pipeline should be fixed once in the current consolidated implementation batch when dependency-safe, rather than through repeated file-specific micro-fixes.

Technical formatting/canonicalization requirements belong in the applicable Technical Spec/Result Contract.

## 14. Non-effects

This release creates no blanket DEV authority outside an exact WP.

It creates no main push, merge, deployment, Production/provider write, broker write, LIVE, auto-rework, auto-merge or autonomous routing right.

BRD/Data Contract/Acceptance semantics are unchanged unless separately revised.

## 15. Release acceptance

For new/re-scoped FOX2 work:

- CLI-first execution is the normal coding path;
- Full Access is the normal coding permission profile unless CHAT explicitly binds another profile;
- permission mismatch fails closed before launch;
- Agent/model/tier/reasoning/permission are immutable after publish;
- Git delivery owner is explicit;
- Agent-owned Git delivery is permitted when `git_code_push=YES`;
- no duplicate Agent/Bridge publication path exists;
- CHAT always performs independent immutable remote readback;
- exact version mismatch is non-blocking when task-material capabilities and tests are sufficient;
- missing material capability blocks/holds;
- non-material UNKNOWN/NOT_EXPOSED does not block;
- post-start execution uncertainty becomes reconciliation, not blind replay;
- whole-WP continuity is preferred over micro-WP fragmentation;
- no main/merge/deploy/Production/broker/LIVE right is created.

`FOX2_POLICY_V1_8_6_STATUS=RELEASED_EFFECTIVE / CLI_FIRST=YES / FULL_ACCESS_DEFAULT=YES / GIT_DELIVERY=DISPATCH_OWNED / TOOL_READINESS=CAPABILITY_BASED / BRIDGE=TRANSPORT_SUPERVISION_NOT_ROUTING`
