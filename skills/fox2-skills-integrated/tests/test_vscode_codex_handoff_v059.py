import json,unittest
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
def skill(n): return (ROOT/'skills'/n/'SKILL.md').read_text(encoding='utf-8')
class IDEFirstRouting(unittest.TestCase):
 def test_router_selects_verified_ide_for_interactive_coding(self):
  s=skill('fox2-mgmt-agent-routing')
  self.assertIn('VS Code Codex Extension',s)
  self.assertIn('VSCODE_EXTENSION',s)
  self.assertIn('MANUAL_PROMPT_HANDOFF',s)
  self.assertIn('CLI/Bridge',s)
 def test_prompt_does_not_claim_ide_execution(self):
  s=skill('fox2-method-prompt-builder')
  for word in ('VS Code','Codex Extension','paste-ready','IDE_HANDOFF_PENDING','AGENT_STARTED','worktree','single','remote commit SHA'):
   self.assertIn(word,s)
  self.assertIn('Do **not** claim to open VS Code',s)
  self.assertIn('does not',s.lower())
 def test_git_owner_and_no_replay(self):
  s=skill('fox2-method-prompt-builder')
  for word in ('delivery_owner=AGENT','BRIDGE','GIT_DELIVERY_PENDING','no-replay','consumed Dispatch'):
   self.assertIn(word.lower(),s.lower())
 def test_test_only_and_pwsh_retained(self):
  s=skill('fox2-method-prompt-builder')
  for w in ('TEST_EVIDENCE_ONLY','CODE_CHANGE','& $Git','$LASTEXITCODE','`pwsh` 7','NOT_RUN'):
   self.assertIn(w,s)
 def test_plugin_version_count_and_safe_release(self):
  d=json.loads((ROOT/'manifest.json').read_text())
  self.assertEqual(d['version'],'0.5.9')
  self.assertEqual(len(d['skills']),11)
  self.assertEqual(d['host_behavioral_certification'],'NOT_RUN')
  self.assertEqual(d['ide_handoff_activation'],'NOT_AUTOMATED_WITHOUT_VERIFIED_CONNECTOR')
 def test_ide_context_handoff_and_no_replay(self):
  s=skill('fox2-mgmt-context-handoff')
  self.assertIn('IDE handoff',s)
  self.assertIn('IDE_HANDOFF_PENDING',s)
  self.assertIn('no-replay',s)
 def test_matrix_and_progress_sync_preserved(self):
  s=skill('fox2-mgmt-delivery')
  for term in ('Skill Routing Matrix','Master Plan/Board','fox2-tech-publication-sync'):
   self.assertIn(term,s)
