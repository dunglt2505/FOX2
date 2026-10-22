---
name: fox2-execution-recovery
description: Locate first causal execution failure, preserve PASS, and prevent unsafe replay.
---

# fox2-execution-recovery

## Activate when
Agent/Bridge/native task execution fails, stalls or has uncertain side effects.

## Work to perform
Inspect concrete error, stage, changed dependency, expected state and observed side effects. For native DEV, correct the causal defect within the existing task; reuse prior accepted evidence and run focused/impacted tests. For Bridge, use actual poll/ledger/host/result Git observations to distinguish NOT_STARTED, CLAIMED/RUNNING, AGENT_EXITED/PUBLISHING, PUSHED_UNREVIEWED and NEEDS_RECONCILIATION. A timeout is not proof of no execution. If claimed/consumed or uncertain, reconcile before any new attempt, and never replay the original Dispatch. Do not rewrite host ledger or reset WIP based on assumed facts.

## Completion / stop
One failure classification, verified preserved evidence and bounded recovery recommendation or STOP.

## Responsibility boundary
Own **diagnosis and safe recovery decision**, not owning Bridge executor implementation, automatic replay or reopening a closed milestone.

## Shared operating and Bridge applicability
FOX2 Agile Lite: one logical task, Build → Test → Deliver, CHAT owns outcome. Use only relevant methods and real evidence. Ordinary native DEV has no mandatory R0–R7/PreExec/Dispatch/extra approval; if the selected real route is Bridge or high-risk, its installed technical controls remain authoritative. No unrelated version churn, protected operations or consumed-attempt replay. This Skill does not authorize execution or grant external rights.
