"""B03 / 241250086: candidate must retain the complete COPY input list."""
import pytest
from draft.autobuild import prepare_candidate


def test_candidate_cannot_silently_drop_makefile():
    baseline = 'FROM python:3.13-slim\nWORKDIR /work\nCOPY main.c Makefile ./\nRUN make\nCMD ["./hello"]\n'
    candidate = baseline.replace('FROM python:3.13-slim', 'FROM python:3.13-slim@sha256:' + 'a' * 64)
    candidate = candidate.replace('COPY main.c Makefile ./', 'COPY main.c ./').replace('RUN make', 'RUN apt-get install -y build-essential\nRUN make')
    with pytest.raises(ValueError, match='required project/build/runtime'):
        prepare_candidate(baseline, candidate)


def test_existing_pinned_baseline_is_supported():
    pinned = 'FROM python:3.13-slim@sha256:' + 'a' * 64
    baseline = pinned + '\nRUN make\nCMD ["./hello"]\n'
    candidate = baseline.replace('RUN make', 'RUN apt-get install -y build-essential\nRUN make')
    assert prepare_candidate(baseline, candidate) == baseline


def test_existing_baseline_digest_cannot_change():
    baseline = 'FROM python:3.13-slim@sha256:' + 'a' * 64 + '\nRUN make\n'
    candidate = baseline.replace('a' * 64, 'b' * 64).replace('RUN make', 'RUN apt-get install -y build-essential\nRUN make')
    with pytest.raises(ValueError, match='base image'):
        prepare_candidate(baseline, candidate)
