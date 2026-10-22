# FOX2 Bridge E2E technical contract — Skill support v0.4.1

REFERENCE FOR BRIDGE/GIT EXECUTION OWNERS ONLY, NOT A PROMPT BUILDER CHECKLIST. This file documents the existing Bridge RC1 R5 machine interface; it does not make new Policy, Schema, preflight, or runtime. Applicable ONLY when `execution_path=BRIDGE`, not native reversible DEV. Inspect actual installed Bridge version and adapt to its observed contract before assignment. If older or different, STOP the affected handoff and inspect its matching contract.

## 1. Input decision and route
- Owner outcome, existing logical task/WP, authorized scope, actual actor, measurable acceptance and STOP.
- Route Runtime selects CODEX or COPILOT plus policy/model/reasoning/permissions based on real host capability, quota and complexity **before** PreExec. For Bridge the tuple must match `agent_policy.validate_selection` and actual CLI help/version. Never choose High just by feature name. Do not silently switch a pinned actor/model.
- `CODEX` allows `PINNED`, `CURRENT_CONFIG`, `PINNED_PREFERRED`, `reasoning_effort` only when supported (`low|medium|high` in inspected R5). `COPILOT` allows its supported native/pinned policies; don't give CODEX effort to Copilot. Current Bridge `FULL_ACCESS` permission profile is a machine contract, not authority to access live assets. Actual allowed paths and protected operation denials still apply.

## 2. Immutable task and prompt publication
- Confirm chosen machine Dictionary `SOURCE_COMMIT` and current schema/Policy version in the **installed** normalizer, not the largest Git Policy filename. Human Policy v2.1 does NOT mean an old Bridge dispatch may use v2.1. Preserve old locks.
- In the authorized non-main Git branch write `docs/agent_handoff/<WP>/task.md` plus exact `prompt.md` in `docs/agent_handoff/<WP>/` (or compatible authorized path). The task declares scope, route, tests, allowed code/report paths and STOP; prompt includes bounded coding instructions and the selected delivery owner. Do not put secrets in public Git.
- Fetch/read back committed task and prompt by their exact commit. Compute and verify SHA-256 bytes, Git blob SHA-1 and immutable commit. Reusing a printed prompt without bytes/commit is DRAFT. Remote branch/worktree must be clean/owned before execution; no blind reset.
- Report files, when actually required by the task/result contract, include `reports/<WP>/report.md` and `reports/<WP>/evidence_manifest.json` inside allowlisted paths. Code-only acceptance and runtime report are not interchangeable. The observed pushed result SHA is reported outside its own committed report to avoid self-reference.

## 3. Generate Dispatch v3 by a real validator, never by guessing PASS
The inspected Bridge R5 `FOX2_LOCAL_AGENT_DISPATCH_SCHEMA_v3.json` requires:
`schema_version=3.0`, `project=FOX2`, `dispatch_id`, `dispatch_action=EXECUTE_LOCAL_AGENT`, `wp_id`, `target_agent`, `workspace_id`, `dictionary`, `policy`, `task`, `prompt`, `source`, `routing`, `execution_path=BRIDGE`, `delivery_owner`, `permissions`, `decision_receipt`, `runtime_contract`, `required_tests`, `created_by=CHAT`, `created_at` (ISO date-time), `max_runs=1`.
- `dictionary`: version, git_path, git_commit_sha, sha256 — exact installed `project_dictionary.py` identity.
- `policy`: version, sha256, git_path, git_commit_sha — exact **machine** `CURRENT['policy']` identity, not latest management Policy by filename.
- `task`: path, commit_sha, sha256. `prompt`: path, git_commit, git_blob_sha1, sha256. `source`: commit_sha, `git_source_ready=YES` only if actually verified.
- `routing`: model_policy, permission_profile and compatible model/effort/tier for the selected Agent. `runtime_contract`: repo, branch, worktree, base_sha, allowed_code_paths, allowed_report_paths, required_capabilities, stop_conditions. 
- `permissions`: code_allowed, git_code_push, git_report_write, git_report_push and protected fields (`pr_create=false`, `merge_allowed=false`, `production_provider=false`, `broker_write=false`, `live=false`). Do not conflate `delivery_owner=BRIDGE` with authorization for Agent to commit/push.
- `decision_receipt`: policy_check, task_state_check, source_binding_check, routing_r0_r7, assignment_check must be observed PASS; material_capability_check must be observed PASS/PASS_NON_MATERIAL_DEVIATION; execution_authorized and code_allowed must truly be YES; dev_grant_ref must come from actual authority. Never auto-fill these on a generated draft.
- Use current Bridge schema validation and `dispatch_normalizer.normalize_dispatch` checks, then publish a **new unused** Dispatch ID under configured pattern on configured control branch. Git readback and observed compatible branch/path are required before claiming DISPATCH_ADMITTED. Do not publish an executable Bridge Dispatch with unobserved material PreExec; no automatic regeneration of consumed Dispatch.

## 4. Bridge execution and result handback
- Bridge poller observes configured control branch/candidate path and ledger atomically claims a dispatch **once**. PreExec/host fencing and real actual code/run permissions apply for this Bridge route. Observe installed host state; don't infer status from Git alone.
- Bridge retrieves prompt by exact commit, blob and SHA-256. Mismatch stops. Bridge selects CODEX or COPILOT CLI without silent substitution. Actual observed CLI model/effort must satisfy route. Protect one writer, allowed code/report paths and clean worktree.
- `delivery_owner=AGENT`: the Agent is instructed to commit/push exact authorized branch and Bridge verifies observed remote SHA. `delivery_owner=BRIDGE`: Agent leaves Git history unchanged, Bridge verifies changes and commits/pushes them. Never ask Agent and Bridge to publish concurrently.
- Only genuine result evidence can advance to `PUSHED_UNREVIEWED` (not CHAT DONE). CHAT independently reads pushed commit, diff, reports and tests, compares task acceptance, and records `DONE`, `REWORK`, or `BLOCKED` on same logical task.
- Failed, timeout or uncertain post-start state goes to `NEEDS_RECONCILIATION`; reconcile ledger, ACK, side effects and remote Git before any follow-up. A consumed Dispatch is NEVER replayed. A bounded safe correction may be a NEW immutable attempt within the SAME logical task, after checking authority and actual previous status.

## 5. Owner-operated Windows PowerShell (only if actually requested)
- The actual verified host-launch executor supplies **full, copy-ready `pwsh` 7+ script inline** in CHAT, with first executable guard rejecting `$PSVersionTable.PSVersion.Major -lt 7` and STOP on missing installed commands or unknown flags.
- The script must confirm correct task branch, source identity, clean worktree, single writer, actual PreExec/Bridge receipt and no-replay; use real observed CLI syntax and STOP before any unsafe mutation. Do not invent `work.exe`, use `powershell.exe` 5.1 or create generic local host commands without verifying capability.
- `OWNER_LAUNCH_READY` is only a verified handoff; it is NOT Agent executed, result pushed or CHAT accepted.
