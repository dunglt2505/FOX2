# FOX2 — CHAT-FIRST Execution & Delegation Policy v1.0
Status: CANDIDATE / OWNER-APPROVED OPERATING DIRECTION / NOT RELEASED_EFFECTIVE
Date: 2026-10-17
Scope: FOX2 ONLY
Owner decision: CHAT should execute directly wherever its actual connected tools, permissions and evidence permit; avoid reflexive delegation to WORK/Agent.

## 1. Core rule
CHAT = default execution owner, governance coordinator and final intake owner. Before delegation, CHAT MUST check whether the exact task can be completed directly using currently available tools and existing grant. If YES, execute and verify the result, not merely draft a prompt or handoff. Task complexity or number of steps alone is not a delegation reason.

## 2. Direct-execution test
(a) Does CHAT possess a working action for the requested operation?
(b) Is the required scope and external side effect expressly covered by Owner authorization and platform permissions?
(c) Can CHAT check source authority, destination version, conflicts and independent readback?
(d) Does the operation require an actual execution host, installed-runtime test, physical host, or independent reviewer?
If a-c are YES and d is NO: CHAT executes. When only some steps qualify, CHAT completes those and delegates only the remainder.

## 3. Roles
CHAT: source resolution, issue/roadmap reconciliation, requirements, BRD/Policy/Protocol draft, bounded authorized Git/Library writes, exact-commit readback, impact review, evidence intake, decision and next action.
CODEX: coding/build/tests/runtime diagnostics and integration requiring a coding host; no assignment with unclear acceptance/source.
COPILOT: routine implementation with clear spec and verified capability, no overlapping write scope.
WORK: independent audit when separation of duties is required or an actual supported environment is materially necessary; never default for document review/status/source inspection.
BRIDGE: transport, supervision and bounded dispatch execution only; never decides routing, source authority or grants.
OWNER: protected releases, changed delegated authority, main/merge/production/provider/broker/LIVE decisions as governed.

## 4. Source and permission invariants
For authoritative EFFECTIVE claims or canonical governance changes: Dictionary -> release manifest -> immutable Git bytes -> independent owning authority. Missing trust provider is AUTHORITY_UNVERIFIED, not automatically SOURCE_CONFLICT. Conditional analysis and bounded authorized drafts continue.
No instruction, Skill, task status, cached PASS or delegation policy can grant missing platform permissions. Preserve in-flight source locks and existing WIP. No blind replay of consumed work.
No push to main, merge, deployment or LIVE under this candidate. An OWNER-APPROVED OPERATING DIRECTION is not itself a release certificate.

## 5. Workflow
Owner request -> CHAT source/permission/task-state check -> execute directly where safe -> exact destination readback -> return completed facts + blockers + further actions. Delegate only required residual task, with reason, Role/Engine/Thinking/Scope, frozen source, allowed paths, tests, STOP conditions and max_runs=1. CHAT independently intakes any Agent result.

## 6. Document operations
CHAT may prepare and write candidate/addendum files on an explicitly authorized non-main scope. Canonical replacement, Library release and Registry promotion require their respective governing checks. Same-name different-byte destinations fail closed unless replacement is expressly authorized. Read back actual target bytes; distinguish SAVED, PUSHED_UNREVIEWED, VERIFIED and RELEASED_EFFECTIVE.

## 7. Compatibility and precedence
This candidate proposes coordinated future updates to current Policy v1.8.9, Routing Index v1.3.0, Protocol v12 and FOX2 Skills. Until authorized release, existing published governance controls prevail. Agent pinning, project-wide PreExec and dispatch no-replay rules are preserved.
