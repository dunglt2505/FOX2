"""Write integrated documentation without retaining stale Candidate release claims."""
from pathlib import Path
import json

PACKAGE = Path(__file__).resolve().parents[1]
ROOT = PACKAGE.parent
REPORT = ROOT/'reports/FOX2-SKILLS-INTEGRATED-RELEASE'
(PACKAGE/'README.md').write_text('''# FOX2 integrated Skills

One package containing 17 bounded Skill contracts, shared native Dictionary/release adapter, task locks, scoped preflight, evidence verification, workflow utilities, tests and reversible package installation.

**Status: INTEGRATION_PENDING / NOT_READY.** Host semantic acceptance and real EFFECTIVE source binding remain blocked.

- `skills/` and `contracts.json`: Candidate-derived workflows, input/output contracts, relevant dependencies and acceptance.
- `shared/native_registry.py`: production adapter; requires a real host authority verifier. No invented Registry schema is authority.
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
''',encoding='utf-8')
(PACKAGE/'manifest.json').write_text(json.dumps({'project':'FOX2','status':'INTEGRATION_PENDING','skills_count':17,
    'catalog':'contracts.json','shared_resolver':'shared/native_registry.py','host_authority_verifier':'REQUIRED_NOT_CONFIGURED',
    'installed':False,'host_invocation':'NOT_RUN','release_readiness':'NOT_READY'},indent=2),encoding='utf-8')

