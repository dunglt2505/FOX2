# FOX2 — Governance/Product Release Gate Decoupling
**Owner decision / release date:** 2026-10-19  
**Scope:** Project-wide internal **governance document authority and CHAT coordination**, not installed runtime, broker or product deployment.  
**Status:** OWNER-DIRECTED GOVERNANCE RELEASE RULE — APPLIES TO NEW / RE-SCOPED WORK  
**Authority basis:** Owner's explicit 2026-10-19 instruction in the FOX2 project conversation to decouple Policy/Dictionary/Routing release from product/Bridge feature tests and to have CHAT implement it. This CHAT-authored record preserves the directive; it is not a forged cryptographic Owner signature or third-party approval.  
**Normative source:** `docs/governance/FOX2_POLICY_V2.0.0.md`, especially §§1, 6, 10; existing immutable Git/Library publication receipt.

## 1. Release domains — distinct meanings

| Domain | What can be declared | Required evidence; what is NOT a default prerequisite |
| --- | --- | --- |
| A. GOVERNANCE_DOCUMENT | `GOVERNANCE_EFFECTIVE` for an explicitly approved, scoped Policy/Dictionary/Routing document | Owner approval in scope; exact Git source commit/path/hash; applicable consistency/supersession check; published release manifest/Registry pointer; Git–Library byte readback where required. **No APP build, Windows Bridge install, Worker, Canary or broker tests** merely to release Governance. |
| B. MACHINE_CONTRACT | `MACHINE_CONTRACT_SUPPORTED` for a named generator/schema/consumer | Versioned compatibility, generated binding, validator/schema and focused consumer tests **only where affected**. Unaffected consumers remain pinned; no blanket Bridge/full-product gate. |
| C. INSTALLED_RUNTIME | `INSTALLED_RUNTIME_ADOPTED` per named host/install | Actual installed machine readback, process/ledger/admission proof as material to that installation. No claim from Git/hosted CI alone. |
| D. PRODUCT | `PRODUCT_ACCEPTED` per actual feature/route | Relevant build/API/UI/negative/security/Canary/broker evidence for the product milestone, not for governing document publication. |

`GOVERNANCE_EFFECTIVE` means the specified internal document controls **new/re-scoped CHAT work** and supersedes conflicting historical project direction; it is NOT an assertion that any installed Bridge automatically reloaded generated Python bindings or that all application features passed.

## 2. Current explicit scoped adoption

For new/re-scoped internal FOX2 governance and CHAT task source selection, Owner-approved Policy **2.0.0**, Project Dictionary **1.3**, and Routing Index **1.4.0** are the governing document source set, as independently pinned by their existing immutable paths/commits/hashes in `FOX2_POLICY_V2.0.0_RELEASE_MANIFEST_20261019.json` and `releases/FOX2_CURRENT_SOURCE_RESOLUTION_20261019.json`. Existing source files' embedded `MIGRATION_CANDIDATE / NOT_INSTALLED_EFFECTIVE` labels remain historical descriptions of migration/deployment state, **superseded for the GOVERNANCE_DOCUMENT domain ONLY by this Owner-directed release**, not silently edited or relabeled as runtime PASS.

BRD-00/06/08 v0.5, M1 Tech Spec v0.1, Market Data Contract v0.4 and Git-first Protocol v12 retain independent approved semantics/identities. BRD-09, Bridge Tech candidate and Git-first v13 candidate are **not** auto-promoted by this decision. Policy v1.8.9, Dictionary v1.2, Routing v1.3 and 2026-10-18 prepromotion candidates remain immutable provenance of previous phases. Old Bridge RC1 WP-only Registry stays WP-only.

The project-wide Governance Registry is published separately at `docs/governance/FOX2_PROJECTWIDE_GOVERNANCE_REGISTRY.json` on the authorized Governance release branch; **do not** use the Bridge `FOX2_RC1_TRUST_BUNDLE_20261017/REGISTRY.json` as project-wide authority.

## 3. Compatibility transition, no false evidence

- CHAT resolves Registry → versioned immutable Dictionary/Policy/Routing source set **at the beginning of each new/re-scoped task**, checks applicable BRD/TechSpec/contract impacts, then freezes task-specific source SHA; no newest filename/branch guessed.
- Existing executing/consumed Dispatches and historical source sets are not automatically rebound, cancelled or replayed. A transition must identify the actual changed consumer and an authorized new task/attempt before execution.
- A future Agent handoff must still publish/read back its exact task/prompt on Git and receive a Git result for CHAT intake. Owner override is separate from a technical `PASS`.
- Generated bindings supporting Dictionary 1.3 and hosted CI **111 Linux + 414 Windows PASS** are historical *source compatibility evidence*, not installed-runtime or product acceptance. The applicable consumer decides whether further focused tests are material at its own execution checkpoint.
- If consumer support is unknown, record `MACHINE_ADOPTION_UNKNOWN` for **that consumer** and stop only its incompatible execution path; **do not revoke Governance effectivity** or block independent offline APP development solely due to Bridge readiness.
- Do not infer entitlement for merge, main, deploy, real provider/broker, LIVE, or new DEV Agent assignment from this documentation release.

## 4. Supersession and release checks

The newer Owner-approved CODE-FIRST/CHAT-FIRST direction supersedes historical BRIDGE_FIRST scheduling for **new tasks**. Keep historical Master Plan copies intact and use the current operating addendum. Source/authority verification and exact Library readback remain mandatory for governed document publication; product installation/Canary tests move to their actual product checkpoint, rather than becoming new approval bureaucracy.

**Decision boundary:** `GOVERNANCE_EFFECTIVE=OWNER_AUTHORIZED_SCOPED`; `GLOBAL_MACHINE_RUNTIME_ADOPTION=NOT_ATTESTED`; `PRODUCT_ACCEPTANCE=NOT_CLAIMED`; `HISTORICAL_FAILURES=UNCHANGED`.
