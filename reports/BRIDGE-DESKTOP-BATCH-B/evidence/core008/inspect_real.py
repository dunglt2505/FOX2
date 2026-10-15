"""Read-only real-root audit, gated on complete disposable success."""
import hashlib
import json
import os
from pathlib import Path
import sqlite3
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[4]
EV = Path(__file__).parent


def save(name, value):
    (EV/name).write_text(json.dumps(value, sort_keys=True, indent=2)+'\n', encoding='utf-8')


if __name__ == '__main__':
    isolated = json.loads((EV/'isolated_summary.json').read_text())
    assert isolated['status'] == 'PASS' and isolated['all_required_isolated_gates_pass']
    real = Path.home()/'AppData/Local/FOX2/AgentBridge'
    links = [str(p.relative_to(real)) for p in real.rglob('*') if p.is_symlink() or p.is_junction()]
    assert not links and not any(p.is_symlink() or p.is_junction() for p in (real, *real.parents))
    def inventory(directory):
        return {p.relative_to(real).as_posix(): hashlib.sha256(p.read_bytes()).hexdigest()
                for p in directory.rglob('*') if p.is_file()}
    versions = []
    for p in (real/'versions').iterdir():
        receipt = p/'receipt.json'
        versions.append(dict(name=p.name, files=inventory(p), receipt=json.loads(receipt.read_text()) if receipt.is_file() else None))
    with sqlite3.connect((real/'data/bridge.db').as_uri()+'?mode=ro', uri=True) as db:
        dispatches = [dict(dispatch_id=i, state=s) for i, s in db.execute('SELECT dispatch_id,state FROM dispatches ORDER BY dispatch_id')]
        worker = json.loads(db.execute('SELECT payload FROM worker_state WHERE id=1').fetchone()[0])
    pointer = json.loads((real/'current.json').read_text()) if (real/'current.json').exists() else None
    manual = json.loads((real/'data/manual_consumption.json').read_text())
    save('real_readonly_inventory.json', dict(root=str(real), all_paths_without_links=True,
         versions=versions, current=pointer, manual_consumption=manual,
         dispatches=dispatches, worker={k:worker.get(k) for k in ('state','paused','setup_complete','start_with_windows')},
         durable={n:inventory(real/n) for n in ('config','data','logs','reports')},
         artifacts={n:hashlib.sha256((real/n).read_bytes()).hexdigest() for n in ('current.json','launch.ps1') if (real/n).is_file()},
         mutation=False, disposable_lifecycle_gate='PASS'))
    command = r'''$ErrorActionPreference='Stop'; $i=[Security.Principal.WindowsIdentity]::GetCurrent();
$name='FOX2Bridge-'+$i.User.Value; $t=Get-ScheduledTask -TaskName $name -ErrorAction SilentlyContinue;
$v=@{sid=$i.User.Value;name=$name;exists=[bool]$t};
if($t){$u=$t.Principal.UserId; if($u -notlike 'S-1-*'){$u=([Security.Principal.NTAccount]::new($u)).Translate([Security.Principal.SecurityIdentifier]).Value};
$v.principal_sid=$u; $v.run_level=[string]$t.Principal.RunLevel; $v.logon_type=[string]$t.Principal.LogonType;
$v.actions=@($t.Actions|ForEach-Object{@{execute=$_.Execute;arguments=$_.Arguments}});$v.instances=[string]$t.Settings.MultipleInstances};
$v.processes=@(Get-CimInstance Win32_Process | Where-Object {($_.ExecutablePath -and $_.ExecutablePath.StartsWith($env:FOX2_CORE008_ROOT,[StringComparison]::OrdinalIgnoreCase)) -or ($_.Name -eq 'pwsh.exe' -and $_.CommandLine -and $_.CommandLine.Contains($env:FOX2_CORE008_ROOT))} | ForEach-Object {@{pid=$_.ProcessId;executable=$_.ExecutablePath}});
$v|ConvertTo-Json -Depth 6 -Compress'''
    r = subprocess.run(['pwsh','-NoProfile','-Command',command], env={**os.environ,'FOX2_CORE008_ROOT':str(real)},
                       capture_output=True,text=True,timeout=30)
    assert r.returncode == 0
    save('real_readonly_task_process.json', json.loads(r.stdout))
    print('REAL_READONLY_INSPECTION_COMPLETE')
