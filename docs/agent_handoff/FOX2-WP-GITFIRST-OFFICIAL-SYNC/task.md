# FOX2 official sync — Owner-assigned WORK task

```json
{
  "project": "FOX2",
  "task_id": "FOX2-GITFIRST-OFFICIAL-ROLLOUT-001",
  "wp_id": "FOX2-WP-GITFIRST-OFFICIAL-SYNC",
  "change_id": "FOX2-OFFICIAL-SYNC-V13-20261012",
  "assigned_role": "WORK Document Publisher / Synchronization Operator / Workflow Integrator",
  "owner_grant": "Current Owner master assignment in this conversation; transcription below is task input, not an independent CHAT approval",
  "policy_version": "1.3.0",
  "policy_sha256": "2138d9dfdfb13eac9e58235dba81a7dca2a18b409709b3ce2c50f03168f36641",
  "approved_base_commit": "bd44dc2bb2fa1ba43070ea1052764320a86507c3",
  "branch": "work/FOX2-GITFIRST-OFFICIAL-SYNC-work-20261012",
  "api_publisher_staging": "fox2_full_audit/publication; no shared Windows worktree touched",
  "writer_lease": "Exclusive new branch created by current assigned WORK; expected-head CAS every update",
  "model": "NOT_EXPOSED",
  "thinking": "NOT_EXPOSED",
  "quota": "NOT_EXPOSED",
  "allowed_paths": [
    "docs/governance/FOX2_POLICY_V1.3.md",
    "docs/governance/FOX2_POLICY_V1.3_RELEASE_MANIFEST_20261012.json",
    "docs/agent_handoff/*v2*",
    "docs/agent_handoff/README.md",
    "docs/agent_handoff/SOURCE_INDEX.json",
    "docs/agent_handoff/SYNC_DELTA_WORKFLOW.md",
    "docs/agent_handoff/FOX2-WP-GITFIRST-OFFICIAL-SYNC/**",
    "reports/FOX2-WP-GITFIRST-OFFICIAL-SYNC/**",
    ".gitattributes"
  ],
  "forbidden_paths": [
    "backend/**",
    "frontend/**",
    "tests/**",
    "fixtures/**",
    "main",
    "any other writer branch"
  ],
  "permissions": {
    "git_source_read": true,
    "git_document_publish_write": true,
    "git_document_publish_push": true,
    "git_report_write": true,
    "git_report_push": true,
    "pr_create": true,
    "code_allowed": false,
    "git_code_push": false,
    "main_push": false,
    "merge_allowed": false,
    "dnse_production": false,
    "broker_write": false,
    "live": false
  },
  "acceptance_ids": [
    "SYNC-A01-INVENTORY",
    "SYNC-A02-POLICY",
    "SYNC-A03-M1",
    "SYNC-A04-REMOTE",
    "SYNC-A05-BRANCH",
    "SYNC-A06-V2",
    "SYNC-A07-PILOT",
    "SYNC-A08-NEGATIVE",
    "SYNC-A09-SECURITY"
  ],
  "stop": [
    "SOURCE_HASH_MISMATCH",
    "WRITER_COLLISION",
    "PLATFORM_SAFETY_BLOCK",
    "SECRET_OR_LICENSE_RISK",
    "MAIN_OR_RUNTIME_CHANGE"
  ],
  "expected_result": [
    "reports/FOX2-WP-GITFIRST-OFFICIAL-SYNC/report.md",
    "reports/FOX2-WP-GITFIRST-OFFICIAL-SYNC/evidence_manifest.json"
  ],
  "independent_review": "CHAT NOT_RUN; no self-acceptance"
}
```

Execute source/branch audit, authorized current delta publication and same-WP Git-read task/report pilot. Existing safety-blocked source contents must not be re-sent. Full sync remains PARTIAL if required released sources cannot be published legitimately; preserve their source hashes and precise blocker. No runtime implementation or integration.
