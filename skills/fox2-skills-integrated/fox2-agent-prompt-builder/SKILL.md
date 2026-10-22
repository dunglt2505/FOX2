---
name: fox2-agent-prompt-builder
description: Build execution-ready bounded Agent prompts, with full Bridge Git/Dispatch/result handoff only when that route is selected.
---

# fox2-agent-prompt-builder

## Activate when
CHAT must delegate genuinely residual implementation, independent audit, or a selected Bridge-controlled execution to an Agent.

## Work to perform
### First determine which output is needed
1. CHAT direct: do the work without generating an executable Agent prompt. Native independent CODEX/Copilot: create one short authorized goal/scope/tests/result/STOP prompt with actor and proportional model/thinking. No separate Git-prompt/Dispatch/PreExec ceremony.
2. Selected `execution_path=BRIDGE`: produce the full **Bridge handoff package** below. Do not use native prompt completeness as Bridge readiness. Keep the selected Route Runtime actor/model/thinking and actual host capabilities unchanged. `ROUTE_RATIONALE` belongs in the existing task only when material, not a separate approval document.

### Bridge handoff package — one logical task, exact machine schema
A. **Route and source** — task/WP ID, Owner scope, actor CODEX/COPILOT, pinned or validated current-config model, reasoning effort if actually supported, permissions, required tests and limits. Read trusted Governance Policy v2.1.0 for human management. Independently read Bridge installed `project_dictionary.py`, `dispatch_schema_v3_contract.py`, `dispatch_normalizer.py` and actual host PreExec profile. Never send Policy 2.1.0 as Bridge `policy` if this machine normalizer requires its pinned historical Policy 1.8.9. Do not increase Dictionary/BRD/TechSpec version just for aesthetics.
B. **Task and prompt** — write one existing-WP `docs/agent_handoff/<WP>/task.md` and immutable UTF-8 `prompt.md` at allowed path on non-main Git; define measurable output, exact allowed code/report paths, branch, writer, tests, scope STOP and `delivery_owner`. Preserve existing approved PASS when unchanged. For `delivery_owner=AGENT`, Agent must commit/push only exact branch; for `BRIDGE`, Agent must not commit/push because Bridge owns publication.
C. **Source readback** — verify remote source commit, task path+SHA-256 and prompt path+Git commit/blob SHA-1/SHA-256 from actual Git bytes. Record control branch and machine Dictionary lock separately. Missing bytes/permissions/branch => `HANDOFF_SOURCE_HOLD`, not synthetic PASS.
D. **PreExec evidence** — request real Bridge host route-selected material checks, writer/worktree, permissions, CLI capability/versions, no-replay. No PreExec receipt is a prompt-generation achievement. If status is NOT_RUN/BLOCKED/UNKNOWN, stop publishing executable Dispatch, continue permitted preparatory work only.
E. **Dispatch generation** — use installed Schema v3 + normalizer; populate required `dictionary`, `policy`, `task`, `prompt`, `source`, `routing`, `runtime_contract`, `permissions`, `decision_receipt`, `required_tests`, `delivery_owner`, metadata, `max_runs=1`. `decision_receipt` PASS fields come only from real checks, `dev_grant_ref` only from actual authority; protected flags false. Validate against installed schema. Publish a NEW unused dispatch ID to the installed configured Git control branch/path, read back bytes and observed SHA. Never reuse or reissue consumed ID.
F. **Owner/manual launch** — when actual local Owner-operated Windows CLI invocation is necessary, verify installed CLI version/arguments and render a fully copy-ready `pwsh` 7+ script **inline**, with version guard first and correct exact source, worktree, writer, no-replay, PreExec and STOP checks. No placeholders, no imaginary `work.exe` or guessed flags. If no verified host command, say `HOST_NOT_VERIFIED`, do not write speculative launcher.
G. **Result contract** — require appropriate code changes, focused tests and reports (`reports/<WP>/report.md`, `reports/<WP>/evidence_manifest.json` only when relevant contract requires); remote commit/branch readback and observed SHA. Result is `PUSHED_UNREVIEWED`, never DONE. CHAT subsequently uses Result Review and records DONE/REWORK/BLOCKED in same task.

### Bridge outcome classifications
`DRAFT` (planning) → `HANDOFF_SOURCE_VERIFIED` (bytes/authority, no agent started) → `DISPATCH_ADMITTED` (real compatible receipt + published unused Dispatch) → `AGENT_STARTED` (observed host/ledger only) → `PUSHED_UNREVIEWED` (remote result verified) → `CHAT_ACCEPTED`/`REWORK`/`BLOCKED` (actual CHAT decision). Emit only the highest state actually evidenced. Handing out a script or prompt alone is not completion.

**STOP triggers:** missing source digest/authority; wrong runtime Policy/Dictionary/Schema; model/CLI mismatch; no observed PreExec PASS; conflicting writers/WIP; unexpected control branch or schema; consumed Dispatch; insufficient allowed paths; protected main/deploy/LIVE permissions; attempted rerun after uncertain side effect. Always protect unrelated safe work.

## Completion / stop
Produce the concrete deliverable and actual proof with DONE/REWORK/BLOCKED or a precisely named lower execution state. Do not mark completed because a prompt, Dispatch, tool invocation or plan exists. CHAT owns the end-to-end result.

## Shared operating and Bridge applicability
Apply shared `../../shared/operating_rules.md`. A routine reversible independent native task needs no Bridge Dispatch, manual R0–R7 artifact or immutable prompt publication. When and only when the actual execution is Bridge-controlled, follow `../../shared/bridge_e2e_v041.md` and the **installed** runtime contract, not an assumed current version. All source/receipt/test evidence must be observed, not invented. Old consumed attempts remain immutable and non-replayable. Complete outcomes in the SAME logical task; do not create administrative micro-WPs.
