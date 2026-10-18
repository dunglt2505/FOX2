"""Read-only Windows filesystem notifications for the real UI save."""
import ctypes
from ctypes import wintypes
from datetime import datetime, timezone
import json
import os
from pathlib import Path
import struct

out = Path(__file__).resolve().parent
vault = Path(os.environ['LOCALAPPDATA'])/'FOX2/BridgeDesktop/Artifacts'
k = ctypes.WinDLL('kernel32', use_last_error=True)
k.CreateFileW.argtypes = [wintypes.LPCWSTR, wintypes.DWORD, wintypes.DWORD, ctypes.c_void_p, wintypes.DWORD, wintypes.DWORD, wintypes.HANDLE]
k.CreateFileW.restype = wintypes.HANDLE
k.ReadDirectoryChangesW.argtypes = [wintypes.HANDLE, ctypes.c_void_p, wintypes.DWORD, wintypes.BOOL, wintypes.DWORD, ctypes.POINTER(wintypes.DWORD), ctypes.c_void_p, ctypes.c_void_p]
k.ReadDirectoryChangesW.restype = wintypes.BOOL
handle = k.CreateFileW(str(vault), 1, 7, None, 3, 0x02000000, None)
if handle == wintypes.HANDLE(-1).value:
    raise ctypes.WinError(ctypes.get_last_error())
actions = {1:'ADDED', 2:'REMOVED', 3:'MODIFIED', 4:'RENAMED_OLD_NAME', 5:'RENAMED_NEW_NAME'}
events = []
start = datetime.now(timezone.utc).isoformat()
(out/'observer_ready.json').write_text(json.dumps(dict(started_utc=start,index_file_id_before=(vault/'index.json').stat().st_ino))+'\n')
print('OBSERVER_READY', flush=True)
while True:
    buffer = ctypes.create_string_buffer(16384)
    returned = wintypes.DWORD()
    if not k.ReadDirectoryChangesW(handle, buffer, len(buffer), False, 0x11, ctypes.byref(returned), None, None):
        raise ctypes.WinError(ctypes.get_last_error())
    offset = 0
    while offset < returned.value:
        following, action, length = struct.unpack_from('<III', buffer, offset)
        name = buffer.raw[offset+12:offset+12+length].decode('utf-16-le')
        events.append(dict(observed_utc=datetime.now(timezone.utc).isoformat(), action=actions.get(action, str(action)), name=name))
        if not following:
            break
        offset += following
    (out/'atomic_index_events.json').write_text(json.dumps(dict(started_utc=start, events=events), indent=2)+'\n')
    if any(x['action']=='RENAMED_NEW_NAME' and x['name']=='index.json' for x in events):
        print('INDEX_ATOMIC_RENAME_OBSERVED', flush=True)
        break
k.CloseHandle(handle)
