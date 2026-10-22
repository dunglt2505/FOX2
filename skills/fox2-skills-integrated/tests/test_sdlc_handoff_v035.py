import unittest
from pathlib import Path
R=Path(__file__).resolve().parents[1]
class HandoffV041(unittest.TestCase):
 def test_native_is_not_bridge(self):
  t=(R/'skills/fox2-agent-prompt-builder/SKILL.md').read_text()
  self.assertIn('No separate Git-prompt/Dispatch/PreExec ceremony',t)
  self.assertIn('Bridge handoff package',t)
 def test_result_return_is_not_new_task(self):
  t=(R/'skills/fox2-thread-handoff/SKILL.md').read_text()
  self.assertIn('RESULT_RETURN',t);self.assertIn('REWORK',t)
 def test_manual_shell_requires_real_host(self):
  t=(R/'skills/fox2-agent-prompt-builder/SKILL.md').read_text()
  self.assertIn('pwsh',t);self.assertIn('HOST_NOT_VERIFIED',t)
