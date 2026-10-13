# FOX2 — M1-P2-01 CONDITIONAL DEV AUTHORIZATION RECORD
Date: 2026-10-13
Status: OWNER_SCOPE_APPROVED / CONDITIONAL_NOT_ACTIVE
WP: FOX2-M1-P2-01

## Owner decision
The Owner approved the V1.8.4 re-baselined execution plan and directed CHAT to implement it quickly. This record converts that approved P2-01 scope into an exact task-bound conditional grant; it does not broaden the approved plan.

## Activation conditions — ALL required
1. Exact task source readback PASS:
   `588da7b1c1a642ddfd935ff6372af83a35acaa2f:docs/agent_handoff/M1/P2-01/FOX2_M1_P2_01_PREDEV_REBIND_V184_20261013.md`.
2. Policy V1.8.4 and Routing Index V1.2.4 readback PASS.
3. Remote branch exists:
   `work/FOX2-M1-P2-01-foundation-codex`.
4. A dedicated clean local worktree is attached to that exact branch/base.
5. No writer collision/WIP is observed on that worktree.
6. Minimum P2-01 local toolchain is available without unsafe network/package changes.
7. Actual Agent session is usable; model/mode/quota may remain NOT_EXPOSED if no material runtime unavailability is observed.
8. CHAT records `ASSIGNMENT_CHECK=PASS` for the same source/scope after receiving the local setup evidence.

Until all conditions pass:
`CODE_ALLOWED=NO`, `GIT_CODE_PUSH=NO`.

## Activated permissions
When and only when all activation conditions pass:
- `CODE_ALLOWED=YES_FOR_FOX2_M1_P2_01_ONLY`
- `GIT_CODE_PUSH=YES_OWN_TASK_BRANCH_ONLY`
- `GIT_REPORT_WRITE/PUSH=YES_TASK_BOUND_SANITIZED_EVIDENCE_ONLY`

Allowed implementation paths:
- `backend/**`
- `tests/p2_01/**`

If implementation requires any root packaging/config file, another test namespace, docs, migrations/store/DSM/API/UI/provider code or any path outside the allowlist, STOP and return to CHAT for scope review.

## Denied
- `agent_bridge/**`
- `source_freshness/**`
- `frontend/**`
- `docs/**`
- `.github/**`
- root `tests/**` outside `tests/p2_01/**`
- root packaging/config unless separately granted
- P2-02 store/migrations
- P2-03 DSM implementation
- P2-04 API integration
- DNSE/provider network
- broker/account/order operations
- main push/merge/rebase/reset/force-push
- Production/LIVE

## Result boundary
Agent may end at `PUSHED_UNREVIEWED` only.
CHAT independently reads the remote result, tests/evidence and exact SHA before any ACCEPTED disposition.

## STOP
Stop on source drift, branch/base mismatch, dirty/colliding worktree, secret exposure, unexpected network use, path expansion, missing dependencies requiring unapproved installation, push failure or any safety/platform refusal.

This conditional authorization does not authorize merge, deployment, provider production, broker write or LIVE.
