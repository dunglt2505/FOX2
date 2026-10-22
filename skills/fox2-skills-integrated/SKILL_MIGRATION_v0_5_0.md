# FOX2 Skills 0.5.0 — three-layer migration map

This is a *rename/consolidation* of the EXISTING plugin, not a second plugin and not 17 aliases. The names in the first column are retired from active plugin discovery; update callers to the new target when the old name is needed. Historical Git references to prior immutable releases remain unchanged.

| Previous Skill | Current Skill | Layer |
|---|---|---|
| `fox2-strategic-agent-triage` | `fox2-mgmt-delivery` | 1 — Management |
| `fox2-status-roadmap` | `fox2-mgmt-delivery` | 1 — Management |
| `fox2-project-health` | `fox2-mgmt-delivery` | 1 — Management |
| `fox2-agent-route-runtime` | `fox2-mgmt-agent-routing` | 1 — Management |
| `fox2-thread-handoff` | `fox2-mgmt-context-handoff` | 1 — Management |
| `fox2-agent-prompt-builder` | `fox2-method-prompt-builder` | 2 — Method |
| `fox2-brd-change-control` | `fox2-method-requirements-design` | 2 — Method |
| `fox2-techspec-validator` | `fox2-method-requirements-design` | 2 — Method |
| `fox2-source-resolver` | `fox2-method-source-contracts` | 2 — Method |
| `fox2-dictionary-impact` | `fox2-method-source-contracts` | 2 — Method |
| `fox2-result-review` | `fox2-method-result-acceptance` | 2 — Method |
| `fox2-feature-certification` | `fox2-method-result-acceptance` | 2 — Method |
| `fox2-research-validation` | `fox2-method-research-validation` | 2 — Method |
| `fox2-document-publication` | `fox2-tech-publication-sync` | 3 — Technical |
| `fox2-source-sync` | `fox2-tech-publication-sync` | 3 — Technical |
| `fox2-governance-preflight` | `fox2-tech-route-preflight` | 3 — Technical |
| `fox2-execution-recovery` | `fox2-tech-execution-recovery` | 3 — Technical |

**No runtime migration implied.** Skills are methods, not Bridge code changes. For Bridge results, technical status and CHAT acceptance remain separate. Do not create replacement aliases or duplicate Skills in discovery.
