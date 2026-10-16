import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'tools'))
from package_install import install, rollback


class InstallationTests(unittest.TestCase):
    def test_install_invoke_fail_closed_and_rollback(self):
        source = Path(__file__).resolve().parents[1]
        with tempfile.TemporaryDirectory() as tmp:
            destination = Path(tmp,'package')
            receipt = install(source,destination)
            self.assertEqual(len(list((destination/'skills').glob('*/SKILL.md'))),17)
            req = Path(tmp,'request.json')
            req.write_text(json.dumps({'task_id':'smoke','cutoff':'2026-10-16'}))
            process = subprocess.run([sys.executable,'-m','shared.runtime','--skill','fox2-project-health',
                '--request',str(req),'--evidence-root',tmp],cwd=destination,capture_output=True,text=True)
            self.assertEqual(process.returncode,2)
            self.assertEqual(json.loads(process.stdout)['status'],'BLOCKED')
            rollback(receipt)
            self.assertFalse(list(destination.rglob('SKILL.md')))
    def test_preserve_modified_wip(self):
        with tempfile.TemporaryDirectory() as tmp:
            source = Path(tmp,'source'); source.mkdir(); (source/'f').write_bytes(b'original')
            receipt = install(source,Path(tmp,'destination'))
            Path(receipt['root'],'f').write_bytes(b'user modified')
            with self.assertRaises(ValueError): rollback(receipt)
            self.assertEqual(Path(receipt['root'],'f').read_bytes(),b'user modified')
    def test_no_overwrite(self):
        with tempfile.TemporaryDirectory() as tmp:
            with self.assertRaises(ValueError): install(tmp,tmp)
