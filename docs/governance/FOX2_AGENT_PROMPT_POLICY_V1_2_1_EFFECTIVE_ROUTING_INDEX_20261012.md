# FOX2 — Agent Prompt Policy V1.2.1: Execution Routing Selector Index (NOT a separate policy)

**Owner decision:** 2026-10-12. **Authority:** `/Trading/FOX2/00_Governance/FOX2_POLICY_V1.8.1.md`, especially C1/C1.1/C2A/C5/C5A/C5B/C6/C6F. **Scope:** FOX2 ONLY. This note is a derivative quick-reference, not a standalone authority or DEV grant.

1. CHAT performs the executable-WP decision chain exactly once: `POLICY_CHECK → TASK_STATE_CHECK → R0–R7 → ASSIGNMENT_CHECK`, plus applicable `GIT_SOURCE_READY` and `EXECUTION_AUTHORIZED`.
2. When the exact prompt/WP is `PROMPT_READY_TO_DISPATCH`, CHAT shows **Screen 1 — Execution Path** with exactly: `MANUAL_VSCODE` and `CONFIGURE_AUTOMATED_AGENT`. Confirmed manual VS Code ends the CHAT routing workflow with no Bridge dispatch.
3. Only `CONFIGURE_AUTOMATED_AGENT` opens **Screen 2 — Agent / Model / Thinking**. CHAT shows one recommended configuration plus eligible alternatives, records actual exposed model/mode values, and requires explicit Owner confirmation. Do not invent Copilot Thinking values or silently substitute models.
4. After Screen 2 confirmation, CHAT shows **Screen 3 — Transport** with exactly: `DISPATCH_VIA_LOCAL_BRIDGE`, `BACK_TO_AGENT_CONFIGURATION`, `CANCEL_EXECUTION`. There is no `SAVE_PROMPT_ONLY` or `SAVE_CONFIGURATION_ONLY` option.
5. Preferred UI when exposed by the current ChatGPT client: single-select radio group + explicit confirmation CTA. A preselected option is recommendation only, never approval. Text/number fallback must preserve the same explicit-confirmation semantics.
6. On confirmed `DISPATCH_VIA_LOCAL_BRIDGE`, CHAT publishes one immutable schema-v1.1 dispatch artifact to `docs/agent_handoff/<WP_ID>/dispatch/<DISPATCH_ID>.json`, including the Owner-confirmed Agent/Model/Thinking configuration and selection receipt.
7. The Local Bridge performs `LOCAL_RUNTIME_ATTESTATION` only. It verifies exact source/dispatch identities, host/CLI/Git/worktree/writer facts, and exact requested Agent/model/mode availability. It must not repeat BRD/Policy/routing decisions or substitute configuration.
8. Each `DISPATCH_ID` is single-use (`max_runs=1`). Runtime mismatch is `LOCAL_RUNTIME_BLOCKED`; duplicate is `DISPATCH_DUPLICATE_IGNORED`; CHAT decides recovery/retry.
9. Result Contract v2 and independent CHAT review remain unchanged. Dispatch is transport + Owner intent, not result/acceptance/merge/release.
10. C6F.2A standing Copilot report authorization remains in force for qualifying report-only WPs; staged Local dispatch does not expand it to DEV.
