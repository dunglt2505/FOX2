import unittest,json,hashlib
from pathlib import Path
R=Path(__file__).resolve().parents[1]
class PackageTests(unittest.TestCase):
 def test_overlay_digest_inventory(self):
  m=json.loads((R/'manifest.json').read_text()); idx=json.loads((R/m['current_file_hashes']).read_text())
  self.assertEqual(idx['version'],'0.5.5');self.assertEqual(idx['inventory'],'CHANGED_OVERLAY_FILES_ONLY')
  for rel,item in idx['files'].items():
   b=(R/rel).read_bytes();self.assertEqual(len(b),item['bytes'],rel)
   self.assertEqual(hashlib.sha256(b).hexdigest(),item['sha256'],rel)
 def test_source_claims_do_not_overstate_runtime(self):
  m=json.loads((R/'manifest.json').read_text())
  self.assertEqual(m['host_behavioral_certification'],'NOT_RUN')
  self.assertEqual(m['plugin_rollout'],'GUIDANCE_ONLY_NO_BRIDGE_RUNTIME_OR_TASK_REBIND')
  self.assertTrue(m['no_replay'])
