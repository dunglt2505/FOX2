import unittest,json
from pathlib import Path
R=Path(__file__).resolve().parents[1]
class SkillContractsV041(unittest.TestCase):
 def test_conditional_contract_no_eight_fields_required_for_native(self):
  s=list((R/'skills').glob('*/SKILL.md'));self.assertEqual(len(s),17)
  for p in s:
   t=p.read_text();self.assertIn('## Work to perform',t);self.assertIn('## Completion / stop',t)
   self.assertIn('Bridge applicability',t)
   self.assertNotIn('## Controlling guards',t)
 def test_preserve_legacy_evidence_security_method(self):
  f=R/'shared/skill_execution_contract_v036.md'
  if not f.exists():self.skipTest('retained historical method absent in overlay')
  s=f.read_text();self.assertIn('self-declared',s);self.assertIn('NOT live behavioral tests',s)
 def test_current_host_validation_not_faked(self):
  m=json.loads((R/'manifest.json').read_text());self.assertEqual(m['host_behavioral_certification'],'NOT_RUN')
  self.assertEqual(m['skill_compliance']['runtime_validator'],'NOT_DEPLOYED')
