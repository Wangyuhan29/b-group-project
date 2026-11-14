"""Generate personal 241250075 E8/E9 evidence; apply every style patch in its own copy."""
import argparse
import hashlib
import json
import shutil
from pathlib import Path
from lab import demo, run, save, scan


def snapshot(project):
    return {p.relative_to(project).as_posix(): hashlib.sha256(p.read_bytes()).hexdigest()
            for p in sorted(project.rglob('*')) if p.is_file() and '.git' not in p.relative_to(project).parts}


def tools_log(project):
    lines = []
    for cmd in [['gcc', '--version'], ['make', '--version'], ['git', '--version'], ['python3', '--version']]:
        lines.append('$ ' + ' '.join(cmd))
        lines.append(run(cmd, project).splitlines()[0])
    return '\n'.join(lines) + '\n'


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
    (e8 / 'apply-check.log').write_text(run(['git', 'apply', '--check', str(e8 / 'candidate.patch')], project))
    stale = json.loads((e8 / 'expected-failure.json').read_text())
    assert stale['error'] == 'STALE_REPORT'
    assert snapshot(project) == before
    assert run(['git', 'status', '--porcelain'], project) == ''
    save(e8 / 'source-after.json', snapshot(project))
    (e8 / 'tools.log').write_text(tools_log(project))
    demo('e9', out / 'e9', 'B')
    e9 = out / 'e9'
    checks = []
    for style in ['direct', 'macro', 'mixed']:
        original = e9 / style
        style_before = snapshot(original)
        save(e9 / (style + '-input.json'), scan(original))
        save(e9 / (style + '-before.json'), style_before)
        style_patch = e9 / (style + '.patch')
        (e9 / (style + '-apply-check.log')).write_text(run(['git', 'apply', '--check', str(style_patch)], original))
        copy = e9 / (style + '-apply-copy')
        shutil.copytree(original, copy)
        run(['git', 'apply', str(style_patch.resolve())], copy)
        (e9 / (style + '-applied-Makefile')).write_bytes((copy / 'Makefile').read_bytes())
        rescanned = scan(copy)
        assert not any(f['type'] == 'MISSING' for f in rescanned['findings'])
        (e9 / (style + '-build.log')).write_text(run(['make', 'clean'], copy) + run(['make', 'app'], copy))
        output = run(['./app'], copy)
        (e9 / (style + '-output.log')).write_text(output)
        assert output == '1\n'
        assert snapshot(original) == style_before
        assert run(['git', 'status', '--porcelain'], original) == ''
        save(e9 / (style + '-after.json'), snapshot(original))
        checks.append({'style': style, 'patch_applies': True, 'original_unchanged': True,
                       'copy_no_missing': True, 'copy_output': output.strip()})
    save(out / 'verification.json', {'passed': True, 'e8_stale_rejected': True, 'e8_source_unchanged': True,
                                     'e9': checks})
    print(json.dumps({'passed': True, 'output': str(out)}))


if __name__ == '__main__':
    main()