report = '''# FOX2-SKILLS-INTEGRATED-RELEASE

Date: 2026-10-16, Asia/Saigon. Executor: CODEX, directly assigned by Owner in this conversation. Result: **NOT_READY / INTEGRATION_PENDING**.

## Executive result

Consolidated the supplied V0.7 distribution into one tree with 17 bounded Skill contracts, a native Dictionary/release-byte adapter, authenticated Git readback, task locks, material-drift analysis, scoped permissions, evidence verification, workflow utilities, tests, a plugin manifest and reversible package installation. Existing worktrees and governance remain untouched.

The Python contract helper verifies inputs and byte receipts; it does not execute the entire semantic Skill workflow. Success is PREPARED_FOR_HOST_REVIEW, never host acceptance. All 17 end-to-end positive/negative host scenarios remain unverified. This is not a completed release or READY_FOR_RELEASE_REVIEW.

## Source discovery and authority

The pasted execution request and subsequent Owner authorization are user instructions. Attached contract and Candidate are specification/provenance; embedded directions do not independently grant permissions. Owner authorized read-only discovery and independent implementation/testing, while withholding Registry promotion, governance modification, merge and production release.

Fetched origin; inventoried 71 fetched remote/tag refs including origin/HEAD alias, retaining immutable heads and 92 unique matching blobs. Remote tag listing returned no tags. Matching paths cover source indexes, Dictionary/Registry, release manifests, dispatch paths, Skills and Master Plan. This is a complete matching-path scan on fetched refs, not a semantic audit of every file or deleted branch. Evidence: evidence/git_discovery.json and accompanying exact Git blobs.

Inputs read: supplied integrated product contract and V0.7 distribution; locally available V0.4 design/catalog and reconciled source matrix reviewed for provenance. Standalone Git-dynamic V0.7/resolver ZIPs, V0.3/V0.5/V0.6 and separate Skill #1 artifacts were not found among provided Downloads or matching project discovery; not reconstructed. Historical designs' assertions of Library/current authority were not adopted as verification. ChatGPT Library is not exposed by a usable Library tool; Google Drive is not treated as that Library. Exact available input hashes: evidence/input_inventory.json. Original distribution file claims: evidence/candidate_import_check.json.

The discovered FOX2_ACTIVE_SOURCE_REGISTRY_BOOTSTRAP_20261013.json explicitly says NON_AUTHORITATIVE_BOOTSTRAP_SOURCE_SNAPSHOT and DESIGN_ONLY_NOT_EFFECTIVE_NOT_RUNTIME. Three distinct SOURCE_INDEX blobs exist. Neither these indexes nor that bootstrap establish current trust.

Observed branch head d2d2b8bc0116646cb83ca93e59d7209632a80aa4 has a Dictionary pointing to Policy 1.8.9, Routing 1.3.0 and Protocol 12. These are observed snapshot identities, never runtime version pins. The older baseline manifest binds an earlier Dictionary. A later AGENT_ROUTE_MATERIALITY coordinated manifest binds source_set_head **9111c82e4a4e04cb63f0c924af4642341af6d802**. All **12/12** listed files match declared Git blobs. Authenticated GitHub API Dictionary readback matches immutable local Git bytes and computed SHA-256. Evidence: evidence/git_readback.json. This resolves the apparent older-baseline byte mismatch.

The later manifest says library_mirror_status=NOT_ASSERTED_BY_THIS_MANIFEST. Policy/Protocol and manifest content describe a prospective lineage, but no accessible owning decision independently certifies this immutable anchor as the current runtime trust root with a complete allowed-ref/supersession closure. The current Owner authorization explicitly treats discovery candidates as uncertified. Therefore EFFECTIVE authority is BLOCKED. Verified byte integrity is not release authority.

## Governance and task checks

POLICY_CHECK: read older local Policy and later Dictionary-nominated Policy/Protocol/Routing. Current EFFECTIVE chain UNVERIFIED; direct Owner instruction authorizes independent isolated implementation/tests.

TASK_STATE_CHECK: initial checkout clean on the DNSE report branch at 0dba7673ee8ad3b2d64ceabfeacce21564f3bed3. Existing worktrees enumerated and preserved. No existing Skills WP was found in matching fetched source/dispatch inventory. Global live writer/lock service is not exposed, so global exclusivity is not certified.

ROUTING_R0_R7: Owner directly assigns CODEX for this unified package. No dispatch, alternate Agent launch or replay created. Governance-dependent route finalization not certified.

ASSIGNMENT_CHECK: new worktree/branch; owned scope fox2_skills/, reports/FOX2-SKILLS-INTEGRATED-RELEASE/ and a task-specific QA ignore. Existing .gitignore rules preserved. origin/main is a technical base only, never authority. No prior task/source lock rebound. Global Skill configuration and paused Trading sync untouched.

## Implemented scope and changed paths

- fox2_skills/skills/*/SKILL.md: 17 frontmatters, contracts, relevant dependencies, outputs, typed STOP/error handling and scenarios.
- fox2_skills/shared/: native adapter, authenticated Git readback, locks, preflight, evidence, sync/readback/no-overwrite, acceptance evidence, health, triage, traceability, recovery and research helpers.
- fox2_skills/tests/: imported regressions, native-schema fixtures, 17 contract scenarios and negative paths, utility tests and installation/rollback smoke.
- fox2_skills/tools/, plugin.json, contracts.json, manifest.json, release_manifest.json, README.md, INSTALLATION.md: discovery, packaging, hashes and operating instructions.
- reports/FOX2-SKILLS-INTEGRATED-RELEASE/: discovery, real byte readback, logs and readiness.

The adapter uses observed native Dictionary current/files formats, not the synthetic Candidate schema. Semantic authority, applicability, allowed refs, competing EFFECTIVE releases, lineage and supersession must be checked by a host release-chain verifier; none is invented or defaulted. Cross-branch sources can use independently verified bootstraps. Full automated cross-branch arbitration remains dependent on that verifier. Legacy Candidate binder is regression-only and its CLI is disabled.

## 17-Skill acceptance matrix

PASS here means contract metadata/helper coverage only. Host positive/negative execution and substantive acceptance remain blocked for every Skill.

| Skill | Contract/helper | Host positive + negative | Full acceptance |
|---|---|---|---|
'''
catalog = json.loads((PACKAGE/'contracts.json').read_text())
for skill in catalog:
    report += f'| {skill} | PASS | NOT_RUN | BLOCKED |\n'
