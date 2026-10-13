# FOX2 M1-P2-03 — Codex Bridge execution

Execute the already-authorized whole work package `FOX2-M1-P2-03`.

Before editing, read these two local immutable task documents completely:

1. `docs/agent_handoff/M1/P2-03/FOX2_M1_P2_03_DSM_SOURCE_DESIGN_LOCK_20261014.md`
2. `docs/agent_handoff/M1/P2-03/FOX2_M1_P2_03_CODEX_EXECUTE_20261014.md`

The current worktree/branch/base are authoritative. Do not rewrite governance or task documents.

Implement and test the complete bounded P2-03 DSM offline source-selection WP exactly within the allowed paths.

Important execution rules:

- Edit only `backend/src/fox2/dsm/**`, `tests/p2_03/**`, and `reports/FOX2-M1-P2-03/**`.
- Preserve all P2-01 and P2-02 files unchanged.
- No provider/API/frontend/Bridge changes.
- No package installation.
- No provider network, broker, account, secret, Production or LIVE action.
- Do not run `git add`, `git commit`, `git push`, merge or PR. FOX2 Bridge owns Git commit/push after you finish.
- Run the required offline P2-03 suite and relevant upstream regression subsets.
- Produce `reports/FOX2-M1-P2-03/report.md` and `reports/FOX2-M1-P2-03/evidence_manifest.json` plus sanitized hashed evidence under `reports/FOX2-M1-P2-03/evidence/**`.
- Distinguish offline subcase PASS from canonical/provider/API/UI obligations that remain PARTIAL/NOT_RUN.
- If a frozen interface or out-of-scope change is required, stop without modifying forbidden paths and clearly report the blocker.

When implementation, tests, result evidence, scope checks, secret scan and no-network proof are complete, end your final response with exactly:

`FOX2_M1_P2_03_DELIVERY_READY`
