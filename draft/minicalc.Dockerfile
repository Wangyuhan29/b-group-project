# Candidate only: NOT BUILT or VERIFIED in the current environment.
# Build from the B project root, not from fixtures/minicalc/source.
FROM gcc:14-bookworm
RUN apt-get update && apt-get install -y --no-install-recommends python3 make && rm -rf /var/lib/apt/lists/*
WORKDIR /workspace/minicalc
COPY fixtures/minicalc/source/ /workspace/minicalc/
COPY scripts/verify_minicalc.py /opt/b-group/verify_minicalc.py
RUN make clean && make -j2 && python3 /opt/b-group/verify_minicalc.py .
CMD ["python3", "/opt/b-group/verify_minicalc.py", "."]
