# FOX2 Git-first handoff entry point

For all **new or re-scoped FOX2 work**, use the current operating set:

- released Policy: `docs/governance/FOX2_POLICY_V1.8.6.md`;
- effective Routing Index: `docs/governance/FOX2_AGENT_PROMPT_POLICY_V1_2_7_EFFECTIVE_ROUTING_INDEX_20261014.md`;
- dispatch schema: `docs/agent_handoff/FOX2_LOCAL_AGENT_DISPATCH_SCHEMA_v2.json`;
- Git-first protocol: `docs/agent_handoff/FOX2_GIT_FIRST_TASK_RESULT_PROTOCOL_v9.md`;
- Result Contract: `docs/agent_handoff/FOX2_AGENT_RESULT_SCHEMA_v2.json` + `FOX2_AGENT_RESULT_TEMPLATE_v4.md`;
- CHAT intake: `docs/agent_handoff/FOX2_CHAT_RESULT_INTAKE_CHECKLIST_v8.md`.

Historical Policy/protocol/schema/checklist files remain immutable evidence for already-bound legacy WPs. Do not silently reuse them for new work.

## Current operating rules

1. CHAT owns source binding, routing, Agent/model/tier/reasoning, permission profile, execution path, delivery owner and acceptance.
2. Codex CLI / Copilot CLI are the primary implementation engines.
3. Normal coding permission baseline is `FULL_ACCESS`; Full Access is technical execution permission, not merge/Production/LIVE authority.
4. Git delivery follows the immutable dispatch:
   - `git_code_push=YES + delivery_owner=AGENT` -> Agent may commit/push exact non-main scope;
   - `git_code_push=YES + delivery_owner=BRIDGE` -> Bridge may commit/push exact non-main scope;
   - otherwise no code publication.
5. Tool/runtime readiness is capability-based. Version mismatch alone is not a STOP if task-material capabilities exist and required validation passes.
6. One bounded WP continues through internal implementation/test/evidence/publication checkpoints. Do not create micro-WPs for ordinary operational reconciliation.
7. Post-start uncertain failure -> `NEEDS_RECONCILIATION`, dispatch consumed, no blind replay, no silent Agent substitution.
8. After remote publication, CHAT independently reads the exact SHA and decides acceptance. `PUSHED_UNREVIEWED` is delivery only.

No main push, PR creation, merge, deploy, Production/provider write, broker write or LIVE is created by these handoff documents.

See the current WP task/source lock and the active Bridge Technical Spec for task-specific details.
