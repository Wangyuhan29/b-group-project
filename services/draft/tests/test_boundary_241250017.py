"""241250017: reject unsafe fixture/output boundaries before invoking Docker."""
import pytest
from draft import autobuild


def fixture_files(tmp_path):
    fixture = tmp_path / 'fixture'
    fixture.mkdir()
    baseline = 'FROM python:3.13-slim\nRUN make\nCMD ["./hello"]\n'
    (fixture / 'Dockerfile.broken').write_text(baseline)
    candidate = tmp_path / 'candidate.Dockerfile'
    candidate.write_text(baseline.replace('python:3.13-slim', 'python:3.13-slim@sha256:' + 'a' * 64).replace('RUN make', 'RUN apt-get install -y build-essential\nRUN make'))
    return fixture, candidate


@pytest.mark.parametrize('nested', [False, True])
def test_output_cannot_overwrite_or_enter_fixture(tmp_path, monkeypatch, nested):
    fixture, candidate = fixture_files(tmp_path)
    before = (fixture / 'Dockerfile.broken').read_bytes()
    calls = []
    monkeypatch.setattr(autobuild, 'execute', lambda *a, **k: calls.append(a))
    output = fixture / 'evidence' if nested else fixture
    with pytest.raises(ValueError, match='Output must be outside fixture'):
        autobuild.auto_build(fixture, candidate, output, 'hello E3')
    assert not calls
    assert (fixture / 'Dockerfile.broken').read_bytes() == before
    if nested:
        assert not output.exists()


def test_external_symlink_rejected_before_build(tmp_path, monkeypatch):
    fixture, candidate = fixture_files(tmp_path)
    outside = tmp_path / 'outside.txt'
    outside.write_text('outside-project-content')
    (fixture / 'linked.txt').symlink_to(outside)
    calls = []
    monkeypatch.setattr(autobuild, 'execute', lambda *a, **k: calls.append(a))
    output = tmp_path / 'evidence'
    with pytest.raises(ValueError, match='Symlink fixtures are unsupported'):
        autobuild.auto_build(fixture, candidate, output, 'hello E3')
    assert not calls
    assert not output.exists()
    assert outside.read_text() == 'outside-project-content'
