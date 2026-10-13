# TRADING / FOX2 — CHAT-FIRST publication and applicability register (2026-10-13)

**Status:** `PUBLICATION_INDEX / NOT_NEW_POLICY / NO_EXECUTION_GRANT`.
**Owner authorization:** “publish Policy, các tài liệu liên quan hết luôn đi” after the explicit CHAT-first routing direction. Scope is the governance and prompt allocation delta, not cross-project migration and not runtime Bridge/SFR implementation.

## Current documents and their roles

| Name | Effective document | Authority |
|---|---|---|
| **FOX2 Policy** | `FOX2_POLICY_V1.8.3.md` | Official FOX2 Library Governance, released Policy; supersedes V1.8.2 for new/current governance decisions. |
| **FOX2 Agent Routing Index** | `FOX2_AGENT_PROMPT_POLICY_V1_2_3_EFFECTIVE_ROUTING_INDEX_20261013.md` | Effective derivative / guide for new task handoffs; not separate Policy; supersedes v1.2.2 for new prompts. |
| **Trading shared Prompt Template** | `TRADING_AGENT_PROMPT_TEMPLATE_v1.8.md` | Current Owner-directed operational template, conditional on project-specific effective policy, no independent execution authority. |
| **Trading CHAT-first Owner Directive** | `TRADING_CHAT_FIRST_AGENT_ALLOCATION_OWNER_DIRECTIVE_20261013.md` | Attributable cross-project routing preference, no DEV grant, already published; no additional separate Policy family. |

## Not modified; do not mechanically version bump

- FOX2 Bridge Technical v0.4 RELEASED_EFFECTIVE — technical behavior unchanged; permission/dispatch gates unchanged.
- FOX2 SFR Registry Resolver Spec v0.1 CANDIDATE — implementation/runtime NOT_VERIFIED; no automatic policy release-detection claim.
- FOX2 released BRD, M1 Technical and mapping — no functional or contract delta caused by this routing change.
- Shared Trading Agent Evidence Handoff v1.8 and related sync/recovery addenda — retain their independently established actual statuses. CHAT-first narrows who performs eligible remote operations, it does not override existing evidence publication controls.
- Historical FOX2 BRG-003 / other Git prompts carrying Policy V1.8.2 are **not executable as new handoffs without source refresh**. Preserve their immutable historical receipts; new prompts must resolve V1.8.3 + Index V1.2.3 and task specific BRD/Tech/latest released manifest. This is not a new grant of code or Git push.
- FOX, Silkworm, Mantis each have separate existing governance/authority. The shared Owner directive and template guide CHAT routing but DO NOT auto-replace their project Policy or launch cross-project synchronization (Owner-paused remains paused).

## Enforcement requirements

At every new/re-scoped task, CHAT independently verifies applicable latest released sources through authorized Library + Git readback, performs directly any remote GitHub/Library/Issue task that its tools can safely accomplish, and delegates only irreducible local-host or coding work. New prompts must include `CHAT_CAPABILITY_CHECK` disposition, `CHAT_DIRECT_ACTIONS_DONE`, delegated delta and observed STOP/source/permission gates. Use R0–R7 and unchanged release controls. Git mirrors are not globally merged policy publication, and document publication is not an automated runtime mechanism.

## Publication receipts

- FOX2 Policy V1.8.3: `/Trading/FOX2/00_Governance/FOX2_POLICY_V1.8.3_RELEASE_MANIFEST_20261013.json`.
- FOX2 Routing Index V1.2.3: `/Trading/FOX2/00_Governance/FOX2_AGENT_PROMPT_ROUTING_INDEX_V1_2_3_PUBLICATION_RECEIPT_20261013.json`.
- Trading Prompt Template v1.8: `/Trading/00_Governance/TRADING_AGENT_PROMPT_TEMPLATE_v1.8_PUBLICATION_RECEIPT_20261013.json`.

**No automatic Bridge dispatch/DEV/merge/broker/LIVE is granted by this register.**
