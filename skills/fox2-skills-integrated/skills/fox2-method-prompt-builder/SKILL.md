---
name: fox2-method-prompt-builder
description: "Write bounded, high-quality Agent task prompts from a route already chosen; never own Dispatch, PreExec or result intake."
---

# fox2-method-prompt-builder

**FOX2 Layer 2 — Domain methods — Agile Lite 0.5.0**

## Activate when
CHAT has decided to delegate one residual task to CODEX, Copilot or independent WORK.

## Input
Already-selected actor/model/thinking/transport, objective, acceptance, allowed scope, applicable source context, execution constraints supplied by the actual transport.

## Work to perform
**Only six content elements:**
1. `Goal` — an observable result and reason.
2. `Scope` — allowed files/actions, exclusions, single-writer constraint when relevant.
3. `Context` — applicable BRD/TechSpec/source references and factual assumptions; exact immutable identity *when provided/required by chosen transport*.
4. `Execution` — copy the ROUTER-selected Agent/Model/Thinking unchanged; do not re-route or default High.
5. `Acceptance` — observable behavior, focused tests and material negative/regression cases.
6. `Return` — code/artifacts, actual test outcome, concise report and destination requested by the runner.

For **native DEV**, output a concise prompt directly. For **Bridge**, output task/prompt *content* matching Bridge's accepted `task.md` and `prompt.md` interface. Incorporate *supplied* delivery constraints, e.g. "Do not commit/push; Bridge publishes" when publication owner is BRIDGE. Never decide delivery owner yourself.

Prompt quality checklist: task is independently understandable; allowed scope and STOP precise; no secrets placed into a public repository; no prompt-only claim that tests/permissions were verified; rework reuses the SAME logical task. When Owner needs manual execution, request host-specific verified launch instructions from the actual execution owner; do not invent CLI flags or generate speculative PowerShell.

**Bridge boundary:** Git task/prompt publishing, SHA readback, Dispatch v3 construction/validation, route capability PreExec, decision receipt, ledger/no-replay claim, CLI launch, result transport and status progression belong to Bridge/Git technical execution, NOT this Skill. Prompt Builder may mention those constraints *as context only*.

## Output
One executable, bounded prompt (plus task text when selected transport requires it), status `PROMPT_READY` or a named missing input. `PROMPT_READY` is not DISPATCH_ADMITTED, AGENT_STARTED or DONE.

## Responsibility boundary
Owns wording and completeness of instructions ONLY. Never generates/validates Dispatch, sets technical PASS, runs PreExec, chooses route/delivery owner, publishes to Git, launches Agent or reviews result.

## Common rules
One logical Kanban task; only material checks for selected action. Ordinary native DEV has no mandatory Bridge/PreExec/R0–R7 paperwork. For actual Bridge execution the installed Bridge enforces its own machine protocol and no-replay; never fabricate PASS, permissions or host actions. CHAT owns result acceptance; no broker/LIVE, protected branch or irreversible side effects without real authority. 
