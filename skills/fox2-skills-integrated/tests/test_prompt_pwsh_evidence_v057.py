import unittest
from pathlib import Path
R=Path(__file__).resolve().parents[1]
load=lambda name:(R/'skills'/name/'SKILL.md').read_text(encoding='utf-8')
class PromptPowershellAndEvidence(unittest.TestCase):
 def test_host_version_and_git_executable(self):
  s=load('fox2-method-prompt-builder')
  for term in ['PowerShell 5.1','`pwsh` 7','Get-Command git -CommandType Application','& $Git','`$LASTEXITCODE`','GV','NOT_RUN']:
   self.assertIn(term,s)
 def test_no_forced_product_code_diff_in_evidence_only(self):
  s=load('fox2-method-prompt-builder')
  for term in ['CODE_CHANGE','TEST_EVIDENCE_ONLY','UNRESOLVED','no product code diff is required','actual required tests','verified remote SHA','GIT_DELIVERY_PENDING','NOT_RUN']:
   self.assertIn(term,s)
 def test_acceptance_must_be_executed(self):
  s=load('fox2-method-result-acceptance')
  for term in ['No-code result acceptance','actual executed test/check command','exit status','source/worktree identity','NOT_RUN','remote Git evidence']:
   self.assertIn(term,s)
 def test_host_gate_and_publisher_boundary(self):
  a=load('fox2-tech-route-preflight');b=load('fox2-tech-publication-sync')
  self.assertIn('PowerShell/Git host gate',a)
  self.assertIn('`& $Git`',a)
  self.assertIn('Evidence-only Git delivery',b)
  self.assertIn('Bridge publication remains governed',b)
 def test_existing_boundary_and_11_skills(self):
  self.assertEqual(len(list((R/'skills').glob('*/SKILL.md'))),11)
  s=load('fox2-method-prompt-builder')
  for term in ['Never generates/validates Dispatch','never publishes','TEST_EVIDENCE_ONLY']:
   self.assertIn(term.lower(),s.lower())
