"""241250075: personal E11-B style samples with stale reports, and the real Minicalc C0/C1 request."""
import json
import os
from pathlib import Path
from lab import commit, fixture, run, scan
from pipeline import ROOT, save

PIN = '@sha256:f82c96458eedc847b233e582eb31336f4954b39cae020b6dcf5b3ed0e5cbcd74'
SAMPLE_BROKEN = ('FROM BASE_IMAGE\nWORKDIR /work\nCOPY main.c helper.c config.h extra.h unused.h Makefile ./\n'
                 'RUN make app\nCMD ["./app"]\n')
MINICALC_BROKEN = ('FROM BASE_IMAGE\nWORKDIR /work\nCOPY src ./src\nCOPY include ./include\nCOPY Makefile ./\n'
                   'RUN make\nCMD ["./minicalc", "1+2*3"]\n')
MINICALC = {'base': 'e3a1eda0965e545d96467d275bccaf78c890fcac',
            'target': 'f863c2deff1bd95e56f1578b872ae6aa26e3bfc8'}


def repaired(broken, base_image):
    """Digest-pinned FROM plus one recorded RUN line that installs the missing build tools."""
    update = 'apt-get update'
    mirror = os.environ.get('COURSE_DEBIAN_MIRROR')
    if mirror:
        update = 'sed -i "s/deb.debian.org/%s/g" /etc/apt/sources.list.d/debian.sources && apt-get update' % mirror
    install = ('RUN %s && apt-get install -y --no-install-recommends build-essential'
               ' && rm -rf /var/lib/apt/lists/*\nRUN ') % update
    return broken.replace('FROM ' + base_image, 'FROM ' + base_image + PIN).replace('RUN ', install, 1)


def report(commit_sha, data):
    return {'schema_version': 'e11e12-1', 'kind': 'fixed-md', 'status': 'SUCCEEDED', 'commit': commit_sha, 'data': data}


def style_sample(root, style, base_image):
    """Two commits in one declaration style; C1 makes main.c include extra.h, as in the shared sample."""
    root.mkdir()
    project = root / 'repo'
    fixture(project, style)
    broken = SAMPLE_BROKEN.replace('BASE_IMAGE', base_image)
    (project / 'Dockerfile.broken').write_text(broken, encoding='utf-8')
    base = commit(project, style + ' C0')
    # Scanned while C0 was HEAD, so this is the report the previous commit would have produced.
    old = report(base, scan(project))
    save(root / 'c0-report.json', old)
    (project / 'main.c').write_text('#include "extra.h"\n' + (project / 'main.c').read_text(), encoding='utf-8')
    target = commit(project, style + ' C1 add project include')
    fixed = report(target, scan(project))
    save(root / 'fixed-md.json', fixed)
    save(root / 'stale-zero.json', dict(fixed, commit='0' * 40))
    save(root / 'stale-inner.json', dict(fixed, data=old['data']))
    (root / 'candidate.Dockerfile').write_text(repaired(broken, base_image), encoding='utf-8')
    run(['git', 'bundle', 'create', str(root / 'repo.bundle'), '--all'], project)
    paths = {name: str(root / name) for name in
             ['repo', 'candidate.Dockerfile', 'fixed-md.json', 'stale-zero.json', 'c0-report.json', 'stale-inner.json']}
    request = {'repo': paths['repo'], 'base': base, 'target': target, 'candidate': paths['candidate.Dockerfile'],
               'expected_output': '1', 'build_timeout': 600}
    save(root / 'e11-b.json', dict(request, mode='e11-b', fixed_report=paths['fixed-md.json']))
    save(root / 'e11-stale-zero.json', dict(request, mode='e11-b', fixed_report=paths['stale-zero.json']))
    save(root / 'e11-stale-old.json', dict(request, mode='e11-b', fixed_report=paths['c0-report.json']))
    save(root / 'e11-stale-inner.json', dict(request, mode='e11-b', fixed_report=paths['stale-inner.json']))
    save(root / 'dataset.json', {'source': 'course-generated controlled C/Make project, ' + style + ' declaration style',
                                 'base_commit': base, 'target_commit': target,
                                 'fixed_md_dependencies': ['config.h', 'extra.h'], 'expected_output': '1'})
    return {'sample': style, 'base_commit': base, 'target_commit': target}


def minicalc_sample(root, base_image):
    run(['git', 'clone', '-q', str(ROOT / 'fixtures/minicalc/history.bundle'), str(root / 'real-minicalc')], ROOT)
    config = root / 'real-config'
    config.mkdir()
    broken = MINICALC_BROKEN.replace('BASE_IMAGE', base_image)
    (config / 'Dockerfile.broken').write_text(broken, encoding='utf-8')
    (config / 'candidate.Dockerfile').write_text(repaired(broken, base_image), encoding='utf-8')
    save(config / 'e12.json', {'mode': 'e12', 'profile': 'minicalc', 'repo': str(root / 'real-minicalc'),
                               'base': MINICALC['base'], 'target': MINICALC['target'],
                               'candidate': str(config / 'candidate.Dockerfile'),
                               'broken_dockerfile': str(config / 'Dockerfile.broken'),
                               'expected_output': '7', 'build_timeout': 600})


def shared_sample_stale():
    """Zero-commit variant of the shared sample's fixed report, for rerunning the archived rejection."""
    sample = ROOT / 'data/integration-sample'
    fixed = json.loads((sample / 'fixed-md.json').read_text(encoding='utf-8'))
    save(sample / 'stale-zero.json', dict(fixed, commit='0' * 40))
    request = json.loads((sample / 'e11-b.json').read_text(encoding='utf-8'))
    save(sample / 'e11-stale-zero.json', dict(request, fixed_report=str(sample / 'stale-zero.json')))


def main():
    root = ROOT / 'data/personal-241250075'
    if root.exists():
        raise SystemExit('data/personal-241250075 already exists; preserve it and choose a new workspace')
    base_image = os.environ.get('COURSE_BASE_IMAGE', 'python:3.13-slim')
    root.mkdir(parents=True)
    samples = [style_sample(root / style, style, base_image) for style in ('macro', 'mixed')]
    minicalc_sample(root, base_image)
    shared_sample_stale()
    save(root / 'dataset.json', {'samples': samples,
                                 'minicalc': dict(MINICALC, source='upstream history.bundle, tags c0 and c1')})
    print(root)


if __name__ == '__main__':
    main()
