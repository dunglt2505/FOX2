# COPILOT — EXECUTE FOX2 P1 RESULT DELIVERY RECOVERY (Policy V1.6, C6F)

**Purpose:** fix GitHub Issue #5 by recovering P1 findings **already performed** from this Copilot conversation, producing machine/human deliverables, and submitting through Git **only after verified report-only host access**. Do **not** repeat P1 or implement P2. Owner explicitly requested resolution; CHAT has already corrected the active Issue body and published a narrow report-only grant supplement. This task is not a request to re-design Policy.

## Frozen authorities and pointers

- Repository `dunglt2505/FOX2`; Issue `https://github.com/dunglt2505/FOX2/issues/5`.
- Policy: `FOX2-POLICY-V1` V1.6.0, raw SHA-256 `8cf205ab2b3c8d0d5be9edaa81c0a3bcfb73644caaf2eaa25fd52a6491a62081`, `docs/governance/FOX2_POLICY_V1.6.md` + V1.6 release manifest, Git policy commit `66b94ae274292a6f3046cf934f050b1ce15a1dbc`.
- P1 task + source manifest: `docs/agent_handoff/FOX2-WP-M1-0-DNSE-HOST-EVIDENCE-READONLY/{task.md,source_manifest.json}` at `4df6088c4ba29fbbcc991ea0f9f96cd22fefd6d7`.
- Owner-scoped REPORT-ONLY grant supplement: `docs/agent_handoff/FOX2-WP-M1-0-DNSE-HOST-EVIDENCE-READONLY/delivery_grant.md` at remote commit `802064a2a7831ebe5ef37f4713b7c95226b78880` (this file is **authority within scope**, not proof of actual Windows Git credentials/writer status).
- M1 v0.4 official source snapshot: `955e74ff67e6b4ed184dc2c2dcd4260c51dc529b`.
- Contract: `docs/agent_handoff/FOX2_AGENT_RESULT_SCHEMA_v2.json`; reporting protocol v5 and CHAT intake v5 at the Git supplement commit.
- WP: `FOX2-WP-M1-0-DNSE-HOST-EVIDENCE-READONLY`; Task: `FOX2-M1-P1-RESULT-RECOVERY-20261012`.

## Mandatory R0–R7 precheck and safety

1. Confirm the **existing P1 task is reported DONE but the result is still DELIVERY_PENDING**, so reuse prior conversation. Do not run Windows P1 again, repeat provider checks, or fabricate lost logs.
2. Verify Policy/version/raw SHA/release receipt/task/source/grant exactly at immutable remote commits. If mismatch, return `BLOCKED_POLICY_MISMATCH` and STOP affected execution.
3. Confirm actual GitHub Copilot product, model/mode/quota if exposed; otherwise report `NOT_EXPOSED`. Ensure actual `FoxLe-PC` and repository access. Inspect `C:\Projects\FOX2` WIP/worktrees/branch/HEAD without changing them; reported local main `6662d5b61770291db4e493c0852fbc2f3b923a7b` is old. Never silently pull/rebase/stash/reset/clean checkout, alter `C:\Projects\Fox` or overwrite user files.
4. CHAT recorded Owner's **scoped `GIT_REPORT_WRITE` and `GIT_REPORT_PUSH` authorization** to this WP on the exact report branch; **verify actual Windows Git identity/host credential and exclusive writer/worktree safety before using it**. `PR_CREATE=NO`, so leave `PR_URL=NONE`. If auth/lease are not verified, STOP push, report exact failure; no blanket DEV inferred.
5. Compare CHAT, COPILOT, CODEX, WORK at routing: CHAT already owns Policy/Issue and independent review; COPILOT is the appropriate reporter because it alone has prior P1 conversation; CODEX/WORK not needed for this report-only recovery. Model/effort is the cheapest currently supported sufficient option, report actual settings if visible.

## Exact deliverables — never invent paths

Result branch already initialized by CHAT:
`work/FOX2-WP-M1-0-DNSE-HOST-EVIDENCE-READONLY-copilot`

Only allowed Git modifications:
- `reports/FOX2-WP-M1-0-DNSE-HOST-EVIDENCE-READONLY/report.md`
- `reports/FOX2-WP-M1-0-DNSE-HOST-EVIDENCE-READONLY/evidence_manifest.json`
- `reports/FOX2-WP-M1-0-DNSE-HOST-EVIDENCE-READONLY/evidence/**` for existing sanitized evidence only.

Use **Report Template v4** R01–R12 and **schema-v2** to create a **truthful, limited recovery**. Do not alter Task, Policy, source mirrors, or runtime. Do not create fake evidence merely to make the folder non-empty.

Recover findings from actual prior Copilot messages if still accessible, with precise file paths and commands only if these are recorded in the old conversation. The Owner-forwarded receipt presently supports these as **self-reported, unverified**:
- Windows host `FoxLe-PC`, Git 2.56.0, Python 3.13.15; Node/npm absent on PATH.
- Local FOX2 reported clean on old `main` SHA `6662d5b61770291db4e493c0852fbc2f3b923a7b`; one worktree, no merge/rebase. Must not rewrite WIP or infer current state from earlier report.
- Legacy `C:\Projects\Fox` read-only technical patterns: GET-only public data transport, synthetic fixtures, UNKNOWN/hash controls, Vietnamese timezone and backend-mediated UI; JSON cache needs redesign; no WebSocket seen in inspected portion.
- DNSE *historical metadata only*: 7 symbols × 40 bars, UTC 2026-08-10 to 2026-10-07, refresh 2026-10-08; stale and **not live**. Data rights, freshness, corporate actions, price units and completeness unknown.
- M1 acceptance 105 tests and DNSE Production REST/WS tests `NOT_RUN`; Git host/source write rights and Copilot model/mode/quota unverified in prior run.

