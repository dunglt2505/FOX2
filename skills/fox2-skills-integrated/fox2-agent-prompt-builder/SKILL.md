---
name: fox2-agent-prompt-builder
description: Create one concise runnable instruction only when delegation is needed.
---

# fox2-agent-prompt-builder

**FOX2 Skills source v0.4.0 candidate — not installed.**

## Activate when
Create one concise runnable instruction only when delegation is needed.

## Action
Include objective, scope/allowed writes, agent/model/thinking where material, acceptance, output pointer, and STOP risk. Use Git-pinned prompt and receipts only if an actually chosen runtime requires them or irreversible risk merits it.

## Output
Produce the concrete task-specific result, actual supporting evidence, remaining risks or blocker, and next useful action. No extra review/approval stage unless the action itself requires one.

## Shared operating rules
The canonical source is `../shared/operating_rules.md`. In environments unable to read sibling resources, apply this minimum: one task → working output → relevant tests → CHAT review; no routine administrative PreExec/Dispatch/17-Skill gate; preserve real rights, risk controls, immutable historical evidence and no-replay. Never auto-claim installed adoption.
