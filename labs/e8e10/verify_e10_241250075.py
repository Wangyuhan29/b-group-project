"""Generate personal 241250075 E10 evidence: reference scenarios, then candidates that must be rejected."""
import argparse
import csv
import difflib
import hashlib
import json
from pathlib import Path
from lab import commit, demo, fixture, patch, run, save, scan, validate

# Each candidate is the target() Makefile with these replacements. The expectations follow from C/Make
# semantics: main.c includes config.h and extra.h, and stdio.h is only reachable through the system path.
CANDIDATES = [
    {'name': 'partial-md',
     'defect': 'declares config.h only; extra.h is still included by main.c but absent from the rule',
     'replace': [('main.o: main.c unused.h\n', 'main.o: main.c unused.h config.h\n')],
     'checks': {'patch_applies': True, 'build': True, 'test': True, 'header_change': True, 'no_missing': False},
     'error': None, 'remaining': [['main.o', 'extra.h']]},
    {'name': 'compile-failure',
     'defect': 'complete dependency repair, but the recipe drops the system include path',
     'replace': [('main.o: main.c unused.h\n', 'main.o: main.c unused.h config.h extra.h\n'),
                 ('\tgcc $(CFLAGS) -c main.c -o main.o\n', '\tgcc $(CFLAGS) -nostdinc -c main.c -o main.o\n')],
     'checks': {'patch_applies': True},
     'error': ['COMMAND_FAILED', 'no include path in which to search for stdio.h'], 'remaining': None},
]


def target(project):
    """Fixture at its second commit: main.c also includes extra.h, like the E11/E12 sample target."""
    fixture(project)
    (project / 'main.c').write_text('#include "extra.h"\n' + (project / 'main.c').read_text())
    return commit(project, 'C1 add project include')


def candidate_patch(project, spec, path):
    """Write the unified diff from the committed Makefile to the candidate text."""
    before = (project / 'Makefile').read_text()
    text = before
    for old, new in spec['replace']:
        if text.count(old) != 1:
            raise ValueError('fixture line not unique: ' + repr(old))
        text = text.replace(old, new)
    diff = ''.join(difflib.unified_diff(before.splitlines(True), text.splitlines(True),
                                        fromfile='a/Makefile', tofile='b/Makefile'))
    Path(path).write_text(diff)
    return diff


def sha256(data):
    return hashlib.sha256(data).hexdigest()


def check_reference(out):
    """Re-read the reference accept/reject/rollback results instead of trusting gate.json."""
    with (out / 'results.csv').open(newline='') as handle:
        rows = {row['case']: row['passed'] for row in csv.DictReader(handle)}
    reject_test = json.loads((out / 'reject-test/validation.json').read_text())
    accepted = json.loads((out / 'accept/validation.json').read_text())
    reject_patch = json.loads((out / 'reject-patch/validation.json').read_text())
    recheck = json.loads((out / 'recheck-buildchecker/findings.json').read_text())
    missing = [f for f in recheck['findings'] if f['type'] == 'MISSING']
    redundant = [(f['target'], f['dependency']) for f in recheck['findings'] if f['type'] == 'REDUNDANT']
    return {
        'rows': rows,
        'test-rejection': {'accepted': reject_test['accepted'], 'rollback': reject_test['rollback'],
                           'source_unchanged': reject_test['source_unchanged'], 'checks': reject_test['checks']},
        'patch-rejection': {'accepted': reject_patch['accepted'], 'rollback': reject_patch['rollback'],
                            'source_unchanged': reject_patch['source_unchanged'], 'error': reject_patch['error']},
        'accepted': {'accepted': accepted['accepted'], 'rollback': accepted['rollback'], 'checks': accepted['checks']},
        'buildchecker': {'status': recheck['status'], 'MISSING': len(missing), 'REDUNDANT': redundant},
    }


def reference_ok(results):
    return (results['rows'] == {'test-rejection': 'True', 'accepted': 'True', 'patch-rejection': 'True'}
            and results['test-rejection'] == {'accepted': False, 'rollback': True, 'source_unchanged': True,
                                              'checks': {'patch_applies': True, 'build': True, 'test': False,
                                                         'header_change': True, 'no_missing': True}}
            and results['patch-rejection']['accepted'] is False
            and results['patch-rejection']['rollback'] is True
            and results['patch-rejection']['source_unchanged'] is True
            and results['patch-rejection']['error'].startswith('COMMAND_FAILED')
            and results['accepted'] == {'accepted': True, 'rollback': False,
                                        'checks': {'patch_applies': True, 'build': True, 'test': True,
                                                   'header_change': True, 'no_missing': True}}
            and results['buildchecker']['status'] == 'SUCCEEDED'
            and results['buildchecker']['MISSING'] == 0
            and results['buildchecker']['REDUNDANT'] == [('main.o', 'unused.h')])


