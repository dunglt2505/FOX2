# FOX2 — POLICY V1.8.5 | SIMPLIFIED PARALLEL ROUTING

**Document ID:** `FOX2-POLICY-V1`  
**Version:** `1.8.5`  
**Status:** `RELEASED_EFFECTIVE`  
**Project:** `FOX2 ONLY`  
**Date:** 2026-10-13  
**Released predecessor:** `FOX2_POLICY_V1.8.4.md` (`RELEASED_EFFECTIVE` historical predecessor)  
**Purpose:** remove routing friction that serializes independent FOX2 work, simplify the Local Agent Bridge governance boundary, and preserve safe parallel execution without weakening source, scope, Git, merge, Production or LIVE controls.

> **Owner release decision 2026-10-13:** “Tốt, triển khai đi” after approving the simplified Bridge and parallel-routing plan. This release supersedes V1.8.4 for new/re-scoped FOX2 work. Existing accepted immutable work keeps its historical binding unless a material impact requires transition.

## 1. Simplified operating model

```text
Owner
  -> CHAT decides/decomposes/binds scope
  -> up to two independent implementation lanes
       -> Copilot
       -> Codex
  -> optional Local Bridge transport for an already-approved lane
  -> Agent implements/tests in isolated worktree/branch
  -> Agent delivers authorized non-main result
  -> CHAT independently reads back and reviews immutable remote result
```

The Local Agent Bridge is a **command transport/launcher**, not a second governance engine, project manager, semantic reviewer or acceptance authority.

## 2. Project Parallel Lane Control

FOX2 may keep up to:

```text
MAX_PARALLEL_MATERIAL_WRITERS = 2
```

when all of the following are true:

- WPs are dependency-safe for concurrent work;
- shared interfaces required by both lanes are frozen enough for the planned scope;
- branches/worktrees are distinct;
- writable file paths do not overlap;
- each lane has one accountable writer and its own tests/evidence.

A blocked lane does **not** block an unrelated safe lane. Priority order is not blanket serialization.

When one lane completes or becomes materially blocked, CHAT should either route the next eligible independent WP or record `NO_ELIGIBLE_PARALLEL_WP` with the actual material reason.

## 3. Batch Owner authorization for exact WPs

The Owner may approve multiple exact WPs/lanes in one decision.

A batch decision is valid only when each WP has its own immutable task identity and bounded scope, including Agent/execution path, branch/worktree, allowed code paths, allowed report paths, relevant Git permissions and STOP conditions.

Once such a batch decision is recorded, CHAT and Bridge MUST NOT request the same Owner confirmation again for unchanged internal sub-steps of that WP.

A new Owner decision is needed only when a material execution input changes, including scope expansion, different Agent/path, branch/worktree ownership change, new sensitive permission, merge/deploy/Production/LIVE, or another genuine authority change.

## 4. Materiality of UNKNOWN / NOT_EXPOSED

`UNKNOWN` and `NOT_EXPOSED` block only when material to the operation being performed.

Examples:

- Polling or validating Git dispatch does not require Agent model/Optimize/quota visibility -> record `NOT_APPLICABLE`, continue.
- Launching an exact Owner-selected Agent/model that cannot be resolved -> block that launch.
- Numeric quota percentage is not exposed but the selected Agent can actually execute -> do not block solely because the percentage is unavailable.
- Required host/Git/write access cannot be verified -> block the affected write/launch.

Any generic `quota_unknown` STOP condition is subordinate to this materiality rule.

## 5. In-flight source transition

A newer released Policy/Technical source appearing after a WP started does **not** automatically invalidate that in-flight WP.

```text
NEW_RELEASE
  -> MATERIAL_TO_THIS_WP ?
       NO  -> keep frozen binding and continue
       YES -> preserve WIP/evidence and rebind only affected assumptions
```

New or re-scoped WPs use the newest applicable released source. Historical accepted results remain immutable evidence.

## 6. Deterministic implementation and result paths

Every executable coding handoff must bind implementation paths and result paths separately:

```yaml
allowed_code_paths: [...]
allowed_report_paths:
  - reports/<WP_ID>/report.md
  - reports/<WP_ID>/evidence_manifest.json
  - reports/<WP_ID>/evidence/**
```

