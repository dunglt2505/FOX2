# FOX2 Git-first handoff entry point

Library owns issued Policy/BRDs. SOURCE_INDEX.json is a derived exact-byte index, not a new release authority. Use Policy V1.4 and Result Contract v2 for new WPs;Protocol/Template/Intake guides v3 supersede v2 guidance. One GIT_SOURCE_READY decision before implementation: NO→SOURCE_PENDING,YES only with all WP-required remote/readback hashes. Publisher/recovery may continue in verified scope. Old v1 reports and prepared M1-0 task remain historical; do not dispatch them as current grants.

1. CHAT supplies released source identity/hash and scoped task/grants. WORK validates Library; Copilot/Codex validate pinned Git/local copies, not Library access.
2. Source publisher syncs verified delta on a sole-writer non-main branch; readback determines SYNC_VERIFIED. Missing/stale/blocked sources cannot support DEV handoff.
3. Task input: <WP_ID>/task.md and source_manifest.json at an immutable commit. Result: reports/<WP_ID>/report.md + evidence_manifest.json matching schema v2, with each material PASS linked to raw-hash evidence.
4. After push supply full remote SHA externally. CHAT independently validates report/schema/diff/evidence at that SHA, then writes a separate review receipt on an authorized reviewer branch. No Agent self-acceptance.

Current handoff baseline remains PARTIAL: released M1v0.4 bytes have been verified in Library but required Git mirrors are missing. Backend/frontend/tests contain only .gitkeep; service deployment and trading DEV are not ready. SOURCE_INDEX records per-file source state. No main push/merge/provider/LIVE in publisher grants.

See SYNC_DELTA_WORKFLOW.md and the current WP task. Read branch at a pinned commit; branch labels are not evidence of deployability.
