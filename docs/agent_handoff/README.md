# FOX2 Git-first handoff entry point

For all **new or re-scoped FOX2 work**, resolve the operating set from:

`docs/governance/FOX2_PROJECT_DICTIONARY_v1.json`

Current Dictionary resolution (Dictionary version 1.1):

- Policy: `docs/governance/FOX2_POLICY_V1.8.8.md`;
- Routing Index: `docs/governance/FOX2_AGENT_PROMPT_POLICY_V1_2_9_EFFECTIVE_ROUTING_INDEX_20261014.md`;
- Dispatch Schema: `docs/agent_handoff/FOX2_LOCAL_AGENT_DISPATCH_SCHEMA_v3.json`;
- PreExec Evidence Protocol: `docs/agent_handoff/FOX2_PREEXEC_EVIDENCE_PROTOCOL_v1.md`;
- Preflight Receipt Schema: `docs/agent_handoff/FOX2_PREFLIGHT_RECEIPT_SCHEMA_v1.json`;
- CHAT Preflight Intake: `docs/agent_handoff/FOX2_CHAT_PREFLIGHT_INTAKE_CHECKLIST_v1.md`;
- Git-first Protocol: `docs/agent_handoff/FOX2_GIT_FIRST_TASK_RESULT_PROTOCOL_v11.md`;
- Result Contract: `FOX2_AGENT_RESULT_SCHEMA_v2.json` + `FOX2_AGENT_RESULT_TEMPLATE_v4.md`;
- CHAT Intake: `FOX2_CHAT_RESULT_INTAKE_CHECKLIST_v9.md`.

Do not independently hard-code these as "current" in code/handoff generators. Human docs may repeat them for readability, but machine consumers resolve from the Dictionary.

## Project-wide pre-execution gate

Every new/re-scoped executable FOX2 WP now follows:

```text
source/task ready
 -> material preflight
 -> durable PASS/BLOCKED/INFRA_FAILED receipt
 -> CHAT remote readback
 -> final assignment only after PASS
 -> executable Dispatch
 -> Agent execution
```

A preflight BLOCKED state is evidence, not an Agent result. It does not consume a dispatch and must be pushed to the exact task branch when safe Git publication is available.

No task-local preflight may redefine this lifecycle.

## Canonical current transport

```text
control branch = work/FOX2-DISPATCH-chat
dispatch path  = docs/agent_handoff/DISPATCH/<dispatch_id>.json
schema         = 3.0
```

The path is deliberately version-neutral.

Legacy v2/v0.6 dispatch/control/path identities remain historical compatibility only according to the Dictionary.

## Current operating rules

1. CHAT resolves Project Dictionary first, then owns source binding/routing/preflight intake/result acceptance.
2. Codex CLI / Copilot CLI are primary implementation engines.
3. Normal coding permission currently resolves to `FULL_ACCESS`.
4. Git delivery is dispatch-owned: AGENT or BRIDGE exactly; no duplicate publisher.
5. Tool readiness is capability-based, not exact-version-based.
6. One bounded WP continues through implementation/test/evidence/publication; do not create operational micro-WPs.
7. Pre-start BLOCKED/INFRA_FAILED follows the project-wide PreExec contract; no executable Dispatch/Agent run/dispatch consumption.
8. Post-start uncertainty -> `NEEDS_RECONCILIATION`, consumed, no blind replay/substitution.
9. Supported dispatch schemas normalize into one execution representation.
10. After publication CHAT independently reads exact remote SHA; `PUSHED_UNREVIEWED` is not acceptance.

No main push, PR, merge, deploy, Production/provider write, broker write or LIVE right is created here.

Historical Policy/protocol/schema/checklist files remain immutable evidence for already-bound legacy WPs.
