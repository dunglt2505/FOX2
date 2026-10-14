# FOX2 Bridge Desktop Batch B: stopped at launch gate

Status: BLOCKED_PREEXEC. Whole-WP implementation and installed certification did not start.

The host Python environment lacks `setuptools>=80,<90`, the build requirement declared by `agent_bridge/pyproject.toml` for `setuptools.build_meta`. The required installer/package launch capability is therefore not established. No dependency installation, package build, installer change, or accepted Batch A rewrite was performed. Windows native IExpress/tar tools are available; their presence does not supply the declared Python build backend. Optional PyInstaller/build/wheel and common installer tools are also absent, but those optional absences are not independently classified as mandatory failures.

The controlling instruction requires STOP for a missing material packaging dependency. This attempt stops at that gate and publishes only bounded report evidence.

Pre-execution evidence:

- Full Dispatch Schema v3 validation, including date-time format and additional-property constraints: PASS.
- Exact Dictionary, Policy, Task, Prompt SHA-256 and Prompt Git blob binding: PASS.
- Initial branch and approved base: exact match; initial worktree clean.
- Control remote SHA: 801a68beaeae8db8e8841ef53b009fc064ed9fc1.
- Task remote SHA before this report: fd84006c4152fa8f0cda7c5df7c0b4c56ac7d48b.
- Current Codex process: gpt-6.1-sol / medium / danger-full-access; session approval policy never.
- Known runtime ledger: zero matching dispatch rows; no installed AgentBridge runtime found in the two inspected LocalAppData locations.
- Competing material writer: none observed. No execution lock was claimed after the failed prerequisite.

Read sources: immutable dispatch at control commit, pinned task, Dictionary v1.2, Policy V1.8.9, Dispatch Schema v3, Git-first Protocol v12, PreExec Evidence Protocol v1.1, Bridge Technical Spec v0.7 Candidate REV10, and Usage/Routing Contract Candidate REV5.

All 24 acceptance gates are recorded individually in `evidence/acceptance_gates.json`. Installed runtime, real eligible canary, runtime routing enforcement, usage, restart/no-replay, and full Bridge tests are NOT_RUN. Source/schema prechecks do not discharge the six carried Batch A certification obligations. No application readiness or Windows runtime PASS is asserted.

Lifecycle: no implementation, installation, Agent certification launch, Bridge claim, consumption, replay, or substitution occurred in this attempt. The existing ledger was opened read-only. This durable blocked record does not authorize automatic retry. Return the missing packaging capability to CHAT for reconciliation before any further execution.

Only reports/BRIDGE-DESKTOP-BATCH-B was written. Report-only publication is on the authorized task branch; no main, PR, merge, release, deploy, provider, broker, or LIVE operation is performed. Publication/readback evidence is recorded separately from installed-runtime acceptance.

FOX2_BRIDGE_DESKTOP_BATCH_B_PUSHED_UNREVIEWED is not earned by a blocked report. INTERNAL_FOX2_BRIDGE_READY remains an independently accepted CHAT target.
