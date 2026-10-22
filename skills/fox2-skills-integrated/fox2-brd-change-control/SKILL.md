---
name: fox2-brd-change-control
description: Control substantive business-requirement changes and affected acceptance behavior.
---

# fox2-brd-change-control

## Activate when
FOX2 business rules, product behaviors, users, thresholds or acceptance criteria change.

## Work to perform
Identify old/new user-observable behavior, business rationale, actor, thresholds, timing, failure cases and test impact. Trace to changed TechSpec/API, relevant downstream consumers and migration needs. Example: changing retention 30→90 days must update affected API/tests, not merely a sentence. Ignore purely editorial or unrelated Policy/version edits. Preserve prior approved business intent and avoid task-per-consumer micro-WPs.

## Completion / stop
One scoped BRD/acceptance change recommendation with impacted tests and owners.

## Responsibility boundary
Own **business semantic change**, not code architecture approval, source publication or feature certification.

## Shared operating and Bridge applicability
FOX2 Agile Lite: one logical task, Build → Test → Deliver, CHAT owns outcome. Use only relevant methods and real evidence. Ordinary native DEV has no mandatory R0–R7/PreExec/Dispatch/extra approval; if the selected real route is Bridge or high-risk, its installed technical controls remain authoritative. No unrelated version churn, protected operations or consumed-attempt replay. This Skill does not authorize execution or grant external rights.