For everything without preserved proof, write `SELF_REPORTED / NOT_RETAINED / NOT_VERIFIED`; if the schema acceptance status cannot express NOT_VERIFIED, use `BLOCKED` with explicit missing-evidence reason rather than false PASS. Mark `NOT_RUN` only when the step truly was not run. Set `evidence: []` if no proof files actually exist. Schema `submission_state=PARTIAL` is expected if evidence is missing; even a successful push is **not** P1 acceptance.

## Publication decision, privilege and proof

- Confirm dedicated branch has the expected starting ref (grant supplement commit) and there is no parallel writer; work in an isolated safe workspace if needed, without changing the existing FOX2 checkout/WIP. **Do not force-push**.
- If actual scoped Git report-write/push permissions and exclusive writer are **PASS**, write the above two files only, validate JSON/schema v2 with an available validator (if unavailable mark schema validation NOT_RUN, not PASS), inspect staged diff for report-only paths/secret-free content, commit and push on the designated result branch only.
- After push, independently resolve full remote result commit and read both required files at that immutable SHA; verify hash/path and report the result SHA. Git manifest must not embed its containing commit SHA.
- If issue-comment capability is observed, comment on Issue #5: WP, Policy V1.6 binding, status, result branch, full remote result SHA, report+manifest paths, evidence limitations, next CHAT reviewer. **Do not close Issue #5 or self-accept**.
- If push is unavailable: return `PUSH_BLOCKED/LOCAL_ONLY` and exact failure/permission barrier; provide complete sanitized draft report/manifest text in the conversation (not secrets) as recovery material for an authorized independent CHAT publisher. Do not call a local file a remote Git delivery.

## Final mandatory external receipt

```text
FOX2_AGENT_DELIVERY_RECEIPT
WP_ID: FOX2-WP-M1-0-DNSE-HOST-EVIDENCE-READONLY
TASK_ID: FOX2-M1-P1-RESULT-RECOVERY-20261012
ACTUAL_AGENT: GitHub Copilot / VS Code
ACTUAL_MODEL: <observed or NOT_EXPOSED>
ACTUAL_MODE: <observed or NOT_EXPOSED>
HOST: <observed host>
QUOTA_OBSERVATION: <observed or NOT_EXPOSED>
POLICY_VERSION: 1.6.0
POLICY_SHA256: 8cf205ab2b3c8d0d5be9edaa81c0a3bcfb73644caaf2eaa25fd52a6491a62081
POLICY_GIT_COMMIT: 66b94ae274292a6f3046cf934f050b1ce15a1dbc
TASK_GIT_COMMIT: 4df6088c4ba29fbbcc991ea0f9f96cd22fefd6d7
REPORT_GRANT_GIT_COMMIT: 802064a2a7831ebe5ef37f4713b7c95226b78880
SOURCE_GIT_COMMIT: 955e74ff67e6b4ed184dc2c2dcd4260c51dc529b
EXECUTION_STATUS: <self-reported truthful status>
DELIVERY_STATUS: <PUSHED_UNREVIEWED | PUSH_BLOCKED | LOCAL_ONLY | SUBMISSION_INCOMPLETE>
REPOSITORY: dunglt2505/FOX2
RESULT_BRANCH: work/FOX2-WP-M1-0-DNSE-HOST-EVIDENCE-READONLY-copilot
REMOTE_COMMIT_SHA: <full 40-char RESULT SHA or NONE>
PR_URL: NONE
REPORT_PATH: reports/FOX2-WP-M1-0-DNSE-HOST-EVIDENCE-READONLY/report.md
MANIFEST_PATH: reports/FOX2-WP-M1-0-DNSE-HOST-EVIDENCE-READONLY/evidence_manifest.json
EVIDENCE_COUNT: <actual>
REMOTE_READBACK_STATUS: <actual>
GIT_REPORT_WRITE_GRANT: <owner-scope authorized; actual capability PASS/UNKNOWN/BLOCKED>
GIT_REPORT_PUSH_GRANT: <owner-scope authorized; actual capability PASS/UNKNOWN/BLOCKED>
WRITER_OWNERSHIP: <actual verified status>
CODE_ALLOWED: NO
P1_DONE: <reported summary>
P1_PARTIAL: <reported summary>
P1_NOT_RUN: <reported summary>
OPEN_BLOCKERS: <specific>
NEXT_ACTOR: CHAT
NEXT_REQUIRED_ACTION: Independent delivery verification and acceptance
END_FOX2_AGENT_DELIVERY_RECEIPT
```

**STOP / never claim:** `RESULT_DELIVERY_VERIFIED=YES` or `P1_ACCEPTED` — only CHAT can attest after independently fetching and reviewing immutable Git output. `CODE_ALLOWED=NO`, `GIT_CODE_PUSH=NO`, `MAIN_PUSH=NO`, `MERGE_ALLOWED=NO`, `PR_CREATE=NO`, `DNSE_PRODUCTION=NO`, `BROKER_WRITE=NO`, `LIVE=NO`.
