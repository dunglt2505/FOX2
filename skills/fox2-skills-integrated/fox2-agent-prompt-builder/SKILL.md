---
name: fox2-agent-prompt-builder
description: Write precise, executable Agent prompts from an already selected route; no Dispatch/PreExec/Bridge execution ownership.
---

# fox2-agent-prompt-builder

## Activate when
CHAT must delegate a bounded residual implementation or independent audit task to CODEX, Copilot or WORK.

## Work to perform
**Input:** task objective and acceptance, Owner-approved scope, selected Actor/Model/Thinking from `fox2-agent-route-runtime`, relevant BRD/TechSpec/source context, tool limitations and delivery constraints that the actual execution route provides.

**Output:** one concise Agent instruction (and `task.md` text when the selected transport requires a separate task artifact), containing:
1. **Goal:** observable result and why it matters.
2. **Scope:** allowed changes, excluded paths/actions, one writer if necessary.
3. **Context:** source documents and factual constraints; reference exact immutable versions only if the chosen transport requires them.
4. **Execution direction:** reuse the *already selected* Actor/Model/Thinking; do not re-route or default High.
5. **Acceptance:** required behavior, focused tests, negative/regression cases where material.
6. **Return:** changed code/artifact, test outcomes, short blocker/result summary and the requested destination.

For **native DEV**, provide the prompt directly; no Git handoff bureaucracy. For **Bridge**, provide the same task content in the format the Bridge task/prompt publisher accepts. Incorporate constraints supplied by Bridge, e.g. if Bridge publishes the result, instruct Agent not to commit/push. The *publisher/Bridge* owns Git publication, commit/blob hashes, Dispatch Schema v3, route verification, PreExec, delivery ownership, ledger, host launch and result transport. Do not infer these facts from the prompt or populate technical PASS receipts.

If a human must operate a local CLI, do not invent host commands; pass the need for a verified launch procedure to the actual host-execution owner. The Agent prompt is not a substitute for a verified PowerShell script.

## Completion / stop
One usable, bounded prompt/task-content artifact, with acceptance and result contract. `PROMPT_READY` is not `AGENT_STARTED`, `DISPATCH_ADMITTED` or `DONE`. If route, authorization or essential context is missing, report that precise dependency, not a new approval document.

## Responsibility boundary
Own **only task wording and quality**. Route Runtime chooses Agent/model; Git/Bridge handles source publication, Dispatch, PreExec and delivery owner; Result Review judges returned work. Do not create additional approval stages, artifacts or WPs.

## Shared operating and Bridge applicability
FOX2 Agile Lite: one logical task, Build → Test → Deliver, CHAT owns outcome. Use only relevant methods and real evidence. Ordinary native DEV has no mandatory R0–R7/PreExec/Dispatch/extra approval; if the selected real route is Bridge or high-risk, its installed technical controls remain authoritative. No unrelated version churn, protected operations or consumed-attempt replay. This Skill does not authorize execution or grant external rights.
