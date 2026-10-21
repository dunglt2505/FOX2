# FOX2 — Owner Directive — Physical Host Only Target

Date: 2026-10-21
Whole-WP: `FOX2-BRIDGE-RC1-TO-INTERNAL-READY`
Feature: `FOX2-BRIDGE-MANUAL-LOCAL-ADMISSION`

## Exact Owner statement

> máy của ông chủ physical Lenovo Windows 11 Pro và chỉ chạy trên máy này

## Scoped interpretation

FOX2 Bridge F1 is to operate only on the Owner's physical Lenovo Windows 11 Pro host. There is no separate VM/secondary host available for the intended deployment target.

This statement supersedes the earlier operational assumption that G3 must execute on a disposable/isolated VM. It does **not** by itself turn the previously BLOCKED G3 PreExec receipt into PASS and does not authorize unsafe direct application of an isolated-host AppLocker allowlist to the daily-use machine.

## Required consequence

Before further privileged G3 execution on the physical host:

1. re-evaluate G1/G2 AppLocker assumptions for a single daily-use host;
2. preserve the prior BLOCKED receipt `14a02ab5f42a7659efd2b1e60324c49ff70695b5`;
3. redesign policy enforcement so host-critical and Owner-required applications are not implicitly denied;
4. require rollback-first, audit-first same-host admission;
5. re-run a re-scoped physical-host PreExec under a new task identity after the design/build correction is accepted.

## Non-effects

This directive does not authorize:
- main/merge;
- Canary009;
- provider/trading broker/LIVE;
- declaration of `INTERNAL_FOX2_BRIDGE_READY`;
- rewriting historical FAIL/BLOCKED/NOT_RUN;
- replay of G2 A01 or the blocked G3 PreExec receipt.

