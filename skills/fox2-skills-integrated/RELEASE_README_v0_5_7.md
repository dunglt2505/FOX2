# FOX2 Skills v0.5.7 — PowerShell/Git script reliability and no-code evidence

- Host-specific PowerShell 5.1 vs pwsh 7; executable variable invocation with `&`, correct Git exit-code checks, no GV/alias assumptions or blind push/reset. Host-unknown scripts remain NOT_RUN, not copy-ready certified.
- Distinguish CODE_CHANGE vs TEST_EVIDENCE_ONLY. Real tests and authorized remote report/evidence SHA can satisfy an explicitly test-only task without modifying product code. Missing/unrun/stale tests or missing Git publisher evidence can never become DONE.
- Bridge publisher/recovery/Dispatch remains installed host's responsibility. No changes to runtime, governance or protected branches.
- Retain all 11 Skills and v0.5.6 progress Watch management behavior.
- Static/fixture tests only; actual Windows PS5.1/7 and Bridge host E2E NOT_RUN here.
