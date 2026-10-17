---
name: fox2-dictionary-impact
description: Analyze dictionary term changes and downstream references.
---
# Assess machine-identity changes and actual downstream consumers

- Compare the supplied before/after Dictionary entries and identify changed paths, versions, identifiers or compatibility values. Keep machine identity separate from business semantics.
- Find or inspect the actual supplied consumers, generated bindings, schemas and tests. Report impacted consumers and unknown coverage; do not invent search results.
- Produce a draft impact/migration plan and the evidence needed to validate it. Preserve an in-flight task's source lock pending material impact review.
- A semantic conflict must be resolved by the owning Policy/BRD/Contract/Technical source. Do not rewrite Registry, migrate consumers or promote the proposed delta without the relevant grant.

Read [scope and source guidance](../../shared/host_guidance.md) when authority, canonical sources, task state or effects matter.
