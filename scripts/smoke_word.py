#!/usr/bin/env python3
"""Real LibreOffice smoke check; never substitutes for all-page visual review."""
import argparse
import json
from pathlib import Path
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[1]


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output', type=Path, required=True)
    parser.add_argument('--soffice', required=True)
    parser.add_argument('--font', default='DejaVu Sans')
    args = parser.parse_args()
    out = args.output.resolve()
    if out.is_relative_to(ROOT) or out.exists():
        parser.error('Use a new output directory outside the repository')
    out.mkdir(parents=True)
    source = out / 'report.md'
    source.write_text('# Scope\n\nSynthetic toolchain check.\n\n## Inputs\n\nNo customer data.\n\n# Delivery\n\nVisual review remains required.\n', encoding='utf-8')
    meta = out / 'metadata.json'
    meta.write_text(json.dumps({'title': 'Synthetic delivery check', 'version': 'test', 'status': 'DRAFT', 'date': '2026-10-09', 'purpose': 'Toolchain validation only'}), encoding='utf-8')
    def run(name, command):
        result = subprocess.run([sys.executable, '-B', '-X', 'utf8'] + list(map(str, command)), capture_output=True, text=True, encoding='utf-8', timeout=600)
        (out / (name + '.log')).write_text(result.stdout + '\n' + result.stderr, encoding='utf-8')
        if result.returncode:
            raise RuntimeError(name + ' failed; inspect log')
    scripts = ROOT / 'plan-ai-project-delivery/scripts'
    docx = out / 'report.docx'
    run('build', [scripts / 'build_report.py', '--markdown', source, '--metadata', meta, '--output', docx, '--body-font', args.font, '--heading-font', args.font])
    run('finalize', [scripts / 'finalize_word.py', '--docx', docx, '--output-dir', out / 'qa', '--renderer', scripts / 'render_word_generic.py', '--renderer-mode', 'generic', '--soffice', args.soffice])
    record = json.loads((out / 'qa/word-finalization.json').read_text(encoding='utf-8'))
    if record['font_verification']['status'] != 'MATCHED' or record['page_count'] < 1:
        raise RuntimeError('Final PDF font or page verification failed')
    print('PASS: real conversion, contents convergence and fonts; visual review still required')


if __name__ == '__main__':
    main()
