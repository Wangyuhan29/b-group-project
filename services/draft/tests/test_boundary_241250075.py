"""241250075: reject malformed replay candidates and run settings before Docker."""
import pytest
from draft import autobuild

PINNED = 'FROM python:3.13-slim@sha256:' + 'a' * 64
BASE = PINNED + '\nWORKDIR /work\nCOPY main.c Makefile ./\nRUN make\nCMD ["./hello"]\n'


def folded_candidate():
    return BASE.replace(
        'RUN make',
        'RUN apt-get update \\\n    && apt-get install -y build-essential \\\n    && rm -rf /var/lib/apt/lists/*\nRUN make',
    )


def test_truncated_continuation_rejected_before_docker():
    truncated = '\n'.join(folded_candidate().splitlines()[:4]) + '\n'
    assert truncated.rstrip('\n').splitlines()[-1].endswith('\\')
    with pytest.raises(ValueError, match='Incomplete line continuation'):
        autobuild.prepare_candidate(BASE, truncated)


def test_extra_build_stage_rejected_whole_candidate():
    staged = folded_candidate().replace('CMD ["./hello"]', 'CMD ["./hello"]\n' + PINNED + '\nRUN true')
    with pytest.raises(ValueError, match='single-stage'):
        autobuild.prepare_candidate(BASE, staged)


def test_non_positive_timeout_fails_fast_without_docker(tmp_path, monkeypatch):
    calls = []
    monkeypatch.setattr(autobuild, 'execute', lambda *a, **k: calls.append(a))
    with pytest.raises(ValueError, match='Timeouts must be positive'):
        autobuild.auto_build(tmp_path, tmp_path / 'candidate.Dockerfile', tmp_path / 'evidence', 'hello E3', timeout=0)
    assert not calls
    assert not (tmp_path / 'evidence').exists()
