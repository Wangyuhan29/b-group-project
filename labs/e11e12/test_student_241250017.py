"""E12: transfer integrity is byte based, not JSON semantic equality."""
import hashlib
import json
import tempfile
import unittest
from pathlib import Path
import pipeline


class PersonalArtifactContract(unittest.TestCase):
    def test_json_whitespace_change_invalidates_original_digest(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / 'report.json'
            report = {'schema_version': 'e11e12-1', 'kind': 'incremental-check',
                      'commit': 'a' * 40, 'status': 'SUCCEEDED'}
            path.write_text(json.dumps(report, separators=(',', ':')))
            digest = hashlib.sha256(path.read_bytes()).hexdigest()
            self.assertEqual(pipeline.load_artifact(path, digest), report)
            path.write_text(json.dumps(report, indent=2) + '\n')
            self.assertEqual(json.loads(path.read_text()), report)
            with self.assertRaises(pipeline.Failure) as caught:
                pipeline.load_artifact(path, digest)
            self.assertEqual(caught.exception.code, 'ARTIFACT_HASH_MISMATCH')
            updated_digest = hashlib.sha256(path.read_bytes()).hexdigest()
            loaded = pipeline.load_artifact(path, updated_digest)
            pipeline.check_envelope(loaded, 'a' * 40, 'incremental-check')


if __name__ == '__main__':
    unittest.main()
