# Trading — Existing source-authority controls and reusable gaps

**Record:** TSG-SRC-AUDIT-20261013 · **Scope:** documentary survey for future project creation · **Status:** AUDIT_REFERENCE / NOT_POLICY / NO_RUNTIME_ATTESTATION · **Date:** 2026-10-13.

## Survey boundary

Checked current Library directory `/Trading/00_Governance/` (full directory listing, `next_cursor=null`), relevant FOX2 official and candidate materials, and FOX2 Git reference at an immutable commit. This is a **scoped document survey**, not a historical inventory of every Trading file or verification that legacy FOX/Mantis/Silkworm runtime tools exist. No shared Trading migration/synchronization process is resumed by this survey. Every source below retains its own documented status and applicability; a reference's presence is **not** a new effective-policy declaration.

| Existing artifact / document family | Already specifies | Residual gap for new project | Disposition |
|---|---|---|---|
| `/Trading/00_Governance/TRADING_AGENT_EVIDENCE_HANDOFF_POLICY_v1.8.md` | Latest applicable approved source, Library pagination, exact bytes, Git execution mirror, P0–P7 publication, source-lock checks, status distinctions; explicit warning native Library webhook is unproven | No turnkey project-neutral registry schema + typed family resolver with proven deployment | REUSE AS REFERENCE; do not duplicate normative text |
| `/Trading/00_Governance/TRADING_AGENT_PROMPT_TEMPLATE_v1.7.md` | Required prompt/source-lock fields, prompt pre-send checks, actual Agent checkout attestations | Manual/header template; no automatic current release-head resolution or trigger installed by the document | REUSE concept; offer project-configurable starter handoff template |
| `/Trading/00_Governance/TRADING_AGENT_POLICY_ENFORCEMENT_ADDENDUM_v1.0.md` | Separate LIBRARY_PUBLICATION, PROMPT_HANDOFF and AGENT_CHECKOUT gates, Source Lock/prompt packet, fail-closed | Describes FOX checker examples; document says Git integration/policy gate pending, not a universal running service | REUSE gate semantics, do not assert universal enforcement |
| `/Trading/00_Governance/TRADING_AGENT_POLICY_ENFORCEMENT_ADDENDUM_v1.1_CANDIDATE.md` | Distinguishes SOURCE_INVENTORY_LOCK, APPLICABILITY_AND_AUTHORITY_REGISTER, TASK_AUTHORIZATION_RECEIPT, PACKET, CHECKOUT_ATTESTATION; two-phase bootstrap | Candidate/NOT_EFFECTIVE; not a released change to earlier projects | INCORPORATE safe *conceptual separation* into opt-in kit, never promote Candidate silently |
| `/Trading/00_Governance/TRADING_AUTOMATIC_SOURCE_LOCK_REGISTRATION_CI_RECOVERY_ADDENDUM_v0.1.md` | Combined document + source-lock transaction, CI negative tests, receipts and bounded repair | Written as proposal/review candidate; no cross-project live Publisher/Registry demonstrated | REFERENCE for publication design, not a runtime pass |
| `/Trading/00_Governance/TRADING_AUTOMATIC_DECISION_DOCUMENT_GIT_SYNC_POLICY_ADDENDUM_v0.1.md` | Decision→document→Git byte-exact sync, role and receipt distinctions | Scope/use may be pending Git publication; automation is not proven | REFERENCE for template checklist |
| `/Trading/00_Governance/TRADING_AUTONOMOUS_DOCUMENT_SYNC_AND_RECOVERY_POLICY_ADDENDUM_v1.0.md` | Same-turn permitted sync, T0/T1/T2 approvals, error recovery, event/schedule fallback | Explicitly not a native Library webhook; cannot guarantee unattended recency | DO NOT duplicate/presume its watch is running; project-specific proof required |
| FOX2 Policy V1.8.2, Agent Prompt Routing Index V1.2.2 | Owner/Policy precedence, R0–R7, `SOURCE_FRESHNESS_PRECHECK`, `SOURCE_LOCK`, stale block | FOX2-only and reference to then-current FOX2 SHA; cannot simply clone as live policy in other projects | GENERALIZE configurable process only; preserve FOX2 authority |
| FOX2 Source Freshness Registry/Resolver Spec v0.1 Candidate and Issue #11 | Typed registry, actual Library family-head resolution, CAS, release event, runtime split, negative tests | Candidate; no implemented Resolver or Library event capability demonstrated | Use as design seed, not proof of implementation |

## Root cause pattern

1. **Identity vs freshness:** A correct SHA on an old published document does not prove it is the newest applicable effective release.
2. **Authority vs inventory:** A Source Lock or Registry describes facts; neither grants project authority, DEV, Git write, merge or LIVE.
3. **Publication vs transport:** Library release, Git mirror, Agent checkout and actual executor permission are different evidence classes.
4. **Source versus task permission:** A task's applicability/authorization receipt must not be derived from an Agent-controlled boolean in a prompt.
5. **Detection versus enforcement:** A written `SOURCE_FRESHNESS_PRECHECK` or GitHub webhook is not a demonstrated Library-connected Resolver; only a real reader and negative/race tests can establish automatic enforcement.
6. **Bootstrap circularity:** A new project must be able to prepare its first source checkout without claiming an already approved DEV prompt.

## Decision for future projects

Create **one non-binding reusable Starter Kit** (this folder's `01`–`05` files), rather than another Trading-wide effective policy. The new project's Owner/CHAT explicitly selects the source policy and may adopt the kit by issuing its own project-specific effective policy and technical contract. GitHub links or copied starter files do not opt in a project, and FOX2-only grants/branches/hosts are never inherited. Nothing here unpauses cross-project migration or propagates controls into FOX/Mantis/Silkworm.

## Routing R0–R7 (this authoring task)

R0 document survey retained, no previous implementation rerun. R1 reusable documentation/bootstrap design only. R2 source authority separated, no DEV or release rights conveyed. R3 actual Copilot/Codex/Work quota, access and host worktree remain UNKNOWN, irrelevant to CHAT document drafting. R4 CHAT is sufficient for material-neutral documentation; Copilot/Codex/Work not assigned to code. R5 isolated new files/branch only, no user Windows worktree touched. R6 exact Library/Git receipt required for artifacts delivered here; runtime handoff remains absent. R7 STOP before importing a template into any live project's normative policy, git release, or DEV without that project's separate gates.
