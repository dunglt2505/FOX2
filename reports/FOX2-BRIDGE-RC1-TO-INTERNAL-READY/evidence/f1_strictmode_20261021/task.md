# StrictMode correction in the existing Whole-WP

Whole-WP: FOX2-BRIDGE-RC1-TO-INTERNAL-READY
Owner authority: current 2026-10-21 request explicitly authorizes the ScheduledTask property correction, regression tests and non-main Git result. This supersedes an older coding HOLD only for these exact requested paths/actions; no Agent model change or new Agent launch.
Source base: 434276765b2d09dbf8bf3a74716f40c20c878083
Branch: work/FOX2-BRIDGE-F1-CHAT-DIRECT-INTEGRATED-20261021
Actor: CHAT direct candidate authoring through GitHub connector, mocked offline PowerShell tests in workspace; no CODEX/Copilot/WORK assignment, no Dispatch, no replay. The current app model/settings are preserved, not changed or independently attested by this record.
Allowed changes: agent_bridge/scripts/f1_host_discovery_readonly.ps1; agent_bridge/tests/test_f1_host_discovery.py; existing Whole-WP reports and evidence; opened feature status only. No workflow changes unless separately justified.
Acceptance: guard optional Execute/Arguments using PSObject.Properties; null/non-exec actions cannot erase later matching task candidates; name, Execute-only and Arguments-only matches work; valid behavior and sanitized output preserved; static read-only command allowlist plus DENY/HOLD assertions; record real test results, no old PASS reused.
STOP: head drift, unknown source bytes, out-of-scope changes, required capability unavailable. No merge/main/deploy/install/Canary/real host diagnostic, provider/broker, ledger or Agent invocation. F1 remains DENY/HOLD.
Delivery: report.md + evidence_manifest.json at reports/FOX2-BRIDGE-RC1-TO-INTERNAL-READY, source lock/precheck and test logs under its evidence/f1_strictmode_20261021 directory; observed remote SHA outside the committed report; connector remote readback and bounded review. This is CHAT direct evidence, never impersonated Agent Result v2 or independent audit.
