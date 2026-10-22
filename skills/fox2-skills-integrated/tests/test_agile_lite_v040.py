"""v0.4.0 Agile Lite invariants forward-compatible with v0.4.1 Bridge support."""
import unittest,json
from pathlib import Path
R=Path(__file__).resolve().parents[1]
class AgileLiteRetained(unittest.TestCase):
 def test_17_skills_keep_agile_and_bridge_conditional(self):
  skills=list((R/'skills').glob('*/SKILL.md'));self.assertEqual(len(skills),17)
  for p in skills:
   t=p.read_text();self.assertTrue(t.startswith('---\nname: '+p.parent.name))
   self.assertIn('## Shared operating and Bridge applicability',t)
   self.assertNotIn('## Controlling guards (self-contained',t)
 def test_version_advances_without_identity_change(self):
  for f in ['plugin.json','.codex-plugin/plugin.json','manifest.json']:
   v=json.loads((R/f).read_text());self.assertEqual(v['version'],json.loads((R/'plugin.json').read_text())['version'])
   self.assertEqual(v['name'],'fox2-skills-integrated')
 def test_keep_safety_and_easy_native(self):
  t=(R/'shared/operating_rules.md').read_text()
  for needle in ['one writer','PreExec','no-replay','LIVE','consumed','native development']:
   self.assertIn(needle,t)
