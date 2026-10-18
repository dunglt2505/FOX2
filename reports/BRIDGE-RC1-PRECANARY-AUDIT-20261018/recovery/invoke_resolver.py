import importlib.util,sys,json,pathlib,hashlib,datetime,termios
attr=termios.tcgetattr(sys.stdin);attr[3] &= ~termios.ECHO;termios.tcsetattr(sys.stdin,termios.TCSANOW,attr)
spec=importlib.util.spec_from_file_location('fox2_cloud_shared_resolver',pathlib.Path('recovery/plugin/shared/git_resolver.py'))
module=importlib.util.module_from_spec(spec);sys.modules[spec.name]=module;spec.loader.exec_module(module)
cache={};requests=[]
def transport(path):
 if path not in cache:
  print('FOX2_REQUEST '+json.dumps({'path':path}),flush=True)
  line=sys.stdin.readline()
  if not line:raise RuntimeError('Authenticated connector transport closed')
  response=json.loads(pathlib.Path(line.strip()).read_text())
  if response.get('transport_error'):raise RuntimeError(response['transport_error'])
  cache[path]=response
  requests.append({'path':path,'received_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'response_sha256_canonical_json':hashlib.sha256(json.dumps(response,sort_keys=True,separators=(',',':')).encode()).hexdigest()})
 return cache[path]
remote=module.GitHub('dunglt2505/FOX2',transport=transport)
registry_ref='b27f1085ee13d8dce56fd2735e100ea1616e6e23';rp='docs/governance/FOX2_RC1_TRUST_BUNDLE_20261017/REGISTRY.json'
registry=json.loads(remote.read_file(rp,remote.commit(registry_ref)))
results={}
for family in registry['families']:
 try:results[family]={'status':'VERIFIED_EFFECTIVE','binding':module.bind_effective(remote,registry_ref,rp,family).__dict__}
 except Exception as e:results[family]={'status':'UNVERIFIED','reason':str(e)}
approval=registry['owner_release_approval'];approval_bytes=remote.read_file(approval['path'],remote.commit(approval['ref']));owner=json.loads(approval_bytes)
owner_checks={'externally_nominated_by_current_owner_request':True,'registry_wp_scope':registry['registry_scope']=='WP_ONLY_TRUST_BINDING','owner_approval_sha256':hashlib.sha256(approval_bytes).hexdigest()=='6185200cc2585e9a6c3fda620ed4c12841f5863b9462ba77d874253ace13de53','owner_wp_matches':owner['whole_wp']=='FOX2-BRIDGE-RC1-TO-INTERNAL-READY','owner_status_approved':owner['status']=='APPROVED','owner_source_freeze_matches':owner['immutable_source_commit']=='c916de489e0aee51d6fe30c5b8b4cd9f4cd9a359','no_protected_authority':not any(registry['protected_authority'].values()),'no_global_promotion':owner['scope']['global_semantic_promotion'] is False}
result={'status':'PASS' if all(x['status']=='VERIFIED_EFFECTIVE' for x in results.values()) and all(owner_checks.values()) else 'BLOCKED','resolver_sha256':hashlib.sha256(pathlib.Path('recovery/plugin/shared/git_resolver.py').read_bytes()).hexdigest(),'python':sys.version.split()[0],'transport':'Authenticated GitHub connector via resolver supported Callable; each uncached get served live, no substitute resolver','local_token':'NOT_PRESENT_NOT_REQUIRED_FOR_CONNECTOR_TRANSPORT','registry':registry_ref,'registry_path':rp,'families':results,'caller_owner_trust_checks':owner_checks,'requests':requests,'completed_utc':datetime.datetime.now(datetime.timezone.utc).isoformat()}
pathlib.Path('recovery/resolver_execution.json').write_text(json.dumps(result,indent=2)+'\n')
print('FOX2_DONE '+json.dumps({'status':result['status'],'families':len(results),'live_requests':len(requests)}),flush=True)
raise SystemExit(0 if result['status']=='PASS' else 2)
