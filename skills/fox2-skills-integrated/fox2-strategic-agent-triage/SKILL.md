---
name: fox2-strategic-agent-triage
description: Triage owner decisions and prioritize FOX2 work.
---

# fox2-strategic-agent-triage

## Agile Lite Owner-approved precedence

Use project-wide Policy v2.1.0 and `../shared/operating_rules.md`: one Kanban task, actual delivered result, necessary testing, CHAT acceptance. Historical R0-R7/PreExec/Git-prompt/Dispatch requirements apply only to the technical route which materially needs them. Preserve each specialized skill's real technical evidence requirements, protected operations, source history and no-replay. Avoid administrative micro-WPs and version-only churn.

## Activate when
Multiple competing tasks/blockers or unclear next owner.

## Work to perform
Separate source conflicts from missing authority, WIP from completed task, code cause from tooling cause, and independently required review from redundant delegation. Choose smallest actionable NEXT with risk/cost.

## Completion / stop
Priority, justification, CHAT/WORK/CODEX roles, unblock conditions.


Completion is governed by the **Execution Contract v0.3.6** below; apply conditional obligations only when triggered, report bounded HOLD otherwise.

## Execution Contract v0.3.6 — observable completion
- **TRIGGER:** Competing priorities, next actor/dependency choice or multi-stage task continuation after evidence intake.
- **PRECONDITIONS:** Owner priority, real task state, available tools/actors and release/permission boundaries.
- **REQUIRED_ACTIONS:** Compare direct CHAT work before WORK/host; choose next value-producing safe action, avoid administrative micro-handoff.
- **REQUIRED_EVIDENCE:** Task/source/priority observations, actual capability and cost limits when available.
- **DELIVERABLES:** One prioritized NEXT_SAFE_ACTION and owner/actor justification with blocker or successful action evidence.
- **VALIDATION:** Check that an authorized safe next step was attempted rather than stopping at a recommendation.
- **FAILURE_STATE:** `NEXT_ACTION_BLOCKED` / `ROUTE_NOT_VERIFIED` if no permitted action; no fabricated ongoing work.
- **COMPLETION_GATE:** Progress actual authorized work as far as possible and report one justified next action; avoid premature DONE.
## Owner-first priority and cost
Owner's current bounded decision has higher FOX2 internal priority than superseded task scheduling. Prioritize runnable offline product coding under real DEV access/rights, not administrative Bridge readiness; keep installed runtime and production gates for relevant lane. Before delegation do direct CHAT work; compare COPILOT/CODEX/WORK actual availability and cost, never default WORK for document/source work or CODEX for every coding task. Each Agent task must follow Git prompt publish → Agent remote Git result → CHAT independent readback/review. Preserve Whole-WP continuity, no replay.

## Direct first, no micro-handoffs
Do not finish at “next action recommended” when the requested outcome also authorizes CHAT to perform that safe action now. Identify and execute the smallest viable correction directly, continue through verification, and reserve WORK for required materially independent audit only. Avoid growing a single Whole-WP into administrative micro-WPs.

## Cross-stage continuation with bounded state (v0.3.5)
On task opening or stage result intake, ask `CURRENT_STAGE? EXIT_GATE_PROOF? MANDATORY_SKILLS_APPLIED? NEXT_SAFE_ACTION?`. Do not fragment six stages into administrative WPs, duplicate source versions, or call WORK for the routine next step. If a new external assignment really is necessary, call Prompt Builder and specify delivery artifacts. Do not assign a task merely because an opened feature has no stage label: classify it from evidence first.


## v0.3.7 — Domain-specific bounded recovery
Before another WP/Agent/Attempt require `FIRST_FAILURE + VALID_PASS + IMPACT_EDGE + MINIMAL_DELTA + NEXT_SAFE_ACTION`. Prefer direct CHAT review and one bounded correction; no duplicated audit or end-to-end rerun without material reason.


## v0.3.7 — Project-wide focused correction and PASS preservation
FOX2 all stages: earliest causal divergence. Accepted PASS is REUSE_VERIFIED by default; no blanket recheck. Retest only changed fact→affected gate or mandatory gates. CONSUMED Attempt cannot replay; accepted PASS evidence from it is reusable. NOT_RUN/UNKNOWN remain scoped.
