---
name: fox2-mgmt-delivery
description: "Plan, prioritize, track, and report FOX2 delivery in one Agile Kanban; merges triage, roadmap and project health."
---

# fox2-mgmt-delivery

**FOX2 Layer 1 — Project management — Agile Lite 0.5.0**

## Activate when
Owner asks what to build next, current status, a blocker, project health or priority.

## Input
Owner outcome, live task status, actual Git/test/host evidence, dependencies and deadlines if supplied.

## Work to perform
1. Pick the highest-value safe outcome; prioritize user-visible product progress and real defects over administrative documents.
2. Keep ONE board `BACKLOG → DOING ↔ BLOCKED → DONE`, one logical task containing `ID · goal · scope · owner · acceptance · status · evidence/blocker`. No independent stage gate or project-level R0–R7 paperwork.
3. Preserve accepted, unaffected PASS. Mark a task DONE only when evidence meets its acceptance; `prompt published`, `Agent started` and Bridge `PUSHED_UNREVIEWED` are not DONE.
4. Report product capabilities, changed facts, true blockers, next owner action and cycle time where observed. Unknown or untested evidence stays UNKNOWN. WIP ideally ≤2 simultaneous material code writers with non-overlapping paths; treat this as operating guidance, not a blocking certificate.
5. For a necessary Agent choice request the routing method; for result quality request result acceptance. Avoid creating new micro-WPs because one attempt needs correction.

## Output
One prioritized task or concise project delivery view; next safe action and evidence-based DONE/DOING/BLOCKED.

## Responsibility boundary
Owns outcome priority, one Kanban and reporting. Does NOT choose Model/Thinking, write prompts, perform tests, publish governance, execute Bridge, or certify releases.

## Common rules
One logical Kanban task; only material checks for selected action. Ordinary native DEV has no mandatory Bridge/PreExec/R0–R7 paperwork. For actual Bridge execution the installed Bridge enforces its own machine protocol and no-replay; never fabricate PASS, permissions or host actions. CHAT owns result acceptance; no broker/LIVE, protected branch or irreversible side effects without real authority. 
