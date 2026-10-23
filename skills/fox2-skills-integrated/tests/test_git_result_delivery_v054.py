import json, unittest
from pathlib import Path
R = Path(__file__).resolve().parents[1]
def read(name):
    return (R/name).read_text(encoding="utf-8")
def verdict(route, owner, remote_sha, allowed):
    if route=="BRIDGE" and owner not in ("AGENT","BRIDGE"):
        return "BLOCKED_OWNER_UNKNOWN"
    if not allowed:
        return "GIT_DELIVERY_PENDING"
    if not remote_sha or len(remote_sha)!=40 or any(ch not in "0123456789abcdef" for ch in remote_sha):
        return "GIT_DELIVERY_PENDING"
    return "READY_FOR_CHAT_REVIEW"
class GitResultDelivery(unittest.TestCase):
    def test_prompt_contains_git_output_contract(self):
        s=read('skills/fox2-method-prompt-builder/SKILL.md')
        for phrase in ('authorized result branch','remote result commit SHA','GIT_DELIVERY_PENDING','delivery_owner=AGENT','delivery_owner=BRIDGE'):
            self.assertIn(phrase,s)
    def test_native_prompt_not_forced_git_prompt(self):
        s=read('shared/operating_rules.md')
        self.assertIn('Git-published **prompt**',s)
        self.assertIn('This exemption does not waive Git result delivery',s)
    def test_publication_owned_by_transport(self):
        s=read('skills/fox2-method-prompt-builder/SKILL.md')
        self.assertIn('never publishes or verifies commits itself',s)
        self.assertIn('Never generates/validates Dispatch',s)
        p=read('skills/fox2-tech-publication-sync/SKILL.md')
        self.assertIn('authorized CHAT publisher',p)
        self.assertIn('For Agent results: verify branch, remote commit SHA',p)
    def test_chat_requires_remote_sha(self):
        s=read('skills/fox2-method-result-acceptance/SKILL.md')
        self.assertIn('ANY delegated Agent assignment',s)
        self.assertIn('GIT_DELIVERY_PENDING',s)
        self.assertIn('verified remote Git result branch',s)
    def test_existing_logical_task_and_no_replay(self):
        self.assertIn('SAME logical task',read('skills/fox2-method-result-acceptance/SKILL.md'))
        self.assertIn('no-replay',read('shared/operating_rules.md'))
    def test_native_agent_pushed(self):
        self.assertEqual(verdict('NATIVE','AGENT','b'*40,True),'READY_FOR_CHAT_REVIEW')
    def test_bridge_agent_push(self):
        self.assertEqual(verdict('BRIDGE','AGENT','b'*40,True),'READY_FOR_CHAT_REVIEW')
    def test_bridge_bridge_push(self):
        self.assertEqual(verdict('BRIDGE','BRIDGE','b'*40,True),'READY_FOR_CHAT_REVIEW')
    def test_bridge_owner_missing(self):
        self.assertEqual(verdict('BRIDGE',None,'b'*40,True),'BLOCKED_OWNER_UNKNOWN')
    def test_local_only_never_done(self):
        self.assertEqual(verdict('NATIVE','AGENT',None,True),'GIT_DELIVERY_PENDING')
    def test_no_git_permission_not_done(self):
        self.assertEqual(verdict('NATIVE','AGENT','b'*40,False),'GIT_DELIVERY_PENDING')
    def test_manifest_lifecycle(self):
        m=json.loads(read('manifest.json'))
        self.assertEqual(m['skills_count'],11)
        self.assertEqual(m['result_delivery_contract'],'AGENT_OR_BRIDGE_GIT_PUSH_REMOTE_SHA_VERIFIED_BEFORE_CHAT_DONE')
        self.assertEqual(m['host_behavioral_certification'],'NOT_RUN')
