"""Personal E10/E11-B/E12 evidence runner; existing pipeline stays unchanged."""
import argparse
import copy
import difflib
import hashlib
import json
import shutil
from pathlib import Path
import pipeline
from lab import fixture, scan, validate, commit, run
import prepare


def save(path, data):
    pipeline.save(path, data)


def digest(data):
    return hashlib.sha256(data).hexdigest()


def verify_chain(folder, mode):
    result = json.loads((folder / 'result.json').read_text())
    assert result['status'] == 'SUCCEEDED', result
    expected = ['draft', 'fixed-md', 'repair', 'recheck'] if mode == 'e11-b' else ['draft', 'full-check', 'incremental-check', 'repair', 'recheck']
    assert [x['name'] for x in result['stages']] == expected
    checked = 0
    def verify_artifact(artifact):
        nonlocal checked
        prefix = 'artifact://' + result['job_id'] + '/'
        assert artifact['uri'].startswith(prefix)
        relative = artifact['uri'][len(prefix):]
        path = (folder / relative).resolve()
        assert path.is_relative_to(folder.resolve())
        data = path.read_bytes()
        assert digest(data) == artifact['sha256'] and len(data) == artifact['bytes'], path
        checked += 1
    for entry in result['stages']:
        verify_artifact(entry['artifact'])
        envelope = json.loads((folder / (entry['name'] + '.json')).read_text())
        assert envelope['job_id'] == result['job_id']
        assert envelope['trace_id'] == result['trace_id']
        expected_commit = result['base_commit'] if entry['name'] == 'full-check' else result['target_commit']
        pipeline.check_envelope(envelope, expected_commit, entry['name'])
        for artifact in envelope['artifacts']:
            verify_artifact(artifact)
        if entry['name'] == 'repair':
            verify_artifact(envelope['data']['input_report'])
    for artifact in result['artifacts']:
        verify_artifact(artifact)
    summary = {'passed': True, 'job_id': result['job_id'], 'trace_id': result['trace_id'],
               'target_commit': result['target_commit'], 'base_commit': result['base_commit'],
               'stages': expected, 'verified_hash_entries': checked}
    save(folder.parent / (folder.name + '-contract-verification.json'), summary)
    return summary


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--out', type=Path, required=True)
    args = parser.parse_args()
    out = args.out.resolve()
    out.mkdir(parents=True, exist_ok=False)
    # Capture a buildable but incomplete candidate and original bytes.
    project = out / 'e10-remaining-md/project'
    fixture(project)
    before = (project / 'Makefile').read_bytes()
    candidate = out / 'e10-remaining-md/candidate.patch'
    candidate.write_text(''.join(difflib.unified_diff(before.decode().splitlines(True),
        before.decode().replace('main.c unused.h', 'main.c').splitlines(True),
        fromfile='a/Makefile', tofile='b/Makefile')))
    verdict = validate(project, candidate, out / 'e10-remaining-md/rejected')
    after = (project / 'Makefile').read_bytes()
    (out / 'e10-remaining-md/Makefile.before').write_bytes(before)
    (out / 'e10-remaining-md/Makefile.after').write_bytes(after)
    assert verdict['checks']['build'] and verdict['checks']['test']
    assert not verdict['checks']['no_missing'] and verdict['rollback'] and not verdict['accepted']
    assert before == after
    save(out / 'e10-remaining-md/source-byte-check.json', {'before_sha256': digest(before), 'after_sha256': digest(after), 'equal': True})

    prepare.main()
    sample = pipeline.ROOT / 'data/integration-sample'
    # Explicit HTTPS mirror adaptation; retain the fixed image digest and commands.
    candidate_file = sample / 'candidate.Dockerfile'
    candidate_file.write_text(candidate_file.read_text().replace('http://mirrors.huaweicloud.com', 'https://mirrors.huaweicloud.com'))
    request = json.loads((sample / 'e11-b.json').read_text())
    assert pipeline.execute(request, out / 'e11-direct')['status'] == 'SUCCEEDED'
    direct = verify_chain(out / 'e11-direct', 'e11-b')

    macro = pipeline.ROOT / 'data/241250017-macro'
    run(['git', 'clone', '--no-hardlinks', str(sample / 'repo'), str(macro)], pipeline.ROOT)
    run(['git', 'config', 'user.name', '241250017'], macro)
    run(['git', 'config', 'user.email', '2983618236@qq.com'], macro)
    text = (macro / 'Makefile').read_text()
    assert 'main.o: main.c unused.h' in text
    (macro / 'Makefile').write_text('DEPS = main.c unused.h\n' + text.replace('main.o: main.c unused.h', 'main.o: $(DEPS)'))
    target = commit(macro, '241250017 macro declaration input')
    fixed = {'schema_version': 'e11e12-1', 'kind': 'fixed-md', 'status': 'SUCCEEDED', 'commit': target, 'data': scan(macro)}
    save(sample / '241250017-macro-fixed.json', fixed)
    macro_request = dict(request, repo=str(macro), target=target, fixed_report=str(sample / '241250017-macro-fixed.json'))
    save(sample / '241250017-macro-request.json', macro_request)
    assert pipeline.execute(macro_request, out / 'e11-macro')['status'] == 'SUCCEEDED'
    macro_check = verify_chain(out / 'e11-macro', 'e11-b')
    diff = (out / 'e11-macro/candidate.patch').read_text()
    assert '+DEPS = main.c unused.h config.h extra.h' in diff
    assert not any(x.startswith(('+main.o:', '-main.o:', '+\t', '-\t')) for x in diff.splitlines())
    assert 'main.o: $(DEPS)' in (out / 'e11-macro/target-project/Makefile').read_text()
    stale = copy.deepcopy(fixed)
    stale['commit'] = '0' * 40
    save(sample / '241250017-stale-fixed.json', stale)
    stale_request = dict(macro_request, fixed_report=str(sample / '241250017-stale-fixed.json'))
    save(sample / '241250017-stale-request.json', stale_request)
    rejected = pipeline.execute(stale_request, out / 'e11-stale')
    assert rejected['status'] == 'FAILED' and rejected['error']['code'] == 'STALE_REPORT'
    assert not any(x['name'] == 'repair' for x in rejected['stages'])

    request12 = json.loads((sample / 'e12.json').read_text())
    assert pipeline.execute(request12, out / 'e12')['status'] == 'SUCCEEDED'
    full = verify_chain(out / 'e12', 'e12')
    save(out / 'verification.json', {'passed': True, 'e10_remaining_md_rejected': True,
         'e11_direct': direct, 'e11_macro': macro_check, 'e11_stale_rejected': True, 'e12': full})
    print(json.dumps({'passed': True, 'output': str(out)}))


if __name__ == '__main__':
    main()
