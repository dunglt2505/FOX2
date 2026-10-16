import copy
import json
import tempfile
import unittest
from pathlib import Path
from shared.core import Hold, TaskStore, assess_drift, digest, preflight, verify_evidence
from shared.native_registry import bind
from shared.runtime import invoke, ROOT


class NativeFixture:
    """Synthetic bytes in the observed native schema, never release authority."""
    authenticated = True
    def __init__(self):
        self.dictionary = {'dictionary_id': 'FOX2_PROJECT_DICTIONARY', 'status': 'RELEASED_EFFECTIVE',
                           'project': {'id': 'FOX2'}, 'current': {'policy': {'path': 'policy.md'}}}
        self.bootstrap = {'commit': 'a'*40, 'dictionary_path': 'dictionary.json', 'manifest_path': 'manifest.json'}
        self.files = {'policy.md': b'fixture policy', 'dictionary.json': json.dumps(self.dictionary).encode()}
        self.rehash()
    def rehash(self):
        self.files['manifest.json'] = json.dumps({'files': [{'path': p, 'sha256': digest(b), 'bytes': len(b)}
                                                  for p,b in self.files.items() if p != 'manifest.json']}).encode()
    def read_file(self, path, commit):
        return self.files[path]


def fixture_authority(*args):
    return {'status': 'VERIFIED_EFFECTIVE', 'evidence': ['SYNTHETIC_TEST_AUTHORITY']}


class CoreTests(unittest.TestCase):
    def setUp(self):
        self.git = NativeFixture()
    def test_native_success(self):
        result = bind(self.git, self.git.bootstrap, 'policy', fixture_authority)
        self.assertEqual(result['sha256'], digest(b'fixture policy'))
    def test_missing_bootstrap(self):
        with self.assertRaises(Hold): bind(self.git, None, 'policy')
    def test_no_authority_from_status(self):
        with self.assertRaises(Hold): bind(self.git, self.git.bootstrap, 'policy')
    def test_hash_mismatch(self):
        self.git.files['policy.md'] = b'altered'
        with self.assertRaises(Hold): bind(self.git, self.git.bootstrap, 'policy', fixture_authority)
    def test_dictionary_hash_mismatch(self):
        self.git.files['dictionary.json'] += b' '
        with self.assertRaises(Hold): bind(self.git, self.git.bootstrap, 'policy', fixture_authority)
    def test_candidate(self):
        self.git.dictionary['current']['policy']['status'] = 'CANDIDATE'
        self.git.files['dictionary.json'] = json.dumps(self.git.dictionary).encode()
        self.git.rehash()
        with self.assertRaises(Hold): bind(self.git, self.git.bootstrap, 'policy', fixture_authority)
    def test_authority_conflict(self):
        with self.assertRaises(Hold) as caught:
            bind(self.git, self.git.bootstrap, 'policy', lambda *a: {'status':'SOURCE_CONFLICT'})
        self.assertEqual(caught.exception.status, 'SOURCE_CONFLICT')
    def test_offline(self):
        def offline(*args): raise OSError('offline')
        self.git.read_file = offline
        with self.assertRaises(Hold) as caught: bind(self.git, self.git.bootstrap, 'policy', fixture_authority)
        self.assertEqual(caught.exception.status, 'UNAVAILABLE')
    def test_unauthenticated(self):
        self.git.authenticated = False
        with self.assertRaises(Hold): bind(self.git, self.git.bootstrap, 'policy', fixture_authority)
    def test_missing_source(self):
        del self.git.files['policy.md']
        with self.assertRaises(Hold): bind(self.git, self.git.bootstrap, 'policy', fixture_authority)
    def test_permissions(self):
        for operation in ['DEV', 'merge', 'LIVE']:
            with self.subTest(operation=operation), self.assertRaises(Hold): preflight(operation, [], {}, [])
    def test_lock_and_no_replay(self):
        with tempfile.TemporaryDirectory() as tmp:
            store = TaskStore(tmp)
            lock = store.start('task', {'policy':'original'})
            with self.assertRaises(Hold): store.start('task', {'policy':'changed'})
            self.assertEqual(store.resume('task'), lock)
    def test_material_drift(self):
        old = {'policy':'old'}
        self.assertEqual(assess_drift(old, {'policy':'old','other':'new'}, ['policy'])['status'], 'RETAIN_LOCK')
        self.assertEqual(assess_drift(old, {'policy':'new'}, ['policy'])['status'], 'IMPACT_ASSESSMENT_REQUIRED')
        self.assertEqual(old, {'policy':'old'})
    def test_evidence_traversal_and_mismatch(self):
        with tempfile.TemporaryDirectory() as tmp:
            Path(tmp, 'e').write_bytes(b'e')
            verify_evidence(tmp, [{'path':'e','sha256':digest(b'e')}])
            for p,h in [('e','0'*64), ('../outside',digest(b'e'))]:
                with self.assertRaises(Hold): verify_evidence(tmp, [{'path':p,'sha256':h}])


class AllSkillContractTests(unittest.TestCase):
    def test_17_positive_and_negative_helpers(self):
        catalog = json.loads((ROOT/'contracts.json').read_text())
        self.assertEqual(len(catalog), 17)
        with tempfile.TemporaryDirectory() as tmp:
            Path(tmp,'receipt').write_bytes(b'observed')
            for skill, contract in catalog.items():
                with self.subTest(skill=skill):
                    request = {'task_id':'fixture','cutoff':'2026-10-16T00:00:00+07:00','state':'ACTIVE',
                               'input':{k:'fixture input' for k in contract['inputs']},
                               'evidence':[{'path':'receipt','sha256':digest(b'observed')}]}
                    bindings = {f:{'status':'VERIFIED_EFFECTIVE'} for f in contract['sources']}
                    self.assertEqual(invoke(skill,request,bindings,[skill],tmp)['status'], 'PREPARED_FOR_HOST_REVIEW')
                    bad = copy.deepcopy(request)
                    del bad['input'][contract['inputs'][0]]
                    with self.assertRaises(Hold): invoke(skill,bad,bindings,[skill],tmp)
                    bad = copy.deepcopy(request); bad['state']='COMPLETED'
                    with self.assertRaises(Hold): invoke(skill,bad,bindings,[skill],tmp)
                    with self.assertRaises(Hold): invoke(skill,request,bindings,[],tmp)


if __name__ == '__main__': unittest.main()
