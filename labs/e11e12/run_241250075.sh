#!/usr/bin/env bash
# 241250075 personal E10-E12 rerun on the course server (ecs-833a).
# Usage, from the repository checkout: bash labs/e11e12/run_241250075.sh <expected source commit>
# Everything stays in this student's own directory. git user.name is the numeric student ID, so the shared
# entry run_e11e12.py builds and runs course-e11e12:241250075; the API is published on 127.0.0.1:18075 only.
# Evidence is collected in ../evidence and ../241250075-e10e12-evidence.tar.gz next to the checkout.
# Runs at the student's explicit request, driven by the ZCode (GLM) agent over SSH.
set -u
SID=241250075
TIP=${1:?usage: run_241250075.sh <expected source commit>}
PORT=18075
PULL_IMAGE=m.daocloud.io/docker.io/library/python:3.13-slim
MIRROR=mirrors.huaweicloud.com
COURSE_DRAFT=course1027-draft@sha256:edcc9be43e726802ae0d079122422cc04fd6baeed3b5c11c3b0bf4aa064114c3

BASE=$PWD
IMG=course-e11e12:$SID
META=$BASE/work/run-metadata
API=$BASE/work/api-final
URL=http://127.0.0.1:$PORT
mkdir -p "$META"

say() { echo "[$(date -u +%FT%TZ)] $*" | tee -a "$META/commands.log"; }
step() {  # step NAME -- command...   (stdout+stderr to work/run-metadata/NAME.log, exit code to status.log)
  local name=$1 rc; shift 2
  say "\$ $*"
  "$@" > "$META/$name.log" 2>&1
  rc=$?
  echo "$name=$rc" >> "$META/status.log"
  say "=> $name exit $rc"
  return $rc
}
http() {  # http NAME METHOD PATH [BODYFILE]  -> response to NAME.json, code to codes.txt
  python3 - "$API" "$URL" "$@" <<'PY'
import sys, urllib.error, urllib.request
folder, base, name, method, path = sys.argv[1:6]
data = open(sys.argv[6], 'rb').read() if len(sys.argv) > 6 else None
request = urllib.request.Request(base + path, data=data, method=method, headers={'Content-Type': 'application/json'})
try:
    with urllib.request.urlopen(request, timeout=60) as response:
        code, body, headers = response.status, response.read(), response.headers
except urllib.error.HTTPError as error:
    code, body, headers = error.code, error.read(), error.headers
open(folder + ('/candidate.patch' if name == 'download' else '/' + name + '.json'), 'wb').write(body)
if name == 'download':
    open(folder + '/download-headers.txt', 'w').write(str(headers) + '\n')
with open(folder + '/codes.txt', 'a') as log:
    log.write(name + '=' + str(code) + '\n')
PY
}
field() { python3 -c "import json,sys;print(json.load(open(sys.argv[1])).get(sys.argv[2]))" "$@"; }
start_api() {
  nohup python3 run_e11e12.py serve --port "$PORT" > "$META/api-server-$1.log" 2>&1 < /dev/null &
  for i in $(seq 1 60); do
    if http health GET /health 2>/dev/null; then return 0; fi
    sleep 2
  done
  return 1
}
stop_api() {
  for id in $(docker ps -q --filter "publish=$PORT"); do
    [ "$(docker inspect --format '{{.Config.Image}}' "$id")" = "$IMG" ] || { say "REFUSE: port $PORT belongs to $id ($IMG expected)"; exit 4; }
    docker kill "$id" > /dev/null
  done
  sleep 3
}

