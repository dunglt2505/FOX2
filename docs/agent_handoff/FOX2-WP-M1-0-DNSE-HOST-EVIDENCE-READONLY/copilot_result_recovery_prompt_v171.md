# FOX2 — Copilot P1: Recover Existing Results and Submit under Policy V1.7.1

**Role:** GitHub Copilot Pro / VS Code (FoxLe-PC); **Model / effort:** Auto/Efficiency if truly available, otherwise lowest adequate supported; record actual settings or NOT_EXPOSED. **Scope:** report-only, no P1 rerun or code.

## Pinned binding (must validate before action)
- Policy: `FOX2-POLICY-V1` version `1.7.1`, Library SHA256 `9c8784781d13e05a59749e33a72b2912ed29a9398aadcc2034fc7b60e044c99d`.
- Policy Git commit: `ef3975952006868ef2fd4e64619ebdbf3cfc8411`; `docs/governance/FOX2_POLICY_V1.7.1.md` and its release manifest. Protocol v7, Intake Guide v7; Contract JSON schema v2 unchanged.
- Official M1 source commit: `955e74ff67e6b4ed184dc2c2dcd4260c51dc529b`.
- P1 task/manifest: `docs/agent_handoff/FOX2-WP-M1-0-DNSE-HOST-EVIDENCE-READONLY/task.md`, `source_manifest.json`, **use the exact new CHAT-published task commit provided with the handoff**, not old V1.6 task or Git main.
- Tracking Issue: https://github.com/dunglt2505/FOX2/issues/5.

## Required operations
1. Perform POLICY_CHECK, TASK_STATE_CHECK and routing R0–R7. P1 execution is **OWNER/COPILOT_REPORTED_DONE**, delivery and independent verification remain **NO**; do not rerun Windows inspections or DNSE tests merely because original logs were not retained.
2. Confirm Policy/SHA/source and current Git branch, host/credential, untracked/ignored WIP, expected branch writer. The standing C6F.2A authority already grants **internal report-only write/push for eligible Copilot roles on registered FOX2 WP**; do **not** ask for another per-WP authorization. This does **not** establish actual technical push access or GitHub path ACLs. If technical checks fail/UNKNOWN, STOP Git write and report exact cause + sanitized draft.
3. Recover findings from your prior Copilot conversation only (no invented logs). Windows FoxLe-PC; Git 2.56.0, Python 3.13.15, Node/npm absent on PATH, local old main `6662d5b61770291db4e493c0852fbc2f3b923a7b`; legacy Fox GET/fixture/UNKNOWN/hash/VN timezone/backend patterns; historic 7-symbol x 40-bar DNSE cache metadata (last 2026-10-08); no observed WebSocket; data rights unknown; M1 105 acceptance and DNSE Production not run. These are self-reported, **NOT_VERIFIED** unless original admissible evidence exists.
4. Only submit paths on branch `work/FOX2-WP-M1-0-DNSE-HOST-EVIDENCE-READONLY-copilot`:
   - `reports/FOX2-WP-M1-0-DNSE-HOST-EVIDENCE-READONLY/report.md` (R01–R12 human report, DONE/PARTIAL/NOT_RUN/BLOCKED)
   - `reports/FOX2-WP-M1-0-DNSE-HOST-EVIDENCE-READONLY/evidence_manifest.json` (valid Result Contract v2; do not invent fields/statuses)
   - `reports/FOX2-WP-M1-0-DNSE-HOST-EVIDENCE-READONLY/evidence/**` only for actually retained, sanitized proof with hashes.
   Use `evidence: []` if none retained; a report's presence does NOT prove earlier checks PASSED. No runtime, Policy/task, BRD or unrelated edits. Preserve current local WIP; no reset/rebase/stash/pull overwrite/force push.
5. After actual host rights/writer checks PASS, write, schema-validate if validator available, inspect full diff, commit and push on designated non-main branch. Read back the report and manifest at **full immutable remote RESULT commit SHA**. If Issue comment access exists, post status/pointer on Issue #5; never self-close or self-accept.
6. Respond with `FOX2_AGENT_DELIVERY_RECEIPT` including WP/task, actual model/mode/host/quota, Policy V1.7.1 SHA/source/task binding, actual Git result branch/full pushed result SHA or NONE, report/manifest paths, evidence count, allowed status `PUSHED_UNREVIEWED` or `PUSH_BLOCKED/LOCAL_ONLY`, verification and next CHAT action. **Only CHAT** can set `RESULT_DELIVERY_VERIFIED=YES` and decide ACCEPTED/REWORK/BLOCKED.

**Forbidden:** CODE_ALLOWED, GIT_CODE_PUSH, MAIN_PUSH, MERGE_ALLOWED, PR_CREATE, DNSE_PRODUCTION, BROKER_WRITE and LIVE are all **NO** in this handoff.
