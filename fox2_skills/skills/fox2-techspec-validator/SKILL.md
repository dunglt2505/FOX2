---
name: fox2-techspec-validator
description: Validate technical specifications against BRD, interfaces and acceptance criteria.
---
# Check specifications against requirements and testable interfaces

- Read the actual specification, owning BRD/requirements, interfaces, data contract and acceptance evidence supplied for the task. Identify missing dependencies instead of pretending a data-contract binding alone is complete.
- Trace requirement -> interface/behavior -> implementation/test evidence. Inspect incompatible field types, lifecycle assumptions, error paths and unimplemented interfaces.
- Report supported coverage, concrete gaps, unresolved conflicts and a technical decision with provenance. Do not return PASS merely because traceability keys exist.
- Technical validation of Candidate/conditional documents is allowed when assigned. Hold claims of canonical conformance or release readiness that depend on unverified governing sources.

Read [scope and source guidance](../../shared/host_guidance.md) when authority, canonical sources, task state or effects matter.
