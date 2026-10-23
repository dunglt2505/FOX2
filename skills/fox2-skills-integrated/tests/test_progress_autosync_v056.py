import unittest
from pathlib import Path
R=Path(__file__).resolve().parents[1]
class ProgressSync(unittest.TestCase):
 def test_management_scope_and_events(self):
  s=(R/'skills/fox2-mgmt-delivery/SKILL.md').read_text()
  for term in ['scheduled Watch','Master Plan','Board','SYNCED','SYNC_PENDING/BLOCKED','NO_MATERIAL_CHANGE','PUSHED_UNREVIEWED','fox2-tech-publication-sync']:
   self.assertIn(term.lower(),s.lower(),term)
 def test_handoff_and_actual_publisher(self):
  a=(R/'skills/fox2-method-result-acceptance/SKILL.md').read_text()
  b=(R/'skills/fox2-tech-publication-sync/SKILL.md').read_text()
  self.assertIn('Progress handoff',a)
  self.assertIn('Project progress documents',b)
  self.assertIn('remote readback',b)
 def test_safety_no_new_skill(self):
  s=(R/'skills/fox2-mgmt-delivery/SKILL.md').read_text()
  self.assertIn('not a daemon',s)
  self.assertIn('no implicit main merge',s)
  self.assertIn('Preserve immutable historical copies',s)
