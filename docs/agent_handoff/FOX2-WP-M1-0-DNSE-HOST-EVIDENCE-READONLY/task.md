# FOX2 — P1 (existing work) RESULT RECOVERY · Current Git-first Task V1.6

**Record status:** `CURRENT_V1_6_TRANSITION / RESULT_DELIVERY_SETUP_PENDING / NO_NEW_P1_EXECUTION`  
**WP_ID:** `FOX2-WP-M1-0-DNSE-HOST-EVIDENCE-READONLY`  
**TASK_ID:** `FOX2-M1-P1-RESULT-RECOVERY-20261012`  
**Tracking Issue:** `https://github.com/dunglt2505/FOX2/issues/5`  
**Owner decision:** FOX2 Owner explicitly asked CHAT to implement C6F/C6F.0 and obtain Copilot's existing P1 results; this is a report/intake operation only, no DEV/merge grant.

## Authority and Policy Binding — STOP if mismatch

- Policy family: `FOX2-POLICY-V1`; **Policy:** `FOX2_POLICY_V1.6.md`, version **`1.6.0`**, status `RELEASED_EFFECTIVE` after Library publication/readback receipt.
- **Policy raw SHA-256:** `8cf205ab2b3c8d0d5be9edaa81c0a3bcfb73644caaf2eaa25fd52a6491a62081`.
- **Policy Git commit SHA:** `66b94ae274292a6f3046cf934f050b1ce15a1dbc`.
- Policy path: `docs/governance/FOX2_POLICY_V1.6.md`.
- Release manifest: `docs/governance/FOX2_POLICY_V1.6_RELEASE_MANIFEST_20261012.json`.
- Result Contract v2 remains unchanged: `docs/agent_handoff/FOX2_AGENT_RESULT_SCHEMA_v2.json`.
- **Protocol v5:** `docs/agent_handoff/FOX2_GIT_FIRST_TASK_RESULT_PROTOCOL_v5.md`; intake v5.
- **M1 authoritative source/sync receipt:** `955e74ff67e6b4ed184dc2c2dcd4260c51dc529b`; 8/8 official released M1 source files and 2/2 companions were exact remote readback at this commit; source index later evolved on authorized CHAT branch.
- Task/source manifest actual containing Git SHA is provided by **CHAT's external immutable task pointer after commit**; this file cannot reference its own commit SHA.
- Historical V1.2 P1 `task.md` and `source_manifest.json` on older commits are **superseded as current routing** only by this observed V1.6 transition; never backdate or erase their Git provenance.

## Scope — recover only work already performed

COPILOT is reported by Owner to have finished P1 on Windows. Do not repeat tests, install packages, checkout/reset/rebase/clean WIP, edit source, connect to DNSE Production, copy Fox old project, or start P2/P3. Inspect existing Copilot chat/local report files and known command outputs **read-only**, using actual Windows host if available, and honestly distinguish DONE/PARTIAL/NOT_RUN/UNKNOWN. If original evidence was not saved, note `NOT_RETAINED`; do **not** reconstruct fabricated PASS logs.

Check or report: Windows host identity (non-sensitive), local `C:\Projects\FOX2` origin/HEAD/branch/worktrees/tracked/untracked/ignored WIP without content disclosure, local/source Policy mismatch, Python/Node/Git environment, legacy `C:\Projects\Fox` reuse inventory (metadata only), model/mode/quota observation, DNSE provider rights/retention status and risk/next step. Source binding is proof for docs **only**, not DEV/host/rights readiness.

## CHAT-owned deterministic destination (Result Contract v2)

- Repository: `dunglt2505/FOX2`
- Tracking Issue: `#5`
- Designated Agent result branch: `work/FOX2-WP-M1-0-DNSE-HOST-EVIDENCE-READONLY-copilot` (exclusive one-writer target; existence/lease must be observed before any write).
- Report path: `reports/FOX2-WP-M1-0-DNSE-HOST-EVIDENCE-READONLY/report.md`
- Machine manifest path: `reports/FOX2-WP-M1-0-DNSE-HOST-EVIDENCE-READONLY/evidence_manifest.json`
- Evidence folder: `reports/FOX2-WP-M1-0-DNSE-HOST-EVIDENCE-READONLY/evidence/` (sanitized minimum only).
- Required schema: `docs/agent_handoff/FOX2_AGENT_RESULT_SCHEMA_v2.json`.
- Agent final receipt in response is mandatory and must include full **observed** remote commit/PR pointer if truly pushed. Do not embed own commit SHA in in-commit files.

## Permission matrix (separate, no implicit grants)

- `GIT_SOURCE_READ`: verify on actual Copilot host.
- `GIT_REPORT_WRITE`: `NOT_YET_VERIFIED_FOR_COPILOT`; permissible only with an explicit WP-bound grant **and** observed host rights/branch writer ownership.
- `GIT_REPORT_PUSH`: `NOT_YET_VERIFIED_FOR_COPILOT`; permissible only with an explicit WP-bound grant **and** observed host Git permission, target/lease/remote readback.
- `PR_CREATE`: `NOT_YET_VERIFIED_FOR_COPILOT`.
- `CODE_ALLOWED=NO`, `GIT_CODE_PUSH=NO`, `MAIN_PUSH=NO`, `MERGE_ALLOWED=NO`, `DNSE_PRODUCTION=NO`, `BROKER_WRITE=NO`, `LIVE=NO`.
- `REPORT_DELIVERY_PATH_READY=UNKNOWN/NO` until CHAT confirms separate report grants and actual Copilot host+writer permission; merely having a branch or report path does not make this YES. Therefore this is a **status-only recovery/capability request until gates pass**, not an executable Git-push command.

## Precheck and mandatory final receipt

Follow `POLICY_CHECK → TASK_STATE_CHECK → R0...R7 → ASSIGNMENT_CHECK`; verify V1.6 Policy and source bytes from pinned Git. Before reporting `PUSHED_UNREVIEWED`, BOTH required files must have been pushed to authorized branch and observed on a single full remote commit. If no report write/push grant, stop before modifying Git and send `PUSH_BLOCKED` / `LOCAL_ONLY` receipt with exactly what was done earlier and what access/approval is needed; do **not** call the task delivered. CHAT will own a permitted report publication and independent review.

Return `FOX2_AGENT_DELIVERY_RECEIPT` with WP/Task ID, actual product/model/mode/host/quota or `NOT_EXPOSED`, Policy version/SHA/full commit, task commit, source commit, DONE/PARTIAL/NOT_RUN, report and manifest absolute local or repo-relative paths, branch, observed remote SHA or NONE, PR URL or NONE, Git error/grant state, evidence count and next action. **No self-acceptance.**

**STOP:** Policy mismatch, source drift, writer/WIP collision, missing report grant, unsafe provider/private data, or branch/main/merge permission issues. No DEV as part of P1 recovery.
