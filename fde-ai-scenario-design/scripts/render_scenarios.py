#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Render authored scenarios and browser captures to Markdown and offline HTML.

The renderer does not create product screens or capture them. Each scene must
link to its independently authored HTML/CSS simulation in the delivery folder.
"""
import argparse
import base64
import html
import json
import os
from pathlib import Path
import re
import sys
from urllib.parse import quote, urlparse

FIELDS = [('actor', 'Operator'), ('trigger', 'Trigger'), ('starting_point', 'Common starting point and inputs'),
          ('pain', 'Specific difficulty'), ('result', 'Result and handoff'), ('human', 'Human responsibilities'),
          ('exceptions', 'Exceptions and continuation'), ('change', 'Work change and verification'), ('questions', 'Open conditions')]

def require_string(obj, key, where):
    if not isinstance(obj, dict):
        raise ValueError(where + ' must be an object')
    value = obj.get(key)
    if not isinstance(value, str) or not value.strip():
        raise ValueError(f'{where}.{key}  must be nonempty text')
    return value

def local_source(value, base):
    parsed = urlparse(value)
    if parsed.scheme in ('http', 'https'):
        return value
    if parsed.scheme or Path(value).is_absolute():
        raise ValueError('Sources require relative paths or http(s) links: ' + value)
    target = (base / value).resolve()
    if not target.exists():
        raise ValueError('Source not found: ' + value)
    return quote(os.path.relpath(target, base), safe='/')

def image_bytes(path):
    data = path.read_bytes()
    if data.startswith(b'\x89PNG\r\n\x1a\n'):
        mime = 'image/png'
    elif data.startswith(b'\xff\xd8\xff'):
        mime = 'image/jpeg'
    elif data[:4] == b'RIFF' and data[8:12] == b'WEBP':
        mime = 'image/webp'
    else:
        raise ValueError('Only actual PNG/JPEG/WebP images: ' + str(path))
    return f'data:{mime};base64,' + base64.b64encode(data).decode()

def delivery_file(value, base, label):
    target = (base / value).resolve()
    if urlparse(value).scheme or Path(value).is_absolute() or not target.is_relative_to(base.resolve()):
        raise ValueError(label + ' must be a relative path inside delivery: ' + value)
    return target

def positive_number(value):
    return isinstance(value, (int, float)) and not isinstance(value, bool) and 0 < value < float('inf')

def validate(data, base):
    for key in ['title', 'scope']:
        require_string(data, key, 'document')
    cap = data.get('capability', {})
    if not isinstance(cap, dict):
        raise ValueError('capability must be an object')
    if 'mode' in data or 'image_generation' in cap:
        raise ValueError('Remove legacy mode and image_generation, use capability.browser_capture')
    if not isinstance(cap.get('browser_capture'), bool):
        raise ValueError('capability.browser_capture must be boolean')
    require_string(cap, 'reason', 'capability')
    scenes = data.get('scenes')
    if not isinstance(scenes, list) or not scenes:
        raise ValueError('At least one complete scenario is required')
    sources = data.get('sources')
    if not isinstance(sources, list) or not sources:
        raise ValueError('Traceable sources are required')
    source_ids = set()
    for src in sources:
        sid = require_string(src, 'id', 'source')
        if not re.fullmatch(r'[A-Za-z][A-Za-z0-9_-]*', sid) or sid in source_ids:
            raise ValueError('Duplicate source ID or invalid anchor: ' + sid)
        source_ids.add(sid)
        for key in ['label', 'nature', 'path']:
            require_string(src, key, sid)
        src['_href'] = local_source(src['path'], base)
    ids = set()
    incomplete = []
    for s in scenes:
        sid = require_string(s, 'id', 'scene')
        if not re.fullmatch(r'[A-Za-z][A-Za-z0-9_-]*', sid) or sid in ids:
            raise ValueError('Duplicate scenario ID or invalid anchor: ' + sid)
        ids.add(sid)
        for key in ['title', 'status', *[k for k, _ in FIELDS]]:
            require_string(s, key, sid)
        for key in ['functions', 'before', 'after', 'source_ids']:
            if not isinstance(s.get(key), list) or not s[key] or any(not isinstance(x, str) or not x.strip() for x in s[key]):
                raise ValueError(f'{sid}.{key} requires a nonempty text array')
        if not set(s['source_ids']) <= source_ids:
            raise ValueError(sid + ' references an unknown source ID')
        demo = require_string(s, 'demo', sid)
        demo_path = delivery_file(demo, base, 'Simulation page')
        if demo_path.suffix.lower() != '.html' or not demo_path.is_file() or not demo_path.stat().st_size:
            raise ValueError(sid + '.demo requires an actual nonempty .html file: ' + demo)
        if demo_path.name == 'scenario-comparison.html':
            raise ValueError(sid + '.demo cannot use the explanatory overview as a simulation')
        if not isinstance(s.get('result_required', False), bool):
            raise ValueError(sid + '.result_required must be boolean')
        figures = s.get('images', [])
        if not isinstance(figures, list):
            raise ValueError(sid + '.images must be an array')
        phases = set()
        for fig in figures:
            if not isinstance(fig, dict):
                raise ValueError(sid + '.images entries must be objects')
            phase = fig.get('phase')
            if phase not in ('before', 'after', 'result') or phase in phases:
                raise ValueError(sid + ': Duplicate or unknown image phase')
            phases.add(phase)
            for key in ['caption', 'provenance']:
                require_string(fig, key, sid + '.image')
            state = fig.get('status')
            if state not in ('captured', 'reused', 'failed', 'unverified'):
                raise ValueError(sid + ': Unknown image status')
            if state == 'failed':
                require_string(fig, 'reason', sid + '.image')
                incomplete.append(sid + '/' + phase + ': ' + fig['reason'])
                continue
            file = require_string(fig, 'file', sid + '.image')
            image_path = delivery_file(file, base, 'Screenshot')
            if state == 'captured':
                if require_string(fig, 'page', sid + '.image') != demo:
                    raise ValueError(sid + '.image.page must match the scene demo')
                viewport = fig.get('viewport')
                if not isinstance(viewport, dict) or not all(positive_number(viewport.get(k)) for k in ('width', 'height', 'device_scale_factor')):
                    raise ValueError(sid + '.image.viewport requires positive width, height, device_scale_factor')
            if not image_path.is_file():
                fig['_error'] = 'Screenshot file not found: ' + file
                incomplete.append(sid + '/' + phase + ': ' + fig['_error'])
                continue
            fig['_data'] = image_bytes(image_path)
            if state == 'unverified' or fig.get('checked') is not True:
                incomplete.append(sid + '/' + phase + ': Image has not been visually reviewed')
        required = {'before', 'after'} | ({'result'} if s.get('result_required', False) else set())
        for phase in sorted(required - phases):
            incomplete.append(sid + '/' + phase + ': Screenshot pending' + (' (browser capture is unavailable in this environment)' if not cap['browser_capture'] else ''))
    return incomplete

def clean(value):
    return html.escape(str(value), quote=True)

def paragraph(value):
    return '<p>' + clean(value).replace('\n', '<br>') + '</p>'

def steps(items):
    return '<ol>' + ''.join('<li>' + clean(x) + '</li>' for x in items) + '</ol>'

def mdtext(value):
    # Authored fields are plain text, not executable markup.
    return re.sub(r'([\\`*_{}\[\]<>|])', r'\\\1', str(value))

def render(data, base, incomplete):
    state = 'Screenshots pending or unverified' if incomplete else 'Scenario descriptions and screenshots complete'
    md = [f'# {mdtext(data["title"])}', '', f'Status: {state}', '', mdtext(data['scope']), '',
          'Production method: ' + mdtext(data['capability']['reason']), '',
          'This file explains the scenario comparison. Open separate simulations through their links. When sharing, retain screens and other demo directories with relative paths. Interfaces use HTML/CSS simulations, not deployed systems.', '', '## Scenario overview', '',
          '|ID|Scenario|Operator|Functions|Status|', '|---|---|---|---|---|']
    for s in data['scenes']:
        md.append('|' + '|'.join(mdtext(x) for x in [s['id'], s['title'], s['actor'], ', '.join(s['functions']), s['status']]) + '|')
    cards = []
    for s in data['scenes']:
        sid = s['id']
        md += ['', f'## {sid} · {mdtext(s["title"])}', '', 'Scenario status: ' + mdtext(s['status']), '',
               'Functions: ' + mdtext(', '.join(s['functions'])), '',
               f'[Open this scenario simulation](<{quote(s["demo"], safe="/")}>)']
        head = f'<header class="scene-head"><span class="number">{clean(sid)}</span><h2>{clean(s["title"])}</h2><p>{clean(s["status"])}</p><p>Functions: {clean(", ".join(s["functions"]))}</p></header>'
        head = head.replace('</header>', f'<a href="{clean(quote(s["demo"], safe="/"))}" target="_blank" rel="noopener">Open this scenario simulation</a></header>')
        details = ''
        for key, label in FIELDS[:4]:
            md += ['', f'### {label}', '', mdtext(s[key])]
            details += f'<div class="detail"><h3>{label}</h3>{paragraph(s[key])}</div>'
        columns = []
        for key, label in [('before', 'Before: current work'), ('after', 'After: proposed work')]:
            md += ['', f'### {label}', ''] + [f'{i}. {mdtext(v)}' for i, v in enumerate(s[key], 1)]
            figures = [x for x in s.get('images', []) if x['phase'] == key]
            html_figs, md_figs = render_figures(figures)
            md += md_figs
            columns.append(f'<section class="{key}"><h3>{label}</h3>{steps(s[key])}{html_figs}</section>')
        tail = ''
        for key, label in FIELDS[4:]:
            md += ['', f'### {label}', '', mdtext(s[key])]
            tail += f'<div class="detail"><h3>{label}</h3>{paragraph(s[key])}</div>'
        hfig, mfig = render_figures([x for x in s.get('images', []) if x['phase'] == 'result'])
        md += mfig
        refs = ', '.join(s['source_ids'])
        md += ['', 'Evidence: ' + mdtext(refs), '']
        tail += '<p class="sources">Evidence: ' + ' · '.join(f'<a href="#source-{clean(r)}">{clean(r)}</a>' for r in s['source_ids']) + '</p>'
        cards.append(f'<article id="{clean(sid)}" class="scene">{head}<div class="facts">{details}</div><div class="comparison">{"".join(columns)}</div><div class="outcome">{tail}{hfig}</div></article>')
    md += ['## Sources and provenance', '']
    source_html = []
    for src in data['sources']:
        md += [f'- {mdtext(src["id"])} · [{mdtext(src["label"])}](<{src["_href"]}>): {mdtext(src["nature"])}']
        source_html.append(f'<li id="source-{clean(src["id"])}"><a href="{clean(src["_href"])}">{clean(src["id"])} · {clean(src["label"])}</a>{paragraph(src["nature"])}</li>')
    notices = ''
    if incomplete:
        md += ['', '## Pending or unverified captures', ''] + ['- ' + mdtext(x) for x in incomplete]
        notices = '<aside class="notice"><strong>Screenshots pending or unverified</strong>' + steps(incomplete) + '</aside>'
    nav = ''.join(f'<a href="#{clean(s["id"])}">{clean(s["id"])} · {clean(s["title"])}</a>' for s in data['scenes'])
    page = '''<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1"><title>''' + clean(data['title']) + '''</title><style>
:root{color-scheme:light;--ink:#183a39;--muted:#546863;--line:#d8e2db;--paper:#f5f6f0;--green:#166653}*{box-sizing:border-box}body{margin:0;background:var(--paper);color:var(--ink);font:16px/1.85 system-ui,-apple-system,"PingFang SC","Microsoft YaHei",sans-serif}a{color:var(--green);text-underline-offset:4px}main{max-width:1320px;margin:auto;padding:52px 28px 80px}.eyebrow{font-size:12px;letter-spacing:2px;font-weight:700}h1{font-size:clamp(30px,4vw,48px);line-height:1.25;max-width:1000px}h2{font-size:27px;line-height:1.4;margin:12px 0}h3{font-size:16px;margin:0 0 8px}p{margin:0 0 12px;overflow-wrap:anywhere}.intro{max-width:980px}.mode{border:1px solid var(--green);border-radius:24px;padding:4px 14px;display:inline-block;font-size:13px;margin-bottom:18px}.toolbar{display:flex;gap:12px;align-items:center;margin:28px 0 12px;flex-wrap:wrap}input{flex:1;min-width:180px;max-width:560px;padding:12px 16px;border:1px solid var(--line);border-radius:8px;font:inherit}button{font:inherit;cursor:pointer;border:1px solid var(--line);background:white;padding:10px 16px;border-radius:8px}nav{display:flex;flex-wrap:wrap;gap:8px;margin:12px 0 30px}nav a{font-size:14px;text-decoration:none;background:#fff;border:1px solid var(--line);padding:7px 12px;border-radius:6px}.scene{background:white;border:1px solid var(--line);border-radius:14px;margin:28px 0;overflow:hidden;scroll-margin-top:20px}.scene-head{padding:28px 32px;border-bottom:1px solid var(--line)}.scene-head p{color:var(--muted);font-size:14px}.number{font:700 14px/1.4 ui-monospace,monospace;color:var(--green)}.facts{display:grid;grid-template-columns:1fr 1fr;gap:18px 30px;padding:24px 32px}.comparison{display:grid;grid-template-columns:1fr 1fr;border-top:1px solid var(--line);border-bottom:1px solid var(--line)}.comparison section{padding:26px 30px}.before{background:#f6f3ec}.after{background:#ecf5f0;border-left:1px solid var(--line)}ol{padding-left:22px;margin:12px 0}li{padding-left:4px;margin-bottom:12px}figure{margin:20px 0 4px}img{display:block;width:100%;height:auto;cursor:zoom-in;border:1px solid var(--line);border-radius:6px}figcaption{font-size:13px;line-height:1.65;color:var(--muted);margin-top:10px}.outcome{padding:28px 32px}.outcome .detail{margin-bottom:22px}.sources{font-size:14px;border-top:1px solid var(--line);padding-top:15px}.notice{background:#fff1dc;padding:20px;border-radius:8px;margin:16px 0}.failure{font-size:14px;color:#784b14}dialog{max-width:96vw;max-height:96vh;padding:16px;border:none;border-radius:10px}dialog::backdrop{background:#10211de0}dialog img{width:auto;max-width:90vw;max-height:82vh;object-fit:contain;cursor:default}dialog button{display:block;margin:0 0 12px auto}#empty{padding:25px}footer{font-size:13px;color:var(--muted);border-top:1px solid var(--line);padding-top:24px}[hidden]{display:none!important}@media(max-width:760px){main{padding:28px 16px}.facts,.comparison{grid-template-columns:1fr}.after{border-left:0;border-top:1px solid var(--line)}.scene-head,.facts,.comparison section,.outcome{padding:22px}h2{font-size:23px}}@media print{nav,.toolbar,dialog{display:none}main{padding:0}.scene{break-inside:auto}.comparison{display:block}.comparison section{break-inside:avoid}body{background:white}a{color:inherit}img{max-height:650px;object-fit:contain}}
</style></head><body><main><div class="eyebrow">Business scenarios · Before and after</div><h1>''' + clean(data['title']) + '</h1><div class="mode">' + state + '</div><div class="intro">' + paragraph(data['scope']) + paragraph(data['capability']['reason']) + '</div>' + notices + '<div class="toolbar"><input id="search" type="search" aria-label="Filter scenarios" placeholder="Search people, tasks, or functions"><button id="clear">Show all</button><button id="print">Print current content</button><span id="count" aria-live="polite"></span></div><nav aria-label="Scenario navigation">' + nav + '</nav><p id="empty" hidden>No matching scenarios. Try another keyword.</p>' + ''.join(cards) + '<section><h2>Sources and provenance</h2><ul>' + ''.join(source_html) + '</ul></section><footer>This page explains scenarios; open simulated interfaces through each scene link. Images are embedded; sharing interactive demos still requires screens and other demo directories with relative paths. HTML/CSS simulated interfaces do not establish deployment or business-owner approval.</footer></main><dialog id="viewer"><button id="close" aria-label="Close enlarged image">Close</button><img alt="Enlarged scenario image"></dialog><script>\n' + '''
const search=document.querySelector('#search'),cards=[...document.querySelectorAll('.scene')],links=[...document.querySelectorAll('nav a')];
function filter(){const q=search.value.trim().toLowerCase();let n=0;cards.forEach((c,i)=>{const show=c.textContent.toLowerCase().includes(q);c.hidden=!show;links[i].hidden=!show;if(show)n++});document.querySelector('#count').textContent=n+' / '+cards.length+' scenarios';document.querySelector('#empty').hidden=n!==0}
search.addEventListener('input',filter);document.querySelector('#clear').addEventListener('click',()=>{search.value='';filter()});document.querySelector('#print').addEventListener('click',()=>window.print());filter();
const viewer=document.querySelector('#viewer');document.querySelectorAll('figure img').forEach(img=>{img.tabIndex=0;img.setAttribute('role','button');img.setAttribute('aria-label','Enlarge image: '+img.alt);const open=()=>{viewer.querySelector('img').src=img.src;viewer.querySelector('img').alt=img.alt;viewer.showModal()};img.addEventListener('click',open);img.addEventListener('keydown',e=>{if(e.key==='Enter'||e.key===' '){e.preventDefault();open()}})});document.querySelector('#close').addEventListener('click',()=>viewer.close());viewer.addEventListener('click',e=>{if(e.target===viewer)viewer.close()});
''' + '</script></body></html>'
    return '\n'.join(md) + '\n', page

def render_figures(figures):
    h, md = [], []
    for fig in figures:
        caption = fig['caption'] + '; Source/provenance: ' + fig['provenance']
        if fig['status'] == 'failed' or fig.get('_error'):
            msg = 'Screenshot pending: ' + (fig.get('_error') or fig['reason'])
            h.append('<p class="failure">' + clean(msg) + '</p>')
            md += ['', mdtext(msg)]
        else:
            if fig['status'] == 'unverified' or fig.get('checked') is not True:
                caption = 'Image not yet verified. ' + caption
            h.append('<figure><img src="' + fig['_data'] + '" alt="' + clean(fig['caption']) + '"><figcaption>' + clean(caption) + '</figcaption></figure>')
            md += ['', f'![{mdtext(fig["caption"])}](<{quote(fig["file"], safe="/")}>)', '', mdtext(caption)]
    return ''.join(h), md

def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('input', type=Path, help='scenarios.json; outputs are written to the same directory')
    parser.add_argument('--overwrite', action='store_true', help='Explicitly permit updating existing MD and HTML')
    args = parser.parse_args()
    try:
        base = args.input.resolve().parent
        data = json.loads(args.input.read_text(encoding='utf-8'))
        incomplete = validate(data, base)
        md, page = render(data, base, incomplete)
        targets = [base/'scenario-comparison.md', base/'scenario-comparison.html']
        if not args.overwrite and any(x.exists() for x in targets):
            raise ValueError('Outputs exist; retain manual edits, then inspect before using --overwrite or choose another directory')
        for path, content in zip(targets, [md, page]):
            path.write_text(content, encoding='utf-8')
        print(json.dumps({'status':'partial' if incomplete else 'complete', 'browser_capture':data['capability']['browser_capture'], 'scenes':len(data['scenes']), 'outputs':[x.name for x in targets], 'incomplete':incomplete}, ensure_ascii=False))
        return 2 if incomplete else 0
    except (OSError, ValueError, KeyError, TypeError) as exc:
        print('Cannot generate: ' + str(exc), file=sys.stderr)
        return 1

if __name__ == '__main__':
    sys.exit(main())
