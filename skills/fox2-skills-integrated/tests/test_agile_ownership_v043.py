"""Architecture acceptance: outputs and owners, not decorative phrase checks."""
import unittest, json
from pathlib import Path
R=Path(__file__).resolve().parents[1]
SK=R/'skills'
NAMES=['fox2-agent-prompt-builder','fox2-agent-route-runtime','fox2-brd-change-control','fox2-dictionary-impact','fox2-document-publication','fox2-execution-recovery','fox2-feature-certification','fox2-governance-preflight','fox2-project-health','fox2-research-validation','fox2-result-review','fox2-source-resolver','fox2-source-sync','fox2-status-roadmap','fox2-strategic-agent-triage','fox2-techspec-validator','fox2-thread-handoff']
class AgileOwnershipV043(unittest.TestCase):
 def get(self,n):return (SK/n/'SKILL.md').read_text()
 def test_all_17_ids_and_self_contained_boundaries(self):
  self.assertEqual(set(p.parent.name for p in SK.glob('*/SKILL.md')),set(NAMES))
  for n in NAMES:
   s=self.get(n)
   for x in ['## Activate when','## Work to perform','## Completion / stop','## Responsibility boundary','## Shared operating and Bridge applicability']:
    self.assertIn(x,s,n)
   self.assertGreater(len(s),900)
   self.assertNotIn('## Controlling guards (self-contained',s)
 def test_prompt_builder_single_responsibility(self):
  t=self.get('fox2-agent-prompt-builder')
  for x in ['**Goal:**','**Scope:**','**Context:**','**Execution direction:**','**Acceptance:**','**Return:**','PROMPT_READY']:
   self.assertIn(x,t)
  for phrase in ['**Dispatch generation**','**PreExec evidence**','**Source readback**','## Bridge outcome classifications','`max_runs=1`']:
   self.assertNotIn(phrase,t)
  for x in ['does not','Bridge','Result Review']:
   self.assertIn(x,t)
 def test_technical_bridge_controls_live_only_in_technical_reference(self):
  ref=(R/'shared/bridge_e2e_v041.md').read_text()
  for x in ['decision_receipt','max_runs=1','git_blob_sha1','PUSHED_UNREVIEWED','PreExec','source']:
   self.assertIn(x,ref)
  self.assertIn('NOT A PROMPT BUILDER CHECKLIST',ref)
 def test_distinct_ownership_contracts(self):
  checks={
   'fox2-agent-route-runtime':['**selection, not permissions/PreExec','Actor'],
   'fox2-strategic-agent-triage':['**priority and scope decision**'],
   'fox2-source-resolver':['**source decision**'],
   'fox2-dictionary-impact':['**impact analysis**'],
   'fox2-document-publication':['**governed-document lifecycle**'],
   'fox2-source-sync':['**file replication and comparison**'],
   'fox2-result-review':['**product/task acceptance**'],
   'fox2-feature-certification':['**milestone/product-level certification**'],
   'fox2-project-health':['**aggregate health and delivery quality**'],
   'fox2-status-roadmap':['**task plan/state**'],
  }
  for n,tokens in checks.items():
   for token in tokens:self.assertIn(token,self.get(n),(n,token))
 def test_no_universal_gate_and_source_integrity(self):
  s=(R/'shared/operating_rules.md').read_text()
  for t in ['Ordinary reversible native DEV','Bridge','no-replay','one task','archived method references','NOT a Prompt Builder']:
   self.assertIn(t,s)
  for f in ['host_guidance.md','sdlc_skill_routing_v035.md','skill_execution_contract_v036.md','task_level_routing_v037.md']:
   self.assertIn('HISTORICAL REFERENCE — NOT CURRENT', (R/'shared'/f).read_text())
 def test_release_identity(self):
  for x in ['plugin.json','.codex-plugin/plugin.json','manifest.json']:
   j=json.loads((R/x).read_text());self.assertEqual(j['version'],'0.4.3');self.assertEqual(j['name'],'fox2-skills-integrated')
  self.assertEqual(json.loads((R/'manifest.json').read_text())['skills_count'],17)
 def test_native_bridge_scenarios_still_tested(self):
  f=R/'tests/test_bridge_scenarios_v041.py'
  self.assertTrue(f.exists())
  code=f.read_text();self.assertIn('HOLD_MISSING_RECEIPT',code);self.assertIn('STOP_CONSUMED_NO_REPLAY',code)
