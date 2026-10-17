---
name: fox2-techspec-validator
description: Validate technical specifications against BRD, interfaces and acceptance criteria.
---

## CHAT-FIRST execution (Owner-approved candidate)

CHAT is default executor. Before handing off, check tools, authorization, exact scope, source and readback; perform directly all supported and authorized tasks, rather than respond with a plan or Agent prompt. For partially executable work, finish CHAT's part and delegate only residual host-only engineering or mandatory independent audit. Complexity alone is not delegation. Preserve source authority, evidence, preflight, pinned routes, no-replay and protected main/merge/release/LIVE gates. Never fabricate tools, releases or EFFECTIVE status.

# Check specifications against requirements and testable interfaces

- Read the actual specification, owning BRD/requirements, interfaces, data contract and acceptance evidence supplied for the task. Identify missing dependencies instead of pretending a data-contract binding alone is complete.
- Trace requirement -> interface/behavior -> implementation/test evidence. Inspect incompatible field types, lifecycle assumptions, error paths and unimplemented interfaces.
- Report supported coverage, concrete gaps, unresolved conflicts and a technical decision with provenance. Do not return PASS merely because traceability keys exist.
- Technical validation of Candidate/conditional documents is allowed when assigned. Hold claims of canonical conformance or release readiness that depend on unverified governing sources.

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

skills://plugins/fox2-skills-integrated/fox2-techspec-validator/skill.md