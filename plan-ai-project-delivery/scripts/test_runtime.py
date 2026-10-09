#!/usr/bin/env python3
"""Portable runtime contract tests; mocked Office conversion is NOT end-to-end QA.

Run with the Word dependencies installed. Fixtures live only in temporary dirs.
"""
import argparse
import contextlib
import io
import json
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
import unittest
from unittest.mock import patch
from zipfile import ZipFile

import estimate
import inherit_baseline
import check_delivery
import finalize_word
import render_word_generic
from pypdf import PdfWriter

ROOT = Path(__file__).resolve().parents[1]


class RuntimeTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory(prefix='fde-runtime-test-')
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)

    def test_renderer_rasterizes_each_page_and_does_not_touch_source(self):
        source = self.root / 'source-document.docx'
        source.write_bytes(b'test fixture; converter is mocked')
        original = source.read_bytes()
        fixture_pdf = self.root / 'fixture.pdf'
        writer = PdfWriter()
        writer.add_blank_page(width=300, height=400)
        writer.add_blank_page(width=400, height=300)
        writer.write(fixture_pdf)
        output = self.root / 'rendered'

        def office(command, **kwargs):
            self.assertIn('--headless', command)
            self.assertTrue(any(x.startswith('-env:UserInstallation=file:') for x in command))
            self.assertEqual(command[-1], str(source.resolve()))
            self.assertFalse(kwargs.get('shell', False))
            target = Path(command[command.index('--outdir') + 1])
            shutil.copyfile(fixture_pdf, target / (source.stem + '.pdf'))
            return subprocess.CompletedProcess(command, 0, 'mock conversion', '')

        with patch.object(render_word_generic.subprocess, 'run', side_effect=office):
            result = render_word_generic.render(source, output, sys.executable)
        self.assertEqual(result['page_count'], 2)
        self.assertEqual(result['status'], 'RENDERED_VISUAL_REVIEW_REQUIRED')
        from PIL import Image
        with Image.open(output / 'page-1.png') as first:
            self.assertEqual(first.size, (600, 800))
        with Image.open(output / 'page-2.png') as second:
            self.assertEqual(second.size, (800, 600))
        self.assertEqual(source.read_bytes(), original)
        with self.assertRaisesRegex(ValueError, 'new or empty'):
            render_word_generic.render(source, output, sys.executable)

    def test_missing_libreoffice_is_not_silent_success(self):
        source = self.root / 'input.docx'
        source.write_bytes(b'fixture')
        with self.assertRaisesRegex(ValueError, 'not found'):
            render_word_generic.render(source, self.root / 'missing', str(self.root / 'no-office'))
        self.assertFalse((self.root / 'missing').exists())

    def test_codex_cannot_silently_use_generic_soffice(self):
        runtime = self.root / 'runtime'
        runtime.mkdir()
        (runtime / 'soffice').write_text('fixture', encoding='utf-8')
        args = argparse.Namespace(docx=self.root / 'x.docx', output_dir=self.root / 'qa',
                                  renderer=Path(__file__), runtime_bin=runtime,
                                  renderer_mode='codex', soffice='unapproved-other-office', font_dir=[])
        with self.assertRaisesRegex(ValueError, 'only for.*generic'):
            finalize_word.finalize(args)
        self.assertFalse(args.output_dir.exists())

    def test_generic_requires_explicit_office(self):
        args = argparse.Namespace(docx=self.root / 'x.docx', output_dir=self.root / 'qa',
                                  renderer=Path(__file__), runtime_bin=None,
                                  renderer_mode='generic', soffice=None, font_dir=[])
        with self.assertRaisesRegex(ValueError, 'requires --soffice'):
            finalize_word.finalize(args)
        self.assertFalse(args.output_dir.exists())

    def test_bad_office_path_does_not_change_document(self):
        source=self.root/'input.docx'
        source.write_bytes(b'preserve this fixture')
        args=argparse.Namespace(docx=source,output_dir=self.root/'qa',renderer=Path(__file__),
                                runtime_bin=None,renderer_mode='generic',
                                soffice=str(self.root/'no-office'),font_dir=[])
        with self.assertRaisesRegex(ValueError,'not found'):
            finalize_word.finalize(args)
        self.assertEqual(source.read_bytes(),b'preserve this fixture')
        self.assertFalse(args.output_dir.exists())

    def prepare_delivery(self):
        output = self.root / 'v001'
        result = estimate.run(ROOT / 'assets/example-model.json', output)
        token = next(iter(result['public_facts']))
        template = self.root / 'source.md'
        template.write_text('# Fixture\n\n{{' + token + '}}\n', encoding='utf-8')
        md = output / 'client/report.md'
        estimate.render(output / 'results.json', template, md)
        docx = output / 'client/report.docx'
        # Minimal editable archive for provenance checks, not a visual fixture.
        with ZipFile(docx, 'w') as archive:
            archive.writestr('word/document.xml', '<document/>')
        receipt = {'source_sha256': check_delivery.sha(md), 'sha256': check_delivery.sha(docx)}
        docx.with_suffix('.build.json').write_text(json.dumps(receipt), encoding='utf-8')
        return argparse.Namespace(root=output, markdown='client/report.md',
                                  docx='client/report.docx', qa=None)

    def test_delivery_provenance_and_windows_client_classification(self):
        args = self.prepare_delivery()
        with contextlib.redirect_stdout(io.StringIO()):
            check_delivery.check(args)
        index = json.loads((args.root / 'delivery-index.json').read_text(encoding='utf-8'))
        entries = {item['path']: item for item in index['artifacts']}
        self.assertEqual(entries['client/report.docx']['visibility'], 'client')
        self.assertEqual(entries['client/report.md']['visibility'], 'client')
        self.assertEqual(entries['client/report.build.json']['visibility'], 'internal')
        self.assertEqual(entries['model.json']['visibility'], 'internal')
        self.assertEqual(index['word_state'], 'BUILT_NOT_VISUALLY_VERIFIED')

    def test_changed_word_is_rejected(self):
        args = self.prepare_delivery()
        (args.root / args.docx).write_bytes(b'changed fixture')
        with self.assertRaisesRegex(ValueError, 'hash mismatch'):
            check_delivery.check(args)
        self.assertFalse((args.root / 'delivery-index.json').exists())

    def prepare_inherited(self):
        source=self.root/'proposal.txt'
        source.write_text('Fixture agreed estimate 123.45; internal cost 50',encoding='utf-8')
        data={'adoption_instruction':'Preserve this synthetic fixture estimate',
              'sources':[{'id':'S1','path':source.name}],
              'facts':{key:{'source_id':'S1','locator':'line 1','visibility':visibility,
                            'status':'adopted_estimate','unit':'CNY','value':value}
                       for key,value,visibility in [('price','123.45','client'),('cost','50','internal')]},
              'scope_review':{'conclusion':'Same synthetic test scope','changes':[],'conflicts':[],'missing_details':[]}}
        input_path=self.root/'adopt.json'
        input_path.write_text(json.dumps(data),encoding='utf-8')
        output=self.root/'inherited'
        with contextlib.redirect_stdout(io.StringIO()):
            inherit_baseline.adopt(argparse.Namespace(input=input_path,source_root=self.root,output=output))
        return output

    def test_inherited_price_and_portable_provenance(self):
        output=self.prepare_inherited()
        template=output/'internal/report-source.md'
        template.write_text('Service {{baseline.price}}',encoding='utf-8')
        with contextlib.redirect_stdout(io.StringIO()):
            inherit_baseline.render(argparse.Namespace(root=output,template='internal/report-source.md',output='client/report.md'))
        self.assertEqual((output/'client/report.md').read_text(encoding='utf-8'),'Service 123.45')
        self.assertFalse((output/'model.json').exists())
        data=inherit_baseline.check(output)
        self.assertEqual(data['facts']['price']['value'],'123.45')
        self.assertNotIn('\\',data['sources'][0]['snapshot'])

    def test_internal_inherited_cost_cannot_leak_into_client_report(self):
        output=self.prepare_inherited()
        (output/'internal/source.md').write_text('Cost {{baseline.cost}}',encoding='utf-8')
        with self.assertRaisesRegex(ValueError,'Internal fact'):
            inherit_baseline.render(argparse.Namespace(root=output,template='internal/source.md',output='client/leak.md'))
        self.assertFalse((output/'client/leak.md').exists())


if __name__ == '__main__':
    unittest.main()
