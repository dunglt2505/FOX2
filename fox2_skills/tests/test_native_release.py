"""Regression coverage for native byte handling, never authority certification."""
import json
import subprocess
import unittest
from shared.core import Hold, digest
from shared.native_registry import bind
from test_core import NativeFixture, fixture_authority


class NativeReleaseRegressionTests(unittest.TestCase):
    def test_distinct_manifest_and_source_commits(self):
        fixture = NativeFixture()
        source = 'b' * 40
        manifest = json.loads(fixture.files['manifest.json'])
        manifest['source_set_head'] = source
        manifest_bytes = json.dumps(manifest).encode()
        reads = []
        def read(path, commit):
            reads.append((path, commit))
            if path == 'manifest.json':
                self.assertEqual(commit, fixture.bootstrap['commit'])
                return manifest_bytes
            self.assertEqual(commit, source)
            return fixture.files[path]
        fixture.read_file = read
        result = bind(fixture, fixture.bootstrap, 'policy', fixture_authority)
        self.assertEqual(result['commit'], source)
        self.assertEqual(result['dictionary_commit'], source)
        self.assertEqual(result['manifest_commit'], fixture.bootstrap['commit'])
        self.assertEqual(reads.count(('policy.md', source)), 1)

    def test_receipt_uses_verified_read_only(self):
        fixture = NativeFixture()
        original = fixture.read_file
        reads = []
        def read(path, commit):
            reads.append(path)
            if path == 'policy.md' and reads.count(path) > 1:
                return b'unverified later read'
            return original(path, commit)
        fixture.read_file = read
        result = bind(fixture, fixture.bootstrap, 'policy', fixture_authority)
        self.assertEqual(result['sha256'], digest(b'fixture policy'))
        self.assertEqual(reads.count('policy.md'), 1)

    def test_git_process_failures_are_typed_holds(self):
        for error in [subprocess.CalledProcessError(128, ['git', 'show']),
                      subprocess.TimeoutExpired(['git', 'show'], 20)]:
            fixture = NativeFixture()
            def read(*args):
                raise error
            fixture.read_file = read
            with self.subTest(error=type(error).__name__), self.assertRaises(Hold) as caught:
                bind(fixture, fixture.bootstrap, 'policy', fixture_authority)
            self.assertEqual(caught.exception.status, 'UNAVAILABLE')

    def test_duplicate_manifest_paths_conflict(self):
        fixture = NativeFixture()
        manifest = json.loads(fixture.files['manifest.json'])
        manifest['files'].append(manifest['files'][0])
        fixture.files['manifest.json'] = json.dumps(manifest).encode()
        with self.assertRaises(Hold) as caught:
            bind(fixture, fixture.bootstrap, 'policy', fixture_authority)
        self.assertEqual(caught.exception.status, 'SOURCE_CONFLICT')

    def test_invalid_source_set_head_holds(self):
        for source in ['main', None, 'x' * 40]:
            fixture = NativeFixture()
            manifest = json.loads(fixture.files['manifest.json'])
            manifest['source_set_head'] = source
            fixture.files['manifest.json'] = json.dumps(manifest).encode()
            with self.subTest(source=source), self.assertRaises(Hold) as caught:
                bind(fixture, fixture.bootstrap, 'policy', fixture_authority)
            self.assertEqual(caught.exception.status, 'UNVERIFIED')

    def test_source_pointer_does_not_supply_authority(self):
        fixture = NativeFixture()
        manifest = json.loads(fixture.files['manifest.json'])
        manifest['source_set_head'] = 'b' * 40
        fixture.files['manifest.json'] = json.dumps(manifest).encode()
        with self.assertRaises(Hold) as caught:
            bind(fixture, fixture.bootstrap, 'policy')
        self.assertEqual(caught.exception.status, 'UNVERIFIED')
