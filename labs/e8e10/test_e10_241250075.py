"""241250075: E10 candidates that leave a dependency missing or fail to compile are rolled back."""
import json
import tempfile
import unittest
from pathlib import Path
from lab import patch, run, scan, validate
from verify_e10_241250075 import CANDIDATES, candidate_patch, target


class PersonalTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.project = Path(self.temp.name) / 'project'

    def rejected(self, name):
        """Run the named candidate; the verdict must be a rollback that leaves the source untouched."""
        spec = next(c for c in CANDIDATES if c['name'] == name)
        evidence = Path(self.temp.name) / name
        target(self.project)
        before = (self.project / 'Makefile').read_bytes()
        candidate = Path(self.temp.name) / (name + '.patch')
        candidate_patch(self.project, spec, candidate)
        verdict = validate(self.project, candidate, evidence)
        self.assertFalse(verdict['accepted'])
        self.assertTrue(verdict['rollback'])
        self.assertTrue(verdict['source_unchanged'])
        self.assertEqual((self.project / 'Makefile').read_bytes(), before)
        self.assertEqual(run(['git', 'status', '--porcelain'], self.project), '')
        return verdict, evidence

    def test_e10_partial_repair_keeps_md_and_is_rolled_back(self):
        verdict, evidence = self.rejected('partial-md')
        # Build, run and header-change checks pass; only the recheck detects the omitted extra.h.
        self.assertEqual(verdict['checks'], {'patch_applies': True, 'build': True, 'test': True,
                                             'header_change': True, 'no_missing': False})
        self.assertIsNone(verdict['error'])
        recheck = json.loads((evidence / 'recheck.json').read_text())
        self.assertEqual([(f['target'], f['dependency']) for f in recheck['findings'] if f['type'] == 'MISSING'],
                         [('main.o', 'extra.h')])
        # Control: the candidate that also declares extra.h is accepted and written back.
        control = Path(self.temp.name) / 'control'
        target(control)
        complete, _ = patch(control, scan(control))
        (Path(self.temp.name) / 'complete.patch').write_text(complete)
        accepted = validate(control, Path(self.temp.name) / 'complete.patch', control.parent / 'accept')
        self.assertTrue(accepted['accepted'])
        self.assertFalse(accepted['rollback'])

    def test_e10_candidate_failing_to_compile_is_rolled_back(self):
        verdict, _ = self.rejected('compile-failure')
        # The patch applies; the rejection happens in the build and records the compiler diagnostic.
        self.assertEqual(verdict['checks'], {'patch_applies': True})
        self.assertIn('COMMAND_FAILED', verdict['error'])
        self.assertIn('no include path in which to search for stdio.h', verdict['error'])


if __name__ == '__main__':
    unittest.main()
