"""E10: buildable candidates retaining missing edges must not be accepted."""
import difflib
import tempfile
import unittest
from pathlib import Path
from lab import fixture, validate


class PersonalE10(unittest.TestCase):
    def test_buildable_candidate_with_remaining_md_rolls_back(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            project = root / 'project'
            fixture(project)
            before = (project / 'Makefile').read_bytes()
            # Removing RD is buildable, but deliberately does not repair config.h MD.
            changed = before.decode().replace('main.c unused.h', 'main.c')
            candidate = root / 'candidate.patch'
            candidate.write_text(''.join(difflib.unified_diff(
                before.decode().splitlines(True), changed.splitlines(True),
                fromfile='a/Makefile', tofile='b/Makefile')))
            result = validate(project, candidate, root / 'verdict')
            self.assertTrue(result['checks']['patch_applies'])
            self.assertTrue(result['checks']['build'])
            self.assertTrue(result['checks']['test'])
            self.assertFalse(result['checks']['no_missing'])
            self.assertFalse(result['accepted'])
            self.assertTrue(result['rollback'])
            self.assertTrue(result['source_unchanged'])
            self.assertEqual((project / 'Makefile').read_bytes(), before)


if __name__ == '__main__':
    unittest.main()