case "$BASE/" in /root/$SID/*) ;; *) [ "${B03_REHEARSAL:-}" = 1 ] || { echo "REFUSE: $BASE is not below /root/$SID"; exit 2; };; esac
[ "$(git config --local user.name)" = "$SID" ] || { echo "REFUSE: git user.name is not $SID"; exit 2; }
[ "$(git rev-parse HEAD)" = "$TIP" ] || { echo "REFUSE: HEAD is not $TIP"; exit 2; }
[ -z "$(git status --porcelain)" ] || { echo "REFUSE: checkout is not clean"; exit 2; }
stop_api
git rev-parse HEAD > "$META/tested-sha.txt"
{ uname -a; docker version; nproc; free -m; df -h /; } > "$META/host-environment.log" 2>&1
docker images --digests > "$META/docker-images-before.log" 2>&1
say "start: $BASE at $TIP"

# 1. Environment image: the shared Dockerfile first; if the registry route is blocked, the same image is
#    derived from this student's own E8/E9 image plus strace and the teacher BuildChecker.
if step build-original -- timeout --kill-after=30 600 docker build \
    -f labs/e11e12/environment/services/buildchecker/Dockerfile -t "$IMG" labs/e11e12/environment; then
  echo original > "$META/environment-source.txt"
else
  if docker image inspect "course-e8e9:$SID" > "$META/base-image-inspect.json" 2>&1; then
    echo "FROM course-e8e9:$SID" > "$META/environment.Dockerfile"
  else
    { echo "FROM $COURSE_DRAFT"; echo "USER root"
      echo 'RUN apt-get -o Acquire::Retries=2 -o Acquire::https::Timeout=60 update && apt-get install -y --no-install-recommends gcc make libc6-dev && rm -rf /var/lib/apt/lists/*'
    } > "$META/environment.Dockerfile"
  fi
  cat >> "$META/environment.Dockerfile" <<'EOF'
USER root
RUN apt-get -o Acquire::Retries=1 -o Acquire::https::Timeout=20 update && apt-get install -y --no-install-recommends strace && rm -rf /var/lib/apt/lists/*
COPY services/buildchecker /app/
ENV PYTHONPATH=/app
WORKDIR /course
EOF
  echo adapted > "$META/environment-source.txt"
  step build-adapted -- env DOCKER_BUILDKIT=0 docker build -f "$META/environment.Dockerfile" -t "$IMG" \
      labs/e11e12/environment || { echo BUILD_FAILED; exit 1; }
fi
docker image inspect "$IMG" > "$META/image-inspect.json"
docker image inspect "$IMG" --format '{{.Id}}' > "$META/image-id.txt"
docker image inspect "course-e8e9:$SID" --format '{{.Id}} {{json .RepoDigests}}' > "$META/base-image-id.txt" 2>&1
docker run --rm "$IMG" sh -c 'gcc --version | head -1; make --version | head -1; git --version; python3 --version; strace --version | head -1; docker --version; uname -m; grep PRETTY_NAME /etc/os-release; id' \
    > "$META/container-tools.log" 2>&1

# Same container options as the test stage of run_e11e12.py.
CR=(docker run --rm --network none --cap-add SYS_PTRACE --user "$(id -u):$(id -g)" -e HOME=/tmp
    -e PYTHONPATH=/course/labs/e11e12:/course/labs/e8e10:/course/labs/e11e12/vendor:/app
    -v "$BASE:/course" -w /course "$IMG" python3)

# 2. Tests and the E10 reference/personal scenarios.
step contracts -- python3 run_e11e12.py test
step e8e10-tests -- "${CR[@]}" -m unittest discover -s labs/e8e10 -p 'test*.py' -v
step e10-final -- "${CR[@]}" labs/e8e10/lab.py e10 --track B --out work/e10-final
step e10-personal -- "${CR[@]}" labs/e8e10/verify_e10_241250075.py --out work/e10-personal

# 3. Samples: the shared generator, then this student's style samples, stale reports and Minicalc request.
step prepare -- env COURSE_BASE_IMAGE="$PULL_IMAGE" COURSE_DEBIAN_MIRROR="$MIRROR" python3 run_e11e12.py prepare || exit 3
step prepare-personal -- env COURSE_BASE_IMAGE="$PULL_IMAGE" COURSE_DEBIAN_MIRROR="$MIRROR" \
    docker run --rm --network none --user "$(id -u):$(id -g)" -e HOME=/tmp -e COURSE_BASE_IMAGE -e COURSE_DEBIAN_MIRROR \
    -e PYTHONPATH=/course/labs/e11e12:/course/labs/e8e10:/course/labs/e11e12/vendor:/app -v "$BASE:/course" -w /course \
    "$IMG" python3 labs/e11e12/prepare_241250075.py || exit 3
step integration-bundle -- git -C data/integration-sample/repo bundle create "$BASE/data/integration-sample/repo.bundle" --all

# 4. Pipeline runs. Stale runs exit 1 by design: the fixed report is rejected after the DRAFT stage.
run() {
  local name=$1 request=$2 expected=$3 rc
  step "$name" -- python3 run_e11e12.py run --request "$request" --out "work/$name"; rc=$?
  [ "$rc" = "$expected" ] || say "UNEXPECTED exit $rc, expected $expected: $name"
}
run e11-final data/integration-sample/e11-b.json 0
run e11-macro data/personal-241250075/macro/e11-b.json 0
run e11-mixed data/personal-241250075/mixed/e11-b.json 0
run e11-stale-zero data/integration-sample/e11-stale-zero.json 1
run e11-stale-old data/personal-241250075/mixed/e11-stale-old.json 1
run e11-stale-inner data/personal-241250075/macro/e11-stale-inner.json 1
run e12-final data/integration-sample/e12.json 0
run e12-real data/personal-241250075/real-config/e12.json 0

# 5. Loopback API: submit the real Minicalc job, replay, conflict, download, restart, repeat.
mkdir -p "$API"
KEY="$SID-e12-real-$(date -u +%Y%m%dT%H%M%SZ)"
python3 - data/personal-241250075/real-config/e12.json "$API" "$KEY" <<'PY'
import json, sys
request = json.load(open(sys.argv[1], encoding='utf-8'))
for name, body in (('post.json', request), ('post-changed.json', dict(request, target=request['base']))):
    with open(sys.argv[2] + '/' + name, 'w', encoding='utf-8') as handle:
        json.dump({'idempotency_key': sys.argv[3], 'input': body}, handle, indent=2)
PY
start_api first || { stop_api; echo "API did not start"; exit 5; }
http submit POST /v1/jobs "$API/post.json"
JOB=$(field "$API/submit.json" job_id)
say "job $JOB"
for i in $(seq 1 240); do
  STATE=$(python3 - "$URL/v1/jobs/$JOB" <<'PY'
import json, sys, urllib.request
with urllib.request.urlopen(sys.argv[1], timeout=30) as response:
    print(json.load(response).get('status'))
PY
) || STATE=RUNNING
  case "$STATE" in SUCCEEDED|FAILED|TIMED_OUT) break;; esac
  sleep 5
done
say "job ended as $STATE"
http status GET "/v1/jobs/$JOB"
http artifacts GET "/v1/jobs/$JOB/artifacts"
http replay POST /v1/jobs "$API/post.json"
http conflict POST /v1/jobs "$API/post-changed.json"
http download GET "/v1/jobs/$JOB/files/candidate.patch"
stop_api
start_api second || { stop_api; echo "API did not restart"; exit 5; }
http restart-status GET "/v1/jobs/$JOB"
http restart-replay POST /v1/jobs "$API/post.json"
http restart-conflict POST /v1/jobs "$API/post-changed.json"
stop_api
say "API codes:"; cat "$API/codes.txt"

# 6. Independent re-check of every run (commits, job/trace identity, artifact hashes, patch position).
step verification -- "${CR[@]}" labs/e11e12/verify_e11e12_241250075.py --out work/verification.json

# 7. Version, environment and the evidence bundle.
git rev-parse HEAD > "$META/tested-sha-after.txt"
git status --porcelain > "$META/git-status-after.txt"
docker images --digests > "$META/docker-images-after.log" 2>&1
cp "$BASE/labs/e11e12/run_241250075.sh" "$META/run_241250075.sh"
EVIDENCE=$(dirname "$BASE")/evidence
rm -rf "$EVIDENCE"; mkdir -p "$EVIDENCE"
tar -C "$BASE" --exclude='*/.git' --exclude='__pycache__' -cf - work data | tar -C "$EVIDENCE" -xf -
python3 - "$EVIDENCE" "$TIP" "$(cat "$META/image-id.txt")" <<'PY'
import hashlib, json, sys
from pathlib import Path
root, tip, image = Path(sys.argv[1]), sys.argv[2], sys.argv[3].strip()
files = {p.relative_to(root).as_posix(): hashlib.sha256(p.read_bytes()).hexdigest()
         for p in sorted(root.rglob('*')) if p.is_file()}
(root / 'manifest.json').write_text(json.dumps({'tested_sha': tip, 'environment_image_id': image,
                                                'exclusions': ['internal .git', 'Python caches'],
                                                'files': files}, indent=2) + '\n')
print('manifest files:', len(files))
PY
tar -C "$EVIDENCE" -czf "$(dirname "$BASE")/241250075-e10e12-evidence.tar.gz" .
( cd "$(dirname "$BASE")" && sha256sum 241250075-e10e12-evidence.tar.gz > transport.sha256 )
cp "$(dirname "$BASE")/run.log" "$META/run.log" 2>/dev/null
say "status:"; cat "$META/status.log"
echo "ALL_DONE $(date -u +%FT%TZ)"
