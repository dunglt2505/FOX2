# FOX2 â€” Same-Host Guarded Policy BUILD A01 result

## R01 â€” Identification and conclusion

- Task: `FOX2-BRIDGE-RC1-SAMEHOST-BUILD-A01`; Whole-WP: `FOX2-BRIDGE-RC1-TO-INTERNAL-READY`.
- Actor: CODEX / `gpt-6.1-sol` / high / MANUAL_LOCAL / FULL_ACCESS; one implementation attempt, no Agent retry or delegation.
- Reported/finished UTC: `2026-10-21T12:47:14.602391+00:00`.
- Observed CLI process start: `2026-10-21T12:32:55.3553819Z`. Host: Windows; PowerShell 7.6.7; Python 3.13.15.
- Conclusion: **BUILD PASS candidate**. Delivery: `PUSHED_UNREVIEWED`; CHAT acceptance remains pending.
- Implementation commit: `be883bb8106ca1c058b2b34765e55c2529fe883f`.
- No effective AppLocker, AppIDSvc, Windows-service, ProgramData authority-root ACL/state or reboot mutation was performed. No Canary009, broker/provider/LIVE, main or merge operation ran.

## R02â€“R03 â€” Authority, admission and immutable sources

The active Owner assignment and pinned physical-host directive plus CHAT design acceptance authorize this BUILD scope. Governance follows Policy 2.0.0, Dictionary 1.3, Routing 1.4.0 and Git-first Protocol 12 at the exact commits in task.md. The live governance remote was observed at `d34da1e3b4918a902646621b487ca8ad3e05b0e0`. This is scoped Owner/task authority, with no cryptographic signer or installed-machine effectivity claim.

| Binding | Exact commit / identity |
|---|---|
| Task publication | `2a46a456bae3ea83ca236d210e3a0c9901a4b31d` |
| Task path | `docs/agent_handoff/FOX2-BRIDGE-RC1-TO-INTERNAL-READY/samehost/task.md` |
| Raw task SHA-256 | `71c4e1c0401c429878fabb95859f64c568c43dbe02f2ffab7b8c0de41b0837fa` |
| Raw prompt SHA-256 | `2b67241b343989b2da6dd17c6927fc5ace6c75678f28efbfa4934e717875f5d9` |
| Owner physical-host directive | `438169d5728a4b5b5da19b737e79db3fc6515ce0` |
| Accepted design candidate | `c8307980362a1ab64b93ba7d7e020d979017c849` |
| CHAT design acceptance | `0837361aa97f5d7f2116868cb2273eeac3acd0dc` |
| Accepted G2 code | `66e8f0a8b3a93140b5f908628b55ac965e15b96e` |
| Task branch lineage base | `c61ffd259a384e9c96b563968c6b7b98a0f156cd` |
| Entry head / result diff base | `0962ec74617613ff01a629926e64b7ae8b122979` |

The task/prompt at entry are byte-identical to the immutable publication. Missing local design objects were fetched by exact issued SHA before editing; no replacement branch/document was used. [Source binding](evidence/samehost/source_binding.json) records 16 pinned blobs and raw hashes, the Registry/source-resolution chain and scoped authority limits. Result schema v2 was resolved through Dictionary 1.3 and verified at entry.

Metadata PreExec and the existing live-admission probe are PASS. The metadata receipt's live probe remains NOT_RUN; the separately published live-admission receipt proves pinned route reachability only at its recorded time. Current process flags independently match the issued model/high/full-access tuple. Neither receipt was replayed. The branch had one owning worktree, no unrelated WIP and no other observed task writer. R0â€“R7/assignment conclusions are bounded to this Owner-issued MANUAL_LOCAL BUILD tuple, sources, capabilities and path grant; no installed Bridge admission is asserted.

## R04â€“R05 â€” Implemented scope and K1

Five code/test files changed:

- `f1_policy.py`: requires an explicit host baseline; accepts strict exact-hash, exact-publisher and restricted Windows/SystemApps/Program Files path rules. Exe/Script enforce; Msi/Dll default to NotConfigured and require explicit reviewed mode agreement. Existing baseline rules are preserved; unsupported XML, broad/user-writable path forms, ambiguous paths, duplicate IDs, reserved baseline controls and conflicting exact baseline allows are rejected.
- Full `effective_policy_digest` and independent `f1_control_digest` are deterministic. The sealed selector contains UUIDs derived from source/package/inventory. The subset binds actual principals, actions, hashes, current/legacy identities, all collection modes and relied-upon service/SystemApps extensions. Missing, duplicate or unexpected controls fail closed.
- `f1_service.py`: requires both digests and the sealed F1 selector. A legacy single-digest plan cannot grant authority. The broker epoch uses the full effective identity; the sealed adoption-plan digest also binds the F1 identity. Protected-root, runtime hashes, service/pipe authentication, source/package and no-replay code remain in place.
- `f1_policy_artifact.py`: requires `--baseline`; accepts optional local/effective snapshot and rollback artifact inputs as a complete set; writes final/audit XML and transition identities without applying any policy.
- Policy and HostFence tests cover safe baseline preservation, unsafe paths/XML, deterministic identities, mandatory/conditional modes, both drift directions, immutable controls and the offline CLI contract.

