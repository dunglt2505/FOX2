import json,unittest
from pathlib import Path
R=Path(__file__).resolve().parents[1]
class SkillCorpus(unittest.TestCase):
 def test_17_domain_skills_and_shared_rules(self):
  p=list((R/'skills').glob('*/SKILL.md'));self.assertEqual(len(p),17)
  for v in p:
   t=v.read_text()
   self.assertTrue(t.startswith('---\nname: '+v.parent.name))
   for h in ['## Activate when','## Work to perform','## Completion / stop','## Shared operating and Bridge applicability']:
    self.assertIn(h,t,v)
   self.assertNotIn('## Controlling guards (self-contained',t)
  m=json.loads((R/'manifest.json').read_text());self.assertEqual(set(m['skills']),{v.parent.name for v in p})
 def test_preserved_original_git_resolver(self):
  f=R/'shared/git_resolver.py'
  if not f.exists():self.skipTest('Old resolver overlay retained in installed release')
  s=f.read_text();self.assertIn('def bind_effective(',s)
  self.assertIn('SOURCE_BYTES_VERIFIED_AUTHORITY_PENDING',s)
