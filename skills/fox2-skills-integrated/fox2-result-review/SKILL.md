---
name: fox2-result-review
description: Assess returned Agent or task output against acceptance using observed code and test evidence.
---

# fox2-result-review

## Activate when
A real native DEV or Bridge Agent task returns output for CHAT evaluation.

## Work to perform
Compare the original task goal/acceptance with actual changed diff/files, commit/ref as applicable, test execution outputs, negative/security cases and remaining defects. For Bridge read the actual pushed result and verified transport state; `PUSHED_UNREVIEWED` is not CHAT acceptance. Check result and report artifacts only when the **selected task/result contract** required them. Make one conclusion: DONE/CHAT_ACCEPTED, REWORK or BLOCKED in the SAME logical task. A correction can be performed natively when safe; a consumed Bridge attempt cannot replay and any new run needs a genuinely new authorized attempt.

## Completion / stop
One acceptance verdict, concrete evidence and smallest next fix or closure, not a second approval committee.

## Responsibility boundary
Own **product/task acceptance**, not Bridge result publishing, runtime state management, new prompt creation or milestone certification.

## Shared operating and Bridge applicability
FOX2 Agile Lite: one logical task, Build → Test → Deliver, CHAT owns outcome. Use only relevant methods and real evidence. Ordinary native DEV has no mandatory R0–R7/PreExec/Dispatch/extra approval; if the selected real route is Bridge or high-risk, its installed technical controls remain authoritative. No unrelated version churn, protected operations or consumed-attempt replay. This Skill does not authorize execution or grant external rights.
