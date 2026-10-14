# FOX2 Git-first handoff entry point

For all **new or re-scoped FOX2 work**, resolve the operating set from:

`docs/governance/FOX2_PROJECT_DICTIONARY_v1.json`

Current Dictionary resolution:

- Policy: `docs/governance/FOX2_POLICY_V1.8.7.md`;
- Routing Index: `docs/governance/FOX2_AGENT_PROMPT_POLICY_V1_2_8_EFFECTIVE_ROUTING_INDEX_20261014.md`;
- Dispatch Schema: `docs/agent_handoff/FOX2_LOCAL_AGENT_DISPATCH_SCHEMA_v3.json`;
- Git-first Protocol: `docs/agent_handoff/FOX2_GIT_FIRST_TASK_RESULT_PROTOCOL_v10.md`;
- Result Contract: `FOX2_AGENT_RESULT_SCHEMA_v2.json` + `FOX2_AGENT_RESULT_TEMPLATE_v4.md`;
- CHAT Intake: `FOX2_CHAT_RESULT_INTAKE_CHECKLIST_v9.md`.

Do not independently hard-code these as "current" in code/handoff generators. Human docs may repeat them for readability, but machine consumers resolve from the Dictionary.

## Canonical current transport

```text
control branch = work/FOX2-DISPATCH-chat
dispatch path  = docs/agent_handoff/DISPATCH/<dispatch_id>.json
schema         = 3.0
```

The path is deliberately version-neutral.

Legacy v2/v0.6 dispatch/control/path identities remain historical compatibility only according to the Dictionary.

## Current operating rules

1. CHAT resolves Project Dictionary first, then owns source binding/routing/acceptance.
2. Codex CLI / Copilot CLI are primary implementation engines.
3. Normal coding permission currently resolves to `FULL_ACCESS`.
4. Git delivery is dispatch-owned: AGENT or BRIDGE exactly; no duplicate publisher.
5. Tool readiness is capability-based, not exact-version-based.
6. One bounded WP continues through implementation/test/evidence/publication; do not create operational micro-WPs.
7. Post-start uncertainty -> `NEEDS_RECONCILIATION`, consumed, no blind replay/substitution.
8. Supported dispatch schemas normalize into one execution representation.
9. After publication CHAT independently reads exact remote SHA; `PUSHED_UNREVIEWED` is not acceptance.

No main push, PR, merge, deploy, Production/provider write, broker write or LIVE right is created here.

Historical Policy/protocol/schema/checklist files remain immutable evidence for already-bound legacy WPs.
