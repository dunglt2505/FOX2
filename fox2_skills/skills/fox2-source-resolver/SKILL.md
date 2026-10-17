---
name: fox2-source-resolver
description: Resolve trusted Git Registry, release manifests, provenance and effective sources.
---
# Resolve source identities without manufacturing authority

- Determine whether the request needs technical byte inspection or a certified current EFFECTIVE binding. Use the Owner's exact conditional anchor for inspection when supplied.
- Read Dictionary and manifest at immutable commits. Respect the manifest's declared source commit, verify listed file records and return commit/path/digests, provenance and missing families.
- For EFFECTIVE binding use [native_registry.bind](../../shared/native_registry.py) with [ReleaseChainVerifier](../../shared/release_chain.py) and independently trusted host authority evidence. Check scope, semantic ownership, permitted refs, competing releases and supersession.
- Return AUTHORITY_UNVERIFIED for an uncertified root and SOURCE_CONFLICT for an actual conflicting authority set. Do not select main, the latest filename or the highest version as authority.
- Missing authority does not prevent producing a factual byte/provenance report. Do not promote the Registry or reuse a cached PASS.

Read [scope and source guidance](../../shared/host_guidance.md) when authority, canonical sources, task state or effects matter.
