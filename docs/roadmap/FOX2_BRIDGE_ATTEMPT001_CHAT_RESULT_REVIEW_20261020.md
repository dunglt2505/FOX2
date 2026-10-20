# FOX2 — CHAT independent Result Review for Bridge Integrated Attempt-001

**Review date:** 2026-10-20. **Existing Whole-WP:** `FOX2-BRIDGE-RC1-TO-INTERNAL-READY`. **Feature:** `FOX2-BRIDGE-MANUAL-LOCAL-ADMISSION` BUILD/BLOCKED. **Agent attempt:** `FOX2-BRIDGE-RC1-INTEGRATED-RECOVERY-20261020-ATTEMPT-001` — **CONSUMED, NO REPLAY**. **CHAT outcome:** `ACCEPT_RESULT_DELIVERY_AND_BLOCKED_FAILURE_RECORD / HOLD_IMPLEMENTATION_AND_RELEASE`.

## Immutable source and result readback

- Agent task/prompt Git source HEAD `b50dc1ec1ddce4e2f3b772e0244b64338c172663`; original base `c3af81429b389bb3301effc96c68fbf88744aeff`; task commit `ef390c4b58d9f4f6a7e11dcbea1f01f970e729d8`. Task blob `d4a46a8568a53716ff9758d6a1d45624881a0168`; prompt blob `82c7283a6bc3b875f9d201c279a4a7521e515944`; prompt SHA-256 `91e799d7dbe9e482768bf7edb74dc7205f2a9e77bca8bd90cbeee8bdd323a473`. CHAT independently fetched these Git inputs earlier; Agent said its own source verification was not available in that host session.
- Owner-manually-published Git **result SHA** `947cf9a33585a286a2447aa27c35328b146b2fbd` is on `work/FOX2-BRIDGE-RC1-INTEGRATED-RECOVERY-20261020`, ahead of task/prompt commit by exactly one commit; merge-base = task/prompt HEAD. This is an authorized report-only delivery after CODEX failed to use its exec tool, **not** Agent-authenticated code push. CHAT Git readback verified the actual three changed files and no code hunks.
- `reports/FOX2-BRIDGE-RC1-TO-INTERNAL-READY/report.md`: Git blob `5ce9c8638c18030527322d032e6d87f0f8ff40b1`; independently recomputed file SHA-256 `66316ac94afe5187bd7051f2bbfed61b29bff41ff8abaa353835eddc09229cb8`, size 6491 bytes; matches Owner and manifest.
- `reports/FOX2-BRIDGE-RC1-TO-INTERNAL-READY/evidence_manifest.json`: Git blob `f070c81f31922a7ae48ce3ee35e9110bac9d26a3`; SHA-256 `ed02675173c6cfe07cf5beb5f79212119f99258052790c6c70691758c9e75346`, size 997 bytes; matches Owner-reported hash; intentionally excludes self-digest.
- `reports/FOX2-BRIDGE-RC1-TO-INTERNAL-READY/evidence/preflight_blocked.json`: Git blob `35c67478b264631c76deca63083b5faae24d2ddd`; SHA-256 `4af94df641a6debc991c22403b5818c50b7e04adeab605809833161b7a428b97`, size 1672 bytes; agrees with manifest.
- Independent checksum method: SHA-256 on returned UTF-8 Git file bytes, SHA-256 code self-tested with `abc` reference vector. Result branch diff: exactly 3 additions in the allowed `reports/FOX2-BRIDGE-RC1-TO-INTERNAL-READY/**` subtree; no source edit, fixture change, test modification or unapproved path. K1: `report.md` and `evidence_manifest.json` **REQUESTED**; `evidence/preflight_blocked.json` **JUSTIFIED_GENERATED**. No `UNEXPLAINED` code hunks.

## Independent acceptance matrix

