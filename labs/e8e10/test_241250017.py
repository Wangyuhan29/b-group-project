"""241250017: E8 absent input rejection and E9 macro-only modification."""
import tempfile
import unittest
from pathlib import Path
from lab import fixture, scan, patch, run


class PersonalTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.project = Path(self.temp.name) / 'project'

    def test_e8_nonexistent_input_rejected_without_writes(self):
        fixture(self.project)
        report = scan(self.project)
        report['findings'] = [{'type': 'MISSING', 'target': 'main.o', 'dependency': 'absent.h'}]
        before = {p.name: p.read_bytes() for p in self.project.iterdir() if p.is_file()}
        with self.assertRaisesRegex(ValueError, '^MISSING_INPUT$'):
            patch(self.project, report)
        self.assertEqual(before, {p.name: p.read_bytes() for p in self.project.iterdir() if p.is_file()})
        self.assertEqual(run(['git', 'status', '--porcelain'], self.project), '')

    def test_e9_macro_patch_preserves_rule_and_recipes(self):
        fixture(self.project, 'macro')
        before = (self.project / 'Makefile').read_bytes()
        diff, plan = patch(self.project, scan(self.project))
        self.assertEqual(plan, [{'target': 'main.o', 'dependency': 'config.h', 'style': 'macro'}])
        self.assertIn('+DEPS = main.c unused.h config.h\n', diff)
        self.assertNotIn('-main.o:', diff)
        self.assertNotIn('+main.o:', diff)
        self.assertFalse(any(line.startswith(('+\t', '-\t')) for line in diff.splitlines()))
        self.assertEqual((self.project / 'Makefile').read_bytes(), before)
        self.assertEqual(run(['git', 'status', '--porcelain'], self.project), '')


if __name__ == '__main__':
    unittest.main()
