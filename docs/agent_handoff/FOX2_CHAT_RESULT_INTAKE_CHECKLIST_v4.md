# FOX2 — CHAT Agent Result Intake & Review (Guide v4 / Contract v2)

**Authority:** FOX2 Policy V1.5 C6B–C6E. **This is an operational checklist, not a second Policy and not a merge/DEV grant.**

## Intake: minimum steps, strict ordering

1. **Locate remote immutable submission:** verify repo, correct WP, branch, submitted full commit SHA and PR/head ancestry. Only evaluate that commit, not an unpinned moving branch. If inaccessible → `REVIEW_BLOCKED_GIT_ACCESS`.
2. **Read required files:** `reports/<WP_ID>/report.md` and `evidence_manifest.json` *at the same commit*. Parse and validate schema v2 + consistency with report; otherwise `SUBMISSION_INCOMPLETE`/`CONTRACT_INVALID`.
3. **Validate policy/source/grants:** for implementation dispatch require Policy C1B.1 `GIT_SOURCE_READY=YES` with actual required-source remote/readback receipt; prompt correctness is not delivery evidence. A source-publisher/audit PARTIAL result may still be reviewed without making the dependent implementation ready. compare Library-published Policy version/SHA and released BRD/contract to receiver's source manifest and exact Git source commit. Check task, phase, code vs report push grants, model/host and one writer lease. Source mismatch → `SOURCE_STALE/DIVERGED`.
4. **Independently diff paths:** compare approved base to submitted remote commit; reconcile **all** ADD/MODIFY/DELETE paths with allowlist and report. Detect unauthorized runtime/code, protected mirrors, main push, force push, unrelated WIP and unexpected data.
5. **Validate each material claim:** acceptance + tests + evidence IDs resolve to files at the submitted immutable commit. Compute raw SHA-256 and compare; inspect command, environment, actual time and positive/negative coverage. If PASS unproven → `REWORK`; never convert NOT_RUN to PASS.
6. **Check security and domain risks:** redact secrets, no private-account data, no licensed raw DNSE data; validate provenance, completeness, residual risks and any conditional rights/retention. A domain simulation is not operational enforcement.
7. **Issue independent CHAT decision:** `ACCEPTED`, `ACCEPTED_PARTIAL`, `REWORK`, `BLOCKED`. Record reviewer, UTC time, source remote SHA, reviewed acceptance IDs, decisive evidence IDs, outstanding risks and **next actor/gate** separately (e.g., `reports/<WP_ID>/chat_review_receipt.json` on an authorized reviewer branch or PR review). Agent's own status cannot close WP.

## Decision rules

- `ACCEPTED`: all *in-scope* required acceptance evidence verified and no unresolved blocking risk; not a permission to merge, deploy or LIVE.
- `ACCEPTED_PARTIAL`: separately identify accepted sub-results, with full WP remaining OPEN; never treat a partial source mirror as complete sync.
- `REWORK`: credible, repairable discrepancy: missing tests, missing evidence, inconsistent report/JSON or quality issue.
- `BLOCKED`: authority/identity/source conflict, unauthorized diff, secret/license breach, unsafe claim, unverifiable remote Git or conditions preventing safe review.
- `SUBMITTED` / `PUSHED_UNREVIEWED`: delivery only; cannot be counted as an accepted material WP or promote a BRD.

## Non-circular proof rule

The manifest committed within Git cannot embed its own containing Git commit hash. Use an **external immutable remote pointer** from GitHub after push; CHAT independently reads it. Never flag a correctly designed manifest as invalid merely because `remote_commit_sha` is absent from the manifest itself.

## Example negative validations (run as local schema/logic checks if requested)

- Reject self-issued ACCEPTED or direct main push under report-only rights.
- Reject PASS with absent test run/evidence ID, stale source or unlicensed/raw data.
- Reject missing/mismatched evidence hashes and empty or invalid Git result paths.
- Reject report/manifest disagreement and unrelated changed files.
- Reject a local commit labeled as successfully pushed or self-accepted.

**Efficiency:** read the report + manifest first; fetch only evidence linked to material claims, negative controls and risks. Reuse still-valid hashes and prior tests on exactly the same source; do not require unnecessary transcript dumps.

## Mandatory CHAT pre-dispatch responsibility (Policy C1B.1)

CHAT owns upload and recovery. Complete and verify every required released source at a full remote commit BEFORE assigning/issuing an implementation task or prompt. If GIT_SOURCE_READY=NO, keep the implementation task internally SOURCE_PENDING; do not hand it to an Agent to discover or repair missing documents. CHAT records the blocker and precise recovery action, repairs permitted deltas and rechecks remote raw bytes/version/hash. Agent source checking is supplementary; WORK audit is only when assigned. Safety refusal means STOP, no bypass. YES grants source readiness only, never DEV/merge/Production. Result Contract/schema v2 remain unchanged.
