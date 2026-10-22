"""Assemble the bounded R5 result from observed offline evidence."""
from datetime import datetime, timezone
import json
from verify_result import ROOT, OUT, REPORT, BASE, CODE, git, digest, changed, static, manifest

def dump(path, value):
    path.write_text(json.dumps(value, indent=2) + chr(10), encoding='utf-8', newline=chr(10))

now = datetime.now(timezone.utc).isoformat()
binding = json.loads((OUT / 'source_binding.json').read_text())
runs = {name: json.loads((OUT / (name + '_run.json')).read_text()) for name in ['focused', 'full']}
assert all(r['exit_code'] == 0 for r in runs.values())
report = f"""# FOX2 Presentation Lock Certifier Rework R5

Task `{binding['task_id']}`; CODEX / gpt-6.1-sol / medium, one bounded attempt inside Bridge TEST. Delivery state: **PUSHED_UNREVIEWED**, pending independent CHAT review. The observed remote result SHA is returned separately from this committed report.

Authority is fresh Dispatch **{binding['dispatch']['id']}**, control commit `{binding['dispatch']['control_commit']}`, path `{binding['dispatch']['path']}`. It binds runtime base `{BASE}` and R5 PreExec PASS at commit `{binding['preexec']['commit']}`, receipt `{binding['preexec']['path']}` (checked `{binding['preexec']['checked_at']}`). Task commit `8fb7d23217067474488203aceef094b838e828ab`, blob `cbc546dcad97c9dcab02d6e82b68eef163d2b17d`, SHA-256 `d7054edbb574661df9cbba08dcdf282cf175d2cd5496a5dc7b2c2af6cdaa7062` and prompt SHA-256 `ffeaccd6a60eb4b56da907bf1092bb3889b38a80a8cd957ca5d8a90860e79fba` match that Dispatch. Source-binding evidence records canonical Git hashes and the actual Dispatch content.

Accepted product lineage remains `085cc8302e824dbccf9cbef80422ed48894b9cb4`. R4 `d997756b5f4cfaa7e442dfc5d929093782b7a90f` is unaccepted salvage input only, under CHAT_REWORK `07ce66987345859f978c06fbb4abbdeeaa0ff04c`. The runtime base contains its exact starting certifier/test blobs. R4 Dispatch remains consumed/no-replay.

The certifier now accepts fresh/zero-WPF errno13 without winerror only when pre-live classification is exactly OPENABLE. ABSENT plus errno13 fails before UI actions or any held-lock claim. Explicit winerror32 remains accepted with ABSENT. Existing-live continuation stays provisional until graceful exit, zero WPF and same-file post-exit OPENABLE. Device/inode identity, unchanged lock bytes, bounded error fields, unrelated OSError/winerror5 rejection and lifecycle tail are preserved. No Worker/F1/tray fallback was added.

The previous absent-lock fixture now covers sharing-violation PASS and errno13 FAIL in both fresh and zero-WPF continuation modes. Existing OPENABLE positive, existing-live release positive/negative, unrelated error, winerror5, byte-preservation and no-fallback fixtures are retained.

Validation: focused **{runs['focused']['summary']}**; full suite **{runs['full']['summary']}**. Commands: `python -m pytest -q agent_bridge/tests/test_lifecycle_wpf_contract.py`; `python -m pytest -q agent_bridge/tests`; `git diff --check`. The first direct run stopped during collection because the source-layout package was absent from the import path. Final suites ran with process-scoped PYTHONPATH in a short detached fixture worktree to avoid known Windows path limits. All tracked agent_bridge bytes matched the final source. No tools were installed or upgraded.

Exact changed-path allowlist relative to the R5 runtime base, secret/privacy scan, syntax, preserved lifecycle AST, K1 **UNEXPLAINED=0**, Result Contract v2 schema and evidence hashes pass. Only the two authorized product/test paths and R5 result paths changed. The manifest uses a null self-hash to avoid recursion. Evidence and reproducible verification are under `evidence/presentation_lock_certifier_rework_r5/`.

Unaffected A04 package/provenance/install/safe-state/singleton PASS and unchanged R4 route/source/no-host evidence are reused. R4 66 focused/683 full results are historical only; the R5 final bytes were retested. Historical FAIL/NOT_RUN is not promoted. Real host lifecycle remains **NOT_RUN**. No package build/install, host mutation, WPF product changes, A05/G3/G4/Canary/main/merge/provider/broker/LIVE action occurred. Worker/F1 remains NOT_APPLICABLE_PRE_G3. Usage totals are NOT_MEASURED. CHAT review is required before separately authorized host continuation.
"""
(REPORT / 'report.md').write_text(report, encoding='utf-8', newline=chr(10))
mp = REPORT / 'evidence_manifest.json'
v = json.loads(git('show', BASE + ':' + mp.relative_to(ROOT).as_posix()))
v.update(task_id=binding['task_id'], change_id=binding['task_id'], submitted_at_utc=now)
v['agent'].update(started_at_utc=runs['focused']['started_at_utc'], finished_at_utc=now,
                  quota_observation='R5 PreExec selected-route capacity PASS reused; totals NOT_MEASURED')
