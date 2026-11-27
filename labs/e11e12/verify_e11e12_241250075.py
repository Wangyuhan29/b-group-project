"""241250075: re-check the personal pipeline runs: commits, job/trace identity and artifact hashes."""
import argparse
import hashlib
import json
import re
from pathlib import Path
from lab import run
from pipeline import ROOT, save

# Directory below work/, request mode, repaired-rule style, output the DRAFT-verified program must print
# (DRAFT runs before the fixed report is checked, so the stale runs print 1 as well).
RUNS = [
    ('e11-final', 'e11-b', 'direct', '1'), ('e11-macro', 'e11-b', 'macro', '1'), ('e11-mixed', 'e11-b', 'mixed', '1'),
    ('e12-final', 'e12', 'direct', '1'), ('e12-real', 'e12', 'minicalc', '7'),
    ('e11-stale-zero', 'stale', 'direct', '1'), ('e11-stale-old', 'stale', 'mixed', '1'),
    ('e11-stale-inner', 'stale', 'macro', '1'),
]
STAGES = {'e11-b': ['draft', 'fixed-md', 'repair', 'recheck'],
          'e12': ['draft', 'full-check', 'incremental-check', 'repair', 'recheck'], 'stale': ['draft']}
# Changed patch lines, edit style, dependencies in plan order, targets in plan order.
REPAIR = {
    'direct': (['-main.o: main.c unused.h', '+main.o: main.c unused.h config.h extra.h'], 'direct',
               ['config.h', 'extra.h'], ['main.o', 'main.o']),
    'macro': (['-DEPS = main.c unused.h', '+DEPS = main.c unused.h config.h extra.h'], 'macro',
              ['config.h', 'extra.h'], ['main.o', 'main.o']),
    'mixed': (['-main.o: main.c $(HEADERS)', '+main.o: main.c $(HEADERS) config.h extra.h'], 'mixed',
              ['config.h', 'extra.h'], ['main.o', 'main.o']),
    'minicalc': (['-main.o: src/main.c include/config.h include/parser.h',
                  '+main.o: src/main.c include/config.h include/parser.h include/token.h include/util.h',
                  '-parser.o: src/parser.c include/parser.h',
                  '+parser.o: src/parser.c include/parser.h include/config.h include/token.h'], 'direct',
                 ['include/token.h', 'include/util.h', 'include/config.h', 'include/token.h'],
                 ['main.o', 'main.o', 'parser.o', 'parser.o']),
}
# The declaration styles share one two-file project; Minicalc is the upstream four-target project.
PROJECT = {'direct': 'classroom', 'macro': 'classroom', 'mixed': 'classroom', 'minicalc': 'minicalc'}
# (type, target, dependency) at the base commit, added at the target, and left after the repair.
BASELINE = {'classroom': [('MISSING', 'main.o', 'config.h'), ('REDUNDANT', 'main.o', 'unused.h')],
            'minicalc': [('MISSING', 'main.o', 'include/token.h'), ('MISSING', 'main.o', 'include/util.h'),
                         ('MISSING', 'parser.o', 'include/token.h'), ('REDUNDANT', 'util.o', 'include/legacy.h')]}
ADDED = {'classroom': [['MISSING', 'main.o', 'extra.h']], 'minicalc': [['MISSING', 'parser.o', 'include/config.h']]}
FINAL = {'classroom': [('REDUNDANT', 'main.o', 'unused.h')], 'minicalc': [('REDUNDANT', 'util.o', 'include/legacy.h')]}
ACCEPTED = {'accepted': True, 'checks': {'patch_applies': True, 'build': True, 'test': True,
                                         'header_change': True, 'no_missing': True},
            'error': None, 'source_unchanged': False, 'rollback': False}
HTTP = {'health': 200, 'submit': 202, 'status': 200, 'artifacts': 200, 'download': 200, 'replay': 202, 'conflict': 409,
        'restart-status': 200, 'restart-replay': 202, 'restart-conflict': 409}


def load(path):
    return json.loads(Path(path).read_text(encoding='utf-8'))


