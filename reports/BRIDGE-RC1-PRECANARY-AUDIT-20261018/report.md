# FOX2 Bridge RC1 — Pre-Canary audit result
Date: 2026-10-18 (Asia/Ho_Chi_Minh)
Whole-WP: FOX2-BRIDGE-RC1-TO-INTERNAL-READY

**PRECANARY_INDEPENDENT_AUDIT=BLOCKED**

This is a completed bounded Git/package evidence review and a BLOCKED admission receipt for CHAT intake. It is not an admitted WORK audit PASS, PRECANARY_READY, product failure, or release authorization. No product code, existing evidence, dispatch, installed state, or protected ref was changed.

## 1. Scope and authority

Owner explicitly requested independent audit, R0–R7, reuse of CHAT PASS evidence, and Git Result. The handoff was actually read at:
`62cfceee81279596a5ca409630d1b88ac142b33b:docs/roadmap/FOX2_BRIDGE_RC1_PRECANARY_WORK_AUDIT_HANDOFF_20261018.md`
Git blob SHA-1: `be0bd3b926ec879568edf998d9de049319468e6f`.
It is absent at Bridge HEAD; this is a separate governance handoff, not source drift.

Audited Bridge: `f3d6468fedb553ba6c6192ba5811cb1b26a11ab9`.
Implementation product source: `dbaefdf686e06ffdf78b277288515deca9011710`.
Execution/PreExec base: `0789e5d8c3944fdc078090f50f18fb2a3abe6b64`.
Dispatch 004 control: `dc79f8143eec471508bf37565bff38442ce0548a`.

The Owner-selected handoff nominates the WP-only authority chain:
Registry `b27f1085ee13d8dce56fd2735e100ea1616e6e23:docs/governance/FOX2_RC1_TRUST_BUNDLE_20261017/REGISTRY.json`
→ manifests/Owner approval `d8e2331674ef1921844f369bfa9e48b82a73c6a1`
→ source freeze `c916de489e0aee51d6fe30c5b8b4cd9f4cd9a359`.
Owner approval SHA-256: `6185200cc2585e9a6c3fda620ed4c12841f5863b9462ba77d874253ace13de53`.

All ten source-family immutable digests match. Source identities remain Dictionary 1.2, Policy 1.8.9, Routing 1.3.0, Git-first Protocol 12. All manifests have WP_ONLY_TRUST_BINDING, no superseding source, and no global semantic promotion. Authority is inherited from the externally nominated handoff/Owner request, not inferred from a file's self-declared EFFECTIVE. New governance candidates were not substituted.

## 2. Routing Precheck and admission

| Check | Actual evidence and disposition |
|---|---|
| POLICY_CHECK | Read pinned Dictionary, Policy, Routing, PreExec and Git-first sources; verified their SHA-256 through nominated manifests. No global source promotion. |
| R0 | Dispatch 001–004 already consumed/historical; preserved. CHAT 6 critical hashes/13 invariants accepted as intake, not replayed execution. New work closes remaining Git/package coverage. |
| R1 | Independent pre-Canary readiness review; implementation and installed technical results already published. |
| R2 | Owner permits read-only audit and result delivery. CODE_ALLOWED for this audit=false. No Canary, APP-B resume, merge, main, LIVE, provider or broker authority. |
| R3 | Authenticated Git principal dunglt2505; pull/push repository permissions observed. Current host is Codex in Work Mode, Linux. No admitted WORK reviewer identity/signature mechanism or independent-session attestation was exposed. Exact current model/thinking and numeric quota were not exposed. Ongoing successful reads/analysis demonstrate capacity for this evidence review; missing quota numbers alone are not exhaustion or a gate failure. Installed Windows host/ledger access was not available. |
| R4 | CHAT: intake/evidence work supported, cannot replace required WORK certification. CODEX: authored implementation; current session does not establish independently admitted WORK identity. COPILOT: no current admission/capacity/independence probe; historical AUTH_REQUIRED is not treated as fresh proof. WORK: required normative reviewer, admission unverified. No agent silently substituted; no delegation or executable dispatch issued. |
| R5 | Original Windows worktree untouched. Temporary local clone used only as immutable Git object source; no checkout/reset/product edit. Separate new report-only non-main destination was checked absent before creation. No shared writer or existing report overwritten. |
| R6 | Reviewed all 25 closure files plus aggregate report/manifest, their historical supporting manifest, package, tests, receipts and source chain. Git result requires remote byte readback. Current installed ledger and host payload remain unobserved, distinct from recorded claims. |
| R7 | Formal certification HOLD/BLOCKED. Complete conditional factual evidence review and publish a BLOCKED report only. Stop before independent PASS, Canary admission, APP-B resume or release. |

