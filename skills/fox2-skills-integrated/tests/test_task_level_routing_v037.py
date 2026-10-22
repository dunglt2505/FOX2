import unittest
from pathlib import Path
R=Path(__file__).resolve().parents[1]
class RoutingV041(unittest.TestCase):
 def test_select_before_preexec_only_if_bridge(self):
  s=(R/'skills/fox2-agent-route-runtime/SKILL.md').read_text()
  self.assertIn('before freezing Route',s);self.assertIn('PreExec checks compatibility',s)
  self.assertIn('no separate R0–R7 ceremony',s)
 def test_pinned_model_policy_controls(self):
  s=(R/'skills/fox2-agent-route-runtime/SKILL.md').read_text()
  for x in ['PINNED','CURRENT_CONFIG','PINNED_PREFERRED','low|medium|high','CODEX','COPILOT']:
   self.assertIn(x,s)
 def test_no_replay_proof(self):
  s=(R/'shared/operating_rules.md').read_text();self.assertIn('consumed',s)
