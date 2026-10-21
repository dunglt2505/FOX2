"""Bounded command identities/statuses from this Agent's own session only.

Never publishes conversation text, raw tool output, auth/config content or
other sessions. Long inline commands use a digest and short first-line label.
"""
from datetime import datetime, UTC
import hashlib
import json
from pathlib import Path
import re
import sys

OUT = Path(__file__).resolve().parent


def objects(value):
    if isinstance(value, dict):
        if 'chunk_id' in value and ('exit_code' in value or 'session_id' in value):
            yield value
        else:
            for item in value.values(): yield from objects(item)
    elif isinstance(value, list):
        for item in value: yield from objects(item)
    elif isinstance(value, str):
        try:
            yield from objects(json.loads(value))
        except (ValueError, RecursionError):
            # The tool renderer may prefix warnings or truncate a large read.
            # Execution metadata precedes the raw output, so recover only that
            # metadata; never copy a truncated content/credential-bearing tail.
            for line in value.splitlines():
                positions = list(re.finditer(r'\{"(?:chunk_id|i)":', line))
                for position in positions:
                    try:
                        parsed, _ = json.JSONDecoder().raw_decode(line[position.start():])
                        yield from objects(parsed)
                    except ValueError:
                        prefix = line[position.start():].split('"output":', 1)[0]
                        code = re.search(r'"exit_code":\s*(-?\d+)', prefix)
                        if code:
                            yield {'chunk_id': 'truncated-render', 'exit_code': int(code[1])}


def main():
    calls, pending, commands = {}, {}, []
    for line in Path(sys.argv[1]).read_text(encoding='utf-8').splitlines():
        entry = json.loads(line); event = entry.get('payload', {})
        if event.get('type') == 'custom_tool_call' and event.get('name') == 'exec':
            script = event['input']
            found = []
            for match in re.finditer(r'tools\.exec_command\(\{\s*cmd:\s*("(?:[^"\\]|\\.)*")', script):
                command = json.loads(match[1])
                row = {'id': len(commands) + 1, 'at': entry['timestamp'],
                    'identity': command if len(command) <= 1800 else command.splitlines()[0][:120],
                    'command_sha256': hashlib.sha256(command.encode()).hexdigest(),
                    'identity_truncated': len(command) > 1800, 'exit_code': None, 'summary': 'PENDING'}
                commands.append(row); found.append(row)
            polls = [int(m) for m in re.findall(r'tools\.write_stdin\(\{session_id:(\d+)', script)]
            calls[event['call_id']] = (found, polls)
        elif event.get('type') == 'custom_tool_call_output' and event.get('call_id') in calls:
            found, polls = calls[event['call_id']]
            results = list(objects(event['output']))
            targets = found or [pending[s] for s in polls if s in pending]
            for row, result in zip(targets, results):
                if result.get('session_id'):
                    pending[result['session_id']] = row
                row['exit_code'] = result.get('exit_code')
                row['summary'] = ('RUNNING_AT_CUTOFF' if row['exit_code'] is None else
                                  'COMPLETED' if row['exit_code'] == 0 else 'NONZERO_RECORDED')
    receipts = [json.loads(p.read_text()) for p in OUT.glob('*-[0-9][0-9].json')]
    for row in commands:
        match = re.fullmatch(r'python .*?/run_checks.py ([a-z-]+)', row['identity'])
        if match:
            candidates = [r for r in receipts if r['id'] == match[1]]
            if candidates:
                receipt = min(candidates, key=lambda r: abs((datetime.fromisoformat(r['started_at']) -
                    datetime.fromisoformat(row['at'])).total_seconds()))
                if abs((datetime.fromisoformat(receipt['started_at']) - datetime.fromisoformat(row['at'])).total_seconds()) < 15:
                    row['exit_code'] = receipt['exit_code']
                    row['summary'] = 'COMPLETED' if row['exit_code'] == 0 else 'NONZERO_RECORDED'
    result = {'cutoff': datetime.now(UTC).isoformat(), 'commands': commands,
              'note': 'Engineering test details are in dedicated bounded receipts. Final commit/push readback follows this inventory cutoff and is observed in the external delivery pointer.'}
    (OUT / 'command_inventory.json').write_text(json.dumps(result, sort_keys=True, indent=2) + '\n',
                                               encoding='utf-8', newline='\n')
    print(json.dumps({'bounded_command_identities': len(commands),
        'completed_with_exit_code': sum(c['exit_code'] is not None for c in commands)}))


if __name__ == '__main__':
    main()
