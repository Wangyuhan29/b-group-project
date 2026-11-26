"""Personal contract regression tests; independent expected outcomes."""
import hashlib
import json
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch
import pipeline
import server

class StudentContracts(unittest.TestCase):
    def test_restart_marks_interrupted_but_preserves_completed(self):
        with tempfile.TemporaryDirectory() as d:
            root=Path(d)
            for name,status in [('job-running','RUNNING'),('job-done','SUCCEEDED')]:
                pipeline.save(root/name/'state.json',dict(job_id=name,status=status,idempotency_key=name,request_hash='a'))
            store=server.Store(root)
            try:
                self.assertEqual(store.jobs['job-running']['error']['code'],'SERVER_RESTARTED')
                self.assertEqual(store.jobs['job-done']['status'],'SUCCEEDED')
                self.assertEqual(json.loads((root/'job-running/state.json').read_text())['status'],'FAILED')
            finally:store.pool.shutdown()
    def test_artifact_tampering_after_hash_is_rejected(self):
        with tempfile.TemporaryDirectory() as d:
            root=Path(d); p=root/'report.json'; p.write_text('{}')
            digest=hashlib.sha256(p.read_bytes()).hexdigest(); p.write_text('{"changed":true}')
            with self.assertRaises(pipeline.Failure) as caught:pipeline.load_artifact(p,digest)
            self.assertEqual(caught.exception.code,'ARTIFACT_HASH_MISMATCH')
