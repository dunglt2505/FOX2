"""Negative/positive Bridge handoff contract fixtures; no live host/Dispatch mutation."""
import copy, hashlib, unittest

REQUIRED={'schema_version','project','dispatch_id','dispatch_action','wp_id','target_agent','workspace_id','dictionary','policy','task','prompt','source','routing','execution_path','delivery_owner','permissions','decision_receipt','runtime_contract','required_tests','created_by','created_at','max_runs'}
PASS_FIELDS=('policy_check','task_state_check','source_binding_check','routing_r0_r7','assignment_check')
PROTECTED=('pr_create','merge_allowed','production_provider','broker_write','live')
HASH40='a'*40
HASH64='b'*64

def validated_source():
    return {'version':'1.2','git_path':'docs/governance/FOX2_PROJECT_DICTIONARY_v1.json','git_commit_sha':HASH40,'sha256':HASH64}

def fixture():
    return {'schema_version':'3.0','project':'FOX2','dispatch_id':'FOX2-DISPATCH-V041-FIXTURE','dispatch_action':'EXECUTE_LOCAL_AGENT','wp_id':'FOX2-V041','target_agent':'CODEX','workspace_id':'fixture-workspace','dictionary':validated_source(),'policy':{'version':'1.8.9','sha256':HASH64,'git_path':'docs/governance/FOX2_POLICY_V1.8.9.md','git_commit_sha':HASH40},'task':{'path':'docs/agent_handoff/FOX2-V041/task.md','commit_sha':HASH40,'sha256':HASH64},'prompt':{'path':'docs/agent_handoff/FOX2-V041/prompt.md','git_commit':HASH40,'git_blob_sha1':HASH40,'sha256':HASH64},'source':{'commit_sha':HASH40,'git_source_ready':'YES'},'routing':{'model_policy':'PINNED','model':'fixture-model','permission_profile':'FULL_ACCESS','reasoning_effort':'medium'},'execution_path':'BRIDGE','delivery_owner':'BRIDGE','permissions':{'code_allowed':True,'git_code_push':True,'git_report_write':True,'git_report_push':True,**{k:False for k in PROTECTED}},'decision_receipt':{**{k:'PASS' for k in PASS_FIELDS},'material_capability_check':'PASS','execution_authorized':'YES','code_allowed':'YES','dev_grant_ref':'actual-fixture-only'},'runtime_contract':{'repo':'dunglt2505/FOX2','branch':'work/FOX2-V041-FIXTURE','worktree':'C:/FOX2/fixture','base_sha':HASH40,'allowed_code_paths':['agent_bridge/tests/*'],'allowed_report_paths':['reports/FOX2-V041/*'],'required_capabilities':['CODEX'],'stop_conditions':['NO_LIVE']},'required_tests':['pytest -q'],'created_by':'CHAT','created_at':'2026-10-22T10:00:00Z','max_runs':1}

def assess(candidate, *, host_observed=False, consumed=False, actual_git_bytes=False, machine_policy='1.8.9', native=False):
    if native:return 'NATIVE_NO_DISPATCH'
    if consumed:return 'STOP_CONSUMED_NO_REPLAY'
    if not REQUIRED.issubset(candidate):return 'HOLD_REQUIRED_FIELD'
    if candidate['schema_version']!='3.0' or candidate['execution_path']!='BRIDGE' or candidate['max_runs']!=1:return 'HOLD_SCHEMA_ROUTE'
    if candidate['dispatch_action']!='EXECUTE_LOCAL_AGENT' or candidate['created_by']!='CHAT':return 'HOLD_SCHEMA_ROUTE'
    if candidate['policy'].get('version')!=machine_policy:return 'HOLD_MACHINE_POLICY_MISMATCH'
    if candidate['source'].get('git_source_ready')!='YES' or not actual_git_bytes:return 'HOLD_UNVERIFIED_GIT_BYTES'
    if not all(len(candidate['prompt'].get(k,''))==v for k,v in [('git_commit',40),('git_blob_sha1',40),('sha256',64)]):return 'HOLD_IMMUTABLE_PROMPT'
    if candidate['routing'].get('permission_profile')!='FULL_ACCESS':return 'HOLD_ROUTE_MISMATCH'
    if candidate['target_agent'] not in ('CODEX','COPILOT'):return 'HOLD_ROUTE_MISMATCH'
    if candidate['target_agent']=='COPILOT' and candidate['routing'].get('reasoning_effort'):return 'HOLD_ROUTE_MISMATCH'
    if candidate['delivery_owner'] not in ('AGENT','BRIDGE'):return 'HOLD_DELIVERY_OWNER'
    if any(candidate['permissions'].get(k) is not False for k in PROTECTED):return 'HOLD_PROTECTED_AUTHORITY'
    rc=candidate['decision_receipt']
    if any(rc.get(k)!='PASS' for k in PASS_FIELDS):return 'HOLD_MISSING_RECEIPT'
    if rc.get('material_capability_check') not in ('PASS','PASS_NON_MATERIAL_DEVIATION'):return 'HOLD_MISSING_RECEIPT'
    if rc.get('execution_authorized')!='YES' or rc.get('code_allowed')!='YES' or not rc.get('dev_grant_ref'):return 'HOLD_MISSING_RECEIPT'
    if not host_observed:return 'HOLD_HOST_UNVERIFIED'
    return 'FIXTURE_READY_NOT_LIVE'

