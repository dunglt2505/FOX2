# Trading — Reusable Project Source Governance Starter Kit v1.0

**Status:** REFERENCE_TEMPLATE / OPT_IN_ONLY / NOT_EFFECTIVE_IN_ANY_PROJECT. **Created:** 2026-10-13.

Use this when creating a NEW project, so project Policy/BRD/Technical releases cannot silently remain stale in Agent prompts.

## Start here

1. Read `00_EXISTING_CONTROLS_AND_GAPS.md` before copying any policy text. It compares already documented Trading controls and FOX2's design lessons; do not invent or duplicate a second normative policy.
2. Read `01_NEW_PROJECT_SOURCE_AUTHORITY_STARTER_KIT_v1.0_REFERENCE.md` and record a project-specific Owner decision. Existing-project policy takes precedence; no new project can self-adopt merely by copying this folder.
3. Copy and instantiate `02_PROJECT_SOURCE_PROFILE_TEMPLATE.yaml` under the new project's controlled governance. Replace every REPLACE_ME and UNKNOWN with actually verified evidence; no guessed host/credentials/permissions.
4. Use `03_ACTIVE_SOURCE_REGISTRY_SCHEMA_v1.0.json` to define the non-authoritative materialized active-source index. Schema validation does NOT demonstrate Library freshness or runtime.
5. Use `04_AGENT_SOURCE_LOCK_HANDOFF_TEMPLATE.yaml` only after CHAT resolves the latest effective release for each applicable source and independently checks Library raw bytes, manifest and Git (when applicable). Never self-grant CODE_ALLOWED.
6. Run `05_SOURCE_FRESHNESS_ACCEPTANCE_MATRIX_v1.0.md` in a sandbox. It includes stale-valid-SHA, Candidate-only, incomplete pagination, event race, Git drift, authorization and privacy tests. No test is deemed run by this reference package.
7. Issue the project's own immutable policy/technical adoption record. Until then this folder is *reference only*, not an effective release, software, automatic trigger or source registry.

## Distinctions that MUST remain separate

- Library released-policy authority ≠ Registry cached index.
- Version identity/hash match ≠ latest effective version.
- Source Lock ≠ task authorization receipt.
- Git mirror/push ≠ Agent checkout verified ≠ acceptance/merge.
- Automatic documentation instructions ≠ installed Library webhook/Resolver.
- Reusable implementation source ≠ permission to migrate or synchronize other Trading projects.

## Provenance and limitations

Originated from a scoped comparison of `/Trading/00_Governance` documents and FOX2 Agent Prompt Routing Index V1.2.2 / Source Freshness Registry Resolver Spec v0.1 Candidate. No external system install, release trigger, DEV work, CI gate or cross-project change was performed by this package. See `INTEGRITY_MANIFEST_SHA256.json` for package file bytes/hashes; integrity does not establish normative status.
