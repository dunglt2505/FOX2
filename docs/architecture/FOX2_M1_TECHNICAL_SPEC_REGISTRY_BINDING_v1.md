# FOX2 — M1 Technical Spec — Project Dictionary Binding v1

**Status:** `RELEASED_EFFECTIVE TECHNICAL ADDENDUM / NO BUSINESS SEMANTIC CHANGE / NO DEV GRANT`  
**Parent Technical Spec:** `FOX2_M1_TECHNICAL_SPEC_v0.1.md`  
**Registry:** `docs/governance/FOX2_PROJECT_DICTIONARY_v1.json`  
**Date:** 2026-10-14

## 1. Purpose

Bind M1 technical source identity to the project-wide Dictionary without rewriting released Technical Spec v0.1.

M1 business/runtime semantics remain owned by BRD-00/06/08 + Market Data Contract v0.4 + M1 Acceptance v0.4.

## 2. What M1 tooling may resolve from Dictionary

Build/handoff/integration tooling may resolve:
- active Policy/Routing/Protocol/Dispatch schema;
- active BRD/Technical/Data Contract/Acceptance source paths;
- project/repository/workspace identity;
- machine enums when materially needed by tooling.

Application business runtime should not import governance metadata unless a task materially requires it.

## 3. Prohibited duplication

New M1 tooling MUST NOT hand-code competing current:
- Policy version/path;
- Dispatch schema version/path;
- control branch;
- dispatch path convention.

Use Dictionary or generated binding.

## 4. Non-effects

No API/Data Contract/provider/DSM/store/UI semantic changes are created by this addendum.

No DEV/main/merge/provider/broker/LIVE grant.

`M1_TECH_REGISTRY_BINDING=V1_EFFECTIVE / PARENT_SPEC=V0.1 / BUSINESS_RUNTIME_COUPLING=NO_BY_DEFAULT`
