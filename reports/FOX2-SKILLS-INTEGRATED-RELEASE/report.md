# FOX2-SKILLS-INTEGRATED-RELEASE — integrated review and continuation

Date: 2026-10-16 (Asia/Saigon). Decision: **NOT_READY / INTEGRATION_PENDING**.
Real source authority: **AUTHORITY_UNVERIFIED**. Release and substantive host acceptance: **BLOCKED**.

This review continues the existing branch `work/FOX2-SKILLS-INTEGRATED-RELEASE-codex` and worktree `C:/Projects/FOX2-worktrees/FOX2-SKILLS-INTEGRATED-RELEASE`, starting from clean commit `b466d844c141c6c172528585a1c60ab1d3503f2d`. No parallel candidate, new worktree, dispatch, merge, Registry edit, EFFECTIVE promotion or production release was created. The Owner's subsequent decision permits conditional-baseline implementation/testing and explicitly withholds EFFECTIVE certification. That decision is retained with the evidence.

## Readiness by evidence layer

| Layer | Observed result | Meaning |
|---|---|---|
| Uploaded ZIP checksum | VERIFIED | SHA-256 matches its supplied sidecar |
| Uploaded manifest/file integrity | VERIFIED, 146/146 files | Exact match to archive and original clean worktree |
| Uploaded standalone report/guide/test log | VERIFIED | Byte-identical to their ZIP entries |
| Conditional release source bytes | VERIFIED, 12/12 Git blobs | Integrity only; no authority inferred |
| Unit/regression suite | VERIFIED, 53 tests PASS | 34 originals plus 19 new regressions/decision tests |
| Final isolated package installation/readback | VERIFIED, 50 files | Complete package copied and read back without mismatches |
| Actual Codex plugin install/remove | VERIFIED | Executed in a separate runtime home |
| Actual host Skill discovery | VERIFIED, 17/17 enabled, 0 errors | App-server `skills/list`, not a simulated catalog |
| Installed helper missing-grant negatives | VERIFIED, 17/17 | Subprocess contract checks; not model workflow execution |
| Real conditional release-chain audit | AUTHORITY_UNVERIFIED | All 7 contract source families hold; CLI exit 2, effects empty |
| 17 substantive model-host positive/negative workflows | NOT_RUN | Authority unresolved; isolated host also lacks model authentication |
| Full release readiness | BLOCKED | Technical PASS does not satisfy source authority or semantic acceptance |

## Uploaded handoff integrity

The referenced chat exposed all six original attachments. They were checked directly, rather than substituting newer local files. The uploaded ZIP is 325,356 bytes, SHA-256:

`9674d87fe288bbe8c87771aef43eff24d8b3c810858a865e88c6049a148bb012`

It contains 147 entries: 146 manifest-bound files and the matching embedded delivery manifest. There are no duplicate entries, unsafe paths, unmanifested payload files or mismatches. Standalone `report.md`, `INSTALLATION.md` and `unittest.txt` match the archive. The external and embedded delivery manifests match. The original local worktree matched all 146 digests before continuation edits. `integrity-audit.json` records exact input paths, sizes and hashes.

The updated review bundle is a continuation of that same package. Its new hash is supplied separately; the original hash above identifies only the uploaded snapshot. The uploaded report and test log remain historical evidence, not current acceptance results.

## Source authority reconciliation

Authenticated GitHub reads independently confirmed the repository/tree and exact conditional anchors:

- Manifest: `docs/governance/FOX2_AGENT_ROUTE_MATERIALITY_RELEASE_MANIFEST_20261014.json` at `d2d2b8bc0116646cb83ca93e59d7209632a80aa4`.
- Dictionary: `docs/governance/FOX2_PROJECT_DICTIONARY_v1.json` at source commit `9111c82e4a4e04cb63f0c924af4642341af6d802`.
- Manifest SHA-256: `b6a715b5b325352551fb043926cfeebca2c5e374171b0908e96f995c774887d4`.
- Dictionary SHA-256: `7fc3532890f4a60a4abc7bf3b08dc06fe6af6ee000176ac464bfe3aacda2ecd7`.