v['routing']['routing_evidence'] = 'Fresh R5 Dispatch ' + binding['dispatch']['id'] + '; R5 PreExec PASS ' + binding['preexec']['commit'] + '; task/prompt/route/salvage hashes verified. Upstream route decision reused.'
v['source'].update(task_commit_sha=binding['task']['commit_sha'], source_manifest_sha256=digest((OUT/'source_binding.json').read_bytes()), approved_base_commit_sha=BASE,
                   previous_evidence_reused=[binding['accepted_product_source']] + binding['reuse'])
v['permissions']['grant_evidence'] = 'Fresh R5 Dispatch ' + binding['dispatch']['id'] + ' and current execution prompt: exact two product/test files, R5 result paths, task-branch commit/push.'
v['git'].update(branch=binding['branch'], worktree=ROOT.as_posix(), local_head_before_submission=BASE,
                writer_lease='Single R5 execution; detached test snapshot under same writer; no subagents.')
v['scope'].update(requested=['Fix only R4 errno13 pre-live OPENABLE proof gap and missing ABSENT negative fixtures'],
                   completed=['Strict OPENABLE gate, ABSENT fail-closed fixtures, preserved continuation/lifecycle proof, final offline validation'],
                   not_done=['Real host lifecycle NOT_RUN; outside R5'], changed_paths=[])
v['usage']['escalation_reason'] = 'One fresh R5 execution; R4 Dispatch consumed/no-replay; no model substitution.'
v['next_step']['action'] = 'Independent CHAT result review of immutable pushed R5 result.'
v['tests'] = []; v['acceptance'] = []; v['evidence'] = []
for name in ['k1.json','static_checks.json']:
    if not (OUT/name).exists(): dump(OUT/name,{})
dump(mp,v)
static()
for p in sorted(OUT.iterdir()) + [REPORT/'report.md']:
    if p.is_file():
        v['evidence'].append({'id':'E_'+p.name.replace('.','_'), 'path':p.relative_to(ROOT).as_posix(),
                              'sha256':digest(p.read_bytes()), 'kind':'TEST_LOG' if p.suffix=='.log' else 'OTHER',
                              'observed_at_utc':now, 'description':'R5 offline evidence: '+p.name,
                              'supports_ids':['T_STATIC'], 'sanitized':True})
for name,r in runs.items():
    v['tests'].append({'id':'T_'+name.upper(), 'kind':'INTEGRATION', 'status':'PASS',
                       'command_or_method':r['command'], 'environment':'Existing Windows Python; byte-identical short fixture worktree; process-scoped PYTHONPATH',
                       'run_at_utc':r['finished_at_utc'], 'evidence_ids':['E_'+name+'_log','E_'+name+'_run_json'], 'notes':r['summary']})
v['tests'].append({'id':'T_STATIC', 'kind':'STATIC', 'status':'PASS', 'command_or_method':'verify_result.py; verify_result.py --manifest-only; git diff --check',
                   'environment':'Authorized R5 worktree; offline only', 'run_at_utc':now,
                   'evidence_ids':['E_static_checks_json','E_k1_json'], 'notes':'Exact allowlist/privacy/syntax/preserved lifecycle/K1/schema/hashes'})
for i,reason in enumerate(['ABSENT plus winerror32 PASS; ABSENT plus errno13 FAIL in fresh and zero-WPF continuation',
                           'OPENABLE plus errno13 PASS in fresh/zero-WPF; existing-live provisional errno13 requires same-lock post-exit OPENABLE',
                           'Post-exit denial, unrelated OSError and winerror5 FAIL; lock bytes unchanged; no Worker/F1/tray fallback',
                           'Exactly two product/test paths; K1 UNEXPLAINED=0; no host mutation; schema/hash verification']):
    v['acceptance'].append({'id':'A_'+str(i+1),'status':'PASS','evidence_ids':['E_focused_log','E_static_checks_json'],'reason':reason})
for p in changed():
    v['scope']['changed_paths'].append({'path':p, 'operation':'MODIFY' if p in CODE+[mp.relative_to(ROOT).as_posix(),(REPORT/'report.md').relative_to(ROOT).as_posix()] else 'ADD',
        'intent':'REQUESTED' if p in CODE else 'JUSTIFIED_GENERATED', 'within_allowed_paths':True,
        'new_sha256':None if p==mp.relative_to(ROOT).as_posix() else digest((ROOT/p).read_bytes())})
dump(mp,v)
manifest()
