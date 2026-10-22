---
name: fox2-techspec-validator
description: Validate relevant technical contracts, interfaces and failure cases.
---

# fox2-techspec-validator

## Activate when
Architecture/API/type/contract behavior is designed or materially modified.

## Work to perform
Validate BRD acceptance against actual API, types, units, null semantics, as-of timestamps, errors, timeouts, retries/idempotency, concurrency, data contracts and affected producers/consumers. Require focused compatibility, negative and security tests for changed surfaces. For Bridge code changes, inspect impacted normalizer/schema/ledger/adapter contracts **only** when modified. Do not regenerate TechSpec because human Policy version changed.

## Completion / stop
A concise interface/contract defect list or validation verdict with focused tests.

## Responsibility boundary
Own **technical design conformance**, not business requirement approval, code execution or acceptance of an Agent result.

## Shared operating and Bridge applicability
FOX2 Agile Lite: one logical task, Build → Test → Deliver, CHAT owns outcome. Use only relevant methods and real evidence. Ordinary native DEV has no mandatory R0–R7/PreExec/Dispatch/extra approval; if the selected real route is Bridge or high-risk, its installed technical controls remain authoritative. No unrelated version churn, protected operations or consumed-attempt replay. This Skill does not authorize execution or grant external rights.
