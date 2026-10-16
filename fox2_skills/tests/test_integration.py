import unittest, pathlib, sys, re
ROOT=pathlib.Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'shared'))
from legacy_git_resolver import GitHub, bind_effective, SourceError
class SkillIntegration(unittest.TestCase):
 def test_all_17(self):
  files=list((ROOT/'skills').glob('*/SKILL.md'))
  self.assertEqual(len(files),17)
  for f in files:
   s=f.read_text()
   self.assertIn('shared/native_registry.py',s)
   self.assertIn('Before **every new task',s)
   self.assertIn('SOURCE_UNVERIFIED',s)
   self.assertIn('source lock',s)
   self.assertNotRegex(s,r'(?i)(?:policy|routing|dictionary|protocol)\s*(?:v|version)\s*\d+\.\d+')
 def test_general_certification(self):
  s=(ROOT/'skills/fox2-feature-certification/SKILL.md').read_text()
  self.assertIn('not Bridge only',s)
 def test_missing_registry_fails_closed(self):
  g=GitHub('dunglt2505/FOX2',transport=lambda path: {'sha':'a'*40} if path.startswith('commits/') else {'type':'file','encoding':'base64','content':'e30='})
  with self.assertRaises(SourceError):bind_effective(g,'trusted','registry.json','policy')
if __name__=='__main__': unittest.main()
