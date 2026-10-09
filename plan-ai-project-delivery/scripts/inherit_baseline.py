#!/usr/bin/env python3
"""Preserve a user-selected proposal baseline and render its adopted facts.

This checks provenance and declared arithmetic, not a new workload estimate.
The Agent reads the original proposal and prepares the input; users need no JSON.
"""
import argparse
from decimal import Decimal, InvalidOperation
import hashlib
import json
from pathlib import Path
import re
import shutil


def sha(p):
    return hashlib.sha256(p.read_bytes()).hexdigest()


def dump(p, obj):
    p.write_text(json.dumps(obj, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')


def inside(root, name):
    p = (root / name).resolve()
    if not p.is_relative_to(root.resolve()) or not p.is_file():
        raise ValueError('Missing file or path outside declared root: ' + name)
    return p


def validate(data):
    if not data.get('adoption_instruction') or not data.get('sources') or not data.get('facts'):
        raise ValueError('Need adoption_instruction, sources and facts')
    source_ids = [s['id'] for s in data['sources']]
    if len(source_ids) != len(set(source_ids)) or any(not re.fullmatch(r'[A-Za-z0-9_-]+', x) for x in source_ids):
        raise ValueError('Source IDs must be unique portable identifiers')
    for key, fact in data['facts'].items():
        if not re.fullmatch(r'[a-z][a-z0-9_]*', key):
            raise ValueError('Invalid fact key: ' + key)
        if fact.get('source_id') not in source_ids or not fact.get('locator'):
            raise ValueError('Fact needs a source and original location: ' + key)
        if fact.get('visibility') not in ('client', 'internal') or fact.get('status') not in ('adopted_estimate', 'confirmed', 'provisional'):
            raise ValueError('Fact needs explicit visibility and status: ' + key)
        if not fact.get('unit') or 'value' not in fact:
            raise ValueError('Fact needs value and unit: ' + key)
        val = Decimal(str(fact['value']))
        if not val.is_finite():
            raise ValueError('Non-finite value: ' + key)
        if 'display' in fact and Decimal(str(fact['display']).replace(',', '')) != val:
            raise ValueError('Display value differs from adopted value: ' + key)
    review = data.get('scope_review', {})
    if not isinstance(review.get('conclusion'), str) or not review['conclusion'].strip():
        raise ValueError('Need explicit scope comparison conclusion')
    for name in ('changes', 'conflicts', 'missing_details'):
        if not isinstance(review.get(name), list):
            raise ValueError('Scope review needs list: ' + name)
    outcomes = []
    for item in data.get('checks', []):
        values = [Decimal(str(data['facts'][x]['value'])) for x in item['inputs']]
        op = item['operation']
        if op == 'sum':
            actual = sum(values, Decimal(0))
        elif op == 'product':
            actual = Decimal(1)
            for value in values:
                actual *= value
        elif op == 'difference' and len(values) == 2:
            actual = values[0] - values[1]
        elif op == 'percentage' and len(values) == 2 and values[1]:
            actual = values[0] / values[1] * 100
        else:
            raise ValueError('Unsupported arithmetic check: ' + op)
        expected = Decimal(str(data['facts'][item['expected']]['value']))
        tolerance = Decimal(str(item.get('tolerance', '0.01')))
        if not tolerance.is_finite() or tolerance < 0 or abs(actual - expected) > tolerance:
            raise ValueError('Baseline arithmetic mismatch: ' + item['label'])
        outcomes.append({'label': item['label'], 'actual': str(actual), 'expected': str(expected), 'pass': True})
    return outcomes


def adopt(args):
    root = args.output.resolve()
    root.mkdir(parents=True, exist_ok=True)
    if any((root / name).exists() for name in ('baseline.json', 'manifest.json')):
        raise ValueError('Use a new version; baseline already exists')
    data = json.loads(args.input.read_text(encoding='utf-8'))
    outcomes = validate(data)
    # Validate every source before writing the adopted record.
    resolved = []
    for source in data['sources']:
        p = inside(args.source_root, source['path'])
        if source.get('sha256') and source['sha256'] != sha(p):
            raise ValueError('Source changed: ' + source['path'])
        resolved.append(p)
    files = []
    folder = root / 'internal/baseline-inputs'
    folder.mkdir(parents=True, exist_ok=True)
    for source, p in zip(data['sources'], resolved):
        target = folder / (source['id'] + '-' + p.name)
        if target.exists():
            raise ValueError('Snapshot already exists: ' + target.name)
        shutil.copy2(p, target)
        source['original_path'] = source.pop('path')
        source['snapshot'] = target.relative_to(root).as_posix()
        source['sha256'] = sha(target)
        files.append({'file': source['snapshot'], 'sha256': source['sha256']})
    data['mode'] = 'inherited_baseline'
    dump(root / 'baseline.json', data)
    dump(root / 'baseline-check.json', {'status': 'PROVENANCE_AND_DECLARED_ARITHMETIC_CHECKED', 'checks': outcomes,
         'limits': 'Not a new estimate, approval, daily capacity validation or proof of real delivery performance.'})
    for name in ('baseline.json', 'baseline-check.json'):
        files.append({'file': name, 'sha256': sha(root / name)})
    dump(root / 'manifest.json', {'mode': 'inherited_baseline', 'files': files, 'renders': []})
    print(json.dumps({'status': 'BASELINE_ADOPTED', 'facts': len(data['facts']), 'sources': len(files)-2, 'checks': len(outcomes)}))


def check(root):
    root = root.resolve()
    manifest = json.loads((root / 'manifest.json').read_text(encoding='utf-8'))
    if manifest.get('mode') != 'inherited_baseline':
        raise ValueError('Not an inherited baseline')
    for entry in manifest['files']:
        if sha(inside(root, entry['file'])) != entry['sha256']:
            raise ValueError('Baseline file changed: ' + entry['file'])
    data = json.loads((root / 'baseline.json').read_text(encoding='utf-8'))
    for source in data['sources']:
        if sha(inside(root, source['snapshot'])) != source['sha256']:
            raise ValueError('Source snapshot changed')
    validate(data)
    for render in manifest.get('renders', []):
        if sha(inside(root, render['file'])) != render['sha256'] or sha(inside(root, render['template'])) != render['template_sha256']:
            raise ValueError('Rendered report or template changed: ' + render['file'])
        if render['baseline_sha256'] != sha(root / 'baseline.json'):
            raise ValueError('Report uses a different baseline')
    return data


def render(args):
    root = args.root.resolve()
    data = check(root)
    template = inside(root, args.template)
    target = (root / args.output).resolve()
    if not target.is_relative_to(root) or target.exists():
        raise ValueError('Report output must be new and within version directory')
    text = template.read_text(encoding='utf-8')
    used = []
    def replace(match):
        key = match.group(1)
        fact = data['facts'][key]
        if target.is_relative_to(root / 'client') and fact['visibility'] != 'client':
            raise ValueError('Internal fact cannot enter client report: ' + key)
        used.append(key)
        return str(fact.get('display', fact['value']))
    text = re.sub(r'\{\{baseline\.([a-z][a-z0-9_]*)\}\}', replace, text)
    if '{{baseline.' in text or not used:
        raise ValueError('Template must use valid adopted facts')
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(text, encoding='utf-8')
    manifest = json.loads((root / 'manifest.json').read_text(encoding='utf-8'))
    manifest['renders'].append({'file': target.relative_to(root).as_posix(), 'sha256': sha(target),
        'template': template.relative_to(root).as_posix(), 'template_sha256': sha(template),
        'baseline_sha256': sha(root / 'baseline.json'), 'facts': sorted(set(used))})
    dump(root / 'manifest.json', manifest)
    print(json.dumps({'status': 'RENDERED_FROM_ADOPTED_BASELINE', 'facts': sorted(set(used))}))


def main():
    p = argparse.ArgumentParser(description=__doc__)
    sub = p.add_subparsers(dest='command', required=True)
    a = sub.add_parser('adopt'); a.add_argument('--input', type=Path, required=True); a.add_argument('--source-root', type=Path, required=True); a.add_argument('--output', type=Path, required=True)
    a = sub.add_parser('check'); a.add_argument('--root', type=Path, required=True)
    a = sub.add_parser('render'); a.add_argument('--root', type=Path, required=True); a.add_argument('--template', required=True); a.add_argument('--output', required=True)
    args = p.parse_args()
    try:
        if args.command == 'adopt': adopt(args)
        elif args.command == 'render': render(args)
        else: check(args.root); print('INHERITED_BASELINE_CHECK_PASS')
    except (ValueError, KeyError, TypeError, OSError, InvalidOperation) as e:
        p.exit(2, 'inherit_baseline: ' + str(e) + '\n')


if __name__ == '__main__':
    main()
