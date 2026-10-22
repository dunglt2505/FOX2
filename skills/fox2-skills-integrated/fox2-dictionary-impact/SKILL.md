---
name: fox2-dictionary-impact
description: Trace semantic field and machine-contract changes to affected producer/consumer behavior.
---

# fox2-dictionary-impact

## Activate when
A Dictionary field, identifier, unit, type, machine schema, generator or consumer changes semantically.

## Work to perform
Map old/new semantics, producers, active consumers, null/zero, timestamps/as-of, compatibility fixtures and affected generated bindings. Check only consumers proven relevant to the changed field (Bridge parser/normalizer/adapter/ledger when truly touched). Repair the smallest incompatible consumer with focused tests and preserve old immutable identities. Do not bump BRD, TechSpec or old Policy references simply to match a Registry version.

## Completion / stop
Impact map plus exact affected consumer/test changes and unresolved unknowns.

## Responsibility boundary
Own **impact analysis**, not selecting authoritative source, generating Dispatch or publishing new current pointers.

## Shared operating and Bridge applicability
FOX2 Agile Lite: one logical task, Build → Test → Deliver, CHAT owns outcome. Use only relevant methods and real evidence. Ordinary native DEV has no mandatory R0–R7/PreExec/Dispatch/extra approval; if the selected real route is Bridge or high-risk, its installed technical controls remain authoritative. No unrelated version churn, protected operations or consumed-attempt replay. This Skill does not authorize execution or grant external rights.
