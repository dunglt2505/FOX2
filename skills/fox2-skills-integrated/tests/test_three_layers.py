import unittest,json,re
from pathlib import Path
R=Path(__file__).resolve().parents[1]
class ThreeLayerArchitecture(unittest.TestCase):
 def setUp(self):
  self.files={p.parent.name:p.read_text(encoding='utf-8') for p in (R/'skills').glob('*/SKILL.md')}
 def test_exact_11_layer_counts(self):
  self.assertEqual(len(self.files),11)
  self.assertEqual(sum('-mgmt-' in k for k in self.files),3)
  self.assertEqual(sum('-method-' in k for k in self.files),5)
  self.assertEqual(sum('-tech-' in k for k in self.files),3)
 def test_one_owner_one_output_each(self):
  for name,txt in self.files.items():
   self.assertTrue(txt.startswith('---\nname: '+name+'\n'))
   for section in ('## Activate when','## Input','## Work to perform','## Output','## Responsibility boundary'):
    self.assertIn(section,txt,name)
   self.assertTrue(300<len(txt)<6500,name)
 def test_no_retired_skill_files(self):
  active=set(self.files)
  old=[x.strip('` ') for x in (R/'SKILL_MIGRATION_v0_5_0.md').read_text().splitlines() if x.startswith('| `')]
  self.assertEqual(len(old),17)
  self.assertTrue(all(not x.split('`')[1] in active for x in old))
 def test_canonical_manifest_identity(self):
  m=json.loads((R/'manifest.json').read_text())
  self.assertEqual(set(m['skills']),set(self.files))
  self.assertEqual(m['skills_count'],11)
  for p in ('plugin.json','.codex-plugin/plugin.json','manifest.json'):
   q=json.loads((R/p).read_text());self.assertEqual(q['version'],'0.5.7');self.assertEqual(q['name'],'fox2-skills-integrated')
 def test_native_agile_is_not_bridge_admission(self):
  s=(R/'shared/operating_rules.md').read_text()
  for term in ('Native reversible DEV','Bridge', 'one logical task', 'no-replay', 'Prompt Builder'):
   self.assertIn(term,s)
