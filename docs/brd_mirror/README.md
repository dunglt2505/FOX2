# FOX2 BRD Center — Authoring Guide

**Project-wide authoring direction:** Owner approved standard BRD Template v1.0 for new and substantively revised FOX2 BRDs, 2026-10-23.  
**Git state:** Candidate adoption in [PR #31](https://github.com/dunglt2505/FOX2/pull/31); until the PR is integrated, main still contains the historical released BRDs and no effective template file.  
**Canonical template:** [FOX2_BRD_STANDARD_TEMPLATE_v1.0.md](../templates/FOX2_BRD_STANDARD_TEMPLATE_v1.0.md).  
**Authority:** [Project-wide Governance Registry](../governance/FOX2_PROJECTWIDE_GOVERNANCE_REGISTRY.json) is authoritative for the **released BRD set**, not this authoring guide.

## Where to find the authoritative BRDs

| BRD | Status as checked 2026-10-23 | Canonical location / handling |
|---|---|---|
| [BRD-00 v0.5](FOX2-BRD-00_v0.5.md) | RELEASED_EFFECTIVE (Registry) | Preserve original file, IDs and accepted evidence |
| [BRD-06 v0.5](FOX2-BRD-06_v0.5.md) | RELEASED_EFFECTIVE (Registry) | Preserve original file, IDs and accepted evidence |
| [BRD-08 v0.5](FOX2-BRD-08_v0.5.md) | RELEASED_EFFECTIVE (Registry) | Preserve original file, IDs and accepted evidence |
| BRD-09 AgentBridge | CANDIDATE / not registered as released | [PR #25](https://github.com/dunglt2505/FOX2/pull/25): preserve existing requirements and acceptance; standardize **at its next substantive revision**, not by silently replacing that worktree |

Do not infer authority from the greatest filename version or from a Git branch, PR, SHA or this index. Recheck the current Registry/Owner decision before modifying or labeling any specific BRD.

## Authoring workflow — one FOX2 Whole-WP, no extra approval gate

1. **New BRD:** create a new file from the standard template. Keep the 10 numbered sections (mark inapplicable content N/A with a reason), assign one stable requirement ID per behavior and acceptance IDs matching FOX2 conventions.
2. **Existing DRAFT/CANDIDATE BRD:** apply the standard sections **on the next genuine semantic/acceptance revision** where useful, preserving all earlier requirement IDs, acceptance IDs, negative scenarios and historical provenance. BRD-09 is such a candidate. A restructuring-only change must explicitly declare `STRUCTURAL_NO_SEMANTIC_CHANGE` with a content-preservation check; it cannot become a new authority.
3. **Existing RELEASED_EFFECTIVE BRD:** do not mass-convert BRD-00, 06 or 08 solely for presentation. If a real business behavior or acceptance change is authorized later, create a clearly versioned candidate based on the effective document; preserve unrelated accepted requirements and evidence. Promote the changed BRD only through separately verified authorization/Registry release controls.
4. **Separation of concerns:** BRD owns business goals, actors, IN/OUT scope, functional rules, safety semantics and acceptance WHAT/WHY. Tech Spec owns HOW: architecture, APIs, schema, algorithms, implementation commands. Data Contract owns typed data semantics where already assigned; BRD references rather than duplicates that contract.
5. **Traceability:** keep the stable mapping `Requirement ID → Acceptance ID → Technical Spec/Contract → Test → actual Git evidence`. A missing link is `TBD/UNKNOWN`, never a fictional PASS or a new acceptance source with conflicting expectations. Inspect only materially affected consumers when requirements truly change.
6. **Publication:** use a scoped non-main branch/PR with verified source and returned remote SHA. Candidate publication is not `RELEASED_EFFECTIVE`, installed-machine adoption, acceptance, or permission to merge main/LIVE. Never replay consumed Bridge Dispatch.

## Acceptance for authoring (not software runtime tests)

- Required 10 headings and metadata fields are present; BRD content is meaningful, specific and testable.
- Requirement/acceptance IDs are unique and stable; main behavior plus meaningful exception/negative tests are addressed.
- Source authority, version, milestone and dependent Technical Spec/Acceptance Matrix are linked or explicitly TBD.
- No silent BRD semantic changes, broken links, invented PASS, blanket version bumps or writes to released historical files.
- Project Kanban/Master Plan change only if a **material product task or milestone** changes. Applying this editorial authoring template alone does not create a new Whole-WP or imply product DONE.

**Effective scope note:** the Owner's instruction establishes a forward-looking editorial method; the source template and this guide remain Git Candidate until PR #31 is integrated. Existing effective BRD versions, Governance Registry pointers and Bridge runtime remain unchanged by this proposal.
