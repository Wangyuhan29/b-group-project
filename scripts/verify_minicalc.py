#!/usr/bin/env python3
"""Assert actual outputs, unlike upstream make test which only prints them."""
from pathlib import Path
import subprocess
import sys
root=Path(sys.argv[1] if len(sys.argv)>1 else '.').resolve()
for expr,expected in [('1+2*3','7'),('10-4/2','8'),('3*(4+5)','27'),('--version','minicalc 1.0.0')]:
    p=subprocess.run([str(root/'minicalc'),expr],capture_output=True,text=True,timeout=10)
    if p.returncode!=0 or p.stdout.strip()!=expected:
        sys.exit(f'FAIL {expr}: code={p.returncode}, stdout={p.stdout!r}, stderr={p.stderr!r}')
    print(f'PASS {expr} => {expected}')