| Gate | Verdict | Basis |
|---|---|---|
| Agent result source/identity/ancestry | `PASS_SCOPED` | Exact locked task/prompt and new descendant Git result |
| Report, manifest, evidence bytes and hash | `PASS` | Full Git readback and independently recomputed matching SHA-256 |
| Changed-path allowlist | `PASS_REPORT_ONLY` | Exactly 3 report files; no unrelated code |
| Agent execution/test/build capability | `BLOCKED_HOST_SANDBOX` | CODEX observed `Failed to create unified exec process: helper_unknown_error: setup refresh had errors` at first attempted shell command |
| CODEX CLI exit 0 | `NOT_PRODUCT_SUCCESS` | Top-level CLI successful completion printed a blocked report; child `exec_command` startup failed |
| Integrated Bridge code implementation | `NOT_RUN` | No implementation diff and no code/tests executed |
| Tests and installed package | `NOT_RUN` | 0 executed, skips UNKNOWN, no new package |
| F0/F1 product acceptance | `HOLD` | F0 scoped offline acceptance remains historical; F1 not implemented/certified |
| Windows Worker/legacy retirement, Canary, Internal Ready | `NOT_ATTESTED / HOLD` | No executable installed evidence or authority |
| Attempt replay | `PROHIBITED` | Agent invoked and anti-replay marker committed locally by host launcher before invocation |

**Why this is not a normal ACCEPT:** The Agent report accurately says its own Git/host permission check was `NOT_VERIFIED` due to tool failure. CHAT's independent later Git readback supplies a **delivery/source lineage review**, not retrospective PreExec PASS or permission/one-writer proof at the time of execution. Historical failure remains real. **Do not relabel BLOCKED as PASSED.**

## Root blocker and recovery route

One tested event at `2026-10-20T15:48:39.857046Z` shows CODEX's Windows unified exec process failed to start. The exact inner helper/sandbox cause is **UNKNOWN**: Owner's targeted read-only optional log classification reported `sandbox_log_class=NOT_VERIFIED`. No evidence authorizes ACL resets, process killing, disabling sandbox, reinstalling plugins, or Windows Bridge mutation to “fix” this. CODEX Attempt-001 remains **consumed and result-closed with BLOCKED outcome**.

`NEXT_SAFE_ACTION`: obtain ONE read-only, **host-focused** CODEX sandbox initialization diagnostic or verified CLI-host repair certificate, including error/exit-class and actual supported pinned `gpt-6.1-sol` route, not another generic Bridge host inventory. Verify ability to execute a harmless command in an isolated **new** sandbox without reading/touching installed Bridge or any live ledger; do not use consumed Attempt-001 or write code as the smoke test. If host executor is repaired and Owner's scope/permissions and route PreExec hold, prepare ONE fresh source-bound integrated CODEX attempt for original Whole-WP via Prompt Builder, new branch/attempt, one-writer, exact PowerShell 7+ and Git Result Contract. If host remains broken, route safe offline Bridge engineering only through a separately verified authorized host/capability — do not auto-switch pinned model, sandbox or Actor. Do not conflate a harmless host diagnostic with F1 installed positive admission.

**Effective code/product gates remain:** F1 architecture incomplete, package with installed F0 fail-closed not attested, durable legacy writer retirement/one-writer/old consumed records unknown, Canary HOLD. F0 source `611ec26...` offline accepted in previous scoped CHAT result, not current installed runtime.

## Governance and action boundary

Human-authorized Governance Registry blob `1c28a6372a1cbbfd5341691ac9a5f98c8aa03e35`, Policy v2.0.0 and Dictionary v1.3 in permitted CHAT operational scope. `POLICY_CHECK/TASK_STATE_CHECK/SOURCE_RESOLUTION`: immutable task/result source verified and no-replay; `ROUTING_R0–R7`: CHAT independent read-only result review/report publication on **non-main** only; `ASSIGNMENT_CHECK=NOT_APPLICABLE`, no new Agent task. Applied actual Skills: `fox2-result-review`, `fox2-execution-recovery`, `fox2-source-resolver`, `fox2-governance-preflight`, `fox2-feature-certification`, `fox2-status-roadmap`, `fox2-agent-route-runtime`, `fox2-document-publication`. Agent Prompt Builder N/A: no new assignment in this report. Git write is a **PUBLISHED_REVIEW_RECORD**, not document release/EFFECTIVE or installed source.

**STOP:** No Agent replay or new attempt under same ID, no main merge, installed Worker/SQLite/legacy modification, Canary/COMPAT001, broker/provider/LIVE.
