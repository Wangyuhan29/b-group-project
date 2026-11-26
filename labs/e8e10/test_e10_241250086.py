import tempfile
import unittest
from pathlib import Path
from lab import fixture,scan,patch,validate

class E10Personal(unittest.TestCase):
    def test_compilation_failure_never_changes_source(self):
        with tempfile.TemporaryDirectory() as d:
            root=Path(d); p=root/'project'; fixture(p)
            before=(p/'Makefile').read_bytes()
            diff,_=patch(p,scan(p))
            # Independently force a compiler syntax error through a make flag.
            text=(p/'Makefile').read_text().replace('CFLAGS = -O0','CFLAGS = -O0 -include absent.h')
            import difflib
            candidate=root/'candidate.patch'
            candidate.write_text(''.join(difflib.unified_diff(before.decode().splitlines(True),text.splitlines(True),fromfile='a/Makefile',tofile='b/Makefile')))
            result=validate(p,candidate,root/'reject')
            self.assertFalse(result['accepted'])
            self.assertTrue(result['rollback'])
            self.assertEqual((p/'Makefile').read_bytes(),before)
