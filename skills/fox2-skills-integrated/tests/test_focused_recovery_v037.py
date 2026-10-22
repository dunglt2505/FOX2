import unittest
from pathlib import Path
R=Path(__file__).resolve().parents[1]
class RecoveryV041(unittest.TestCase):
 def test_no_replay_and_preserve_pass(self):
  t=(R/'skills/fox2-execution-recovery/SKILL.md').read_text()
  self.assertIn('Preserve accepted, unaffected PASS',t)
  self.assertIn('NEEDS_RECONCILIATION',t)
  self.assertIn('do not replay',t)
 def test_rework_remains_same_task(self):
  t=(R/'skills/fox2-result-review/SKILL.md').read_text()
  self.assertIn('SAME logical task',t)
