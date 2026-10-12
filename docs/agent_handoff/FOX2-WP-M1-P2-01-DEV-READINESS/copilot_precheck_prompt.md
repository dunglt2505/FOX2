# FOX2 P2-01 DEV Readiness Precheck — Copilot

Read `docs/agent_handoff/FOX2-WP-M1-P2-01-DEV-READINESS/task.md` and `source_manifest.json` from the exact task publication commit supplied by CHAT. Recompute the Policy V1.8 raw SHA-256 and verify all pinned source identities before doing anything else.

Execute **only** the READ-ONLY readiness checks in `task.md` on FoxLe-PC. Do not implement P2-01, do not install packages, do not change application files, do not call DNSE/provider/broker endpoints. Preserve all WIP.

Use the designated result branch and write only `reports/FOX2-WP-M1-P2-01-DEV-READINESS/**` after confirming actual Git identity, branch, writer safety and an exact report-only staged diff. Validate `evidence_manifest.json` against Result Contract v2. Push the report result only if the report path/branch access is actually available; otherwise return `PUSH_BLOCKED` and preserve local output without claiming delivery.

Return a final receipt containing the full remote result commit SHA if pushed and the separate readiness verdicts required by task.md. CHAT will independently review and decide whether P2-01 may receive a DEV grant.