All 12 listed source files match their declared Git blob identities at the declared source commit. The current 70 remote branch heads match the previous discovery inventory; its 71st ref is the `origin/HEAD` alias. This bounds the comparison to accessible current branches, not deleted/private/unavailable decisions. The GitHub release collection is empty; that absence is not treated as a mandatory release process or proof against authority. The tag endpoint was rejected by the connector and is not counted as a successful current tag audit.

The older bootstrap was fetched independently from its immutable branch commit. It explicitly labels itself `NON_AUTHORITATIVE_BOOTSTRAP_SOURCE_SNAPSHOT` and `DESIGN_ONLY_NOT_EFFECTIVE_NOT_RUNTIME`. Its earlier Library-authority claim and the later Git-first Dictionary/Policy model cannot be reconciled into a certified trust transition merely by sorting versions or comparing hashes.

Policy 1.8.9 asserts an Owner release direction, identifies Policy/BRD/Contract/Technical documents as semantic owners, and names its predecessor. The Dictionary explicitly separates machine identity from semantic authority. The coordinated manifest declares RELEASED_EFFECTIVE but says `library_mirror_status=NOT_ASSERTED_BY_THIS_MANIFEST`. These are relevant claims and lineage evidence; they are not independent proof that this exact immutable pair is the currently authorized trust root. The Owner's live decision confirms only a conditional technical baseline.

Consequently, no source was assigned real VERIFIED_EFFECTIVE status. The missing evidence is one authoritative, scope-applicable release/trust transition decision with immutable anchors, a complete permitted release/ref closure, owning semantic approvals and competing-release/supersession resolution. It need not be a particular cryptographic format; unsigned commits alone are not a blocker. Git authentication, ownership of a GitHub account, `main`, branch naming and self-declared status do not substitute for that decision.

The selected manifest covers only 3 of the 7 source families used by current contracts: `policy`, `routing_index`, `git_first_protocol`. It does not bind the Dictionary-selected `result_schema`, `result_template`, `data_contract` or `roadmap` paths. Its master execution plan entry is a different path from the Dictionary's `roadmap.path`. Older manifest candidates for three missing paths were inventoried without adopting them as current; no matching Data Contract manifest was found in that bounded manifest snapshot. A family-specific authoritative release closure is still needed. Broadening this manifest or copying hashes would alter governance and was not done.

