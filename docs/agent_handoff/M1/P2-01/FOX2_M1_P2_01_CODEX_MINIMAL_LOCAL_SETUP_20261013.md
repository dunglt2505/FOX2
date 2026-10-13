# FOX2 — M1-P2-01 CODEX MINIMAL LOCAL SETUP PRECHECK
Date: 2026-10-13
Mode: LOCAL_ONLY_DELEGATED / PRE-DEV / NO CODE
Policy: FOX2 V1.8.4
Routing Index: V1.2.4

## Immutable task source
Read:
- `588da7b1c1a642ddfd935ff6372af83a35acaa2f:docs/agent_handoff/M1/P2-01/FOX2_M1_P2_01_PREDEV_REBIND_V184_20261013.md`
- Policy `a366f509899cec97f64316cb111b29a3849325b5:docs/governance/FOX2_POLICY_V1.8.4.md`
- Routing Index `43c3d240615bce7279f2665fa1c1c0afb7f49021:docs/governance/FOX2_AGENT_PROMPT_POLICY_V1_2_4_EFFECTIVE_ROUTING_INDEX_20261013.md`

Remote task branch already created by CHAT:
`work/FOX2-M1-P2-01-foundation-codex`
Initial branch base:
`588da7b1c1a642ddfd935ff6372af83a35acaa2f`

## Architecture-stage disposition
`PASS_TARGET`.
P2-01 does not wait for BRG-003, SFR-010 or Bridge Gate A.
This prompt does NOT grant code editing.

## Task
1. Verify repository `dunglt2505/FOX2`, origin and the exact remote task branch.
2. Check registered worktrees and collision/WIP state.
3. Preferred local path, only if unused and safe:
   `C:\Projects\FOX2-worktrees\FOX2-M1-P2-01-CODEX`
4. If the preferred path does not exist, no other Agent owns it, and the remote task branch exists, you MAY create a local worktree attached to that exact branch. This is setup only.
5. Do not reset/rebase/stash/clean any existing worktree.
6. Verify the new/existing P2-01 worktree is clean and at the expected branch/base.
7. Observe only the P2-01-relevant local toolchain already installed:
   - Python executable/version;
   - pip;
   - pytest availability;
   - FastAPI/Pydantic availability if already installed.
   Do NOT install packages or use network.
8. Observe actual Codex product/model/thinking/quota only where exposed. Use NOT_EXPOSED/UNKNOWN honestly.
9. Confirm no active writer/collision for this exact worktree/branch.
10. Do NOT edit `backend/**`, `tests/**` or any source file.
11. Do NOT commit/push, create another branch, touch main, or run provider/network code.

## Return exactly
FOX2 M1-P2-01 MINIMAL_LOCAL_SETUP

TASK_SOURCE_READBACK:
POLICY_READBACK:
ROUTING_INDEX_READBACK:

ACTUAL_CODEX_MODEL:
ACTUAL_THINKING:
QUOTA_STATUS:

REPO:
ORIGIN:
REMOTE_TASK_BRANCH:
WORKTREE:
WORKTREE_CREATED_THIS_RUN:
LOCAL_BRANCH:
HEAD:
CLEAN_STATUS:
WRITER_COLLISION:

PYTHON:
PIP:
PYTEST:
FASTAPI:
PYDANTIC:

LOCAL_SETUP_VERDICT:
  PASS_READY_FOR_CHAT_DEV_DECISION
  | BLOCKED_SOURCE
  | BLOCKED_BRANCH
  | BLOCKED_WORKTREE
  | BLOCKED_COLLISION
  | BLOCKED_TOOLCHAIN
  | UNKNOWN

CHANGES_MADE:
  worktree_setup_only | NONE
CODE_WRITTEN: NONE
TESTS_RUN: NONE
COMMIT: NONE
PUSH: NONE

OPEN_GATES:
STOP_REASON:

STOP.