`allowed_report_paths` does not expand `allowed_code_paths`.

This rule removes the known failure mode where implementation is authorized but canonical Result Contract delivery is blocked by an incomplete allowlist.

## 7. One whole-WP assignment; internal checkpoints are not new assignments

Do not turn every engineering checkpoint into a new Owner-facing assignment.

If one Agent owns one bounded WP, its internal implementation/test checkpoints run continuously until a genuine STOP condition or final delivery state.

Split/reconfirm only at a real ownership, dependency, authority, safety or review boundary.

## 8. Simplified Bridge governance boundary

For Policy purposes Bridge has only five responsibilities:

1. receive an immutable dispatch already authorized by CHAT/Owner;
2. verify transport identity and minimum runtime facts needed for safe launch;
3. invoke the exact selected local Agent without silent substitution;
4. supervise the local process and return observable execution state;
5. preserve single-use/replay protection.

Bridge MUST NOT redo `POLICY_CHECK`, `TASK_STATE_CHECK`, `R0-R7` or `ASSIGNMENT_CHECK`; reinterpret requirements; create authority; decide semantic acceptance; auto-rework; auto-merge/deploy; or grant provider/broker/LIVE rights.

## 9. VS Code / Agent-session integration boundary

Copilot CLI may integrate with a VS Code workspace, share editor/workspace context and surface a session, but this does **not** prove that every external SDK/CLI-created session is the same session as the already-open VS Code Agent session.

Before Bridge relies on direct VS Code session injection, the integration capability must be demonstrated by a small technical pilot.

Until a stable supported API is proven, a one-click VS Code handoff is an acceptable temporary transport for an otherwise approved WP. It is a `BOOTSTRAP/FALLBACK` interaction method only; it does not change governance, scope, Agent authority or result-review semantics.

## 10. Minimum executable handoff

```yaml
wp_id: <exact>
source_lock: <immutable refs>
agent: <COPILOT|CODEX>
execution_path: <BRIDGE|VSCODE_ONE_CLICK|MANUAL_LOCAL>
worktree: <exact>
branch: <exact non-main>
base_sha: <full SHA>
allowed_code_paths: [...]
allowed_report_paths: [...]
permissions:
  code_allowed: YES|NO
  git_code_push: YES|NO
  git_report_write: YES|NO
  git_report_push: YES|NO
  merge_allowed: NO
  production_provider: NO
  broker_write: NO
  live: NO
required_tests: [...]
stop_if:
  - material_source_drift
  - writer_collision
  - scope_violation
  - required_test_failure
  - secret_exposure
  - denied_required_access
```

Do not add non-material STOP conditions merely because a UI/tool field is not exposed.

## 11. Routing Index transition

The effective derivative routing index must:

- remove unconditional `quota_unknown` blocking;
- replace “newer release => STOP old handoff” with impact-based transition for in-flight WPs;
- recognize batch Owner authorization for exact parallel WPs;
- carry separate `allowed_code_paths` and `allowed_report_paths`;
- treat internal sub-checkpoints as one WP unless a genuine boundary requires a split;
- explicitly classify non-material Agent/model/quota fields as `NOT_APPLICABLE` for transport-only work;
- preserve CHAT-FIRST, immutable source binding, writer isolation and sensitive-permission gates.

## 12. Non-effects

This release grants no unapproved DEV, out-of-scope Git write, main push, merge, deployment, Production/provider/broker write, LIVE, auto-rework or auto-merge.

BRD/Data Contract/Acceptance semantics are unchanged.

## 13. Release acceptance checklist

This release adopts the following acceptance expectations:

- two independent WPs can run in parallel;
- one blocked lane does not freeze the other;
- Bridge does not repeat CHAT governance;
- non-material model/Optimize/quota gaps do not block unrelated transport work;
- in-flight frozen WPs survive unrelated later releases;
- code and report destinations are authorized before execution;
- one whole-WP assignment can cross internal checkpoints without repeated Owner confirmation;
- VS Code direct-session injection is treated as unverified until a supported API is demonstrated;
- one-click VS Code handoff can be used as temporary transport without changing authority;
- no new merge/Production/LIVE right is created.
