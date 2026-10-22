import unittest,json
from pathlib import Path
R=Path(__file__).resolve().parents[1]
class TestOwnerDirectFirstV042(unittest.TestCase):
 def test_chat_owns_full_task_without_default_delegation(self):
  skills=list((R/'skills').glob('*/SKILL.md'));self.assertEqual(len(skills),17)
  for p in skills:
   t=p.read_text();self.assertIn('CHAT owns the end-to-end result',t)
   self.assertIn('Bridge applicability',t)
 def test_no_preexec_for_native_and_real_controls_for_bridge(self):
  t=(R/'shared/operating_rules.md').read_text()
  for x in ['native development','PreExec','no-replay','one writer','NOT_RUN']:
   self.assertIn(x,t)
 def test_provenance_and_authority_distinct(self):
  t=(R/'skills/fox2-source-resolver/SKILL.md').read_text()
  for x in ['SOURCE_BYTES_VERIFIED','AUTHORITY_UNVERIFIED','MACHINE_ADOPTED','HUMAN_POLICY_EFFECTIVE']:
   self.assertIn(x,t)
 def test_current_semver_is_not_locked_in_test(self):
  z=json.loads((R/'plugin.json').read_text());self.assertEqual(z['name'],'fox2-skills-integrated')
  self.assertTrue(z['version'].startswith('0.4.'))
