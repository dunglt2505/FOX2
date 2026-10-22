import hashlib,json,unittest
from pathlib import Path
R=Path(__file__).resolve().parents[1]
class TestReleaseV041(unittest.TestCase):
 def test_identity_and_version(self):
  meta=[json.loads((R/x).read_text()) for x in ['plugin.json','.codex-plugin/plugin.json','manifest.json']]
  self.assertEqual({x['version'] for x in meta},{json.loads((R/'plugin.json').read_text())['version']})
  self.assertEqual({x['name'] for x in meta},{'fox2-skills-integrated'})
  self.assertEqual(meta[2]['skills_count'],17)
 def test_overlay_hashes_not_historical_files(self):
  m=json.loads((R/'manifest.json').read_text());f=json.loads((R/m['current_file_hashes']).read_text())
  self.assertEqual(f['version'],json.loads((R/'plugin.json').read_text())['version'])
  self.assertEqual(f['inventory'],'CHANGED_OVERLAY_FILES_ONLY')
  for rel,v in f['files'].items():
   b=(R/rel).read_bytes();self.assertEqual(v['bytes'],len(b),rel)
   self.assertEqual(v['sha256'],hashlib.sha256(b).hexdigest(),rel)
 def test_historical_machine_not_attested(self):
  m=json.loads((R/'manifest.json').read_text());self.assertEqual(m['host_behavioral_certification'],'NOT_RUN')
  self.assertTrue(m['no_replay'])
