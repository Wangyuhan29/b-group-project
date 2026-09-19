import json
from pathlib import Path
import unittest
import validate as v


class ContractTests(unittest.TestCase):
    def load(self, name):
        return json.loads((v.ROOT / 'contracts/examples' / (name+'.json')).read_text())

    def rejects(self, doc, code):
        with self.assertRaises(v.Invalid) as cm:
            v.validate(doc)
        self.assertEqual(cm.exception.code, code)

    def test_all_samples_and_artifacts(self):
        v.audit_schema(v.SCHEMA)
        v.all_examples()

    def test_server_controls_job_id(self):
        doc = self.load('draft-request'); doc['job_id'] = 'client-supplied'
        self.rejects(doc, 'INPUT_1001')

    def test_failed_job_cannot_carry_success_output(self):
        doc = self.load('draft-response'); doc['status'] = 'FAILED'
        self.rejects(doc, 'INPUT_1001')

    def test_report_finding_commit_must_match(self):
        doc = self.load('md-report'); doc['findings'][0]['commit'] = '0'*40
        self.rejects(doc, 'INPUT_1002')

    def test_bool_is_not_timeout_integer(self):
        doc = self.load('draft-request'); doc['execution']['timeout_seconds'] = True
        self.rejects(doc, 'INPUT_1001')

    def test_repair_checks_report_configuration(self):
        doc = self.load('repair-request'); doc['input']['environment']['configuration_id'] = 'different'
        self.rejects(doc, 'INPUT_1003')

    def test_evidence_matches_type(self):
        doc = self.load('md-report'); doc['findings'][0]['type'] = 'REDUNDANT'
        self.rejects(doc, 'INPUT_1001')

    def test_recheck_count_matches_artifact(self):
        doc = self.load('repair-response')
        doc['output'].update(accepted=False,rejection_reason='MD remains')
        doc['output']['recheck_result'].update(passed=False,remaining_missing_count=1)
        self.rejects(doc, 'REPAIR_6001')

    def test_reject_empty_reason(self):
        doc = self.load('repair-rejected-response'); doc['output']['rejection_reason'] = ''
        self.rejects(doc, 'REPAIR_6001')

    def test_artifact_traversal(self):
        with self.assertRaises(v.Invalid):
            v.read_artifact('artifact://demo/../../README.md')

    def test_unknown_schema_keyword_fails_closed(self):
        with self.assertRaises(RuntimeError):
            v.audit_schema({'type':'object','mystery':True})

    def test_openapi_reuses_same_definitions(self):
        api=json.loads((v.ROOT/'contracts/openapi.json').read_text())
        for name, definition in v.SCHEMA['$defs'].items():
            expected=json.loads(json.dumps(definition).replace('#/$defs/','#/components/schemas/'))
            self.assertEqual(api['components']['schemas'][name],expected)
        self.assertEqual(len(api['paths']),5)

    def test_fixture_bundle_matches_source(self):
        import subprocess, tempfile
        with tempfile.TemporaryDirectory() as tmp:
            subprocess.run(['git','clone','--quiet',str(v.ROOT/'fixtures/source.bundle'),tmp],check=True)
            sha=subprocess.check_output(['git','-C',tmp,'rev-parse','HEAD'],text=True).strip()
            self.assertEqual(sha,self.load('md-report')['repository']['commit'])
            for p in (v.ROOT/'fixtures/draft-project').iterdir():
                self.assertEqual(p.read_bytes(),(Path(tmp)/p.name).read_bytes())

class BoundaryTests(unittest.TestCase):
    def test_const_true_rejects_numeric_one(self):
        doc=json.loads((v.ROOT/'contracts/examples/repair-request.json').read_text())
        doc['input']['recheck']['required']=1
        with self.assertRaises(v.Invalid): v.validate(doc)

    def test_report_contents_cannot_sneak_in_rd(self):
        from unittest.mock import patch
        import tempfile
        doc=json.loads((v.ROOT/'contracts/examples/repair-request.json').read_text())
        report=json.loads((v.ROOT/'contracts/examples/rd-report.json').read_text())
        with tempfile.TemporaryDirectory() as tmp:
            p=Path(tmp)/'report.json'; p.write_text(json.dumps(report))
            meta={'type':'ERROR_REPORT','repository':report['repository'],'configuration_id':report['configuration_id']}
            with patch.object(v,'read_artifact',return_value=(p,meta)):
                with self.assertRaises(v.Invalid) as cm: v.validate(doc)
                self.assertEqual(cm.exception.code,'INPUT_1004')

    def test_wrong_graph_artifact_type_is_rejected(self):
        doc=json.loads((v.ROOT/'contracts/examples/incremental-request.json').read_text())
        doc['input']['baseline']['actual_graph_uri']='artifact://demo/md-report.json'
        with self.assertRaises(v.Invalid) as cm: v.validate(doc)
        self.assertEqual(cm.exception.code,'INPUT_1004')

    def test_timeout_requires_timeout_error(self):
        doc=json.loads((v.ROOT/'contracts/examples/draft-timed_out.json').read_text())
        doc['error']['code']='ENV_3002'
        with self.assertRaises(v.Invalid): v.validate(doc)

    def test_contract_patch_applies(self):
        import subprocess, tempfile
        with tempfile.TemporaryDirectory() as tmp:
            subprocess.run(['git','clone','--quiet',str(v.ROOT/'fixtures/source.bundle'),tmp],check=True)
            subprocess.run(['git','-C',tmp,'apply','--check',str(v.ROOT/'artifacts/demo/fix.patch')],check=True)


if __name__ == '__main__':
    unittest.main()
