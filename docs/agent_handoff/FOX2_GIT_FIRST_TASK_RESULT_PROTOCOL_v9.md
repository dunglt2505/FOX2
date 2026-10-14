# FOX2 — Git-first Task/Result Protocol v9 — Policy V1.8.6

**Controlling authority:** Released `FOX2_POLICY_V1.8.6.md` + effective Routing Index `V1.2.7`. This operational guide is not a second Policy or a merge/DEV grant. **Supersedes protocol v8 for newly dispatched/re-scoped WPs** without rewriting legacy submissions.

## 1. Current task-source set

For new/re-scoped implementation WPs use:

- `docs/governance/FOX2_POLICY_V1.8.6.md` and its release evidence;
- `docs/governance/FOX2_AGENT_PROMPT_POLICY_V1_2_7_EFFECTIVE_ROUTING_INDEX_20261014.md`;
- `docs/agent_handoff/FOX2_LOCAL_AGENT_DISPATCH_SCHEMA_v2.json`;
- `docs/agent_handoff/FOX2_AGENT_RESULT_SCHEMA_v2.json`;
- `docs/agent_handoff/FOX2_AGENT_RESULT_TEMPLATE_v4.md`;
- `docs/agent_handoff/FOX2_CHAT_RESULT_INTAKE_CHECKLIST_v8.md`;
- exact WP task/source/technical/acceptance sources bound by CHAT.

Historical protocols/schemas remain evidence only for already-bound legacy WPs.

## 2. CHAT source and routing responsibility

Before executable implementation, CHAT performs once:

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

CHAT owns source recovery/synchronization and must not delegate missing official-source repair to the implementation Agent.

A newer source release does not automatically invalidate an in-flight WP; apply the Policy V1.8.6 material-impact transition rule.

## 3. CLI-first execution

Codex CLI and Copilot CLI are the primary implementation engines.

Normal coding permission baseline:

```text
permission_profile = FULL_ACCESS
```

CHAT binds Agent/model/tier/reasoning/permission. Bridge or direct CLI execution applies the exact values; no silent substitution or downgrade.

Autopilot is separate from Full Access and must be explicitly selected if ever used.

## 4. Dispatch v2

New/re-scoped executable WPs use `FOX2_LOCAL_AGENT_DISPATCH_SCHEMA_v2.json`.

The dispatch binds:

- exact Agent and model policy;
- exact permission profile;
- execution path;
- explicit `delivery_owner=AGENT|BRIDGE`;
- exact worktree/branch/base;
- allowed code/report paths;
- Git permissions;
- material required capabilities;
- required tests and STOP conditions;
- `max_runs=1`.

Bridge does not rerun CHAT governance.

## 5. Material tool compatibility

Readiness is capability-based, not version-string-based.

A version difference is recorded and continues when all task-material capabilities are available and required validation passes.

Missing material capability blocks. Unknown material capability holds. Non-material UNKNOWN/NOT_EXPOSED does not block.

Do not create a separate corrective WP for a non-material runtime/version deviation.

## 6. Whole-WP continuity

One bounded WP continues across implementation, tests, evidence generation and authorized publication until a genuine STOP or final delivery.

Operational reconciliation such as Git index cleanup, stale local metadata or rerunning a validator is not a new assignment.

A systemic shared-component defect should be fixed once in the current dependency-safe consolidated batch instead of repeated file-specific micro-fixes.

## 7. Result Contract v2 delivery

Required result remains:

- `reports/<WP_ID>/report.md`;
- `reports/<WP_ID>/evidence_manifest.json`;
- `reports/<WP_ID>/evidence/**` as required.

All material PASS claims must resolve to actual evidence.

Generated text-artifact canonicalization/hygiene follows the applicable Technical Spec/Result Contract.

## 8. Git delivery ownership

Publication follows the immutable dispatch.

```text
git_code_push=YES + delivery_owner=AGENT
=> Agent stages/commits/pushes exact allowed task scope on assigned non-main branch

git_code_push=YES + delivery_owner=BRIDGE
=> Bridge stages/commits/pushes exact allowed task scope on assigned non-main branch

git_code_push=NO
=> no code-result publication
```

Do not ask Owner again for ordinary authorized commits/pushes inside the same exact WP.

Do not create duplicate Agent/Bridge publication paths.

Main push, PR creation, merge, deploy, Production/provider, broker write and LIVE remain forbidden unless separately authorized by a later controlling decision.

## 9. Runtime failure

After Agent start, non-zero/quota/auth/capacity uncertainty is:

```text
NEEDS_RECONCILIATION
dispatch consumed
no blind replay
no automatic Agent substitution
```

Preserve checkpoints/WIP/exit evidence.

Proven pre-spawn failure may remain terminal/actionable.

CHAT decides any replacement or retry dispatch.

## 10. Agent delivery receipt

After true remote publication, Agent or Bridge returns only the factual delivery identity:

```text
repo
WP
branch
full remote commit SHA
delivery_owner
actual Agent
result paths
PUSHED_UNREVIEWED
```

A local commit is not a remote delivery.

The in-commit manifest does not self-reference its own containing Git SHA.

## 11. CHAT independent intake

CHAT reads the immutable remote SHA, validates result/schema/diff/source/grants/evidence, and issues a separate review decision:

```text
ACCEPTED
ACCEPTED_PARTIAL
REWORK
BLOCKED
```

No Agent/Bridge self-acceptance.

Push is delivery only, never acceptance.

## 12. Non-effects

Protocol v9 creates no DEV authority beyond the exact handoff and no main/merge/deploy/Production/broker/LIVE right.

`PROTOCOL_STATUS=V9_CURRENT_FOR_NEW_WP / POLICY=V1.8.6 / ROUTING=V1.2.7 / DISPATCH_SCHEMA=V2 / RESULT_CONTRACT=V2`
