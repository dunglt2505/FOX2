---
name: fox2-method-prompt-builder
description: "Write bounded, high-quality Agent task prompts from a route already chosen; never own Dispatch, PreExec or result intake."
---

# fox2-method-prompt-builder

**FOX2 Layer 2 — Domain methods — Agile Lite 0.5.9**

## Activate when
CHAT delegates one residual task to CODEX, Copilot or independent WORK. For interactive FOX2 coding, honor Router-selected **Codex Extension in Visual Studio Code (VS Code)** as the preferred delivery surface.

## Input
Router-selected actor/model/thinking/transport; exact task objective, scoped workspace/worktree and branch (when observed), accepted sources, tests, write allowlist, Git delivery owner and STOP rules.

## Work to perform
Write one self-contained **VS Code-ready Codex prompt** in six elements, without changing the Router-selected route:
1. `Goal` — observable task result and reason.
2. `Scope` — exact allowed code/test/report paths, excluded actions, worktree/branch and single-writer boundary.
3. `Context` — BRD/TechSpec, immutable source SHA when required, accepted earlier evidence and constraints.
4. `Execution` — selected CODEX/Model/Thinking/transport unchanged; for VS Code, work from the **already opened correct workspace** using Codex Extension, inspect existing code, implement, run focused real tests, and stop at the first material failure. Do not generate a Windows PowerShell launcher for ordinary interactive coding.
5. `Acceptance` — concrete behavior, actual test commands/results, negative/regression checks and explicit `CODE_CHANGE` or `TEST_EVIDENCE_ONLY` semantics.
6. `Return` — actual changed paths, tests/results, report/evidence path, authorized Git result ref, designated publisher and full remote commit SHA after readback. State the **authorized result branch**, **remote result commit SHA** and verified remote SHA. A CHAT summary or local file is not Git delivery.

### Visual Studio Code / Codex Extension handoff contract

- **Preferred for interactive coding only when Router selected it.** Return a single paste-ready prompt and brief handoff instruction: open correct FOX2 worktree as the VS Code workspace; select Codex Extension session; paste/send prompt there. Do **not** claim to open VS Code, inject text into its extension, start an Agent or set a model/effort through an unverified connector.
- Only observed IDE acknowledgement permits Agent start claim; otherwise `PROMPT_READY / IDE_HANDOFF_PENDING`, not `AGENT_STARTED`. No extra WP.
- No automatic PowerShell/CLI launch or Bridge Dispatch for this **native IDE route**; if a task explicitly requires Bridge/headless execution, keep its installed machine contract and locked route. Never rebind/replay consumed Dispatch.
- Publisher selection remains Router/authorized execution contract's responsibility: `delivery_owner=AGENT` means an authorized Codex Agent commits/pushes; `delivery_owner=BRIDGE` means Agent does NOT push and independent Bridge publishes **only when its integration with this worktree/IDE outcome is actually proven**. Otherwise use separately authorized exact-artifact publication; missing publication proof = `GIT_DELIVERY_PENDING`. Never double-push or rely on Agent tail-push after token exhaustion.
- Distinguish `PROMPT_READY`, actual IDE handoff acknowledgement, `AGENT_RUNNING`, `GIT_RESULT_PUBLISHED` and `CHAT_ACCEPTED` as separate facts. CHAT reviews exact remote SHA/tests before DONE and synchronizes the single Master Plan/Board when materially changed.

### PowerShell 5.1 / `pwsh` 7 and Git scripting (exception only)

Generate a PowerShell launcher only for explicitly selected verified host route; prefer tested host launchers. Bind observed `powershell.exe` 5.1 vs `pwsh.exe` 7, absolute `git.exe` path, worktree/branch/base SHA, rights and STOP. Require syntax/test on target shell; until run label `NOT_RUN`.

Call native executable variables with `& $Git`, not `(GV ...)`, the `GV` alias, or `$Git -C ...`; check `$LASTEXITCODE` **immediately** after native Git. Read-only example:

```powershell
$Git = (Get-Command git -CommandType Application -ErrorAction Stop).Source
$head = & $Git -C $Worktree rev-parse --verify HEAD
if ($LASTEXITCODE -ne 0) { throw 'STOP: Git failed' }
```

No unverified CLI flags, unsafe reset, blind `git add -A`, force push, parallel publisher or unsupported PowerShell assumptions.

### Return modes: `CODE_CHANGE` / `TEST_EVIDENCE_ONLY`

Without an explicitly selected mode, set `UNRESOLVED`. `CODE_CHANGE` normally requires authorized code diff and actually executed tests. A specifically authorized `TEST_EVIDENCE_ONLY` task means **no product code diff is required** if **actual required tests** ran against pinned source/worktree, with command, observed exit code/output, nonempty authorized evidence/report and verified pushed remote SHA. Stale or `NOT_RUN` tests, empty success reports or Agent-declared PASS alone do not pass. Reclassifying a code task as evidence-only requires CHAT review; no silent mode change.

Checklist: exact scope, STOP, route, tests, result ref/publisher, no public Git secrets. Unknown IDE capability/rights: name blocker, never fake PASS; same logical task.

**Bridge boundary:** Prompt Builder **never publishes or verifies commits itself**; it writes content, **not** Dispatch v3, preflight/decision receipts, CLI launch, Git commits, no-replay ledger or result acceptance; the installed Bridge/authorized publisher owns those operations. VS Code is not presumed to expose a Bridge-observable completion signal.

## Output
One VS Code Codex Extension-ready bounded prompt when IDE route chosen, or correctly selected alternative prompt. Return `PROMPT_READY / IDE_HANDOFF_PENDING` for non-automated handoff, or exact observed acknowledgement if available; never equate prompt completion to `AGENT_STARTED` or DONE.

## Responsibility boundary
Owns wording and completeness ONLY. **Never generates/validates Dispatch**, **chooses route/delivery owner**, **runs PreExec**, **publishes to Git**, launches Agents or reviews results. All Git and source rights remain external.

## Common rules
One logical Kanban task; only material checks for selected action. Native reversible DEV needs no Bridge/R0–R7 paperwork; Bridge follows actual installed no-replay/permission rules. CHAT owns result acceptance; no broker/LIVE, protected branch or irreversible side effects without real authority.
