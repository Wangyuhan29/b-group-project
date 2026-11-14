"""241250075: E8 macro-definition loss rejection and patch fixed point; E9 mixed style isolation."""
import shutil
import tempfile
import unittest
from pathlib import Path
from lab import commit, fixture, patch, run, scan


class PersonalTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.project = Path(self.temp.name) / 'project'

    def test_e8_missing_macro_definition_rejected_without_writes(self):
        fixture(self.project, 'macro')
        report = scan(self.project)
        text = (self.project / 'Makefile').read_text()
        (self.project / 'Makefile').write_text(
            '\n'.join(line for line in text.splitlines() if not line.startswith('DEPS = ')) + '\n')
        report['commit'] = run(['git', 'rev-parse', 'HEAD'], self.project).strip()
        report['findings'] = [{'type': 'MISSING', 'target': 'main.o', 'dependency': 'config.h'}]
        modified = (self.project / 'Makefile').read_bytes()
        with self.assertRaisesRegex(ValueError, '^UNSUPPORTED_MACRO$'):
            patch(self.project, report)
        self.assertEqual((self.project / 'Makefile').read_bytes(), modified)
        (self.project / 'Makefile').write_text(text)
        self.assertEqual(run(['git', 'status', '--porcelain'], self.project), '')

    def test_e8_patch_reaches_fixed_point_after_apply(self):
        fixture(self.project)
        report = scan(self.project)
        diff, plan = patch(self.project, report)
        self.assertEqual(len(plan), 1)
        out = Path(self.temp.name) / 'candidate.patch'
        out.write_text(diff)
        copy = Path(self.temp.name) / 'copy'
        shutil.copytree(self.project, copy)
        run(['git', 'apply', str(out.resolve())], copy)
        rereport = scan(copy)
        self.assertFalse(any(f['type'] == 'MISSING' for f in rereport['findings']))
        rediff, replan = patch(copy, rereport)
        self.assertEqual((rediff, replan), ('', []))
        self.assertEqual(run(['git', 'status', '--porcelain'], self.project), '')

    def test_e9_mixed_patch_adds_only_target_dependency(self):
        fixture(self.project, 'mixed')
        before = (self.project / 'Makefile').read_bytes()
        diff, plan = patch(self.project, scan(self.project))
        self.assertEqual(plan, [{'target': 'main.o', 'dependency': 'config.h', 'style': 'mixed'}])
        changed = [line for line in diff.splitlines() if line.startswith(('+', '-')) and not line.startswith(('+++', '---'))]
        self.assertEqual(changed, ['-main.o: main.c $(HEADERS)', '+main.o: main.c $(HEADERS) config.h'])
        self.assertIn('+main.o: main.c $(HEADERS) config.h\n', diff)
        self.assertNotIn('HEADERS =', '\n'.join(line for line in diff.splitlines() if line.startswith(('+', '-'))))
        self.assertNotIn('-\t', diff)
        self.assertNotIn('+DEPS', diff)
        self.assertEqual((self.project / 'Makefile').read_bytes(), before)
        self.assertEqual(run(['git', 'status', '--porcelain'], self.project), '')


if __name__ == '__main__':
    unittest.main()
