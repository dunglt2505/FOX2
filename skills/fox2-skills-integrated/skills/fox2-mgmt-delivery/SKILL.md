---
name: fox2-mgmt-delivery
description: "Plan, prioritize, promote, track, and report FOX2 delivery in one Agile Kanban; merges triage, roadmap and project health."
---

# fox2-mgmt-delivery

**FOX2 Layer 1 — Project management — Agile Lite 0.5.3**

## Activate when
Owner asks what to build next, current status, a blocker, project health, priority, or whether a Master Plan/Roadmap feature should enter the Agile Board; also when Watch/CHAT observes a verified delivery, acceptance or material project-state change.

## Input
Owner outcome, Master Plan/Roadmap feature candidates, live task status, actual Git/test/host evidence, dependencies, acceptance readiness and deadlines if supplied.

## Work to perform
1. Pick the highest-value safe outcome; prioritize user-visible product progress and real defects over administrative documents.
2. Keep ONE board `BACKLOG → DOING ↔ BLOCKED → DONE`, one logical task containing `ID · goal · scope · owner · acceptance · status · evidence/blocker`. No independent stage gate or project-level R0–R7 paperwork.
3. Evaluate Master Plan/Roadmap features with the **Board promotion contract** below. Promotion changes management visibility/status only; it does not create a duplicate feature, new authority, Agent route, or release right.
4. Preserve accepted, unaffected PASS. Mark a task DONE only when evidence meets its acceptance; `prompt published`, `Agent started` and Bridge `PUSHED_UNREVIEWED` are not DONE.
5. Report product capabilities, changed facts, true blockers, next owner action and cycle time where observed. Unknown or untested evidence stays UNKNOWN. WIP ideally ≤2 simultaneous material code writers with non-overlapping paths; treat this as operating guidance, not a blocking certificate.
6. For a necessary Agent choice request the routing method; for result quality request result acceptance. Avoid creating new micro-WPs because one attempt needs correction.

## Evidence-driven progress synchronization (CHAT / scheduled Watch)

**Activation:** On a scheduled FOX2 Project Progress Watch, verified Agent/Bridge Git delivery, CHAT acceptance/rework, material blocker/dependency change, or explicit Owner status request. Skills are instructions, **not** a self-running daemon: the Watch/CHAT must invoke this method, and only an authorized Git publisher can actually write files.

1. **Read current evidence:** Resolve the effective Master Plan plus operating addenda and single Project Kanban; compare actual Git refs/SHA, tests, CI, CHAT acceptance and previous synced state. Do not infer DONE from `PUSHED_UNREVIEWED`, unreviewed PRs, local logs or missing evidence.
2. **Update Board on material task events:** For an existing logical task, write verified status `BACKLOG/DOING/BLOCKED/DONE`, owner, precise result SHA, blocker, acceptance verdict and next safe action. Do not duplicate WPs or mirror all distant roadmap features.
3. **Update Master Plan only on strategic changes:** Milestone acceptance, dependency, scope, release sequencing or material roadmap changes. Preserve immutable historical plans; use the currently authorized live plan/addendum, never silently overwrite divergent Library copies.
4. **Publish safely:** Request `fox2-tech-publication-sync` for authorized Git changes; compare expected remote base, publish to scoped non-main branch/PR when protected main cannot be written, then read back exact files/SHA. No merge, governance promotion or LIVE permission is implied.
5. **Return truthful sync evidence:** `SYNCED` only after remote readback, `NO_MATERIAL_CHANGE` with no empty commit, or `SYNC_PENDING/BLOCKED` with exact missing permission/source/conflict. Report separate `BOARD_UPDATED` and `MASTER_PLAN_UPDATED` booleans; do not claim a document changed merely because a summary was produced.

**Idempotency:** Use the observed event/result SHA and existing document content to avoid repeated updates. If source/branch/ownership conflicts, preserve current files, provide a bounded proposed delta and stop before overwriting.

## Board promotion contract

Evaluate promotion when a current WIP slot frees, a dependency/source/acceptance fact changes, Owner asks what is next, or a roadmap feature enters the near delivery horizon.

Set `READY_FOR_BOARD=YES` only when all five checks are true:

- `OUTCOME_DEFINED`: the feature has an observable user/product outcome, not merely an activity or document.
- `DEPENDENCIES_KNOWN`: material upstream dependencies and their current states are known; they need not all be DONE to put the feature in BACKLOG.
- `SOURCE_READY_ENOUGH`: source/authority/contracts are sufficient for the **next safe action**. Do not require every future BRD/provider/runtime fact to be complete before backlog visibility.
- `ACCEPTANCE_ACTIONABLE`: there is a measurable acceptance condition for the next meaningful increment.
- `NEXT_SAFE_ACTION_KNOWN`: CHAT can name a concrete next action that is permitted now or immediately after a known dependency.

Return exactly one promotion decision:

- `KEEP_IN_MASTER_PLAN`: one or more readiness checks are false, or the feature is too far outside the actionable horizon. This is **not BLOCKED**.
- `PROMOTE_TO_BACKLOG`: `READY_FOR_BOARD=YES`, but the feature is not selected for active execution because of priority, dependency timing or WIP capacity.
- `PROMOTE_TO_DOING`: `READY_FOR_BOARD=YES`, the feature is the selected highest-value safe outcome, its immediate dependency is available, and a WIP slot exists or Owner explicitly reprioritizes.
- `BLOCKED`: the feature is board-worthy and would otherwise proceed, but a concrete prerequisite prevents the next safe action. Name the exact unblocker; never use BLOCKED for distant backlog work.

WIP capacity decides `BACKLOG` versus `DOING`; it does **not** decide `READY_FOR_BOARD`.

Do not mirror the entire Master Plan onto the Board. Keep only the actionable/near-horizon portfolio plus active work. Preserve the same Feature/Whole-WP identity when promoted or reprioritized; normal correction remains the SAME logical task.

For every promotion assessment record the five checks, the decision, evidence for any false/blocked condition, and `NEXT_SAFE_ACTION`.

## Output
One prioritized task or concise project delivery view, including `READY_FOR_BOARD` and one promotion decision when roadmap promotion is in scope; next safe action and evidence-based DONE/DOING/BLOCKED.

## Responsibility boundary
Owns outcome priority, Master Plan→Board promotion, one Kanban and reporting. Does NOT choose Model/Thinking, write prompts, perform tests, publish governance, execute Bridge, or certify releases.

## Common rules
One logical Kanban task; only material checks for selected action. Ordinary native DEV has no mandatory Bridge/PreExec/R0–R7 paperwork. For actual Bridge execution the installed Bridge enforces its own machine protocol and no-replay; never fabricate PASS, permissions or host actions. CHAT owns result acceptance; no broker/LIVE, protected branch or irreversible side effects without real authority.
