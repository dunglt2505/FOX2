"""Synthetic authority fixtures exercise decisions, never certify real FOX2."""
from dataclasses import replace
import json
import unittest
from shared.core import digest
from shared.release_chain import AuthoritySnapshot, ApprovedRelease, Ownership, ReleaseChainVerifier


class ReleaseChainTests(unittest.TestCase):
    def setUp(self):
        self.bootstrap={'commit':'a'*40,'manifest_path':'manifest.json','dictionary_path':'dictionary.json'}
        self.dictionary=json.dumps({'dictionary_id':'FOX2_PROJECT_DICTIONARY','status':'RELEASED_EFFECTIVE',
            'project':{'repository':'dunglt2505/FOX2'},'current':{'policy':{'path':'policy.md'}}}).encode()
        self.manifest=json.dumps({'source_set_head':'b'*40}).encode()
        self.release=ApprovedRelease('fixture-release','RELEASED_EFFECTIVE','fixture-scope',
            'a'*40,'manifest.json',digest(self.manifest),'b'*40,digest(self.dictionary),
            (Ownership('policy','policy.md','fixture-policy-owner',('SYNTHETIC_OWNER_APPROVAL',)),),
            ('SYNTHETIC_RELEASE_APPROVAL',))
        self.snapshot=AuthoritySnapshot('dunglt2505/FOX2','fixture-scope','fixture-cutoff',
            ('SYNTHETIC_ROOT_APPROVAL',),('SYNTHETIC_COMPLETE_INVENTORY',),
            frozenset(['a'*40,'b'*40]),(self.release,))
    def check(self,snapshot=None,provider=None):
        verifier=ReleaseChainVerifier('fixture-scope','fixture-cutoff',provider or (lambda *a:snapshot or self.snapshot))
        return verifier(self.bootstrap,self.dictionary,self.manifest,'policy')
    def test_valid_fixture_chain(self):
        self.assertEqual(self.check()['status'],'VERIFIED_EFFECTIVE')
    def test_conditional_baseline_never_certifies(self):
        verifier=ReleaseChainVerifier('fixture-scope','fixture-cutoff')
        self.assertEqual(verifier(self.bootstrap,self.dictionary,self.manifest,'policy')['status'],'AUTHORITY_UNVERIFIED')
    def test_serialized_claim_is_not_authority_snapshot(self):
        self.assertEqual(self.check(provider=lambda *a:{'status':'VERIFIED_EFFECTIVE'})['status'],'AUTHORITY_UNVERIFIED')
    def test_incomplete_competing_release_inventory(self):
        self.assertEqual(self.check(replace(self.snapshot,complete_inventory_evidence=()))['status'],'AUTHORITY_UNVERIFIED')
    def test_missing_root_and_wrong_cutoff_scope(self):
        for snapshot in [replace(self.snapshot,root_evidence=()),replace(self.snapshot,cutoff='stale'),replace(self.snapshot,scope='OTHER_PROJECT')]:
            with self.subTest(snapshot=snapshot):self.assertEqual(self.check(snapshot)['status'],'AUTHORITY_UNVERIFIED')
    def test_unapproved_immutable_ref(self):
        self.assertEqual(self.check(replace(self.snapshot,allowed_commits=frozenset(['a'*40])))['status'],'AUTHORITY_UNVERIFIED')
    def test_competing_effective_release_conflicts(self):
        other=replace(self.release,identity='competing')
        self.assertEqual(self.check(replace(self.snapshot,releases=(self.release,other)))['status'],'SOURCE_CONFLICT')
    def test_higher_candidate_cannot_supersede_effective(self):
        candidate=replace(self.release,identity='candidate',status='CANDIDATE',supersedes=(self.release.identity,))
        self.assertEqual(self.check(replace(self.snapshot,releases=(self.release,candidate)))['status'],'VERIFIED_EFFECTIVE')
    def test_valid_successor_and_stale_anchor(self):
        old=replace(self.release,identity='older',manifest_commit='c'*40)
        current=replace(self.release,supersedes=('older',))
        snapshot=replace(self.snapshot,releases=(old,current))
        self.assertEqual(self.check(snapshot)['status'],'VERIFIED_EFFECTIVE')
        successor=replace(self.release,identity='successor',manifest_commit='d'*40,supersedes=(self.release.identity,))
        self.assertEqual(self.check(replace(self.snapshot,releases=(self.release,successor)))['status'],'AUTHORITY_UNVERIFIED')
    def test_missing_predecessor_and_cycle_hold(self):
        for records in [(replace(self.release,supersedes=('missing',)),),
                        (replace(self.release,supersedes=(self.release.identity,)),)]:
            with self.subTest(records=records):self.assertEqual(self.check(replace(self.snapshot,releases=records))['status'],'AUTHORITY_UNVERIFIED')
    def test_semantic_owner_conflict_and_missing_approval(self):
        for owner,status in [(Ownership('policy','different.md','owner',('fixture',)),'SOURCE_CONFLICT'),
                             (Ownership('policy','policy.md','',()),'AUTHORITY_UNVERIFIED')]:
            record=replace(self.release,ownership=(owner,))
            self.assertEqual(self.check(replace(self.snapshot,releases=(record,)))['status'],status)
    def test_changed_dictionary_and_manifest_fail(self):
        for record in [replace(self.release,dictionary_sha256='0'*64),replace(self.release,manifest_sha256='0'*64)]:
            self.assertEqual(self.check(replace(self.snapshot,releases=(record,)))['status'],'AUTHORITY_UNVERIFIED')
    def test_authority_provider_is_refreshed_every_call(self):
        calls=[]
        def provider(*args):
            calls.append(args)
            return self.snapshot if len(calls)==1 else None
        verifier=ReleaseChainVerifier('fixture-scope','fixture-cutoff',provider)
        self.assertEqual(verifier(self.bootstrap,self.dictionary,self.manifest,'policy')['status'],'VERIFIED_EFFECTIVE')
        self.assertEqual(verifier(self.bootstrap,self.dictionary,self.manifest,'policy')['status'],'AUTHORITY_UNVERIFIED')
        self.assertEqual(len(calls),2)
