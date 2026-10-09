#!/usr/bin/env python3
"""Inspect font availability or fonts actually used by text in a rendered PDF.

Matching names is a font check only, never visual acceptance. No fonts are
installed, documents changed, or online services contacted. Requires pdfplumber
and pypdf for PDF inspection; availability probing uses local OS tools.
"""
import argparse
import hashlib
import json
import os
from pathlib import Path
import re
import shutil
import subprocess


def family(name):
    value = re.sub(r'^[A-Z]{6}\+', '', str(name).lstrip('/'))
    value = re.sub(r'\((?:TrueType|OpenType)\)', '', value, flags=re.I)
    value = re.sub(r'[\s,_-]+', '', value).casefold()
    # PostScript style suffixes; no alias maps Arial to Helvetica or Liberation.
    value = re.sub(r'(?:bolditalic|boldoblique|bold|italic|oblique|regular)(?:mt|psmt|ps)?$', '', value)
    value = re.sub(r'(?:psmt|mt)$', '', value)
    aliases = {
        '\u5b8b\u4f53': 'simsun', '\u65b0\u5b8b\u4f53': 'nsimsun',
        '\u9ed1\u4f53': 'simhei', '\u7b49\u7ebf': 'dengxian',
        '\u5fae\u8f6f\u96c5\u9ed1': 'microsoftyahei',
        'timesnewromanps': 'timesnewroman',
    }
    return aliases.get(value, value)


def parse_substitutions(values):
    result = {}
    for value in values:
        if '=' not in value:
            raise ValueError('Substitution must be requested-family=accepted-family')
        expected, actual = value.split('=', 1)
        if not expected.strip() or not actual.strip():
            raise ValueError('Substitution families must be nonempty')
        result.setdefault(family(expected), set()).add(family(actual))
    return result


def local_inventory():
    names, sources, notes = set(), [], []
    if os.name == 'nt':
        import winreg
        for hive, label in [(winreg.HKEY_LOCAL_MACHINE, 'system'), (winreg.HKEY_CURRENT_USER, 'user')]:
            try:
                with winreg.OpenKey(hive, r'SOFTWARE\Microsoft\Windows NT\CurrentVersion\Fonts') as key:
                    for index in range(winreg.QueryInfoKey(key)[1]):
                        label_value = winreg.EnumValue(key, index)[0]
                        names.update(x.strip() for x in label_value.split('&'))
                sources.append('Windows font registry: ' + label)
            except OSError:
                notes.append('No accessible ' + label + ' font registry')
    executable = shutil.which('fc-list')
    if executable:
        proc = subprocess.run([executable, '--format', '%{family}\n'], capture_output=True,
                              text=True, encoding='utf-8', errors='replace', timeout=20)
        if proc.returncode == 0:
            names.update(n.strip() for line in proc.stdout.splitlines() for n in line.split(',') if n.strip())
            sources.append('fontconfig fc-list')
    return names, sources, notes


def preflight(expected, substitutions=None):
    names, sources, notes = local_inventory()
    available = {family(n) for n in names}
    substitutions = substitutions or {}
    matches = {}
    for name in expected:
        accepted = {family(name)} | substitutions.get(family(name), set())
        matches[name] = sorted(accepted & available)
    return {
        'status': 'UNVERIFIED' if not names else 'AVAILABLE' if all(matches.values()) else 'MISSING',
        'expected': expected, 'matches': matches, 'sources': sources, 'notes': notes,
        'scope': 'Local font registration only; renderer discovery and actual PDF still require verification.',
    }


def resource_fonts(reader):
    records, seen = {}, set()
    def visit(resources):
        if not resources:
            return
        resources = resources.get_object()
        if id(resources) in seen:
            return
        seen.add(id(resources))
        fonts = resources.get('/Font', {})
        fonts = fonts.get_object() if hasattr(fonts, 'get_object') else fonts
        for ref in fonts.values():
            font = ref.get_object()
            descendants = font.get('/DescendantFonts', [])
            child = descendants[0].get_object() if descendants else font
            descriptor = child.get('/FontDescriptor')
            descriptor = descriptor.get_object() if descriptor else {}
            name = str(font.get('/BaseFont', child.get('/BaseFont', 'UNKNOWN'))).lstrip('/')
            embedded = any(descriptor.get(k) for k in ('/FontFile', '/FontFile2', '/FontFile3'))
            records[name] = {'name': name, 'family': family(name), 'embedded': bool(embedded)}
        objects = resources.get('/XObject', {})
        objects = objects.get_object() if hasattr(objects, 'get_object') else objects
        for ref in objects.values():
            obj = ref.get_object()
            if obj.get('/Subtype') == '/Form':
                visit(obj.get('/Resources'))
    for page in reader.pages:
        visit(page.get('/Resources'))
    return sorted(records.values(), key=lambda r: r['name'])


