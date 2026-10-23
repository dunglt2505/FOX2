---
name: fox2-mgmt-delivery
description: "Plan, prioritize, promote, track, and report FOX2 delivery in one Agile Kanban; merges triage, roadmap and project health."
---

# fox2-mgmt-delivery

**FOX2 Layer 1 — Project management — Agile Lite 0.5.8**

## Activate when
Owner asks to implement with FOX2 Skills, plan/track project status, move Master Plan work to Board, or Watch/CHAT observes new evidence.

## Input
Owner outcome, Master Plan/Roadmap feature candidates, live task status, actual Git/test/host evidence, dependencies, acceptance readiness and deadlines if supplied.

## Work to perform
1. Prioritize proven product progress and real defects, not administration.
2. Keep ONE board `BACKLOG → DOING ↔ BLOCKED → DONE`, one logical task containing `ID · goal · scope · owner · acceptance · status · evidence/blocker`. No independent stage gate or project-level R0–R7 paperwork.
3. Apply the **Board promotion contract** without duplicating features or granting authority.
4. Preserve accepted, unaffected PASS. Mark a task DONE only when evidence meets its acceptance; `prompt published`, `Agent started` and Bridge `PUSHED_UNREVIEWED` are not DONE.
5. Report real capabilities, blockers and next owner action; unknown evidence stays UNKNOWN. Prefer WIP ≤2 independent nonoverlapping writers.
6. Invoke Router only for Agent choice, Result Acceptance only on real results. Correct in SAME task; no micro-WP.

## Skill Routing Matrix — one-Whole-WP orchestration

**Trigger:** Owner says "áp dụng FOX2 Skills để triển khai", a task changes stage, Agent returns, execution fails, or Watch observes a material milestone. CHAT runs this **selection method inside the existing Management Skill**; it is **not a 12th Skill**, executable dispatcher, new gate or standing requirement to call all 11 Skills.

| Event or actual work | Select matching Skill(s), only when needed |
|---|---|
| Priority, whole-task planning, Master Plan/Board/Watch | `fox2-mgmt-delivery` |
| Agent/model/thinking/transport choice | `fox2-mgmt-agent-routing` |
| Thread/actor context transfer | `fox2-mgmt-context-handoff` |
| Compose Agent task prompt | `fox2-method-prompt-builder` |
| BRD/Tech Spec or acceptance-design change | `fox2-method-requirements-design` |
| Source authority / Dictionary contract | `fox2-method-source-contracts` |
| Real returned Git result / acceptance | `fox2-method-result-acceptance` |
| Research or evidence appraisal | `fox2-method-research-validation` |
| Authorized Git/result/doc publishing + remote SHA | `fox2-tech-publication-sync` |
| Material host/Bridge/permission preflight | `fox2-tech-route-preflight` |
| Failed/uncertain execution, quota, crash, no-replay | `fox2-tech-execution-recovery` |

**Coverage:** Classify only applicable Skills as `REQUIRED`, then `APPLIED` **only after actually reading/using** their rules and evidence; use `NOT_APPLICABLE` for out-of-scope Skills and `UNAVAILABLE` when access/capability is missing. Re-evaluate lazily at task assignment, result/rework and closure/progress sync. Report a compact coverage verdict and next safe action in the same logical task, not 11 forms. An unavailable required step blocks only dependent actions; continue safe independent work and never invent technical PASS.

**End-to-end:** CHAT is accountable for **Build → Test → Deliver → CHAT acceptance → Master Plan/Board sync → Git remote readback** when relevant; use the actual publisher for Git writes. Completion means verified outcomes, not merely a generated prompt, plan, PR or Agent start. Existing approved evidence stays valid; do not re-run consumed Dispatch or add WORK audit/Canary/LIVE without actual task need and authority.

## Evidence-driven progress synchronization (CHAT / scheduled Watch)

**Triggers:** Scheduled FOX2 Watch run; verified Agent/Bridge Git delivery; CHAT acceptance/rework; material blocker, dependency or task-status change. A Skill is not a daemon: Watch/CHAT invokes it and an authorized Git publisher writes files.

1. Read authorized Master Plan/addenda, Board, Git/CI/test/CHAT evidence; `PUSHED_UNREVIEWED` is not DONE.
2. Update **Board** on material task state, owner, SHA, blockers and next action; no duplicate WPs.
3. Update **Master Plan** on milestone/dependency/scope/roadmap change. Preserve immutable historical copies and Library/Git conflicts.
4. Delegate exact write/readback to `fox2-tech-publication-sync`: compare remote base, use authorized scoped Git ref (non-main PR if protected), verify full SHA; no implicit main merge or LIVE grant.
5. Return `SYNCED` and `BOARD_UPDATED`/`MASTER_PLAN_UPDATED` plus SHA, `NO_MATERIAL_CHANGE` (no empty commit), or `SYNC_PENDING/BLOCKED`; dedupe by verified SHA.

## Board promotion contract

Evaluate when a milestone, source, dependency or WIP slot changes, or when Owner asks to promote a feature. `READY_FOR_BOARD=YES` requires all five: `OUTCOME_DEFINED` (observable product outcome), `DEPENDENCIES_KNOWN`, `SOURCE_READY_ENOUGH` for the next safe action, `ACCEPTANCE_ACTIONABLE`, and `NEXT_SAFE_ACTION_KNOWN`. Record actual evidence and missing conditions, not speculative PASS.

Use exactly one decision: `KEEP_IN_MASTER_PLAN` (not ready/far horizon), `PROMOTE_TO_BACKLOG` (ready, not selected), `PROMOTE_TO_DOING` (ready, selected with WIP/Owner reprioritization), or `BLOCKED` (selected, real prerequisite stops next action; name unblocker). WIP capacity determines BACKLOG versus DOING, not readiness. Keep only near-term actionable work on Board, preserve the same Feature/Whole-WP identity and accepted evidence; no mirrored roadmap, duplicate task, or administrative micro-WP.

## Output
One prioritized task or concise project delivery view, including `READY_FOR_BOARD` and one promotion decision when roadmap promotion is in scope; next safe action and evidence-based DONE/DOING/BLOCKED.

## Responsibility boundary
Owns outcome priority, Master Plan→Board promotion, one Kanban and reporting. Does NOT choose Model/Thinking, write prompts, perform tests, publish governance, execute Bridge, or certify releases.

## Common rules
One logical Kanban task; only material checks for selected action. Ordinary native DEV has no mandatory Bridge/PreExec/R0–R7 paperwork. For actual Bridge execution the installed Bridge enforces its own machine protocol and no-replay; never fabricate PASS, permissions or host actions. CHAT owns result acceptance; no broker/LIVE, protected branch or irreversible side effects without real authority.
