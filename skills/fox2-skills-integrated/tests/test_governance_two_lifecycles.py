import unittest
from pathlib import Path
R=Path(__file__).resolve().parents[1]
class GovernanceTwoLifecyclesV041(unittest.TestCase):
 def test_human_vs_machine_source(self):
  s=(R/'skills/fox2-source-resolver/SKILL.md').read_text()
  self.assertIn('HUMAN_POLICY_EFFECTIVE',s);self.assertIn('MACHINE_ADOPTED',s)
 def test_do_not_publish_without_real_receipts(self):
  s=(R/'shared/operating_rules.md').read_text();self.assertIn('MUST NOT be published',s)
 def test_no_extra_approval_layer(self):
  s=(R/'shared/operating_rules.md').read_text();self.assertIn('No bureaucracy for native development',s)
