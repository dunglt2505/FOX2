You are CODEX, implementing F0 inside existing Whole-WP FOX2-BRIDGE-RC1-TO-INTERNAL-READY.
One-shot identity: FOX2-BRIDGE-F0-OFFLINE-ATTEMPT04-20261020. Model gpt-6.1-sol, reasoning medium, source-defined FULL_ACCESS, exact scoped paths only.
Read docs/agent_handoff/FOX2-BRIDGE-MANUAL-LOCAL-ADMISSION-DEV-20261019/F0_OFFLINE_ATTEMPT04/task.md and source_lock.json before doing work. Treat both as the bounded task contract.
Do not start unless the supervising CHAT launcher has verified a separate immutable CHAT Final Admission with PASS_TO_ASSIGN, a fresh schema-v1 PreExec receipt, source/task/prompt hashes, clean branch, exclusive writer, and has durably reserved this NEW identity. You cannot self-admit.
The launcher's inherited FOX2_F0_ADMISSION_COMMIT and FOX2_F0_ADMISSION_SHA256 identify the admission; verify its Git content before edits. If absent, STOP without product mutation.
Allowed root: C:\Users\Fox Le\.codex\.chatgpt-projects\g-p-6abcbc976b948191a760dbb0c316a64d\work\f0_offline_20261020\repo; branch work/FOX2-BRIDGE-F0-OFFLINE-ATTEMPT04-20261020; no other checkout or installed Bridge data. All work stays offline except Git delivery.
Implement the minimal durable shared deny-by-default claim guard specified in task.md. Preserve all six original negative fixture tests exactly. Fix the actual direct claim interface, not a Worker-only or real-host-path-only guard.
Run specified focused tests and meaningful restart/concurrency/crash negatives with disposable fixtures; never a paid Agent or installed runtime test.
Respect path allowlist and K1, retain F1/Canary/LIVE HOLD. Produce exactly report.md, evidence_manifest.json (schema v2), test_summary.json, diff_trace.json under reports/FOX2-BRIDGE-MANUAL-LOCAL-ADMISSION-DEV-20261019/.
Validate result schema, changed paths and git diff --check. Commit/push once to the authorized branch when safe, remote-readback, and output actual remote SHA outside the committed manifest.
Do not publish admission/governance or self-accept. If blocked, return the precise blocker without expanding scope. Never replay prior attempts or resume this attempt after ambiguous launch.
