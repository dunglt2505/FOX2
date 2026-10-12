# FOX2 — P1 (existing work) RESULT RECOVERY · Current Git-first Task V1.7.1

**Record status:** `CURRENT_V1_7_1_TRANSITION / REPORT_AUTHORIZED_HOST_VERIFICATION_PENDING / NO_NEW_P1_EXECUTION`  
**WP_ID:** `FOX2-WP-M1-0-DNSE-HOST-EVIDENCE-READONLY`  
**TASK_ID:** `FOX2-M1-P1-RESULT-RECOVERY-20261012`  
**Tracking Issue:** `https://github.com/dunglt2505/FOX2/issues/5`  
**Owner decision:** FOX2 Owner explicitly asked CHAT to implement C6F/C6F.0 and obtain Copilot's existing P1 results; this is a report/intake operation only, no DEV/merge grant.

## Authority and Policy Binding — STOP if mismatch

- Policy family: `FOX2-POLICY-V1`; **Policy:** `FOX2_POLICY_V1.7.1.md`, version **`1.7.1`**, status `RELEASED_EFFECTIVE` after Library publication/readback receipt.
- **Policy raw SHA-256:** `9c8784781d13e05a59749e33a72b2912ed29a9398aadcc2034fc7b60e044c99d`.
- **Policy Git commit SHA:** `ef3975952006868ef2fd4e64619ebdbf3cfc8411`.
- Policy path: `docs/governance/FOX2_POLICY_V1.7.1.md`.
- Release manifest: `docs/governance/FOX2_POLICY_V1.7.1_RELEASE_MANIFEST_20261012.json`.
- Result Contract v2 remains unchanged: `docs/agent_handoff/FOX2_AGENT_RESULT_SCHEMA_v2.json`.
- **Protocol v7:** `docs/agent_handoff/FOX2_GIT_FIRST_TASK_RESULT_PROTOCOL_v7.md`; intake v7.
- **M1 authoritative source/sync receipt:** `955e74ff67e6b4ed184dc2c2dcd4260c51dc529b`; 8/8 official released M1 source files and 2/2 companions were exact remote readback at this commit; source index later evolved on authorized CHAT branch.
- Task/source manifest actual containing Git SHA is provided by **CHAT's external immutable task pointer after commit**; this file cannot reference its own commit SHA.
- Historical V1.2 P1 `task.md` and `source_manifest.json` on older commits are **superseded as current routing** only by this observed V1.7.1 transition; never backdate or erase their Git provenance.

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
- `GIT_REPORT_WRITE`: `AUTHORIZED_BY_STANDING_C6F_2A`; **actual host rights, safe worktree and branch writer ownership remain UNVERIFIED**.
- `GIT_REPORT_PUSH`: `AUTHORIZED_BY_STANDING_C6F_2A`; actual host push credentials, exclusive writer and remote readback remain **UNVERIFIED**.
- `PR_CREATE`: `NOT_GRANTED` for this task.
- `CODE_ALLOWED=NO`, `GIT_CODE_PUSH=NO`, `MAIN_PUSH=NO`, `MERGE_ALLOWED=NO`, `DNSE_PRODUCTION=NO`, `BROKER_WRITE=NO`, `LIVE=NO`.
- `REPORT_DELIVERY_PATH_READY=UNKNOWN/NO` until CHAT verifies actual Copilot host+writer+Git rights, even though standing internal report-only authorization is approved; merely having a branch or report path does not make this YES. Therefore this is a **status-only recovery/capability request until gates pass**, not an executable Git-push command.

## Precheck and mandatory final receipt

Follow `POLICY_CHECK → TASK_STATE_CHECK → R0...R7 → ASSIGNMENT_CHECK`; verify V1.7.1 Policy and source bytes from pinned Git. Before reporting `PUSHED_UNREVIEWED`, BOTH required files must have been pushed to authorized branch and observed on a single full remote commit. If actual Git write/push access or exclusive writer remains unverified, stop before Git modification and send `PUSH_BLOCKED` / `LOCAL_ONLY` receipt with exactly what was done earlier and what access/approval is needed; do **not** call the task delivered. CHAT will own a permitted report publication and independent review.

Return `FOX2_AGENT_DELIVERY_RECEIPT` with WP/Task ID, actual product/model/mode/host/quota or `NOT_EXPOSED`, Policy version/SHA/full commit, task commit, source commit, DONE/PARTIAL/NOT_RUN, report and manifest absolute local or repo-relative paths, branch, observed remote SHA or NONE, PR URL or NONE, Git error/grant state, evidence count and next action. **No self-acceptance.**

**STOP:** Policy mismatch, source drift, writer/WIP collision, missing actual host/writer capability, unsafe provider/private data, or branch/main/merge permission issues. No DEV as part of P1 recovery.


## V1.7.1 standing authorization / supersession note

- V1.7.1 corrects one invalid V1.7.0 byte; existing C6F.2A standing Copilot **internal report-only authorization** applies to this registered WP and future FOX2 WPs **without another per-WP permission grant**.
- Verify actual Copilot account credentials, one writer, expected Git ref and diff allowlist before any write or push; GitHub directory ACL enforcement is **NOT_VERIFIED**.
- Protocol/Intake Guide v7 controls this transition; Result Contract JSON schema v2 is unchanged.
- The V1.6 task and P1-specific grant remain historical only. A dedicated CHAT-observed immutable Git SHA containing this V1.7.1 task is provided **outside this file** after publication (no self-reference).
- No DEV, PR_CREATE, MAIN_PUSH, MERGE, DNSE_PRODUCTION, BROKER_WRITE or LIVE. Do not rerun P1; recover prior conversation results with explicit missing evidence.
