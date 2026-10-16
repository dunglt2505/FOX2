# FOX2 integrated Skills

One package containing 17 bounded Skill contracts, shared native Dictionary/release adapter, task locks, scoped preflight, evidence verification, workflow utilities, tests and reversible package installation.

**Status: INTEGRATION_PENDING / NOT_READY.** Host semantic acceptance and real EFFECTIVE source binding remain blocked.

- `skills/` and `contracts.json`: Candidate-derived workflows, input/output contracts, relevant dependencies and acceptance.
- `shared/native_registry.py`: production adapter; requires a real host authority verifier. No invented Registry schema is authority.
- `shared/release_chain.py`: host-integrated release-chain decision engine; independent authority provider required, conditional baseline stays AUTHORITY_UNVERIFIED.
- `shared/local_git.py`: authenticated CLI/Git readback.
- `shared/core.py`: task locks, drift, scoped preflight and evidence.
- `shared/operations.py`: sync/save receipts, health, traceability, triage, recovery and research utilities.
- `shared/runtime.py`: contract/evidence preparation, not host certification.
- `tests/legacy_git_resolver.py`: imported Candidate compatibility code for regression tests only; synthetic Registry is not production authority and its CLI binder is disabled.
- `tests/`, `tools/`, `plugin.json`: verification and integrated packaging.
- `provenance/`: original Candidate release claims, preserved as historical input.
- `release_manifest.json`: exact package hashes, excluding itself and bytecode.

Read [installation and rollback](INSTALLATION.md). Run tests from here: `python -m unittest discover -s tests -v`. Runtime has no third-party Python dependency. Metadata QA uses isolated PyYAML.

The full readiness report and evidence are in `../reports/FOX2-SKILLS-INTEGRATED-RELEASE/` in the source checkout. No release, global host installation or production effect is claimed.
