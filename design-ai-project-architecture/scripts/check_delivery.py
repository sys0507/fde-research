#!/usr/bin/env python3
"""Check manifest paths/hashes and basic formats; never certify architecture quality."""
import argparse
import hashlib
import json
from pathlib import Path
from zipfile import ZipFile
from xml.etree import ElementTree


ROLES = {'report', 'conditions', 'report_source', 'research', 'decisions', 'inputs', 'question_state', 'diagram_spec', 'diagram_html', 'diagram_static', 'diagram_receipt', 'diagram_visual', 'word_visual'}
REQUIRED = ROLES.copy()


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('manifest', type=Path)
    a = p.parse_args()
    errors, checked, roles = [], [], set()
    try:
        manifest = json.loads(a.manifest.read_text(encoding='utf-8'))
        base = a.manifest.resolve().parent
        if manifest.get('schema_version') != 1:
            raise ValueError('Expected schema_version 1')
        profile = manifest.get('diagram_profile', 'archify')
        if profile not in ('archify', 'standard'):
            raise ValueError('diagram_profile must be archify or standard')
        required = REQUIRED if profile == 'archify' else REQUIRED - {'diagram_html', 'diagram_receipt'}
        artifacts = manifest['artifacts']
        if not isinstance(artifacts, list):
            raise ValueError('artifacts must be a list')
        seen = set()
        for item in artifacts:
            rel, role = item['path'], item['role']
            if role not in ROLES:
                raise ValueError(f'Unknown role: {role}')
            path = (base / rel).resolve()
            if Path(rel).is_absolute() or not path.is_relative_to(base):
                raise ValueError(f'Artifact must be within run directory: {rel}')
            if (role, rel) in seen:
                raise ValueError(f'Duplicate artifact: {rel}')
            seen.add((role, rel))
            if not path.is_file() or path.stat().st_size == 0:
                errors.append(f'Missing/empty {role}: {rel}')
                continue
            digest = hashlib.sha256(path.read_bytes()).hexdigest()
            if item.get('sha256') != digest:
                errors.append(f'Hash mismatch or missing hash: {rel}')
            if role == 'report':
                if path.suffix.lower() != '.docx':
                    errors.append(f'Formal report is not DOCX: {rel}')
                else:
                    with ZipFile(path) as z:
                        ElementTree.fromstring(z.read('word/document.xml'))
            elif path.suffix.lower() == '.json':
                data = json.loads(path.read_text(encoding='utf-8'))
                if role == 'question_state':
                    qs = data['questions']
                    if data['round_limit'] != 20 or len(qs)>20 or [q['round'] for q in qs] != list(range(1,len(qs)+1)):
                        errors.append('Question ledger is inconsistent or exceeds 20 rounds')
            elif role == 'diagram_html':
                html = path.read_text(encoding='utf-8').lower()
                if '<html' not in html or '<svg' not in html:
                    errors.append(f'No standalone HTML/SVG content: {rel}')
            roles.add(role)
            checked.append({'role':role,'path':rel,'sha256':digest,'bytes':path.stat().st_size})
        errors += [f'Missing artifact role: {r}' for r in sorted(required - roles)]
    except Exception as exc:
        errors.append(str(exc))
    print(json.dumps({'file_checks_pass': not errors,'errors':errors,'checked':checked,'scope':'Existence, hashes and basic formats only; semantic, current-source, screenshot and visual acceptance require actual review.'}, ensure_ascii=False, indent=2))
    raise SystemExit(0 if not errors else 1)


if __name__ == '__main__':
    main()
