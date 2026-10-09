#!/usr/bin/env python3
"""Real synthetic PDF text checks; no Office conversion or visual PASS claims."""
from pathlib import Path
import tempfile
import unittest
from pypdf import PdfWriter
from pypdf.generic import DictionaryObject, NameObject, DecodedStreamObject, ArrayObject, NumberObject
from check_pdf_fonts import inspect_pdf, parse_substitutions


class FontTests(unittest.TestCase):
    def setUp(self):
        temp = tempfile.TemporaryDirectory(prefix='fde-fonts-')
        self.addCleanup(temp.cleanup)
        self.root = Path(temp.name)

    def pdf(self, name='Helvetica', text=True):
        target = self.root/'fixture.pdf'
        writer = PdfWriter()
        page = writer.add_blank_page(width=300, height=400)
        if text:
            font = DictionaryObject({NameObject('/Type'): NameObject('/Font'),
                                     NameObject('/Subtype'): NameObject('/Type1'),
                                     NameObject('/BaseFont'): NameObject('/'+name)})
            descriptor = DictionaryObject({
                NameObject('/Type'): NameObject('/FontDescriptor'),
                NameObject('/FontName'): NameObject('/'+name),
                NameObject('/Flags'): NumberObject(32),
                NameObject('/FontBBox'): ArrayObject([NumberObject(n) for n in [-170,-225,1000,931]]),
                NameObject('/ItalicAngle'): NumberObject(0),
                NameObject('/Ascent'): NumberObject(718),
                NameObject('/Descent'): NumberObject(-207),
                NameObject('/CapHeight'): NumberObject(718),
                NameObject('/StemV'): NumberObject(88),
            })
            font[NameObject('/FontDescriptor')] = writer._add_object(descriptor)
            page[NameObject('/Resources')] = DictionaryObject({NameObject('/Font'): DictionaryObject({NameObject('/F1'): writer._add_object(font)})})
            stream = DecodedStreamObject()
            stream.set_data(b'BT /F1 12 Tf 30 300 Td (Font verification fixture) Tj ET')
            page[NameObject('/Contents')] = writer._add_object(stream)
        writer.write(target)
        return target

    def test_real_pdf_matching_family_and_embedding_evidence(self):
        result = inspect_pdf(self.pdf(), ['Helvetica'])
        self.assertEqual(result['status'], 'MATCHED')
        self.assertEqual(result['used_fonts'][0]['pages'], [1])
        self.assertFalse(result['font_resources'][0]['embedded'])
        self.assertEqual(len(result['pdf_sha256']),64)

    def test_silent_substitution_rejected(self):
        result = inspect_pdf(self.pdf(), ['Arial'])
        self.assertEqual(result['status'], 'MISMATCH')
        self.assertIn('helvetica', result['unexpected_families'])

    def test_explicit_substitution_recorded(self):
        result = inspect_pdf(self.pdf(), ['Arial'], parse_substitutions(['Arial=Helvetica']))
        self.assertEqual(result['status'], 'SUBSTITUTION_ACCEPTED')
        self.assertEqual(result['substitutions_used'], ['helvetica'])

    def test_image_only_or_empty_page_not_verified(self):
        result = inspect_pdf(self.pdf(text=False), ['Arial'])
        self.assertEqual(result['status'], 'UNVERIFIED')
        self.assertEqual(result['pages_without_inspectable_text'], [1])

    def test_subset_and_style_font_names(self):
        result = inspect_pdf(self.pdf(name='ABCDEF+Helvetica-Bold'), ['Helvetica'])
        self.assertEqual(result['status'], 'MATCHED')
        self.assertEqual(result['used_fonts'][0]['name'], 'ABCDEF+Helvetica-Bold')


if __name__ == '__main__':
    unittest.main()
