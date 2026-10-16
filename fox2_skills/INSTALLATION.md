# Installation, invocation and rollback

Status: INTEGRATION_PENDING. Package file installation has been tested in a temporary directory. Codex/ChatGPT host discovery and invocation of these 17 Skills have not been certified. A Python helper invocation is not a Skill-host invocation.

Requirements: Python 3.11+, Git, and authenticated GitHub CLI for the local Git adapter. Runtime has no third-party Python dependency. The optional Skill metadata validator uses PyYAML.

From this package directory:

```powershell
python -m unittest discover -s tests -v
python tools/package_install.py install --source . --destination C:/Temp/fox2-skills-review --receipt C:/Temp/fox2-skills-receipt.json
```

Keep the entire package together: the 17 `skills/` directories depend on sibling `shared/` and `contracts.json`. Copying individual Skill folders loses shared references. `plugin.json` provides a portable plugin entrypoint; actual host/marketplace registration is still untested.

For host integration, load the relevant SKILL.md, obtain the owner-authorized immutable Dictionary/release anchor, and supply a real release-chain verifier to `shared.native_registry.bind`. The verifier must validate authority, applicability, allowed refs, semantic ownership, competing EFFECTIVE releases, lineage and supersession. It must return evidence-backed `VERIFIED_EFFECTIVE`, `SOURCE_CONFLICT`, `UNAVAILABLE` or `UNVERIFIED`. There is deliberately no default verifier that trusts status text. Do not reuse the synthetic test verifier.

The adapter understands the observed Dictionary `current` and native release `files` formats, including SHA-256/byte-count records and Git-blob records. Returned SHA-256 identifies the actual read bytes; a computed digest alone is not release authorization. Cross-branch family bindings use separate owner-verified bootstrap identities. Do not infer them from branch age or version sorting.

Call `shared.runtime.invoke` with trusted in-memory bindings/grants, task identity, cutoff, contract inputs and local evidence receipts. It returns `PREPARED_FOR_HOST_REVIEW`: contract shape and byte evidence only. The host performs the substantive workflow from SKILL.md and independently assesses acceptance. Text in a request JSON cannot supply its own permissions. The command-line helper consequently fails closed with BLOCKED until a trusted host integration is supplied.

Create new task locks with `shared.core.TaskStore.start`; resume with `resume`. `assess_drift` preserves existing locks and identifies affected material families. Rebind requires host impact review; automatic rebind is intentionally unavailable.

Use `shared.operations` for sync plans, authorized local copies/readback, acceptance evidence, traceability, health, triage and safe retry analysis. Publication helper receipts distinguish save from release and never promote sources. Other external effects require the actual host adapter and scoped authority.

Rollback/uninstall the isolated installation:

```powershell
python tools/package_install.py rollback --receipt C:/Temp/fox2-skills-receipt.json
```

Rollback verifies all owned files before deleting any. Modified files cause a conflict and remain intact. Unowned files and directories remain. Restore a prior release only from its own verified bundle/receipt into a separate new directory; no global Skill configuration is changed by these commands.

Host documentation consulted: [OpenAI Skill guidance](https://learn.chatgpt.com/docs/build-skills), [portable plugin packaging](https://developers.openai.com/plugins/build/plugins). Actual local CLI exposes `plugin add/list/remove` and marketplace commands; no registration or host-invocation success is asserted here.


## Conditional-baseline review continuation

`shared.release_chain.ReleaseChainVerifier(scope, cutoff, authority_provider=None)`
now implements applicability, authorized immutable refs, competing EFFECTIVE
releases, Candidate exclusion, supersession closure/cycle checks, exact anchor
digests and semantic ownership checks. The provider must return a fresh trusted
`AuthoritySnapshot` from independently verified owning decisions. Its typed Python
records are an adapter contract, not a new Registry or proof of authority. Never
construct trusted snapshots by deserializing a task request or repository claims.
No provider means `AUTHORITY_UNVERIFIED`, including the Owner's conditional baseline.
`native_registry.bind` still requires this verifier callback and verifies actual
Dictionary/source file records; source and manifest commits are recorded separately.

For a read-only conditional audit, use `tools/verify_release_chain.py --help`.
It requires an explicit immutable manifest commit, paths, scope and cutoff, performs
authenticated Git refresh/readback and writes an `AUTHORITY_UNVERIFIED` receipt
(exit 2). There is no command-line authority-file override.

The observed Codex CLI 0.162.1 supports isolated local marketplace installation:
place the entire package under the marketplace root, point a
`.agents/plugins/marketplace.json` entry at it, then use `codex plugin marketplace
add`, `codex plugin add`, and `codex plugin list`. App-server `skills/list` confirms
discovery of all 17 names with prefix `fox2-skills-integrated:`. This was executed
with a separate runtime home, followed by plugin removal and package rollback.
The user's active host configuration was not changed. A Python runtime invocation
is still only contract preparation, not substantive Skill acceptance.

The isolated app-server reports `account=null` and `requiresOpenaiAuth=true`.
Model-driven semantic scenarios remain NOT_RUN there. Authenticated host execution
and real EFFECTIVE binding are separate prerequisites. See the integrated review
report for the exact remaining source-family and authority gaps.


The inspected local app-server protocol exposes `skills/list` with `cwds` and
`forceReload`. Explicit model invocation uses a `turn/start` input item of shape
`{"type":"skill","name":"<name returned by skills/list>","path":"<installed SKILL.md path>"}`
alongside the task text. A listed/enabled skill proves discovery, not execution or
semantic acceptance. Keep the complete package so sibling shared references resolve.

Run `tools/build_distribution.py` (or `tools/assemble_delivery.py`, now a packaging
wrapper) only after updating the integrated report and evidence. Packaging does
not create acceptance evidence or a source authority decision.