def inspect_pdf(pdf, expected, substitutions=None):
    import pdfplumber
    from pypdf import PdfReader
    pdf = Path(pdf).resolve()
    if not expected or any(not name.strip() for name in expected):
        raise ValueError('Provide the intended body/heading font families')
    substitutions = substitutions or {}
    unknown_keys = set(substitutions) - {family(n) for n in expected}
    if unknown_keys:
        raise ValueError('Substitution does not name an expected family: ' + ', '.join(sorted(unknown_keys)))
    original = {family(n) for n in expected}
    accepted = original | {n for alternatives in substitutions.values() for n in alternatives}
    used, text_pages, empty_pages = {}, [], []
    with pdfplumber.open(pdf) as document:
        count = len(document.pages)
        for number, page in enumerate(document.pages, 1):
            chars = [c for c in page.chars if c.get('text', '').strip()]
            (text_pages if chars else empty_pages).append(number)
            for char in chars:
                name = char.get('fontname') or 'UNKNOWN'
                used.setdefault(name, set()).add(number)
    actual = {family(n) for n in used}
    unexpected = sorted(actual - accepted)
    substitutions_used = sorted(actual - original - set(unexpected))
    status = ('UNVERIFIED' if not used else 'MISMATCH' if unexpected
              else 'SUBSTITUTION_ACCEPTED' if substitutions_used else 'MATCHED')
    return {
        'status': status, 'pdf_sha256': hashlib.sha256(pdf.read_bytes()).hexdigest(),
        'page_count': count, 'text_pages': text_pages, 'pages_without_inspectable_text': empty_pages,
        'expected': expected,
        'allowed_substitutions': {k: sorted(v) for k, v in substitutions.items()},
        'used_fonts': [{'name': n, 'family': family(n), 'pages': sorted(p)} for n, p in sorted(used.items())],
        'unexpected_families': unexpected, 'substitutions_used': substitutions_used,
        'expected_not_observed': sorted(original - actual),
        'font_resources': resource_fonts(PdfReader(pdf)),
        'scope': 'PDF text font names and embedding evidence only; image text, glyph correctness, layout and visual acceptance remain unverified.',
    }


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('pdf', type=Path, nargs='?')
    parser.add_argument('--preflight', action='store_true', help='Inspect local font registration without opening a PDF')
    parser.add_argument('--font', action='append', required=True, help='Intended family; repeat for body/headings')
    parser.add_argument('--allow-substitute', action='append', default=[], help='Explicitly accepted requested=actual family')
    parser.add_argument('--output', type=Path, required=True, help='New internal JSON report; never overwrite evidence')
    args = parser.parse_args()
    try:
        if args.output.exists():
            raise ValueError('Output exists; use a new report path')
        if args.preflight == bool(args.pdf):
            raise ValueError('Choose --preflight or provide a PDF')
        substitutes = parse_substitutions(args.allow_substitute)
        result = preflight(args.font, substitutes) if args.preflight else inspect_pdf(args.pdf, args.font, substitutes)
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(json.dumps(result, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
        print(json.dumps({'status': result['status'], 'report': str(args.output)}, ensure_ascii=True))
        return 0 if result['status'] in ('AVAILABLE', 'MATCHED', 'SUBSTITUTION_ACCEPTED') else 3 if result['status'] == 'UNVERIFIED' else 2
    except (OSError, ValueError, ImportError, subprocess.TimeoutExpired) as exc:
        parser.exit(2, 'check_pdf_fonts: ' + str(exc) + '\n')


if __name__ == '__main__':
    raise SystemExit(main())
