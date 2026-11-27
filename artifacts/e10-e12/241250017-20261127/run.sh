#!/bin/bash
set -eu
cd /root/241250017/e10-e12-20261127
out=work/241250017-e10-e12
docker image inspect course-e11e12:241250017 > "$out/image-inspect.json"
image=$(docker image inspect course-e11e12:241250017 --format '{{.Id}}')
printf '%s\n' "$image" > "$out/image-id.txt"
args=(--rm --cap-add SYS_PTRACE --cpus 1 --memory 768m --pids-limit 512 --user 0:0 -e HOME=/tmp -e PYTHONPATH=/course/labs/e11e12:/course/labs/e8e10:/course/labs/e11e12/vendor:/app -v "$PWD:/course" -w /course)
run_step() { name=$1; shift; set +e; "$@" > "$out/$name.log" 2>&1; code=$?; set -e; echo "$name=$code" >> "$out/status.log"; test "$code" -eq 0; }
run_step tools docker run "${args[@]}" --network none "$image" bash -c 'git --version; gcc --version; make --version; strace --version; python3 --version; uname -a'
run_step e10-tests docker run "${args[@]}" --network none "$image" python3 -m unittest discover -s labs/e8e10 -p 'test*.py' -v
run_step contract-tests docker run "${args[@]}" --network none "$image" python3 -m unittest discover -s labs/e11e12 -p 'test*.py' -v
run_step e10 docker run "${args[@]}" --network none "$image" python3 labs/e8e10/lab.py e10 --track B --out "$out/e10"
run_step integration docker run "${args[@]}" --network bridge -v /var/run/docker.sock:/var/run/docker.sock -e COURSE_BASE_IMAGE=m.daocloud.io/docker.io/library/python -e COURSE_DEBIAN_MIRROR=mirrors.huaweicloud.com "$image" python3 labs/e11e12/verify_241250017.py --out "$out/integration"
git rev-parse HEAD > "$out/tested-sha.txt"
git status --porcelain > "$out/source-status-after.txt"
echo COMPLETED
