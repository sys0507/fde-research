#!/usr/bin/env python3
"""Run this edition's isolated regression suites with strict text encodings."""
import argparse
import json
import os
from pathlib import Path
import re
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[1]
SUITES = [
    'plan-ai-project-delivery/scripts/test_estimate.py',
    'plan-ai-project-delivery/scripts/test_runtime.py',
    'design-ai-project-architecture/scripts/test_delivery_profiles.py',
    'fde-ai-scenario-design/scripts/test_screen_labels.py',
    'plan-ai-project-delivery/scripts/test_portability.py',
    'plan-ai-project-delivery/scripts/test_fonts.py',
    'scripts/test_package.py',
    'scripts/test_release.py',
]


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output', type=Path, required=True, help='External directory for logs')
    args = parser.parse_args()
    output = args.output.resolve()
    if output.is_relative_to(ROOT):
        parser.error('Keep test outputs outside the repository')
    output.mkdir(parents=True, exist_ok=True)
    env = dict(os.environ, PYTHONDONTWRITEBYTECODE='1', PYTHONUTF8='0', PYTHONIOENCODING='utf-8', PYTHONWARNDEFAULTENCODING='1')
    results = []
    for suite in SUITES:
        command = [sys.executable, '-B', '-X', 'utf8=0', '-X', 'warn_default_encoding', '-W', 'error::EncodingWarning']
        if suite.endswith('/test_runtime.py'):
            # Exceptions apply only to two third-party metadata readers.
            command += ['-W', 'ignore::EncodingWarning:pypdfium2_raw.version', '-W', 'ignore::EncodingWarning:pypdfium2.version']
        run = subprocess.run(command + [str(ROOT / suite)], cwd=ROOT, env=env, capture_output=True, text=True, encoding='utf-8', timeout=240)
        log = run.stdout + '\n' + run.stderr
        (output / (Path(suite).stem + '.log')).write_text(log, encoding='utf-8')
        count = re.search(r'Ran (\d+) tests?', log)
        passed = run.returncode == 0 and count is not None and re.search(r'\nOK\s*$', log) is not None
        results.append({'suite': suite, 'passed': passed, 'tests': int(count[1]) if count else None, 'exit_code': run.returncode})
        print(suite + ': ' + ('PASS' if passed else 'FAIL'), flush=True)
    report = {'passed': all(item['passed'] for item in results), 'python': sys.version, 'tests': sum(item['tests'] or 0 for item in results), 'suites': results}
    (output / 'results.json').write_text(json.dumps(report, indent=2) + '\n', encoding='utf-8')
    raise SystemExit(0 if report['passed'] else 1)


if __name__ == '__main__':
    main()