def run_candidate(out, spec):
    folder = out / 'candidates' / spec['name']
    project = folder / 'project'
    target(project)
    before = (project / 'Makefile').read_bytes()
    candidate_patch(project, spec, folder / 'candidate.patch')
    verdict = validate(project, folder / 'candidate.patch', folder / 'validation')
    after = (project / 'Makefile').read_bytes()
    (folder / 'Makefile.before').write_bytes(before)
    (folder / 'Makefile.after').write_bytes(after)
    (folder / 'source-status.txt').write_text(run(['git', 'status', '--porcelain'], project))
    recheck_path = folder / 'validation/recheck.json'
    remaining = []
    if recheck_path.is_file():
        remaining = [[f['target'], f['dependency']]
                     for f in json.loads(recheck_path.read_text())['findings'] if f['type'] == 'MISSING']
    expected_error_ok = (spec['error'] is None and verdict['error'] is None) or \
        (spec['error'] is not None and verdict['error'] is not None
         and all(part in verdict['error'] for part in spec['error']))
    actual = {'accepted': verdict['accepted'], 'rollback': verdict['rollback'],
              'source_unchanged': verdict['source_unchanged'], 'checks': verdict['checks'],
              'error_is_none': verdict['error'] is None, 'remaining': remaining,
              'sha256_before': sha256(before), 'sha256_after': sha256(after),
              'bytes_equal': before == after, 'git_status': (folder / 'source-status.txt').read_text()}
    expected = {'accepted': False, 'rollback': True, 'source_unchanged': True, 'checks': spec['checks'],
                'error_is_none': spec['error'] is None, 'remaining': spec['remaining'] or [],
                'bytes_equal': True, 'git_status': ''}
    passed = (all(actual[key] == value for key, value in expected.items())
              and actual['sha256_before'] == actual['sha256_after'] and expected_error_ok)
    return {'name': spec['name'], 'defect': spec['defect'], 'expected': expected, 'actual': actual, 'passed': passed}


def run_control(out):
    """The complete candidate differs from partial-md only by the omitted dependency, and must be accepted."""
    folder = out / 'candidates' / 'control-complete'
    project = folder / 'project'
    target(project)
    before = (project / 'Makefile').read_bytes()
    diff, plan = patch(project, scan(project))
    (folder / 'candidate.patch').write_text(diff)
    verdict = validate(project, folder / 'candidate.patch', folder / 'validation')
    after = (project / 'Makefile').read_bytes()
    (folder / 'Makefile.before').write_bytes(before)
    (folder / 'Makefile.after').write_bytes(after)
    (folder / 'source-status.txt').write_text(run(['git', 'status', '--porcelain'], project))
    passed = (verdict['accepted'] is True and verdict['rollback'] is False and verdict['source_unchanged'] is False
              and all(verdict['checks'].values()) and len(verdict['checks']) == 5
              and after != before and plan == [{'target': 'main.o', 'dependency': 'config.h', 'style': 'direct'},
                                               {'target': 'main.o', 'dependency': 'extra.h', 'style': 'direct'}])
    return {'expected': {'accepted': True, 'write_back': True, 'edits': 2}, 'actual': verdict, 'passed': passed}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--out', type=Path, required=True)
    out = ap.parse_args().out.resolve()
    out.mkdir(parents=True, exist_ok=False)
    (out / 'tools.log').write_text(''.join('$ ' + ' '.join(cmd) + '\n' + run(cmd, out).splitlines()[0] + '\n'
                                           for cmd in [['gcc', '--version'], ['make', '--version'],
                                                       ['git', '--version'], ['python3', '--version']]))
    demo('e10', out / 'reference', 'B')
    reference = check_reference(out / 'reference')
    save(out / 'reference-check.json', reference)
    candidates = [run_candidate(out, spec) for spec in CANDIDATES]
    control = run_control(out)
    summary = {'passed': reference_ok(reference) and control['passed'] and all(c['passed'] for c in candidates),
               'reference_passed': reference_ok(reference), 'candidates': candidates, 'control': control}
    save(out / 'verification.json', summary)
    print(json.dumps({'passed': summary['passed'], 'reference': summary['reference_passed'],
                      'candidates': {c['name']: c['passed'] for c in candidates},
                      'control': control['passed']}))
    return 0 if summary['passed'] else 1


if __name__ == '__main__':
    raise SystemExit(main())