class BridgeFixtureV041(unittest.TestCase):
    def test_good_codex_and_copilot_route_variants(self):
        p=fixture();self.assertEqual(assess(p,host_observed=True,actual_git_bytes=True),'FIXTURE_READY_NOT_LIVE')
        p['target_agent']='COPILOT';p['routing']={'model_policy':'NATIVE_AUTO','model':'auto','permission_profile':'FULL_ACCESS'}
        self.assertEqual(assess(p,host_observed=True,actual_git_bytes=True),'FIXTURE_READY_NOT_LIVE')
    def test_native_task_bypasses_bridge_specific_fields(self):
        self.assertEqual(assess({'goal':'fix bug'},native=True),'NATIVE_NO_DISPATCH')
    def test_holds_without_material_host_receipt(self):
        self.assertEqual(assess(fixture(),host_observed=False,actual_git_bytes=True),'HOLD_HOST_UNVERIFIED')
    def test_holds_without_git_readback(self):
        self.assertEqual(assess(fixture(),host_observed=True,actual_git_bytes=False),'HOLD_UNVERIFIED_GIT_BYTES')
    def test_holds_consumed(self):
        self.assertEqual(assess(fixture(),host_observed=True,actual_git_bytes=True,consumed=True),'STOP_CONSUMED_NO_REPLAY')
    def test_holds_wrong_machine_policy_no_version_cascade(self):
        x=fixture();x['policy']['version']='2.1.0'
        self.assertEqual(assess(x,host_observed=True,actual_git_bytes=True),'HOLD_MACHINE_POLICY_MISMATCH')
    def test_holds_missing_dispatch_field(self):
        x=fixture();x.pop('decision_receipt')
        self.assertEqual(assess(x,host_observed=True,actual_git_bytes=True),'HOLD_REQUIRED_FIELD')
    def test_holds_invalid_hash(self):
        x=fixture();x['prompt']['sha256']='unknown'
        self.assertEqual(assess(x,host_observed=True,actual_git_bytes=True),'HOLD_IMMUTABLE_PROMPT')
    def test_holds_unknown_model_effort_on_copilot(self):
        x=fixture();x['target_agent']='COPILOT'
        self.assertEqual(assess(x,host_observed=True,actual_git_bytes=True),'HOLD_ROUTE_MISMATCH')
    def test_holds_changed_permission(self):
        x=fixture();x['routing']['permission_profile']='READ_ONLY'
        self.assertEqual(assess(x,host_observed=True,actual_git_bytes=True),'HOLD_ROUTE_MISMATCH')
    def test_holds_protected_pr_merge_live(self):
        for flag in PROTECTED:
            with self.subTest(flag=flag):
                x=fixture();x['permissions'][flag]=True
                self.assertEqual(assess(x,host_observed=True,actual_git_bytes=True),'HOLD_PROTECTED_AUTHORITY')
    def test_holds_no_receipt_in_each_material_gate(self):
        for flag in PASS_FIELDS:
            with self.subTest(flag=flag):
                x=fixture();x['decision_receipt'][flag]='NOT_RUN'
                self.assertEqual(assess(x,host_observed=True,actual_git_bytes=True),'HOLD_MISSING_RECEIPT')
    def test_holds_no_dev_grant(self):
        x=fixture();x['decision_receipt']['dev_grant_ref']=''
        self.assertEqual(assess(x,host_observed=True,actual_git_bytes=True),'HOLD_MISSING_RECEIPT')
    def test_holds_wrong_delivery_owner(self):
        x=fixture();x['delivery_owner']='BOTH'
        self.assertEqual(assess(x,host_observed=True,actual_git_bytes=True),'HOLD_DELIVERY_OWNER')
    def test_holds_max_runs_more_than_one(self):
        x=fixture();x['max_runs']=2
        self.assertEqual(assess(x,host_observed=True,actual_git_bytes=True),'HOLD_SCHEMA_ROUTE')