def digest(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def triples(findings):
    return sorted(tuple(f[k] for k in ('type', 'target', 'dependency')) for f in findings)


def changed_lines(text):
    return [line for line in text.splitlines()
            if line.startswith(('+', '-')) and not line.startswith(('+++', '---'))]


class Check:
    """Collects expected/actual pairs; nothing is taken from the run's own verdicts."""

    def __init__(self, folder):
        self.root = Path(folder)
        self.checks = []
        self.notes = {}

    def expect(self, name, expected, actual):
        self.checks.append({'check': name, 'expected': expected, 'actual': actual, 'passed': expected == actual})

    @property
    def passed(self):
        return all(c['passed'] for c in self.checks)

    def local(self, uri):
        return self.root / uri.split('/', 3)[3]

    def git(self, folder, *args):
        return run(['git', *args], str(self.root / folder))

    def hashes(self, label, entries):
        bad = []
        for entry in entries:
            path = self.local(entry['uri'])
            if not path.is_file():
                bad.append(entry['uri'] + ': missing')
            elif digest(path) != entry['sha256']:
                bad.append(entry['uri'] + ': sha256')
            elif path.stat().st_size != entry['bytes']:
                bad.append(entry['uri'] + ': bytes')
        self.expect(label + ': artifacts whose file, sha256 or size differs', [], bad)

    def run(self, kind, style, output):
        request, result = load(self.root / 'request.json'), load(self.root / 'result.json')
        job, trace, project = result['job_id'], result['trace_id'], PROJECT[style]
        self.expect('schema', 'e11e12-1', result['schema_version'])
        self.expect('job_id and trace_id shape', True, bool(re.fullmatch(r'job-[0-9a-f]{32}', job)
                                                               and re.fullmatch(r'trace-[0-9a-f]{32}', trace)))
        for role in ('base', 'target'):
            resolved = run(['git', 'rev-parse', '--verify', request[role] + '^{commit}'], request['repo']).strip()
            self.expect(role + ' commit resolved in the sample and recorded by the run', [request[role]] * 2,
                        [resolved, result[role + '_commit']])
            self.expect(role + ' snapshot is checked out at that commit', request[role],
                        self.git(role + '-project', 'rev-parse', 'HEAD').strip())
        self.expect('status', 'FAILED' if kind == 'stale' else 'SUCCEEDED', result['status'])
        self.expect('stage order', STAGES[kind], [s['name'] for s in result['stages']])
        for stage in result['stages']:
            name = stage['name']
            envelope = load(self.local(stage['artifact']['uri']))
            self.expect(name + ' envelope identity',
                        {'schema_version': 'e11e12-1', 'job_id': job, 'trace_id': trace, 'kind': name,
                         'commit': request['base'] if name == 'full-check' else request['target'],
                         'status': 'SUCCEEDED'},
                        {key: envelope[key] for key in ('schema_version', 'job_id', 'trace_id', 'kind', 'commit',
                                                         'status')})
            self.expect(name + ' is listed by the hash of its own file',
                        ['artifact://%s/%s.json' % (job, name), digest(self.root / (name + '.json'))],
                        [stage['artifact']['uri'], stage['artifact']['sha256']])
            self.hashes(name, envelope['artifacts'])
        self.hashes('result', result['artifacts'])
        self.expect('artifact list names every file of the run except result.json, and nothing else',
                    sorted(p.relative_to(self.root).as_posix() for p in self.root.rglob('*') if p.is_file()
                           and '.git' not in p.parts and not p.is_symlink() and p != self.root / 'result.json'),
                    sorted(self.local(a['uri']).relative_to(self.root).as_posix() for a in result['artifacts']))

        draft = load(self.root / 'draft.json')['data']
        first, second = draft['attempts']
        self.expect('DRAFT first build fails only because make is missing', [True, 'MISSING_MAKE'],
                    [first['build_exit_code'] != 0, first['failure_class']])
        self.expect('DRAFT second build exit code', 0, second['build_exit_code'])
        self.expect('DRAFT hashes the submitted candidate', digest(request['candidate']), draft['candidate_sha256'])
        program = draft['verification']
        self.expect('DRAFT runs the image built in the second attempt', True, second['image_id'] in program['command'])
        self.expect('DRAFT program: exit code, match flag, printed output', [0, True, output],
                    [program['exit_code'], program['output_matches'], program['actual_output'].rstrip('\r\n')])

        if kind == 'stale':
            self.expect('error code', 'STALE_REPORT', result['error']['code'])
            self.expect('no repair attempted: clean target, no repair stage, no patch', ['', False, False],
                        [self.git('target-project', 'status', '--porcelain'), (self.root / 'repair.json').exists(),
                         (self.root / 'candidate.patch').exists()])
            self.notes = {'job_id': job, 'trace_id': trace, 'message': result['error']['message']}
            return self
        self.expect('no error', None, result.get('error'))

        source = 'fixed-md' if kind == 'e11-b' else 'incremental-check'
        repair = load(self.root / 'repair.json')['data']
        self.expect('MDFixer input is this run\'s ' + source + ' envelope',
                    next(s['artifact'] for s in result['stages'] if s['name'] == source), repair['input_report'])
        lines, edit_style, dependencies, targets = REPAIR[style]
        self.expect('candidate.patch changes exactly the expected declaration line(s)', lines,
                    changed_lines((self.root / 'candidate.patch').read_text(encoding='utf-8')))
        self.expect('the same change is what git sees in the target working copy', lines,
                    changed_lines(self.git('target-project', 'diff')))
        self.expect('repair plan', [{'target': t, 'dependency': d, 'style': edit_style}
                                    for t, d in zip(targets, dependencies)], repair['edits'])

        self.expect('sandbox validation', ACCEPTED, load(self.root / 'validation/validation.json'))
        recheck = load(self.root / 'recheck.json')['data']
        self.expect('recheck verdict equals the sandbox validation', ACCEPTED, recheck['validation'])
        if project == 'minicalc':
            self.expect('repaired Minicalc answers the three expressions', {'1+2*3': '7', '10-4/2': '8', '3*(4+5)': '27'},
                        load(self.root / 'validation/program-outputs.json'))
        self.expect('patched Makefile sha256: recorded, target working copy, validation sandbox',
                    [recheck['patched_makefile_sha256']] * 2,
                    [digest(self.root / 'target-project/Makefile'), digest(self.root / 'validation/sandbox/Makefile')])

        if kind == 'e11-b':
            fixed = load(request['fixed_report'])
            self.expect('fixed report names the target commit', request['target'], fixed['commit'])
            self.expect('fixed report is staged unchanged', fixed['data'], load(self.root / 'fixed-md-input.json')['data'])
            self.expect('fixed report lists config.h and extra.h as MISSING',
                        [('MISSING', 'main.o', 'config.h'), ('MISSING', 'main.o', 'extra.h')],
                        [tuple(f[k] for k in ('type', 'target', 'dependency'))
                         for f in fixed['data']['findings'] if f['type'] == 'MISSING'])
        else:
            self.expect('BuildChecker findings for the base commit', BASELINE[project],
                        triples(load(self.root / 'baseline-full/findings.json')['findings']))
            self.expect('GCC scan cached for the base commit', BASELINE[project],
                        triples(load(self.root / 'baseline-cache.json')['findings']))
            incremental = load(self.root / 'incremental-check.json')
            self.expect('incremental-check commits to the target and carries the staged scan',
                        [request['target'], load(self.root / 'incremental-report.json')],
                        [incremental['commit'], incremental['data']])
            self.expect('findings added and resolved from base to target', [ADDED[project], []],
                        [incremental['data']['added'], incremental['data']['resolved']])

        self.expect('final BuildChecker status', 'SUCCEEDED', load(self.root / 'final-full/findings.json')['status'])
        self.expect('final BuildChecker leaves only the expected REDUNDANT finding', FINAL[project],
                    triples(recheck['findings']))
        self.notes = {'job_id': job, 'trace_id': trace, 'base_commit': result['base_commit'],
                      'target_commit': result['target_commit'], 'artifacts': len(result['artifacts']),
                      'candidate.patch': digest(self.root / 'candidate.patch'),
                      'patched_makefile_sha256': digest(self.root / 'target-project/Makefile'),
                      'draft_image': second['image_id']}
        return self

    def api(self, codes, jobs):
        """Saved HTTP responses: one job_id/trace_id everywhere, and the download hash recomputed."""
        folder = self.root
        for name, code in codes.items():
            self.expect('HTTP status of ' + name, HTTP[name], code)
        submit, status, result = (load(folder / n) for n in ('submit.json', 'status.json', 'artifacts.json'))
        job = submit['job_id']
        self.expect('health', {'status': 'ok', 'schema_version': 'e11e12-1'}, load(folder / 'health.json'))
        self.expect('one job_id for submit, poll, artifacts, replay and the two post-restart calls', [job] * 5,
                    [status['job_id'], result['job_id']] + [load(folder / n)['job_id'] for n in
                                                            ('replay.json', 'restart-status.json', 'restart-replay.json')])
        self.expect('one trace_id for the poll, the artifacts and the persisted state', [status['trace_id']] * 2,
                    [result['trace_id'], load(jobs / job / 'state.json')['trace_id']])
        self.expect('status before and after the restart', ['SUCCEEDED'] * 2,
                    [status['status'], load(folder / 'restart-status.json')['status']])
        self.expect('same key with a changed target is refused before and after the restart',
                    [{'error': 'IDEMPOTENCY_CONFLICT'}] * 2,
                    [load(folder / 'conflict.json'), load(folder / 'restart-conflict.json')])
        header = re.search(r'^X-Content-SHA256:\s*([0-9a-f]{64})', (folder / 'download-headers.txt').read_text(),
                           re.I | re.M)
        self.expect('downloaded candidate.patch: header, downloaded bytes, evidence copy',
                    [next(a['sha256'] for a in result['artifacts'] if a['uri'].endswith('/candidate.patch'))] * 3,
                    [header.group(1).lower() if header else None, digest(folder / 'candidate.patch'),
                     digest(jobs / job / 'evidence/candidate.patch')])
        self.notes = {'job_id': job, 'trace_id': status['trace_id'], 'codes': codes}
        return self


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--work', type=Path, default=ROOT / 'work')
    ap.add_argument('--out', type=Path, required=True)
    a = ap.parse_args()
    work = a.work.resolve()
    report = {'passed': True, 'runs': {}, 'api': None}
    for name, kind, style, output in RUNS:
        if not (work / name / 'result.json').is_file():
            report['runs'][name] = {'passed': False, 'notes': {}, 'checks': [
                {'check': 'run exists', 'expected': True, 'actual': False, 'passed': False}]}
            continue
        check = Check(work / name).run(kind, style, output)
        report['runs'][name] = {'passed': check.passed, 'notes': check.notes, 'checks': check.checks}
    if (work / 'api-final/codes.txt').is_file():
        codes = {name: int(code) for name, code in (line.split('=') for line in
                                                    (work / 'api-final/codes.txt').read_text().split())}
        http = Check(work / 'api-final').api(codes, work / 'api-jobs')
        evidence = Check(work / 'api-jobs' / http.notes['job_id'] / 'evidence')
        real = load(evidence.root / 'request.json').get('profile') == 'minicalc'
        evidence.run('e12', 'minicalc' if real else 'direct', '7' if real else '1')
        report['api'] = {'passed': http.passed and evidence.passed, 'notes': http.notes,
                         'http': http.checks, 'evidence': evidence.checks}
    report['passed'] = all(r['passed'] for r in report['runs'].values()) and \
        (report['api'] is None or report['api']['passed'])
    save(a.out, report)
    print(json.dumps({'passed': report['passed'], 'runs': {k: v['passed'] for k, v in report['runs'].items()},
                      'api': report['api']['passed'] if report['api'] else None}))
    return 0 if report['passed'] else 1


if __name__ == '__main__':
    raise SystemExit(main())
