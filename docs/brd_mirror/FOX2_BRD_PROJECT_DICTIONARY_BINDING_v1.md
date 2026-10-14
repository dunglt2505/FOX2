# FOX2 — BRD Project Dictionary Binding v1

**Status:** `RELEASED_EFFECTIVE / NO_BUSINESS_SEMANTIC_CHANGE / NO_DEV_GRANT`  
**Date:** 2026-10-14  
**Machine-readable registry:** `docs/governance/FOX2_PROJECT_DICTIONARY_v1.json`  
**Policy:** Dictionary-resolved current FOX2 Policy.

## 1. Purpose

This binding applies the FOX2 Project Dictionary to BRD source identity without changing BRD business meaning.

Current active BRD identities are resolved from the Dictionary:
- BRD-00 — Product Vision/Common Rules;
- BRD-06 — Market Data;
- BRD-08 — Presentation/UI;
- BRD-09 — AgentBridge Candidate.

Released BRD-00/06/08 remain immutable semantic authorities. They are not rewritten merely because Policy/Protocol/Dispatch identifiers change.

## 2. Ownership boundary

BRDs own product/business requirements.

The Dictionary owns only machine-readable:
- current document version/path identity;
- status/revision labels;
- compatibility/source lookup metadata.

The Dictionary MUST NOT redefine:
- business requirement meaning;
- market-data semantics;
- acceptance criteria;
- provider rights;
- user-facing safety behavior.

If a BRD meaning changes, revise the owning BRD through its normal release process.

## 3. Technical consumers

Technical Specs, CHAT handoff generation and runtime tooling may resolve BRD identity/path from the Dictionary.

They may not treat a Dictionary pointer as permission to alter BRD semantics.

## 4. No version churn rule

An `IDENTITY_ONLY` Dictionary update does not require BRD version bump.

A `SEMANTIC_SOURCE_CHANGE` does.

## 5. Current binding

`BRD_BINDING_STATUS=V1_EFFECTIVE / BUSINESS_SEMANTICS=UNCHANGED / IDENTITY_SOURCE=PROJECT_DICTIONARY_V1`
