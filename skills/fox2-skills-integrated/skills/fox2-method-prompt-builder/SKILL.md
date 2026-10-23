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
6. `Return` — require a **Git-backed result handoff**: delivered code/artifacts or report, actual test outcomes, the **authorized result branch**, who is allowed to publish (Agent/Bridge/authorized CHAT publisher), and the **observed remote result commit SHA** to return to CHAT. When the selected runner does not supply a valid destination or delivery ownership, identify the missing information before claiming an executable handoff. Report `GIT_DELIVERY_PENDING` until remote publication/readback is proven; a chat summary or local change is not result delivery.

For **native DEV**, output a concise prompt directly without mandatory Git-*prompt* publication, but **require Agent code and material reports to be committed and pushed to the authorized Git result branch** when the Agent has that permission. State the result branch and return remote SHA. For **Bridge**, output task/prompt *content* matching Bridge's accepted `task.md` and `prompt.md` interface. **When `delivery_owner=AGENT`, instruct Agent to commit/push on the authorized task branch; when `delivery_owner=BRIDGE`, instruct Agent explicitly NOT to commit/push and leave result publication to Bridge**. The selected runner supplies delivery ownership; Prompt Builder never chooses or changes it. For **WORK/read-only with Git delivery in task contract**, push report/evidence to authorized report branch if permitted; otherwise deliver exact file bytes to the separately authorized publisher, preserving author/publisher provenance. No alternative channel counts as Git completion until the authorized publisher pushes and CHAT can read back the remote SHA.

Prompt quality checklist: task is independently understandable; **return instructions always give a Git result destination/branch and publication owner for delegated Agent work, with remote readback as delivery criterion**; allowed scope and STOP precise; no secrets placed into a public repository; no prompt-only claim that tests/permissions were verified; rework reuses the SAME logical task. When Owner needs manual execution, request host-specific verified launch instructions from the actual execution owner; do not invent CLI flags or generate speculative PowerShell.

**Bridge boundary:** The Prompt Builder **writes the Agent instruction to deliver via Git**, but never publishes or verifies commits itself. Git task/prompt publishing, SHA readback, Dispatch v3 construction/validation, route capability PreExec, decision receipt, ledger/no-replay claim, CLI launch, result transport and status progression belong to Bridge/Git technical execution, NOT this Skill. Prompt Builder may mention those constraints *as context only*.

## Output
One executable, bounded prompt (plus task text when selected transport requires it), status `PROMPT_READY` or a named missing input. `PROMPT_READY` is not DISPATCH_ADMITTED, AGENT_STARTED or DONE.

## Responsibility boundary
Owns wording and completeness of instructions ONLY. Never generates/validates Dispatch, sets technical PASS, runs PreExec, chooses route/delivery owner, publishes to Git, launches Agent or reviews result.

## Common rules
One logical Kanban task; only material checks for selected action. Ordinary native DEV has no mandatory Bridge/PreExec/R0–R7 paperwork. For actual Bridge execution the installed Bridge enforces its own machine protocol and no-replay; never fabricate PASS, permissions or host actions. CHAT owns result acceptance; no broker/LIVE, protected branch or irreversible side effects without real authority. 
