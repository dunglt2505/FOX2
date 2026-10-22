# FOX2 Skills v0.5.2 — formalize Master Plan → Agile Board promotion

Behavioral update to `fox2-mgmt-delivery` only.

## Added

A formal `READY_FOR_BOARD` contract for evaluating whether a Master Plan/Roadmap feature should remain strategic, enter Agile BACKLOG, move to DOING, or be marked BLOCKED.

Readiness requires all five:

- `OUTCOME_DEFINED`
- `DEPENDENCIES_KNOWN`
- `SOURCE_READY_ENOUGH`
- `ACCEPTANCE_ACTIONABLE`
- `NEXT_SAFE_ACTION_KNOWN`

The management decision is exactly one of:

- `KEEP_IN_MASTER_PLAN`
- `PROMOTE_TO_BACKLOG`
- `PROMOTE_TO_DOING`
- `BLOCKED`

WIP capacity decides BACKLOG versus DOING; WIP is not a readiness criterion. BLOCKED requires a real prerequisite preventing the next safe action. Promotion preserves the same Feature/Whole-WP identity and does not create new authority, Agent routing, release rights or a duplicate task.

## Preserved

- one logical Agile Kanban;
- WIP guidance ≤2 material writers;
- ordinary native DEV simplicity;
- Bridge installed machine contract/no-replay;
- CHAT result acceptance;
- no main/merge/provider/broker/LIVE authority by implication.

## Regression

Added `tests/test_board_promotion_v052.py` to lock the five checks, four decisions, WIP/readiness distinction, real-blocker semantics and same-logical-task rule.

Release metadata remains source/guidance only. Host behavioral certification is NOT_RUN; plugin installation/runtime enforcement is not claimed by this source package.
