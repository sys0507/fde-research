#!/usr/bin/env python3
"""Regressions for package encoding, shared-copy and installation-name checks."""
import ast
from pathlib import Path
import shutil
import tempfile
import unittest
import check_package

ROOT = Path(__file__).resolve().parents[1]


class PackageTests(unittest.TestCase):
    def test_text_encoding_and_binary_exemptions(self):
        bad = "a.read_text(); a.write_text('x'); open('x'); p.open('w', encoding=None)"
        self.assertEqual(len(check_package.encoding_issues(ast.parse(bad))), 4)
        good = "a.read_text('utf-8'); a.write_text('x', encoding='utf-8'); open('x','rb'); p.open('wb'); Image.open(p); pdfplumber.open(p); open('x',encoding=customer_encoding)"
        self.assertEqual(check_package.encoding_issues(ast.parse(good)), [])

    def test_subprocess_text_encoding(self):
        self.assertEqual(len(check_package.encoding_issues(ast.parse("subprocess.run(cmd, text=True)"))), 1)
        self.assertEqual(check_package.encoding_issues(ast.parse("subprocess.run(cmd,capture_output=True); subprocess.run(cmd,text=True,encoding='utf-8')")), [])

    def test_portable_vs_personal_home_paths(self):
        literal = 'C:/' + 'Users/' + 'private-person/project'
        self.assertTrue(check_package.personal_paths(literal))
        self.assertFalse(check_package.personal_paths('%USERPROFILE%/project; $env:USERPROFILE; ~/project'))

    def copy_package(self):
        temp = tempfile.TemporaryDirectory(prefix='fde-package-')
        self.addCleanup(temp.cleanup)
        root = Path(temp.name).resolve() / 'fde-research'
        self.assertTrue(root.is_relative_to(Path(temp.name).resolve()))
        shutil.copytree(ROOT, root, ignore=shutil.ignore_patterns('__pycache__', '*.pyc', '.git', '.github', 'validation'))
        return root

    def test_complete_installed_copy(self):
        report = check_package.check(self.copy_package(), installed=True)
        self.assertTrue(report['passed'], report['errors'])

    def test_wrong_installed_name_rejected(self):
        root = self.copy_package()
        renamed = root.with_name('old-folder')
        root.rename(renamed)
        self.assertFalse(check_package.check(renamed, installed=True)['passed'])
        self.assertTrue(check_package.check(renamed)['passed'])

    def test_shared_template_drift_rejected(self):
        root = self.copy_package()
        template = next((root/'fde-baseline-analysis/assets/templates').glob('*.md'))
        template.write_text(template.read_text(encoding='utf-8')+'\nChanged fixture\n',encoding='utf-8')
        self.assertTrue(any('Shared copies differ' in e for e in check_package.check(root)['errors']))

    def test_new_missing_encoding_rejected(self):
        root = self.copy_package()
        path = root/'plan-ai-project-delivery/scripts/index_inputs.py'
        path.write_text(path.read_text(encoding='utf-8').replace("read_text(encoding='utf-8')","read_text()",1),encoding='utf-8')
        self.assertTrue(any('explicit encoding' in e for e in check_package.check(root)['errors']))

    def test_runtime_environment_rejected_and_not_scanned(self):
        for name, marker in (('.venv', None), ('node_modules', None), ('tools-env', 'pyvenv.cfg')):
            with self.subTest(name=name):
                root = self.copy_package()
                env = root / name
                (env / 'lib').mkdir(parents=True)
                if marker:
                    (env / marker).write_text('home = /usr/bin\n', encoding='utf-8')
                # Third-party code inside the environment must not be linted as package code.
                (env / 'lib' / 'third_party.py').write_text("open('x').read()\n", encoding='utf-8')
                report = check_package.check(root)
                self.assertFalse(report['passed'])
                self.assertTrue(any('Runtime environment inside package: ' + name in e for e in report['errors']))
                self.assertFalse(any('third_party.py' in e for e in report['errors']))


if __name__ == '__main__':
    unittest.main()
