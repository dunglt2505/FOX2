import tempfile
import unittest
from pathlib import Path
from shared.core import Hold, digest
from shared.operations import file_plan, sync_file, acceptance_review, traceability, health, recover, triage, research


class WorkflowTests(unittest.TestCase):
    def test_actual_sync_save_readback_and_no_overwrite(self):
        with tempfile.TemporaryDirectory() as tmp:
            a,b = Path(tmp,'source'),Path(tmp,'dest'); a.write_bytes(b'bytes')
            with self.assertRaises(Hold): sync_file(a,b,tmp)
            first = sync_file(a,b,tmp,True)
            self.assertEqual(sync_file(a,b,tmp,True),first)
            self.assertEqual(first['release_status'],'NOT_RELEASED')
            a.write_bytes(b'new')
            with self.assertRaises(Hold): sync_file(a,b,tmp,True)
            self.assertEqual(b.read_bytes(),b'bytes')
    def test_sync_conflict_and_idempotency(self):
        with tempfile.TemporaryDirectory() as tmp:
            a,b = Path(tmp,'a'),Path(tmp,'b'); a.write_bytes(b'a')
            self.assertEqual(file_plan(a,b)['status'], 'COPY_REQUIRED')
            b.write_bytes(b'a')
            self.assertEqual(file_plan(a,b)['status'], 'IDENTICAL')
            b.write_bytes(b'b')
            self.assertEqual(file_plan(a,b)['status'], 'CONFLICT')
            self.assertEqual(b.read_bytes(),b'b')
    def test_review_non_bridge_feature(self):
        with tempfile.TemporaryDirectory() as tmp:
            Path(tmp,'test.log').write_bytes(b'observed test')
            evidence = {'chart-render': {'outcome':'PASS','observed_by':'fixture-observer',
                        'receipts':[{'path':'test.log','sha256':digest(b'observed test')}]}}
            self.assertEqual(acceptance_review(tmp,['chart-render','missing'],evidence),
                             {'chart-render':'EVIDENCE_PRESENT','missing':'UNVERIFIED'})
            evidence['chart-render']['receipts'][0]['sha256']='0'*64
            self.assertEqual(acceptance_review(tmp,['chart-render'],evidence)['chart-render'],'UNVERIFIED')
    def test_traceability(self):
        self.assertEqual(traceability(['r1','r2'],{'r1':['test']})['gaps'],['r2'])
    def test_health_does_not_infer_from_commits(self):
        self.assertEqual(health(['feature'],{'commits':100,'tests':'PASS'},'cutoff')['acceptance']['feature'],'UNKNOWN')
    def test_recovery(self):
        self.assertEqual(recover(['a','b'],['a'],True)['retry'],['b'])
        with self.assertRaises(Hold): recover(['a'],[],False)
    def test_triage(self):
        self.assertEqual(triage([{'root_cause':'x'},{'root_cause':'x'},{'root_cause':'y'}])['priority'],['x','y'])
    def test_research(self):
        self.assertEqual(research('method','data',None,'limits')['evidence_tier'],'INCOMPLETE')
        self.assertFalse(research('method','data','backtest','limits')['deployment_authorized'])
