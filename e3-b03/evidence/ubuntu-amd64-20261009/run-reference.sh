#!/bin/bash
cd ~/b03-e3-validation/draft || exit 1
E=../evidence
sudo docker build --platform linux/amd64 -f Dockerfile.reference -t b03-e3-draft-reference:amd64 . > "$E/reference-build.log" 2>&1
rc=$?; echo "$rc" > "$E/reference-build.exit"
if [ "$rc" -ne 0 ]; then tail -20 "$E/reference-build.log"; exit 1; fi
sudo docker run --rm --platform linux/amd64 b03-e3-draft-reference:amd64 > "$E/reference-run.log" 2>&1
rc=$?; echo "$rc" > "$E/reference-run.exit"
sudo docker image inspect b03-e3-draft-reference:amd64 > "$E/reference-image.json"
sudo docker image inspect python:3.13-slim > "$E/base-image.json"
cat "$E/reference-run.log"
test "$rc" -eq 0 && test "$(cat "$E/reference-run.log")" = 'hello E3' && echo 'REFERENCE PASS'
