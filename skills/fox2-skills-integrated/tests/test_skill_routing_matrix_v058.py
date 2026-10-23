import unittest
from pathlib import Path
R=Path(__file__).resolve().parents[1]
SKILLS=R/'skills'
class RoutingMatrix(unittest.TestCase):
 def setUp(self):
  self.m=(SKILLS/'fox2-mgmt-delivery'/'SKILL.md').read_text(encoding='utf-8')
  self.names={p.parent.name for p in SKILLS.glob('*/SKILL.md')}
 def test_matrix_routes_all_11_without_new_skill(self):
  self.assertEqual(len(self.names),11)
  self.assertIn('## Skill Routing Matrix',self.m)
  for name in self.names:self.assertIn(f'`{name}`',self.m,name)
 def test_coverage_actual_application_not_fake(self):
  for term in ('REQUIRED','APPLIED','NOT_APPLICABLE','UNAVAILABLE','actually reading/using','next safe action','Re-evaluate lazily'):
   self.assertIn(term,self.m)
 def test_end_to_end_no_micro_wp(self):
  for term in ('Build → Test → Deliver','CHAT acceptance','Master Plan/Board sync','Git remote readback','same logical task','not a 12th Skill'):
   self.assertIn(term,self.m)
 def test_no_reroute_into_bridge_or_auto_approval(self):
  for term in ('consumed Dispatch','technical PASS','WORK audit','Canary','LIVE'):
   self.assertIn(term,self.m)
  pre=(SKILLS/'fox2-tech-route-preflight'/'SKILL.md').read_text()
  self.assertIn('installed Bridge',pre)
 def test_existing_board_contract_kept(self):
  for term in ('READY_FOR_BOARD=YES','OUTCOME_DEFINED','DEPENDENCIES_KNOWN','SOURCE_READY_ENOUGH','ACCEPTANCE_ACTIONABLE','NEXT_SAFE_ACTION_KNOWN','KEEP_IN_MASTER_PLAN','PROMOTE_TO_BACKLOG','PROMOTE_TO_DOING','BLOCKED','SYNCED','NO_MATERIAL_CHANGE'):
   self.assertIn(term,self.m)
 def test_shared_guidance_references_matrix(self):
  s=(R/'shared'/'operating_rules.md').read_text()
  for t in ('Skill Routing Matrix','fox2-mgmt-delivery','REQUIRED/APPLIED/NOT_APPLICABLE/UNAVAILABLE','One Whole-WP'):
   self.assertIn(t,s)
