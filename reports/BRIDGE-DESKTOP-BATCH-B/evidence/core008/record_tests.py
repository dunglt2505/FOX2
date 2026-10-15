"""Record one focused and one full invocation; sanitize fixture URL names only."""
import hashlib
import json
from pathlib import Path
import re
import xml.etree.ElementTree as ET

EV = Path(__file__).parent
results = {}
redactions = []
for name in ('focused', 'full'):
    p = EV/(name+'.xml')
    original = p.read_bytes()
    root = ET.fromstring(original)
    suite = root.find('testsuite')
    assert suite is not None
    assert all(int(suite.attrib[k]) == 0 for k in ('failures', 'errors', 'skipped'))
    results[name+'_tests'] = int(suite.attrib['tests'])
    results[name+'_exit'] = 0
    results[name+'_seconds'] = float(suite.attrib['time'])
    changed = 0
    for case in root.iter('testcase'):
        value = case.get('name', '')
        clean = re.sub(r'https?://[^\s\]]+@[^\s\]]+', '[REDACTED_CREDENTIAL_URL_FIXTURE]', value)
        if clean != value:
            case.set('name', clean)
            changed += 1
    if changed:
        ET.ElementTree(root).write(p, encoding='utf-8', xml_declaration=True)
    redactions.append(dict(file=p.name, testcase_names_redacted=changed,
        original_sha256=hashlib.sha256(original).hexdigest(),
        sanitized_sha256=hashlib.sha256(p.read_bytes()).hexdigest(), counts_and_outcomes_unchanged=True))
results['full_invocations'] = 1
results['focused_invocations'] = 1
(EV/'tests.json').write_text(json.dumps(results, indent=2)+'\n', encoding='utf-8')
(EV/'junit_redaction.json').write_text(json.dumps(redactions, indent=2)+'\n', encoding='utf-8')
print(json.dumps(results))
