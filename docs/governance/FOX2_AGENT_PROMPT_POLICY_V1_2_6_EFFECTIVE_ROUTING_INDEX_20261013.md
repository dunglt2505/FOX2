# FOX2 — Agent Prompt Policy V1.2.6 — Simplified Parallel Routing Index

**Document ID:** `FOX2-AGENT-PROMPT-ROUTING-INDEX`  
**Revision:** `V1.2.6`  
**Date:** 2026-10-13  
**Status:** `EFFECTIVE_DERIVATIVE_ROUTING_INDEX / NOT_SEPARATE_POLICY / NO_DEV_GRANT`  
**Supersedes for NEW/re-scoped prompts:** `V1.2.5`  
**Normative Policy:** `FOX2_POLICY_V1.8.5.md`  
**Bridge Technical:** `FOX2_LOCAL_AGENT_BRIDGE_TECHNICAL_SPEC_v0.6.md`  
**Scope:** FOX2 only.

## 1. Routing rule

CHAT performs the decision/routing work once, binds an exact WP, and delegates only the genuine local/coding delta. Bridge is optional transport for an already-approved WP.

```text
Owner -> CHAT -> up to two independent coding lanes -> CHAT review
                  |                         |
                  +-> Copilot              +-> Codex
                       ^                         ^
                       +------ Bridge -----------+
                         transport/launch only
```

## 2. Parallel-lane control

`MAX_PARALLEL_MATERIAL_WRITERS = 2`. Use parallel lanes only when dependencies/interfaces are safe enough, branches/worktrees are distinct, writable paths do not overlap and each lane has one accountable writer. A blocked lane does not block an unrelated safe lane.

## 3. Batch Owner authorization

One Owner decision may authorize multiple exact WPs. Do not ask again for unchanged internal sub-steps. Reconfirm only for material scope/Agent/path/permission/merge/Production/LIVE changes.

## 4. Materiality of UNKNOWN / NOT_EXPOSED

Unknown or unexposed values block only if material to the requested operation.

- Git polling/transport: model/Optimize/quota -> `NOT_APPLICABLE`.
- Exact model required for launch but unavailable -> block that launch.
- Numeric quota percentage unavailable but Agent can run -> do not block solely on missing percentage.
- Required host/Git/write access unavailable -> block affected operation.

Any older unconditional `quota_unknown` STOP is superseded by this materiality rule.

## 5. Source transition

For an in-flight WP, a newer release triggers impact evaluation, not automatic invalidation. Preserve frozen binding and WIP if the new release is not material. Rebind only affected assumptions if material. New/re-scoped WPs use current released sources.

## 6. Required executable handoff fields

```yaml
wp_id: <exact>
source_lock: <immutable refs>
agent: COPILOT|CODEX
execution_path: BRIDGE|VSCODE_ONE_CLICK|MANUAL_LOCAL
worktree: <exact>
branch: <exact non-main>
base_sha: <full SHA>
allowed_code_paths: [...]
allowed_report_paths:
  - reports/<WP_ID>/report.md
  - reports/<WP_ID>/evidence_manifest.json
  - reports/<WP_ID>/evidence/**
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
stop_if: [material_source_drift, writer_collision, scope_violation, required_test_failure, secret_exposure, denied_required_access]
```

## 7. Bridge-specific routing

Bridge does only receive/verify-minimum-runtime/relay/supervise/replay-protect. It MUST NOT rerun `POLICY_CHECK`, `TASK_STATE_CHECK`, `R0-R7` or `ASSIGNMENT_CHECK`.

For VS Code integration, direct existing-session injection remains `UNVERIFIED` until demonstrated. Preferred order: supported direct API -> workspace-bound CLI session -> one-click VS Code handoff. One-click handoff is acceptable for bootstrap.

## 8. Whole-WP execution

Do not create a new Owner-facing assignment for every internal engineering checkpoint. One bounded WP continues until genuine STOP or final delivery. Legacy BRG labels may remain internal evidence only.

## 9. Non-effects

This index creates no DEV grant, no out-of-scope Git write, no main push, merge, deployment, Production/provider/broker write, LIVE, auto-rework or auto-merge.
