#!/usr/bin/env python3
"""Join calculation provenance, generated report source and editable Word hashes.

This verifies files, not human judgement or visual quality. QA records are declarations
whose final-document binding is checked; screenshots still need actual inspection.
"""
import argparse
import hashlib
import json
from pathlib import Path
import sys
import zipfile
import estimate
import inherit_baseline


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def within(root, name):
    path = (root / name).resolve()
    if not path.is_relative_to(root):
        raise ValueError('Path outside version directory: ' + name)
    if not path.is_file() or not path.stat().st_size:
        raise ValueError('Missing or empty artifact: ' + name)
    return path


def check(args):
    root = args.root.resolve()
    manifest = json.loads((root / 'manifest.json').read_text(encoding='utf-8'))
    if manifest.get('mode') == 'inherited_baseline':
        inherit_baseline.check(root)
    else:
        estimate.check(root)
    md = within(root, args.markdown)
    docx = within(root, args.docx)
    manifest = json.loads((root / 'manifest.json').read_text(encoding='utf-8'))
    rel_md = md.relative_to(root).as_posix()
    if not any(x['file'].replace('\\', '/') == rel_md for x in manifest.get('renders', [])):
        raise ValueError('Report MD must be rendered by its selected calculation or baseline path and tracked in manifest')
    receipt = json.loads(within(root, str(docx.with_suffix('.build.json').relative_to(root))).read_text(encoding='utf-8'))
    if receipt['source_sha256'] != sha(md) or receipt['sha256'] != sha(docx):
        raise ValueError('Word source or final Word hash mismatch; regenerate from current report')
    with zipfile.ZipFile(docx) as z:
        if z.testzip() is not None or not z.read('word/document.xml'):
            raise ValueError('Invalid editable DOCX archive')
    word_state = 'BUILT_NOT_VISUALLY_VERIFIED'
    if args.qa:
        if receipt.get('toc') and not receipt.get('field_update'):
            raise ValueError('Final paginated directory must be updated with finalize_word.py before visual completion')
        qa = json.loads(within(root, args.qa).read_text(encoding='utf-8'))
        if qa.get('docx_sha256') != sha(docx):
            raise ValueError('QA refers to a different final DOCX')
        n = qa.get('page_count')
        if type(n) is not int or n < 1 or qa.get('inspected_pages') != list(range(1, n+1)):
            raise ValueError('QA must declare every actual rendered page inspected, from 1 to page_count')
        if qa.get('status') != 'PASS' or not qa.get('renderer') or qa.get('unresolved_issues', []):
            raise ValueError('QA incomplete or unresolved issues remain')
        pages = qa.get('page_images', [])
        if len(pages) != n:
            raise ValueError('QA page_images must cover actual page count')
        for item in pages:
            if not isinstance(item, dict) or sha(within(root, item['path'])) != item['sha256']:
                raise ValueError('QA page image missing or hash mismatch')
        word_state = 'VISUAL_QA_RECORDED_FOR_CURRENT_DOCX'
    index = {'status':'DRAFT_FOR_HUMAN_REVIEW','word_state':word_state,
             'report_source_sha256':sha(md),'docx_sha256':sha(docx),
             'note':'Mechanical provenance and file check only. Visual QA claims require real inspection; client release includes client/ whitelist only.',
             'artifacts':[]}
    for path in sorted(root.rglob('*')):
        if path.is_file() and path.name != 'delivery-index.json':
            resolved = path.resolve()
            if not resolved.is_relative_to(root):
                raise ValueError('Artifact symlink escapes version directory: '+str(path))
            relative = path.relative_to(root).as_posix()
            index['artifacts'].append({'path':relative,'bytes':path.stat().st_size,'sha256':sha(path),
                                       'visibility':'client' if relative.startswith('client/') and not relative.endswith('.build.json') else 'internal'})
    output = root/'delivery-index.json'
    if output.exists():
        raise ValueError('delivery-index.json exists; preserve old version or remove only a superseded index deliberately')
    output.write_text(json.dumps(index,ensure_ascii=False,indent=2)+'\n', encoding='utf-8')
    print(json.dumps({'status':index['status'],'word_state':word_state,'artifacts':len(index['artifacts'])},ensure_ascii=False))


def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('--root',type=Path,required=True)
    p.add_argument('--markdown',required=True,help='relative report path inside version directory')
    p.add_argument('--docx',required=True,help='relative Word path inside version directory')
    p.add_argument('--qa',help='relative visual QA JSON, optional; omission records Word not visually verified')
    args=p.parse_args()
    try:
        check(args)
    except (ValueError,KeyError,TypeError,OSError,zipfile.BadZipFile) as exc:
        p.exit(2,'check_delivery: '+str(exc)+'\n')

if __name__=='__main__':
    main()
