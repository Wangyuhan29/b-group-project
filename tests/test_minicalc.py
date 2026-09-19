import copy
import hashlib
import json
from pathlib import Path
import unittest
from scripts import minicalc as m


class MinicalcTests(unittest.TestCase):
    def report(self):
        return json.loads((m.ROOT/'contracts/minicalc/md-report.json').read_text())

    def test_snapshot_and_contracts(self):
        m.source_check();m.validate_suite(m.ROOT)

    def test_four_expected_md_edges(self):
        r=self.report()
        self.assertEqual({(f['target'],f['dependency']) for f in r['findings']},{('main.o','include/token.h'),('main.o','include/util.h'),('parser.o','include/config.h'),('parser.o','include/token.h')})
        self.assertTrue(all(f['type']=='MISSING' for f in r['findings']))
        self.assertEqual(r['repository']['commit'],m.source_check()['commits']['C2'])

    def test_id_golden_vector(self):
        v=json.loads((m.ROOT/'contracts/finding-id-v1.json').read_text())['test_vector']
        self.assertEqual(m.finding_id(*v['fields']),v['finding_id'])
        self.assertEqual(json.dumps(v['fields'],ensure_ascii=False,separators=(',',':')),v['canonical_utf8_text'])

    def test_id_changes_for_config_or_type(self):
        a=['repo','cc-default','MISSING','main.o','include/token.h']
        x=m.finding_id(*a);a[1]='other';self.assertNotEqual(m.finding_id(*a),x)
        a[1]='cc-default';a[2]='REDUNDANT';self.assertNotEqual(m.finding_id(*a),x)

    def test_patch_only_adds_expected_dependencies(self):
        before=(m.ROOT/'fixtures/minicalc/source/Makefile').read_text()
        after=m.repair_text(before,self.report()['findings'])
        changed=[(a,b) for a,b in zip(before.splitlines(),after.splitlines()) if a!=b]
        self.assertEqual(len(changed),2)
        for a,b in changed:self.assertTrue(a.startswith(('main.o:','parser.o:')))
        self.assertEqual(m.repair_text(after,self.report()['findings']),after)

    def test_repair_rejects_rd_and_path_escape(self):
        before=(m.ROOT/'fixtures/minicalc/source/Makefile').read_text()
        for key,value in [('type','REDUNDANT'),('dependency','../private.h')]:
            findings=copy.deepcopy(self.report()['findings']);findings[0][key]=value
            with self.assertRaises(ValueError):m.repair_text(before,findings)

    def test_ambiguous_rule_rejected(self):
        before=(m.ROOT/'fixtures/minicalc/source/Makefile').read_text()+'\nmain.o: src/main.c\n'
        with self.assertRaises(ValueError):m.repair_text(before,self.report()['findings'])

    def test_patch_overlay_evidence_matches_patch(self):
        root=m.ROOT/'artifacts/minicalc/c2'
        evidence=json.loads((root/'recheck-evidence.json').read_text())
        self.assertEqual(evidence['patch_sha256'],hashlib.sha256((root/'fix.patch').read_bytes()).hexdigest())
        self.assertEqual(evidence['base_commit'],self.report()['repository']['commit'])
