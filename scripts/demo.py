#!/usr/bin/env python3
"""Run the synthetic explicit-rule repair experiment using cc, make and git."""
import difflib
import hashlib
import json
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from validate import validate


def run(args, cwd, expected=0):
    p = subprocess.run(args, cwd=cwd, capture_output=True, text=True, timeout=60)
    if p.returncode != expected:
        raise RuntimeError(f'{args}: expected {expected}, got {p.returncode}\n{p.stdout}{p.stderr}')
    return p.stdout + p.stderr


def main():
    for tool in ['git', 'make', 'cc']:
        if not shutil.which(tool):
            raise RuntimeError(f'Required tool unavailable: {tool}')
    report = json.loads((ROOT / 'fixtures/md-report.json').read_text())
    validate(report)
    req = json.loads((ROOT / 'contracts/examples/repair-request.json').read_text())
    validate(req)
    with tempfile.TemporaryDirectory(prefix='b-group-demo-') as tmp:
        project = Path(tmp) / 'project'
        run(['git', 'clone', '--quiet', str(ROOT / 'fixtures/source.bundle'), str(project)], ROOT)
        actual_sha = run(['git', 'rev-parse', 'HEAD'], project).strip()
        if actual_sha != report['repository']['commit']:
            raise RuntimeError('Fixture bundle/report commit mismatch')
        logs = {'initial_build': run(['make', 'clean', 'all', 'test', 'EXPECTED=1'], project)}
        # Controlled timestamp prevents platform timestamp resolution hiding the defect.
        header = project / 'config.h'
        header.write_text('#define VALUE 2\n')
        import os
        object_time = (project / 'main.o').stat().st_mtime
        os.utime(header, (object_time + 2, object_time + 2))
        logs['before_repair'] = run(['make'], project)
        stale = run([str(project / 'app')], project).strip()
        if stale != '1':
            raise RuntimeError('Expected stale binary before repair')
        # Deliberately bounded to this fixture; not a general Makefile parser.
        finding = report['findings'][0]
        if (len(report['findings']), finding['type'], finding['target'], finding['dependency'], finding['location']['file']) != (1, 'MISSING', 'main.o', 'config.h', 'Makefile'):
            raise RuntimeError('Demo supports only the provided synthetic fixture')
        makefile = project / 'Makefile'
        before = makefile.read_text()
        needle = 'main.o: main.c\n'
        if before.count(needle) != 1:
            raise RuntimeError('Expected exactly one explicit fixture rule')
        after = before.replace(needle, 'main.o: main.c config.h\n')
        patch = ''.join(difflib.unified_diff(before.splitlines(True), after.splitlines(True), fromfile='a/Makefile', tofile='b/Makefile'))
        patch_path = Path(tmp) / 'fix.patch'; patch_path.write_text(patch)
        logs['patch_check'] = run(['git', 'apply', '--check', str(patch_path)], project)
        logs['patch_apply'] = run(['git', 'apply', str(patch_path)], project)
        logs['after_repair'] = run(['make', 'all', 'test', 'EXPECTED=2'], project)
        # Force a rebuild check with -W; make -q returns 1 when rebuilding is needed.
        logs['local_recheck'] = run(['make', '-q', '-W', 'config.h', 'main.o'], project, expected=1)
        logs['clean_build'] = run(['make', 'clean', 'all', 'test', 'EXPECTED=2'], project)
        output = ROOT / 'work/demo'
        output.mkdir(parents=True, exist_ok=True)
        (output / 'fix.patch').write_text(patch)
        for name, content in logs.items():
            (output / (name + '.log')).write_text(content)
        summary = {'fixture_commit':actual_sha, 'before_repair_output':'1', 'after_repair_output':'2',
                   'patch_sha256':hashlib.sha256(patch.encode()).hexdigest(),
                   'patch_apply_check':True, 'clean_build_and_test':True,
                   'local_oracle_recheck':True, 'a_group_recheck':'NOT_RUN', 'docker_build':'NOT_RUN',
                   'scope':'Synthetic explicit-rule fixture only; not a production REPAIR job result.'}
        (output / 'summary.json').write_text(json.dumps(summary, ensure_ascii=False, indent=2)+'\n')
        print('PASS: reproduced stale output 1, applied generated patch, rebuilt output 2; clean build/test and local recheck passed.')
        print('Logs:', output)


if __name__ == '__main__':
    try:
        main()
    except (RuntimeError, subprocess.TimeoutExpired, ValueError, OSError) as e:
        print('FAIL:', e, file=sys.stderr)
        sys.exit(1)
