"""Generate personal E8/E9 evidence and check patch application in copies."""
import argparse
import hashlib
import json
import shutil
from pathlib import Path
from lab import demo, run, save, scan


def snapshot(project):
    return {p.relative_to(project).as_posix(): hashlib.sha256(p.read_bytes()).hexdigest()
            for p in sorted(project.rglob('*')) if p.is_file() and '.git' not in p.relative_to(project).parts}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--out', type=Path, required=True)
    out = ap.parse_args().out.resolve()
    out.mkdir(parents=True, exist_ok=False)
    demo('e8', out / 'e8', 'B')
    e8 = out / 'e8'
    project = e8 / 'project'
    before = snapshot(project)
    save(e8 / 'source-before.json', before)
    check = run(['git', 'apply', '--check', str(e8 / 'candidate.patch')], project)
    (e8 / 'apply-check.log').write_text(check)
    assert json.loads((e8 / 'expected-failure.json').read_text())['error'] == 'STALE_REPORT'
    assert snapshot(project) == before
    assert run(['git', 'status', '--porcelain'], project) == ''
    save(e8 / 'source-after.json', snapshot(project))
    demo('e9', out / 'e9', 'B')
    e9 = out / 'e9'
    checks = []
    for style in ['direct', 'macro', 'mixed']:
        original = e9 / style
        before = snapshot(original)
        save(e9 / (style + '-input.json'), scan(original))
        save(e9 / (style + '-before.json'), before)
        patch = e9 / (style + '.patch')
        (e9 / (style + '-apply-check.log')).write_text(run(['git', 'apply', '--check', str(patch)], original))
        copy = e9 / (style + '-apply-copy')
        shutil.copytree(original, copy)
        run(['git', 'apply', str(patch)], copy)
        (e9 / (style + '-applied-Makefile')).write_bytes((copy / 'Makefile').read_bytes())
        assert not any(f['type'] == 'MISSING' for f in scan(copy)['findings'])
        assert snapshot(original) == before
        assert run(['git', 'status', '--porcelain'], original) == ''
        save(e9 / (style + '-after.json'), snapshot(original))
        checks.append({'style': style, 'patch_applies': True, 'original_unchanged': True, 'copy_no_missing': True})
    macro = e9 / 'macro-apply-copy'
    (e9 / 'macro-build.log').write_text(run(['make', 'app'], macro))
    output = run(['./app'], macro)
    (e9 / 'macro-output.log').write_text(output)
    assert output == '1\n'
    save(out / 'verification.json', {'passed': True, 'e8_stale_rejected': True, 'e8_source_unchanged': True, 'e9': checks, 'macro_output': output})
    print(json.dumps({'passed': True, 'output': str(out)}))


if __name__ == '__main__':
    main()
