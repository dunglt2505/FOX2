import json, re, unittest
from pathlib import Path
R=Path(__file__).resolve().parents[1]
SK=R/'skills'
REQ=['fox2-agent-prompt-builder','fox2-agent-route-runtime','fox2-brd-change-control','fox2-dictionary-impact','fox2-document-publication','fox2-execution-recovery','fox2-feature-certification','fox2-governance-preflight','fox2-project-health','fox2-research-validation','fox2-result-review','fox2-source-resolver','fox2-source-sync','fox2-status-roadmap','fox2-strategic-agent-triage','fox2-techspec-validator','fox2-thread-handoff']
def s(n):return (SK/n/'SKILL.md').read_text()
class FOX2SkillsV041(unittest.TestCase):
 def test_manifest_identity(self):
  for p in ['plugin.json','.codex-plugin/plugin.json','manifest.json']:
   d=json.loads((R/p).read_text());self.assertEqual(d['name'],'fox2-skills-integrated');self.assertEqual(d['version'],json.loads((R/'plugin.json').read_text())['version'])
 def test_seventeen_domain_skills_and_headers(self):
  self.assertEqual({x.parent.name for x in SK.glob('*/SKILL.md')},set(REQ))
  for name in REQ:
   t=s(name);self.assertTrue(t.startswith('---\nname: '+name+'\n'))
   for heading in ['## Activate when','## Work to perform','## Completion / stop','## Shared operating and Bridge applicability']:
    self.assertIn(heading,t,name)
   self.assertGreater(len(t),1300,name)
   self.assertNotIn('## Controlling guards (self-contained',t,name)
 def test_native_is_lightweight_and_bridge_conditional(self):
  for p in ['shared/operating_rules.md','shared/bridge_e2e_v041.md']:
   self.assertTrue((R/p).exists())
  rule=(R/'shared/operating_rules.md').read_text()
  for token in ['native development','R0–R7','PreExec','actual','no-replay','Policy v2.1.0']:
   self.assertIn(token,rule)
  builder=s('fox2-agent-prompt-builder')
  self.assertIn('Native independent CODEX/Copilot',builder)
  self.assertIn('Selected `execution_path=BRIDGE`',builder)
 def test_prompt_builder_full_bridge_contract(self):
  t=s('fox2-agent-prompt-builder')+(R/'shared/bridge_e2e_v041.md').read_text()
  for token in ['task.md','prompt.md','git_blob_sha1','sha256','max_runs=1','dictionary','policy','decision_receipt','routing','runtime_contract','permissions','required_tests','delivery_owner','PUSHED_UNREVIEWED','PowerShell','pwsh','no-replay','PreExec','model_policy','reasoning_effort','created_at']:
   self.assertIn(token,t)
 def test_bridge_old_machine_policy_not_human_policy(self):
  resolver=s('fox2-source-resolver');builder=s('fox2-agent-prompt-builder')
  self.assertIn('Policy 1.8.9',resolver)
  self.assertIn('Policy 2.1.0',resolver)
  self.assertIn('Never send Policy 2.1.0',builder)
  self.assertIn('historical',resolver)
 def test_real_receipts_not_fabricated(self):
  t=s('fox2-governance-preflight')+(R/'shared/bridge_e2e_v041.md').read_text()
  for k in ['policy_check','task_state_check','source_binding_check','routing_r0_r7','assignment_check','material_capability_check','dev_grant_ref']:
   self.assertIn(k,t)
  for k in ['UNKNOWN','NOT_RUN','PASS','STOP']:
   self.assertIn(k,t)
 def test_real_result_boundary(self):
  result=s('fox2-result-review');recovery=s('fox2-execution-recovery')
  for x in ['PUSHED_UNREVIEWED','CHAT','AGENT','BRIDGE','report.md','evidence_manifest.json']:
   self.assertIn(x,result)
  for x in ['NEEDS_RECONCILIATION','CLAIMED','RUNNING','PUBLISHING','SAME logical task','do not replay']:
   self.assertIn(x,recovery)
 def test_model_route_and_delivery_contract(self):
  route=s('fox2-agent-route-runtime')
  for x in ['CODEX','COPILOT','PINNED','CURRENT_CONFIG','PINNED_PREFERRED','low|medium|high']:
   self.assertIn(x,route)
  contract=(R/'shared/bridge_e2e_v041.md').read_text()
  for x in ['delivery_owner=AGENT','delivery_owner=BRIDGE','protected','model']:
   self.assertIn(x,contract)
 def test_no_version_cascade_or_main_merge(self):
  rule=(R/'shared/operating_rules.md').read_text()
  for x in ['not mass-updated versions','merge main','LIVE','consumed']:
   self.assertIn(x,rule)
 def test_material_bridge_without_observed_preexec_is_hold(self):
  text=(R/'shared/bridge_e2e_v041.md').read_text()
  self.assertIn('Do not publish an executable Bridge Dispatch',text)
  self.assertIn('NOT_RUN',(R/'shared/operating_rules.md').read_text())
  self.assertIn('consumed',text)
 def test_manual_windows_does_not_invent_cli(self):
  t=s('fox2-agent-prompt-builder')+(R/'shared/bridge_e2e_v041.md').read_text()
  for x in ['PowerShell','pwsh','No placeholders','HOST_NOT_VERIFIED']:
   self.assertIn(x,t)
if __name__=='__main__':unittest.main()