[Contract examples](evidence/samehost/contract_examples.json) are fixtures, not host policy, an adoption plan or executable rollback readiness. Snapshot identities preserve the raw prior XML, including unsupported prior collections for exact rollback. Audit evidence is explicitly NOT_RUN_G3 for compatibility/rollback validation and grants no adoption authority.

[K1](evidence/samehost/k1.json) classifies every material hunk as REQUESTED, NECESSARY_DEPENDENCY or JUSTIFIED_GENERATED. **UNEXPLAINED=0**. The old assertion that all four collections always enforce was replaced with the accepted Exe/Script-mandatory, Msi/Dll-conditional contract. The old model's conditional-surface deny assertion now reports NotEnforced when the collection is disabled; it never claims Windows enforcement. Host baselines are not evaluated by that narrow F1 exact-identity fixture model.

Only the five implementation/test paths, this required report/manifest and bounded `evidence/samehost/` additions changed. Historical G2/G3 receipts/results and the existing admission receipt remain byte-identical to entry. Earlier report/manifest versions remain available at the immutable entry and G2 commits.

## R06â€“R08 â€” Tests and evidence

| Check | Result | Evidence |
|---|---|---|
| Immutable source/admission binding | PASS, scoped | [source_binding.json](evidence/samehost/source_binding.json) |
| Initial focused run | FAIL: 2 failed, 136 passed | [focused-01.json](evidence/samehost/focused-01.json) |
| Final focused policy/HostFence/authority/consumer/store/reconcile/native Windows run | PASS: 142 tests | [focused-02.json](evidence/samehost/focused-02.json) |
| Full `python -m pytest -q -p no:cacheprovider agent_bridge/tests` | PASS: 606 tests, 224.92 seconds | [full-01.json](evidence/samehost/full-01.json) |
| Syntax, PowerShell parsing, wheel source contract | PASS: 3 scripts parsed, 40 modules checked | [static-01.json](evidence/samehost/static-01.json) |
| Final allowlist, `git diff --check`, bounded secret scan, source/evidence hashes, Result Contract v2 and K1 | PASS | [delivery_checks.json](evidence/samehost/delivery_checks.json) |
| Physical host enforcement/compatibility/rollback, G3/G4 | NOT_RUN | BUILD-only boundary |
| Complete release-package build | NOT_RUN | Source-module/package regression checks passed; release packaging is outside this BUILD |

Interim evidence assembly also failed on an ignored cache directory, generated JSON CRLF and default code-page decoding of a UTF-8 diff; regular-file enumeration and explicit UTF-8/LF handling corrected result assembly without a product change. [assembly-01.json](evidence/samehost/assembly-01.json) preserves that FAIL.

The initial focused failures exposed a denial-reason bug: AuthorityDeny inherits ValueError, so the new parser exception handler caught intentional drift denials and replaced their reason with POLICY_CONTRACT. An explicit AuthorityDeny passthrough corrected this without permitting execution. The original FAIL remains recorded. Full regression includes current no-replay, consumer, source/package, security and native Windows tests. HostFence OS policy responses are mocked in its fixtures; native inventory constructs XML in memory and does not apply it. Per-child `core.longpaths=true` was used for full regression fixture repositories; no global Git configuration changed.

Acceptance 1â€“13 and 15 are supported by the focused/full/static/delivery evidence. Acceptance 14 is the Result Contract v2 publication with remote readback; the observed remote result SHA is returned outside committed artifacts. No historical PASS/FAIL/BLOCKED/NOT_RUN is reclassified.

## R09 â€” Git delivery

- Repository: `dunglt2505/FOX2`.
- Exact branch: `work/FOX2-BRIDGE-F1-SAME-HOST-POLICY-BUILD-20261021`.
- Dedicated worktree: `C:/Projects/FOX2-worktrees/FOX2-BRIDGE-F1-SAME-HOST-POLICY-BUILD-20261021`.
- The observed remote result SHA is supplied separately after push/readback; this report does not self-reference its containing commit.
- Status remains PUSHED_UNREVIEWED until a separate CHAT-owned result review. No PR/main/merge permission is claimed.

## R10â€“R12 â€” Residual gates and next actor

This BUILD does not establish safe coverage for the Owner's actual applications. Path parsing is a conservative lexical boundary; G3 must prove actual ownership/DACLs, absence of writable descendants/reparse redirection and compatibility for every relied-upon path tree. Unsupported effective-policy XML (including Appx/unknown extensions/exceptions) is rejected rather than silently dropped. A host outside the supported grammar requires bounded design review, never ad hoc policy broadening.

After CHAT accepts the exact source/result SHAs, a new physical-host G3 task and fresh PreExec must verify the physical Lenovo/Windows 11 Pro target, elevation, operational AppLocker cmdlets, exact local/effective snapshots, AppIDSvc and F1 service/root state, complete required-app baseline, protected runtime/source/package inventory, copied legacy closure, audit compatibility, and a generated/readable/syntax-checked/tested rollback artifact bound to the snapshots. No real rollback script was generated or executed in this BUILD. Conditional Msi/Dll enforcement needs separate concrete audited coverage. G3 must record whether it restores the original policy or preserves an explicitly accepted state; G4 adoption remains separate.

Next actor: CHAT applies fox2-result-review to the pushed result. Remaining physical-host gates are NOT_RUN, and the old isolated-host G3 receipt remains BLOCKED. Attempts=1, Agent retries=0; numeric usage/credits are NOT_MEASURED. No escalation or scope expansion occurred.
