import unittest
from pathlib import Path
R=Path(__file__).resolve().parents[1]
def load(name):return (R/'skills'/name/'SKILL.md').read_text()
class RoleBoundaryRegressions(unittest.TestCase):
 def test_prompt_builder_does_not_operate_bridge(self):
  s=load('fox2-method-prompt-builder')
  for t in ('Goal','Scope','Context','Execution','Acceptance','Return'):
   self.assertIn(t,s)
  for phrase in ('Never generates/validates Dispatch','publishes to Git','chooses route/delivery owner','runs PreExec'):
   self.assertIn(phrase,s)
 def test_route_selection_does_not_preexec(self):
  s=load('fox2-mgmt-agent-routing');self.assertIn('BEFORE PreExec',s)
  self.assertIn('selection',s);self.assertIn('no formal R0–R7',s)
 def test_technical_contract_not_removed(self):
  s=load('fox2-tech-route-preflight')
  for t in ('installed','Schema','ledger','no-replay','PASS','protected'):
   self.assertIn(t,s)
 def test_result_review_is_chat_responsibility(self):
  s=load('fox2-method-result-acceptance');self.assertIn('PUSHED_UNREVIEWED',s)
  self.assertIn('CHAT_ACCEPTED',s)
 def test_no_replay_on_recovery(self):
  s=load('fox2-tech-execution-recovery')
  self.assertIn('Never replay',s);self.assertIn('SAME logical task',s)
