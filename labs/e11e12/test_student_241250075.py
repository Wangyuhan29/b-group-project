"""241250075: personal adapter and contract tests; expected outcomes are fixed before running."""
import hashlib
import json
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch
import pipeline
import server
from lab import commit, fixture, run, scan
from lab import patch as make_patch

C0 = 'e3a1eda0965e545d96467d275bccaf78c890fcac'
C1 = 'f863c2deff1bd95e56f1578b872ae6aa26e3bfc8'
# Upstream README and #include lines: main.c reads util.h and token.h through parser.h, parser.c reads
# config.h from C1 on and token.h through parser.h, and util.o never reads the declared legacy.h.
C0_FINDINGS = [('MISSING', 'main.o', 'include/token.h'), ('MISSING', 'main.o', 'include/util.h'),
               ('MISSING', 'parser.o', 'include/token.h'), ('REDUNDANT', 'util.o', 'include/legacy.h')]
C1_ADDED = ('MISSING', 'parser.o', 'include/config.h')
DECLARED = {'main.o': ['include/config.h', 'include/parser.h', 'src/main.c'],
            'parser.o': ['include/parser.h', 'src/parser.c'],
            'token.o': ['include/token.h', 'src/token.c'],
            'util.o': ['include/legacy.h', 'include/util.h', 'src/util.c']}


def findings(report):
    return sorted((f['type'], f['target'], f['dependency']) for f in report['findings'])


class PersonalTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)

    def test_e11_two_missing_dependencies_stay_in_the_declared_style(self):
        expected = {'macro': ['-DEPS = main.c unused.h', '+DEPS = main.c unused.h config.h extra.h'],
                    'mixed': ['-main.o: main.c $(HEADERS)', '+main.o: main.c $(HEADERS) config.h extra.h']}
        for style, changed in expected.items():
            with self.subTest(style=style):
                project = Path(self.temp.name) / style
                fixture(project, style)
                (project / 'main.c').write_text('#include "extra.h"\n' + (project / 'main.c').read_text())
                commit(project, 'C1 add project include')
                before = (project / 'Makefile').read_bytes()
                diff, plan = make_patch(project, scan(project))
                self.assertEqual(plan, [{'target': 'main.o', 'dependency': 'config.h', 'style': style},
                                        {'target': 'main.o', 'dependency': 'extra.h', 'style': style}])
                lines = [line for line in diff.splitlines()
                         if line.startswith(('+', '-')) and not line.startswith(('+++', '---'))]
                self.assertEqual(lines, changed)
                self.assertEqual((project / 'Makefile').read_bytes(), before)
                self.assertEqual(run(['git', 'status', '--porcelain'], project), '')

    def test_e12_minicalc_adapter_reports_the_upstream_defects(self):
        from minicalc import scan as minicalc_scan
        project = Path(self.temp.name) / 'minicalc'
        run(['git', 'clone', '-q', str(pipeline.ROOT / 'fixtures/minicalc/history.bundle'), str(project)],
            self.temp.name)
        run(['git', 'checkout', '-q', '--detach', C0], project)
        c0 = minicalc_scan(project)
        run(['git', 'checkout', '-q', '--detach', C1], project)
        c1 = minicalc_scan(project, c0)
        self.assertEqual((c0['commit'], findings(c0)), (C0, sorted(C0_FINDINGS)))
        self.assertEqual((c1['commit'], findings(c1)), (C1, sorted(C0_FINDINGS + [C1_ADDED])))
        self.assertEqual((c1['added'], c1['resolved']), ([list(C1_ADDED)], []))
        self.assertEqual((c0['declared'], c1['declared']), (DECLARED, DECLARED))
        # Nothing is reused across the two commits: parser.c and config.h both changed.
        self.assertEqual((sorted(c0['refreshed']), sorted(c1['refreshed'])), (sorted(DECLARED), sorted(DECLARED)))
        self.assertEqual((c0['reused'], c1['reused']), ([], []))

    def test_e12_idempotency_keys_survive_restart(self):
        request = {'mode': 'e12', 'repo': str(pipeline.ROOT / 'data/p'), 'base': 'a', 'target': 'b'}
        with tempfile.TemporaryDirectory() as folder, patch.object(server.Store, 'work'):
            first = server.Store(Path(folder))
            try:
                job = first.submit(request, 'key-1')['job_id']
                first.submit(request, 'key-2')
            finally:
                first.pool.shutdown()
            second = server.Store(Path(folder))
            try:
                # After a restart a replayed key still returns its original job and a changed input still conflicts.
                self.assertEqual(second.submit(request, 'key-1')['job_id'], job)
                with self.assertRaisesRegex(ValueError, 'IDEMPOTENCY_CONFLICT'):
                    second.submit(dict(request, target='c'), 'key-1')
                self.assertEqual(sorted(second.keys), ['key-1', 'key-2'])
                self.assertNotEqual(second.submit(request, 'key-3')['job_id'], job)
            finally:
                second.pool.shutdown()

    def test_e12_failed_job_keeps_job_and_trace_ids_with_matching_artifact_hash(self):
        with tempfile.TemporaryDirectory() as folder:
            store = server.Store(Path(folder) / 'jobs')
            try:
                request = {'mode': 'e12', 'repo': str(pipeline.ROOT / 'data/absent'),
                           'base': 'a' * 40, 'target': 'b' * 40}
                with patch.object(store.pool, 'submit'):
                    job = store.submit(request, 'key')['job_id']
                store.work(job, request)
                state = store.jobs[job]
                evidence = Path(folder) / 'jobs' / job / 'evidence'
                result = json.loads((evidence / 'result.json').read_text())
                self.assertEqual((state['status'], state['error']['code']), ('FAILED', 'INVALID_REQUEST'))
                self.assertEqual((result['job_id'], result['trace_id']), (state['job_id'], state['trace_id']))
                stored = (evidence / 'request.json').read_bytes()
                self.assertEqual(json.loads(stored), request)
                self.assertEqual(result['artifacts'], [{'uri': 'artifact://' + job + '/request.json',
                                                        'sha256': hashlib.sha256(stored).hexdigest(),
                                                        'bytes': len(stored)}])
            finally:
                store.pool.shutdown()


if __name__ == '__main__':
    unittest.main()
