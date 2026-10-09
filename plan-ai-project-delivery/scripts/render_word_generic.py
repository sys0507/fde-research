#!/usr/bin/env python3
"""Render a local DOCX with an explicitly selected LibreOffice and pypdfium2.

Portable adapter for finalize_word.py. It never installs software, uses a cloud
service, updates the source DOCX, or claims that visual review has happened.
"""
import argparse
import json
import os
from pathlib import Path
import shutil
import subprocess
import tempfile


def render(docx, output, soffice, dpi=144, emit_pdf=False):
    docx = docx.resolve()
    output = output.resolve()
    if not docx.is_file() or docx.suffix.lower() != '.docx':
        raise ValueError('Input must be an existing DOCX')
    executable = shutil.which(soffice)
    if executable is None:
        candidate = Path(soffice).expanduser().resolve()
        executable = str(candidate) if candidate.is_file() else None
    if executable is None:
        raise ValueError('LibreOffice executable not found; pass --soffice explicitly')
    if not 72 <= dpi <= 300:
        raise ValueError('DPI must be between 72 and 300')
    import pypdfium2 as pdfium
    if output.exists() and any(output.iterdir()):
        raise ValueError('Output directory must be new or empty; preserve previous evidence')
    output.mkdir(parents=True, exist_ok=True)
    # Only a newly created private temporary profile is removed by the context.
    with tempfile.TemporaryDirectory(prefix='fde-lo-') as temp:
        profile = (Path(temp) / 'profile').as_uri()
        command = [executable, '-env:UserInstallation=' + profile,
                   '--headless', '--convert-to', 'pdf:writer_pdf_Export',
                   '--outdir', str(output), str(docx)]
        kwargs = {}
        if os.name == 'nt':
            kwargs['creationflags'] = subprocess.CREATE_NO_WINDOW
        completed = subprocess.run(command, capture_output=True, text=True,
                                   encoding='utf-8', errors='replace', timeout=240, **kwargs)
    (output / 'render.log').write_text(completed.stdout + '\n' + completed.stderr,
                                      encoding='utf-8')
    pdf = output / (docx.stem + '.pdf')
    if completed.returncode or not pdf.is_file() or not pdf.stat().st_size:
        raise ValueError('LibreOffice did not produce PDF; inspect render.log')
    with pdfium.PdfDocument(pdf) as document:
        if not len(document):
            raise ValueError('Rendered PDF has no pages')
        count = len(document)
        for number, page in enumerate(document, 1):
            bitmap = page.render(scale=dpi / 72)
            try:
                bitmap.to_pil().save(output / f'page-{number}.png')
            finally:
                bitmap.close()
                page.close()
    # Keep the actual PDF as provenance even when emit_pdf was not requested.
    return {'status': 'RENDERED_VISUAL_REVIEW_REQUIRED', 'page_count': count,
            'pdf': str(pdf), 'renderer': executable, 'dpi': dpi}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('docx', type=Path)
    parser.add_argument('--output_dir', '--output-dir', dest='output', type=Path, required=True)
    parser.add_argument('--emit_pdf', action='store_true', help='Compatibility with renderer contract; PDF is always retained')
    parser.add_argument('--soffice', required=True, help='Discovered LibreOffice executable or command')
    parser.add_argument('--dpi', type=int, default=144)
    args = parser.parse_args()
    try:
        print(json.dumps(render(args.docx, args.output, args.soffice, args.dpi, args.emit_pdf)))
    except (ValueError, OSError, ImportError, subprocess.TimeoutExpired) as exc:
        parser.exit(2, 'render_word_generic: ' + str(exc) + '\n')


if __name__ == '__main__':
    main()
