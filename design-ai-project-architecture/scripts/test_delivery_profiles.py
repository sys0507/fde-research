#!/usr/bin/env python3
"""Check diagram profile routing with synthetic fixtures; no visual acceptance."""
import hashlib
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest
from zipfile import ZipFile

SCRIPT = Path(__file__).with_name('check_delivery.py')


class DiagramProfileTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory(prefix='fde-diagram-test-')
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        self.manifest = {'schema_version': 1, 'diagram_profile': 'standard', 'artifacts': []}
        for role in ('conditions','report_source','research','decisions','inputs','diagram_spec','diagram_visual','word_visual'):
            self.add(role, role + '.md', b'Explicit test fixture only')
        self.add('diagram_static', 'diagram.svg', b'<svg xmlns="http://www.w3.org/2000/svg"><text>Fixture</text></svg>')
        self.add('question_state', 'questions.json', json.dumps({'round_limit':20,'questions':[]}).encode())
        report = self.root / 'report.docx'
        with ZipFile(report, 'w') as archive:
            archive.writestr('word/document.xml', '<document/>')
        self.add('report','report.docx',report.read_bytes())

    def add(self, role, name, content):
        (self.root / name).write_bytes(content)
        self.manifest['artifacts'].append({'role':role,'path':name,'sha256':hashlib.sha256(content).hexdigest()})

    def run_check(self):
        target = self.root / 'manifest.json'
        target.write_text(json.dumps(self.manifest), encoding='utf-8')
        result = subprocess.run([sys.executable, '-X', 'utf8', str(SCRIPT), str(target)], capture_output=True, text=True, encoding='utf-8')
        return result.returncode, json.loads(result.stdout)

    def test_standard_accepts_no_archify_receipt(self):
        self.assertEqual(self.run_check()[0],0)

    def test_legacy_manifest_still_requires_archify(self):
        del self.manifest['diagram_profile']
        code, result = self.run_check()
        self.assertNotEqual(code,0)
        self.assertIn('Missing artifact role: diagram_receipt',result['errors'])

    def test_standard_still_requires_actual_static_and_word_evidence(self):
        self.manifest['artifacts'] = [item for item in self.manifest['artifacts'] if item['role'] not in ('diagram_static','word_visual')]
        code, result = self.run_check()
        self.assertNotEqual(code,0)
        self.assertIn('Missing artifact role: diagram_static',result['errors'])
        self.assertIn('Missing artifact role: word_visual',result['errors'])

    def test_wrong_profile_is_rejected(self):
        self.manifest['diagram_profile']='archfy'
        self.assertNotEqual(self.run_check()[0],0)

    def test_hash_change_is_rejected(self):
        (self.root / 'diagram.svg').write_bytes(b'changed')
        self.assertNotEqual(self.run_check()[0],0)


if __name__ == '__main__':
    unittest.main()
