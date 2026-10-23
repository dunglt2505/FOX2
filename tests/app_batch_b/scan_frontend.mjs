// Bounded static credential scan; never prints matched values.
// Complements API redaction tests, not a claim to detect every possible secret.
import assert from 'node:assert/strict';
import { readdirSync, readFileSync } from 'node:fs';
import { fileURLToPath } from 'node:url';
import path from 'node:path';

const root = fileURLToPath(new URL('../../frontend/', import.meta.url));
const patterns = [
  ['private-key', /-----BEGIN (?:RSA |EC |OPENSSH )?PRIVATE KEY-----/],
  ['aws-access-key', /\bAKIA[A-Z0-9]{16}\b/],
  ['bearer-literal', /\bBearer [A-Za-z0-9._~-]{20,}/],
  ['credential-assignment', /(?:api[_-]?key|access[_-]?token|client[_-]?secret)\s*[:=]\s*["'`][A-Za-z0-9._~/-]{12,}["'`]/i],
  ['test-secret-in-bundle', /SECRET_TOKEN_DO_NOT_SHOW|TEST_SENTINEL_SECRET/]
];
function files(directory) {
  return readdirSync(directory, { withFileTypes: true }).flatMap(entry =>
    entry.isDirectory() ? files(path.join(directory, entry.name)) : [path.join(directory, entry.name)]);
}
const targets = [...files(path.join(root, 'src')), ...files(path.join(root, 'dist')),
  path.join(root, 'vite.config.ts'), path.join(root, 'index.html')];
const findings = [];
for (const target of targets) {
  const source = readFileSync(target, 'utf8');
  for (const [kind, pattern] of patterns) {
    if (pattern.test(source)) findings.push({ file: path.relative(root, target), kind });
  }
}
console.log(JSON.stringify({ result: findings.length ? 'FAIL' : 'PASS',
  scope: 'frontend source/config and complete dist including sourcemap',
  files: targets.length, patterns: patterns.length, findings }, null, 2));
assert.equal(findings.length, 0, 'Potential credential literal found; inspect privately');
