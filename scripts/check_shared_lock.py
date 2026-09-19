#!/usr/bin/env python3
"""Check the exact bytes shared by A/B, without changing the lock."""
import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def main():
    lock = json.loads((ROOT / 'contracts/shared-lock.json').read_text())
    files = lock['files']
    required = {'contracts/graph.schema.json', 'contracts/finding-id-v1.json'}
    if not required <= files.keys():
        raise SystemExit('FAIL: missing graph or finding ID contract in shared lock')
    for relative, expected in files.items():
        path = (ROOT / relative).resolve()
        if not path.is_relative_to(ROOT) or not path.is_file():
            raise SystemExit(f'FAIL: missing or invalid locked file {relative}')
        if hashlib.sha256(path.read_bytes()).hexdigest() != expected:
            raise SystemExit(f'FAIL: shared contract changed: {relative}')
    print(f'PASS: {len(files)} shared files match SHA-256 lock')


if __name__ == '__main__':
    main()
