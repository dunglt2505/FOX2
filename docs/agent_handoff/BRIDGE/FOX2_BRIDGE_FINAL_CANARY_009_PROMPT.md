# FOX2 Bridge Final Canary 009 — Agent Prompt

You are the selected local Agent invoked by the installed FOX2 Bridge for one immutable certification canary.

## Immutable scope

Dispatch ID:
`FOX2-BRIDGE-FINAL-CANARY-009-CODEX-001`

Expected branch:
`work/FOX2-BRIDGE-FINAL-CANARY-009`

Expected base:
`501822a33ef08c7365154913bbc677544856eee5`

You may modify **only**:

`reports/BRIDGE-DESKTOP-BATCH-B/evidence/final009/canary/**`

Do not modify application, backend, frontend, provider, broker, governance, `agent_bridge/**`, or any other path.

Do not commit or push. Delivery owner is the installed FOX2 Bridge.

## Required result

Create exactly this UTF-8/LF JSON file:

`reports/BRIDGE-DESKTOP-BATCH-B/evidence/final009/canary/agent_result.json`

with these semantic fields:

- `dispatch_id = "FOX2-BRIDGE-FINAL-CANARY-009-CODEX-001"`
- `marker = "FOX2_BRIDGE_FINAL_CANARY_009_AGENT_OK"`
- `source_head = "501822a33ef08c7365154913bbc677544856eee5"`
- `agent_product = "CODEX"`
- `delivery_owner = "BRIDGE"`
- `status = "PASS"`

The file may include additional non-secret diagnostic fields only if useful.

Then verify:
- Git changed paths contain only the required final009 canary report path;
- `git diff --check` passes.

Finally print the exact marker:

`FOX2_BRIDGE_FINAL_CANARY_009_AGENT_OK`

Do not make any other changes.
