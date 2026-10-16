"""Reconcile Candidate contracts with the integrated product contract."""
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
ROWS = [
('agent-prompt-builder', ['outcome','allowed_paths','permissions','tests','stop_conditions','template'], ['policy','routing_index','result_template'], 'Draft one measurable handoff; do not dispatch.'),
('strategic-agent-triage', ['root_causes','options','decision'], ['policy'], 'Group findings by root cause and justify one next decision.'),
('project-health', ['facts','unknowns','blockers','next_milestone'], ['roadmap'], 'Reconcile acceptance with evidence cutoff; never infer completion from commits.'),
('document-publication', ['identity','lineage','destination','save_status','release_status','registry_status','mirror_status'], ['policy'], 'Verify destination bytes; report save, release, Registry and mirror separately.'),
('source-resolver', ['family','bootstrap'], [], 'Call native_registry.bind with host authority verifier; unresolved bootstrap holds dependent work.'),
('governance-preflight', ['operation','authorization','allowed_paths'], ['policy'], 'Evaluate applicable current controls and actual grant; no implicit rights.'),
('result-review', ['claims','tests','findings'], ['git_first_protocol','result_schema'], 'Compare claims to independently read evidence; self-report is not PASS.'),
('source-sync', ['inventory','diff','conflicts','receipts'], ['policy'], 'Detect same-name different-byte conflict; copy only authorized delta and read back.'),
('agent-route-runtime', ['route','capabilities','scope'], ['routing_index'], 'Choose one route supported by current routing and observed host capability.'),
('thread-handoff', ['source_lock','wip','completed','next_action'], ['git_first_protocol'], 'Transfer frozen task state and WIP without dispatch or replay.'),
('brd-change-control', ['requirements_delta','acceptance_impact','approvals'], ['policy'], 'Trace bounded BRD change and required approvals; do not alter canonical BRD.'),
('techspec-validator', ['traceability','gaps','unresolved'], ['data_contract'], 'Cross-check specification against BRD, interfaces and tests.'),
('dictionary-impact', ['identity_delta','consumers','impact'], ['policy'], 'Trace identity consumers; no migration without scoped authorization.'),
('feature-certification', ['feature','installed_behavior','acceptance_map','decision'], ['policy','git_first_protocol'], 'Check any feature, not Bridge only; absence of installed behavior blocks certification.'),
('execution-recovery', ['actual_state','completed_effects','safe_retry','risks'], ['policy'], 'Read actual task state; exclude completed effects from bounded recovery.'),
('status-roadmap', ['health_facts','milestones','unknowns'], ['roadmap'], 'Reuse health and plan facts with cutoff; no competing master status.'),
('research-validation', ['method','data','backtest','limits','evidence_tier'], ['policy'], 'Inspect method, leakage, data and applicability; no untested deployment.')]
catalog = {}
for name, inputs, sources, acceptance in ROWS:
    name = 'fox2-' + name
    catalog[name] = {'inputs': inputs, 'sources': sources, 'acceptance': acceptance}
    path = ROOT / 'skills' / name / 'SKILL.md'
    old = path.read_text(encoding='utf-8').split('\n## Integrated input/output contract')[0]
    # Preserve Candidate workflow/provenance while replacing static resolver linkage.
    old = old.replace('`../../shared/git_resolver.py`', '`../../shared/native_registry.py`')
    old += '\n## Integrated input/output contract\n\n'
    old += 'Required input: task_id, cutoff, actual state, scoped authority, source lock, evidence receipts, and ' + ', '.join(inputs) + '.\n\n'
    old += 'Resolve only relevant source families: ' + (', '.join(sources) or 'requested family') + '. Use the host-authorized native Registry adapter; no synthetic Registry schema is runtime authority.\n\n'
    old += acceptance + '\n\n'
    old += 'Use [shared runtime](../../shared/runtime.py) for contract/preflight and evidence readback. `PREPARED_FOR_HOST_REVIEW` validates supplied input structure and byte receipts only; complete the Skill-specific workflow above in the host before judging semantic acceptance. Return output, source lock, cutoff, factual evidence, unknowns, and typed holds.\n\n'
    old += 'STOP dependent actions for missing material source/authority, conflict, replay, failed readback or writer collision. Continue independent work. Errors: UNVERIFIED, SOURCE_CONFLICT, UNAVAILABLE, BLOCKED. Never interpret helper success as host acceptance or release authority.\n\n'
    old += 'Acceptance scenarios: provide the listed inputs with valid host bindings and evidence; reject missing inputs, material unverified sources and completed task replay. Host behavior must also satisfy: ' + acceptance + '\n'
    path.write_text(old, encoding='utf-8', newline='\n')
(ROOT / 'contracts.json').write_text(json.dumps(catalog, indent=2), encoding='utf-8', newline='\n')
