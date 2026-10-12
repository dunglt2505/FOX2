# FOX2 — Agent Prompt Policy V1.2: Effective Routing & Local Dispatch Index (NOT a separate policy)

**Owner decision:** 2026-10-12. **Authority:** `/Trading/FOX2/00_Governance/FOX2_POLICY_V1.8.md`, especially C1/C1.1/C5/C5A/C5B/C6/C6F. **Scope:** FOX2 ONLY. This note is a derivative quick-reference, not a standalone authority or DEV grant.

1. CHAT performs the executable-WP decision chain exactly once: `POLICY_CHECK → TASK_STATE_CHECK → R0–R7 → ASSIGNMENT_CHECK`, plus applicable `GIT_SOURCE_READY` and `EXECUTION_AUTHORIZED`.
2. When the exact prompt/WP is `PROMPT_READY_TO_DISPATCH`, CHAT exposes Owner actions **`EXECUTE_LOCAL_AGENT`** and **`SAVE_PROMPT_ONLY`**. Do not ask the Owner to restate the prompt, repo, Agent or unchanged grants.
3. On `EXECUTE_LOCAL_AGENT`, CHAT publishes one immutable schema-v1 dispatch artifact to `docs/agent_handoff/<WP_ID>/dispatch/<DISPATCH_ID>.json` on the designated non-main Git branch. No selection = no executable dispatch.
4. The Local Bridge performs `LOCAL_RUNTIME_ATTESTATION` only. It verifies exact dispatch/task/policy/prompt identities and current host/CLI/Git/branch/base/WIP/writer facts; it must not repeat BRD/Policy/routing decisions, reroute the task or self-grant rights.
5. Each `DISPATCH_ID` is single-use (`max_runs=1`). Re-observation is `DISPATCH_DUPLICATE_IGNORED`. Runtime mismatch is `LOCAL_RUNTIME_BLOCKED`; CHAT decides recovery/retry.
6. Result Contract v2 and independent CHAT review remain unchanged. Dispatch is transport + Owner intent, not result/acceptance/merge/release.
7. C6F.2A standing Copilot report authorization remains in force for qualifying report-only WPs; Local dispatch does not expand it to DEV.
8. Visual one-click UI is used only when technically exposed by the current ChatGPT client/integration. Otherwise the exact action-text selection has the same Policy semantics and CHAT performs the Git dispatch operation.