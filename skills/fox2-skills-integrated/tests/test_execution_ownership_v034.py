import unittest
from pathlib import Path
R=Path(__file__).resolve().parents[1]
class ExecutionOwnershipV041(unittest.TestCase):
 def test_chat_end_to_end(self):
  t=(R/'shared/operating_rules.md').read_text();self.assertIn('CHAT independently accepts',t)
  for p in (R/'skills').glob('*/SKILL.md'):
   self.assertIn('CHAT owns the end-to-end result',p.read_text())
 def test_no_automatic_work_handoff(self):
  s=(R/'skills/fox2-agent-route-runtime/SKILL.md').read_text()
  self.assertIn('WORK only for truly independent',s)