The cloud FOX2 Skills route-runtime/source-resolver/result-review and their embedded guidance were actually read. Attempts to read the cloud shared `shared/git_resolver.py` and `shared/host_guidance.md` resources failed. The embedded guidance was available, but the mandatory shared resolver was not executed in this host. Independently implemented immutable Git byte checks below do not claim to satisfy that missing tool invocation. This is an additional procedural limitation, not SOURCE_CONFLICT.

## 3. Verified evidence

Machine-readable details and per-file digests are in `audit_checks.json`. The audit's 34 checks are evidence consistency checks, not newly executed product regression tests.

| Area | Independently observed result | Practical limit |
|---|---|---|
| Closure integrity | 26/26 declared SHA-256 digests match immutable Git bytes, including JPG; full 27 changed-path set matches manifest | Manifest excludes its own self-hash |
| Historical integrity | 67/67 prior manifest digests match at product source; 66 unchanged at audit HEAD; only mutable aggregate report differs and exact original is preserved | No historical failure rewritten |
| Source chain | 10/10 source digests match; exact task/prompt/dispatch bytes and hashes match | WP-only authority; no projectwide promotion |
| PreExec | Source→execution base changes only local_preflight.json; PASS receipt binds product source and WPF material build PASS | Implementation admission evidence, not reviewer admission |
| Scope | Exactly 27 changed paths, all reports/BRIDGE-DESKTOP-BATCH-B/**; product tree and ZIP blob unchanged | Audit does not authorize subsequent code changes |
| Gate matrix | 40 entries = 38 PASS, independent audit PENDING, icon non-gating | Technical PASS does not discharge independent audit |
| Carry-forward | All 25 carried gates had prior PASS; unchanged product/package supports applicability | No lifecycle/regression rerun |
| Python tests | Actual immutable JUnit parsed: 399 testcase elements, no failures/errors/skips | Evidence parsing, not new test execution |
| Desktop | Recorded build PASS and 30 checks PASS in immutable quality receipt; source/package unchanged | Historical executed result retained; no fresh Windows execution |
| Package | ZIP 64,479,644 bytes; SHA-256 a0516aed3d69564c657dc557b7b09cfaab549d6ab04ce4132e9399b50ce5b4ac; CRC valid | Historical two-build determinism retained, no rebuild |
| Package payload | All 252 archive-member SHA-256 values match manifest; EXE/DLL hashes match UI receipt | Archive verification is not re-attestation of installed 252 host files |
| Vault bytes | Selected synthetic TXT equals saved object, 148 bytes, SHA-256 098e31fb461b62f75bccf5eb135607e3b0ab48207734cf48910a2cc467a4c65e | Historical host action reviewed through immutable evidence |
| Vault freshness | Attempt 02:49:33.092Z → UI PID 2568 start 02:49:33.829Z → save 02:50:58.158Z → readback 02:51:06.430Z; same process | No newly performed GUI action |
| Vault semantics | Index 3→4, prior records preserved, one new content-addressed record, LOCAL_SAVED only | git_synced/released=false is semantic interpretation; fields are absent |
| Atomic index | Observer shows adjacent old/new rename, after save; file IDs differ; source uses flushed sibling temp + overwrite move | No independent crash/power-loss/concurrent-reader experiment was required or run |
| UI | Viewed immutable JPG: new TXT row, LOCAL_SAVED, 148 bytes, corresponding time/hash; native-picker receipt consistent | Screenshot does not independently attest process/host authenticity |
| Quality | Changed-text secret patterns have no hits; git diff --check PASS | Pattern scan is not proof of all possible secrets; prior nested package scan retained |
| Dispatch/no replay | max_runs=1, retry_of=003, exact control bytes; recorded manual-consumption receipt true | Live store not accessed; exactly-once consumption not independently attested |
| Canary/APP | Current Git heads unchanged at 501822a33ef08c7365154913bbc677544856eee5 / fc8aba202e15bddfcc5156b2c1bb36ed222329eb | Current host ledger cannot be inferred from Git head |
| Safe state | Immutable final receipt: STOPPED, paused=true, setup_complete=true; per-user Canary dispatch/execution counts 0/0 | Observation belongs to recorded 02:52Z host snapshot, not current host |

All seven closure Python evidence scripts were reviewed as text. None was executed by this auditor. In particular, despite its readback-oriented description, `final_readback.py` writes Dispatch 004 to the manual-consumption store; executing it would mutate evidence/state and hit its consumed-run guard. It was not run. No poll, harness, installer, GUI, Codex/Copilot execution or Canary was invoked.

## 4. Findings and disposition

**B1 — Reviewer admission/independence unverified (blocking).** The handoff §1/§3 and bound task §11 require WORK's independent audit. This session can observe its own bounded analysis and authenticated repository principal, but cannot attest an admitted independent WORK reviewer or provide its authorized audit signature. Do not label this report WORK PASS or treat another Codex session as independent merely because it is a new conversation. Numeric quota is NOT_EXPOSED; demonstrated analysis capacity is adequate for this limited review.

**B2 — Required shared resolver unavailable (procedural block).** The actual cloud resource read failed. Ten-family byte checks passed, but no claim is made that the prescribed shared resolver was executed.

**L1 — Installed-host/current-state limits.** The current installed payload files, pointer, raw manual-consumption store and live ledger were not reachable. The immutable aggregate receipts remain evidence claims from the implementing host. The handoff requires the admitted auditor to assess whether those claims suffice or whether one bounded read-only host attestation is material. No full regression, reinstall, UI save or dispatch replay is justified solely by this limitation.

**N1 — Handoff count correction (non-gating).** The handoff describes 6/27 declared file digests; actual manifest has 26 digests over 27 changed paths, excluding manifest self-hash. All 26 match.

**N2 — Index hash normalization resolved (non-gating).** artifact_ui_certification.json records original CRLF host index hashes. Git stores LF-normalized snapshots. Reconstructing CRLF gives the recorded before hash 469112d8… and after hash ff16829d… exactly; Git hashes are 3146c968… and 31f78d18…. quality_publication.py explicitly normalizes these bytes. This is not tampering or a source conflict.

**N3 — Visual text encoding (non-gating observation).** The JPG/accessibility transcript shows garbled separator text near “RC1 … Local execution console.” No gate/functional failure is inferred and no cosmetic code repair is authorized by this audit.

No material code/package defect was established by this bounded evidence review. That does not convert blocked independent admission into PASS. Historical Dispatch 003's failed UI freshness remains factual; Dispatch 004's separate fresh proof is consistent and does not rewrite the prior failure.

## 5. CHAT intake and required residual

1. Intake this result as BLOCKED reviewer admission with completed reusable evidence coverage. Preserve Dispatch 004 and all previous PASS evidence.
2. Admit the required independent WORK reviewer through the authorized identity/admission mechanism; expose the required shared resolver or resolve that procedural limitation under applicable authority. Suggested Astra/Medium remains a suggestion, not an observed/pinned execution tuple.
3. Have the admitted reviewer use this exact source lock and verification records; decide narrowly whether current read-only installed pointer/payload/manual-store/ledger attestation is material. No automatic repeat of 399/30 tests, rebuild, reinstall or UI save.
4. Return independently signed PASS/FAIL/BLOCKED receipt for CHAT verification. Only CHAT's later source-bound intake may grant PRECANARY_READY. Canary 009 remains forbidden in this task.

Audit identity: current Codex-host assistant / root session, authenticated Git principal dunglt2505. This is a truthful report identity, not a WORK identity attestation or cryptographic signature. No model, quota, host access, independence certificate or test result was fabricated.

Git Result: the containing report-only commit on `work/FOX2-BRIDGE-RC1-PRECANARY-AUDIT-20261018-readonly`, parent f3d6468fedb553ba6c6192ba5811cb1b26a11ab9. Remote commit and exact byte readback are reported separately after publication. No PR/merge/main/release action is included.

## Phân công

CHAT intake báo cáo BLOCKED và xác minh admission; WORK chưa đủ điều kiện chứng nhận trong phiên này; CODEX/COPILOT không có implementation mới. Chỉ chuyển gate khi reviewer độc lập đủ điều kiện và có receipt được CHAT xác minh.
