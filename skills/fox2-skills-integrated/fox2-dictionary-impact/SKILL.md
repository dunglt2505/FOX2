---
name: fox2-dictionary-impact
description: Analyze dictionary term changes and downstream references.
---

## CHAT-FIRST direct-execution override (Owner-approved candidate, 2026-10-17)

CHAT is the DEFAULT task executor, not a prompt generator or handoff coordinator only. Before suggesting WORK, CODEX, COPILOT or another Agent, check actual connected tools, permissions, source binding, available readback, host-only requirements and separation-of-duties requirements. **If CHAT can perform the user's requested work safely within existing authorization, CHAT MUST execute now, independently verify the result, and report concrete changes rather than hand off or stop at a plan.** If only part is executable, complete that part and delegate only the bounded remainder with a material reason. Complexity or number of files alone never justifies delegation. WORK only when independent audit or a needed host capability is materially required; CODEX/COPILOT only for genuine coding/runtime work. Do not invent tools, authority, EFFECTIVE, release status, or a completed write. All original source authority, immutable Git, Owner-grant, no-replay, pinned Agent, preflight and protected release/merge/LIVE rules still apply. This override never creates permission.

# Assess machine-identity changes and actual downstream consumers

- Compare the supplied before/after Dictionary entries and identify changed paths, versions, identifiers or compatibility values. Keep machine identity separate from business semantics.
- Find or inspect the actual supplied consumers, generated bindings, schemas and tests. Report impacted consumers and unknown coverage; do not invent search results.
- Produce a draft impact/migration plan and the evidence needed to validate it. Preserve an in-flight task's source lock pending material impact review.
- A semantic conflict must be resolved by the owning Policy/BRD/Contract/Technical source. Do not rewrite Registry, migrate consumers or promote the proposed delta without the relevant grant.

Apply the embedded scope and source guidance below when authority, canonical sources, task state or effects matter.


## Embedded shared guidance

# FOX2 task scope and source authority

Follow the live Owner grant and applicable project instructions. Keep task identity,
cutoff, evidence provenance and the existing source lock. Do not replay completed
effects or treat files, chat excerpts, hashes or source status text as permissions.

An Owner-authorized draft, read-only review, technical comparison or bounded local
test may proceed using explicitly labeled Candidate/conditional inputs. If a
material input is absent, report the gap and complete the independent useful work.
Do not stop all analysis merely because EFFECTIVE authority is unverified.

Before asserting a source is currently EFFECTIVE, issuing a governance-dependent
executable handoff, modifying canonical sources, or releasing/promoting anything,
resolve the relevant source families through Dictionary -> release manifest ->
immutable Git bytes -> independent owning authority. Use native_registry.bind and
ReleaseChainVerifier when a trusted host provider is available. Without it, return
AUTHORITY_UNVERIFIED / SOURCE_UNVERIFIED; actual competing authority is SOURCE_CONFLICT.
Do not select main, branch recency, latest filename or the highest version as authority.

Do not modify Registry, Policy or canonical BRD/technical sources, grant rights,
dispatch, merge or go LIVE merely because a helper or Skill ran successfully.
Actual authorized local file operations must verify destination bytes and preserve
conflicting WIP. External effects require the existing specific grant.

The Python shared.runtime is optional contract/evidence preparation, not semantic
execution or authorization. Never fabricate VERIFIED_EFFECTIVE bindings to make it
pass. Complete the task-specific analytical workflow directly when a draft/review
does not need that governed execution binding. Return output, observed evidence,
limitations, withheld effects and next action appropriate to the user's request.


This ChatGPT package provides analytical instructions. Native Python helpers and a trusted authority provider are not supplied by this cloud plugin; do not claim those helpers executed. Their absence does not prevent bounded analysis, but certified EFFECTIVE binding remains unavailable without independently verified host capability.



---
Available file URIs for this installed plugin skill. Use these exact URIs when reading files:

skills://plugins/fox2-skills-integrated/fox2-dictionary-impact/skill.md