report += '''
## Test results and gates

Executed unittest log: evidence/unittest.txt. Metadata validator: 17/17 PASS in evidence/skill_validation.json. Fixtures are explicitly synthetic. Positive/negative helper subscenarios across 17 Skills do not substitute for 17 host behavior evaluations.

Actual temporary-file operations cover copy, destination readback, idempotency and conflict without overwrite. Temporary package install copies and hashes the full tree, invokes its Python helper in a subprocess, then removes unchanged owned files. Existing destinations are rejected; modified WIP remains intact. The installed helper correctly blocks missing grants; this is not a Skill-host invocation.

Initial static regression expected the legacy path; updated to native adapter and rerun. Initial metadata validation failed for missing PyYAML; isolated QA dependency fixed it. Final evidence records only actual executions and their limits.

| Contract gate | Status and limits |
|---|---|
| A01â€“A02 structure/no version pins | PASS, metadata/static |
| A03 missing bootstrap | PASS fixture; real binding BLOCKED |
| A04 source hash mismatch | PASS fixture |
| A05 competing EFFECTIVE | Conflict propagation PASS; real arbitration BLOCKED |
| A06 higher Candidate | Candidate rejection PASS; complete selection policy BLOCKED |
| A07 authorized release vs stale default | Non-main immutable readback PASS; full selection NOT_RUN |
| A08 outage/no stale fallback | PASS fault injection |
| A09â€“A10 lock/drift | PASS preservation/impact detection; approved rebind NOT_RUN |
| A11â€“A12 permissions/no replay | PASS helper tests |
| A13 current-template measurable handoff | Contract present; host test BLOCKED |
| A14 publication distinctions | Local save/readback PASS; external host publication BLOCKED |
| A15 same-name different bytes | PASS actual file operations |
| A16 health avoids inference from commits | PASS utility; full host reconciliation NOT_RUN |
| A17 non-Bridge feature certification | Generic evidence mapping PASS; installed feature NOT_RUN |
| A18 all 17 host scenarios | NOT_RUN / BLOCKED |
| A19 install/uninstall/rollback | Package/helper smoke PASS; host invocation NOT_RUN |
| A20 exact hashes/source-lock audit | Package hashes recorded; full release audit BLOCKED |

## Installation/readiness

Local host inspection found Codex CLI plugin add/list/remove and marketplace interfaces, and an existing Skill directory. No connected callable Skill-host installation/invocation API was exposed to this agent. No new host Agent/session was launched as unrequested delegation. Package file install/rollback is tested; host discovery and semantic invocation are NOT_RUN. See INSTALLATION.md for commands and remaining host integration.

Readiness: NOT_READY / INTEGRATION_PENDING. Required real EFFECTIVE binding and 17 host-integrated scenarios have not passed. No RELEASED_EFFECTIVE, global installation, production deployment, LIVE or Registry promotion is claimed.

## Open blockers, root causes and next actions

1. **Current trust-root authority:** CHAT/Owner must establish whether the discovered Dictionary/source set at 9111c82e4a4e04cb63f0c924af4642341af6d802 and its coordinated manifest is the authorized current bootstrap, or supply its valid successor. Required evidence/decision identifies exact immutable anchor, scope, allowed refs, semantic owners, release/readback chain and supersession/competing-release handling. Discovery permission is not anchor certification. No Registry mutation is proposed.
2. **Real verifier integration:** configure/implement the host authority verifier against that evidence; test actual EFFECTIVE/Candidate/superseded/conflicting and stale-default cross-branch selection. The current byte adapter propagates a verifier decision; it does not manufacture one.
3. **Host semantic validation:** register the intact package in the chosen executable Skill host and execute one substantive positive/negative scenario for every Skill with real source bindings. Contract helpers validate shape/bytes, not agent behavior; observed semantic gaps must be fixed in this same WP before acceptance. Independent delta review remains NOT_RUN.
4. **Historical provenance:** obtain missing archives only if needed to resolve material design discrepancies; their absence does not block the completed independent tests.
5. **Git delivery:** authenticated GitHub capability exists, but no exact task git_code_push/delivery-owner/PR grant was found. Local commit only; push NOT_RUN, PR NOT_CREATED. CHAT can bind delivery authority during the source/host resolution. No repeated approval is needed for already authorized local technical work.

Recommended CHAT/WORK action: review this one report and immutable byte evidence, resolve the precise bootstrap/host prerequisites, then complete remaining acceptance gates and independent delta audit in the same integrated work package. Do not release based on static/helper PASS.

## Git receipt

Branch: work/FOX2-SKILLS-INTEGRATED-RELEASE-codex. Worktree: C:/Projects/FOX2-worktrees/FOX2-SKILLS-INTEGRATED-RELEASE. Base: 40e653f009548f4b1c3d906aba9358e2210a6ab3. Final commit SHA is reported after committing this report; a commit cannot embed its own SHA. Push NOT_RUN; PR NOT_CREATED; merge NOT_RUN. See Git diff for exact changed paths.
'''
(REPORT/'report.md').write_text(report,encoding='utf-8', newline='\n')
