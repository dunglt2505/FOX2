---
name: fox2-status-roadmap
description: Maintain single outcome-based FOX2 Kanban across all features and agents.
---

# fox2-status-roadmap

## Activate when
Updating backlog, progress, next milestones or confirmed task closure.

## Work to perform
Use BACKLOG, DOING, BLOCKED, DONE. One record: ID, goal, scope, owner/Agent, done_when, status and result pointer/blocker. Prioritize deliverables and bugs, no parallel stage approval boards. Bridge `PUSHED_UNREVIEWED` remains DOING until CHAT reviews accepted diff/test result. WIP limit two material code writers on disjoint paths. Mark DONE only for observed acceptance, never for a Dispatch or prompt commit alone.

## Completion / stop
Produce the concrete deliverable and actual proof with DONE/REWORK/BLOCKED or a precisely named lower execution state. Do not mark completed because a prompt, Dispatch, tool invocation or plan exists. CHAT owns the end-to-end result.

## Shared operating and Bridge applicability
Apply shared `../../shared/operating_rules.md`. A routine reversible independent native task needs no Bridge Dispatch, manual R0–R7 artifact or immutable prompt publication. When and only when the actual execution is Bridge-controlled, follow `../../shared/bridge_e2e_v041.md` and the **installed** runtime contract, not an assumed current version. All source/receipt/test evidence must be observed, not invented. Old consumed attempts remain immutable and non-replayable. Complete outcomes in the SAME logical task; do not create administrative micro-WPs.
