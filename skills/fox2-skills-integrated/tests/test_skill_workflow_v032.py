import json,unittest
from pathlib import Path
R=Path(__file__).resolve().parents[1]
class WorkflowsV041(unittest.TestCase):
 def test_both_native_and_bridge_supported(self):
  p=(R/'skills/fox2-agent-prompt-builder/SKILL.md').read_text()
  self.assertIn('Native independent CODEX/Copilot',p);self.assertIn('execution_path=BRIDGE',p)
 def test_source_versions_no_blanket_rebind(self):
  s=(R/'skills/fox2-source-resolver/SKILL.md').read_text();self.assertIn('Policy 1.8.9',s)
  self.assertIn('Policy 2.1.0',s)
 def test_manifest_identity(self):
  m=json.loads((R/'manifest.json').read_text());self.assertEqual(m['version'],json.loads((R/'plugin.json').read_text())['version'])
  self.assertEqual(m['current_file_hashes'],'RELEASE_FILE_HASHES_'+json.loads((R/'plugin.json').read_text())['version'].replace('.','_')+'.json')