Sources: [conditional release manifest](https://github.com/dunglt2505/FOX2/blob/d2d2b8bc0116646cb83ca93e59d7209632a80aa4/docs/governance/FOX2_AGENT_ROUTE_MATERIALITY_RELEASE_MANIFEST_20261014.json), [Dictionary](https://github.com/dunglt2505/FOX2/blob/9111c82e4a4e04cb63f0c924af4642341af6d802/docs/governance/FOX2_PROJECT_DICTIONARY_v1.json), [owning Policy claims](https://github.com/dunglt2505/FOX2/blob/9111c82e4a4e04cb63f0c924af4642341af6d802/docs/governance/FOX2_POLICY_V1.8.9.md), [non-authoritative bootstrap](https://github.com/dunglt2505/FOX2/blob/98d7d9f37b1c9397613479be8429665467521c99/docs/agent_handoff/SOURCE_FRESHNESS/FOX2_ACTIVE_SOURCE_REGISTRY_BOOTSTRAP_20261013.json).

## Implementation inspection and corrections

The original runtime only checks task fields, scoped grants, required source status strings and local byte receipts, then returns PREPARED_FOR_HOST_REVIEW. It echoes supplied input; it does not select routes, validate BRD/spec semantics, execute research validation or certify installed features. This distinction in the original report was accurate.

Three native-adapter defects were reproduced and corrected in the existing package:

1. **Separate manifest/source commits.** The old adapter used one commit for every file and ignored native `source_set_head`. The real manifest does not exist at its own declared source commit. Reading everything at a later head can happen to work while losing the exact release identity. The adapter now reads the manifest at the bootstrap commit, reads Dictionary/source bytes at the immutable declared source commit, and records both identities.
2. **Receipt from verified bytes.** The old adapter read the family file twice. A changing provider could return a VERIFIED_EFFECTIVE receipt whose digest belonged to an unverified second read. The adapter now hashes the one verified read. This was demonstrated with a synthetic changing provider; no corruption of immutable Git storage is claimed.
3. **Typed Git failure.** Git process failures and subprocess timeouts now become UNAVAILABLE holds. Duplicate manifest paths produce SOURCE_CONFLICT; malformed source commit pointers remain UNVERIFIED.

`shared/release_chain.py` now supplies a callable decision engine for scope/cutoff applicability, authorized immutable refs, exact manifest/Dictionary digests, semantic owner/path evidence, competing EFFECTIVE records, Candidate exclusion, supersession/predecessor closure and cycle rejection. It asks a trusted host provider for fresh evidence on every invocation; it does not cache a prior PASS. Tests cover actual decision logic, rather than only propagating a callback status.

The typed `AuthoritySnapshot` is an integration contract, not a new Registry or self-authenticating approval schema. Its producer must independently verify the owning evidence. Serialized task or repository claims cannot configure it through the CLI. With no certified provider, the engine returns AUTHORITY_UNVERIFIED. The real provider remains **unconfigured**, so the real authority verifier is not certified operational.

`tools/verify_release_chain.py` performs an authenticated conditional-baseline audit with explicit immutable paths/scope/cutoff. Actual execution checked all 7 families and returned AUTHORITY_UNVERIFIED, exit 2, with no effects. No synthetic provider was used in that real audit. The preliminary characterization probe that deliberately used a synthetic callback is labeled test-only and is not a source-lock receipt.

The packaging entrypoint previously regenerated stale report claims from a fixed string. It now packages the existing integrated report without overwriting readiness evidence. Package metadata, guide and hashes were refreshed. No SKILL.md, Registry, Policy, canonical BRD or owning technical source was changed.

An implementation limitation remains: per-Skill source/input contracts are preparation contracts, not full semantic dependency closure. For example, `fox2-techspec-validator` declares only `data_contract` as a helper dependency while its substantive workflow requires owning BRD, spec/interfaces and acceptance evidence. An executable host must resolve those task-material dependencies and assess actual behavior. The current helper suite cannot prove this obligation satisfied.

## Actual host installation and invocation interface

Codex CLI 0.162.1 was inspected and exercised, not merely inferred from documentation. The complete final 50-file package was installed under an isolated local marketplace/runtime home. `plugin marketplace add`, `plugin add`, `plugin list` and `plugin remove` succeeded. All installed bytes matched their receipt; rollback removed unchanged package-owned files.

An actual app-server process, started without launching a model agent, returned 17 enabled FOX2 Skills with no discovery errors. Names use prefix `fox2-skills-integrated:`. The generated local protocol confirms explicit `turn/start` input items with `type=skill`, `name` and installed `path`. The host API is therefore available; the original blanket host-interface uncertainty is resolved for this installed CLI version.

`account/read` in that isolated environment returned `account=null`, `requiresOpenaiAuth=true`. No credentials were copied and the user's active host installation/configuration was unchanged. Therefore model-driven behavior evaluations were not launched there. Discovery is not invocation; installed Python helper subprocesses are not model Skill execution. Official guidance also distinguishes activation from packaging and local discovery: [Build skills](https://learn.chatgpt.com/docs/build-skills), [Package plugins](https://developers.openai.com/plugins/build/plugins).

## 17-Skill acceptance matrix

Every row has host metadata discovery VERIFIED and an installed-helper missing-grant negative VERIFIED. Both substantive model-host scenarios remain NOT_RUN and full acceptance BLOCKED. The companion `17-skill-acceptance.json` gives a concrete positive and negative scenario for each row; these descriptions are recipes, not execution claims.

| Skill | Discovery | Installed helper negative | Substantive host +/- | Acceptance |
|---|---|---|---|---|
| fox2-agent-prompt-builder | VERIFIED | VERIFIED | NOT_RUN | BLOCKED |
| fox2-strategic-agent-triage | VERIFIED | VERIFIED | NOT_RUN | BLOCKED |
| fox2-project-health | VERIFIED | VERIFIED | NOT_RUN | BLOCKED |
| fox2-document-publication | VERIFIED | VERIFIED | NOT_RUN | BLOCKED |
| fox2-source-resolver | VERIFIED | VERIFIED | NOT_RUN | BLOCKED |
| fox2-governance-preflight | VERIFIED | VERIFIED | NOT_RUN | BLOCKED |
| fox2-result-review | VERIFIED | VERIFIED | NOT_RUN | BLOCKED |
| fox2-source-sync | VERIFIED | VERIFIED | NOT_RUN | BLOCKED |
| fox2-agent-route-runtime | VERIFIED | VERIFIED | NOT_RUN | BLOCKED |
| fox2-thread-handoff | VERIFIED | VERIFIED | NOT_RUN | BLOCKED |
| fox2-brd-change-control | VERIFIED | VERIFIED | NOT_RUN | BLOCKED |
| fox2-techspec-validator | VERIFIED | VERIFIED | NOT_RUN | BLOCKED |
| fox2-dictionary-impact | VERIFIED | VERIFIED | NOT_RUN | BLOCKED |
| fox2-feature-certification | VERIFIED | VERIFIED | NOT_RUN | BLOCKED |
| fox2-execution-recovery | VERIFIED | VERIFIED | NOT_RUN | BLOCKED |
| fox2-status-roadmap | VERIFIED | VERIFIED | NOT_RUN | BLOCKED |
| fox2-research-validation | VERIFIED | VERIFIED | NOT_RUN | BLOCKED |

## Validation and changed paths

Original suite: 34 PASS. Corrected suite: **53 PASS**, including 6 native-release regressions and 13 release-chain decision tests. Synthetic authority positives exercise the engine only. Real conditional audit: authority hold as expected. Final actual host: 17 discoveries, 17 installed-helper negative checks, 50 matching package files, successful uninstall/rollback. Current package hashes and archive integrity were checked after packaging.

Changed implementation paths in this continuation:

- `fox2_skills/shared/native_registry.py`
- `fox2_skills/shared/release_chain.py` (new)
- `fox2_skills/tests/test_native_release.py` (new)
- `fox2_skills/tests/test_release_chain.py` (new)
- `fox2_skills/tools/verify_release_chain.py` (new)
- `fox2_skills/tools/assemble_delivery.py`
- `fox2_skills/INSTALLATION.md`, `README.md`, `manifest.json`, `release_manifest.json`
- `reports/FOX2-SKILLS-INTEGRATED-RELEASE/report.md`, regenerated delivery manifest/ZIP/checksum, and `evidence/review/` with this review's evidence.

Original input evidence is retained. The integrated report replaces the previous report as the current readiness decision; the uploaded report is preserved under review evidence. Exact delta paths, Git receipt and diff are delivered alongside the bundle. Local changes stay in the original work package. Push, PR, merge and release remain NOT_RUN.

## Remaining blockers and precise continuation

1. **AUTHORITY_UNVERIFIED:** an independently authoritative release/trust-transition decision certifying the exact current immutable baseline or its valid successor, with applicability, semantic ownership, permitted refs and complete competing-release/supersession closure. The conditional Owner decision is deliberately insufficient for EFFECTIVE certification. No per-file reconfirmation is requested.
2. **Incomplete family release closure:** valid owning manifests/approvals for the four Dictionary-selected paths absent from the coordinated manifest, and task-material semantic dependencies required by each substantive workflow. Discovery candidates are recorded; no automatic current-version selection was made.
3. **Host semantic acceptance NOT_RUN:** an authenticated executable test host plus independently verified real source bindings. Execute the concrete positive/negative workflows for all 17 Skills, observe results and side effects independently, and fix any resulting gaps in this same package. Missing authentication in the isolated host is an environmental limit, not a claim that the user's active Codex account is logged out.

The package is suitable for continued technical review, not release approval. No checksum, helper PASS, plugin installation or source file's RELEASED_EFFECTIVE label closes those blockers.
