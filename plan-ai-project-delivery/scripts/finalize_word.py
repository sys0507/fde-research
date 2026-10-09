#!/usr/bin/env python3
"""Rebuild native TOC 1-2 results from headings and verify actual rendered pagination.

The default Codex route keeps the bundled documents renderer and runtime.
The explicit generic route accepts a local renderer and LibreOffice executable.
"""
import argparse
import hashlib
import json
import os
from pathlib import Path
import re
import shutil
import subprocess
import sys
from urllib.parse import unquote, urlparse
from zipfile import ZipFile, ZIP_DEFLATED
from lxml import etree as ET
from pypdf import PdfReader
import pdfplumber

NS={'w':'http://schemas.openxmlformats.org/wordprocessingml/2006/main','r':'http://schemas.openxmlformats.org/officeDocument/2006/relationships'}
W='{'+NS['w']+'}'
def sha(p): return hashlib.sha256(p.read_bytes()).hexdigest()
def norm(s): return re.sub(r'\s+','',s)
def load(docx):
    with ZipFile(docx) as z: return {n:z.read(n) for n in z.namelist()}
def save(docx, parts):
    target=docx.with_suffix('.updating.docx')
    with ZipFile(target,'w',ZIP_DEFLATED) as z:
        for n,v in parts.items(): z.writestr(n,v)
    target.replace(docx)
def headings(root, native=False):
    result=[]
    for p in root.findall('.//w:p',NS):
        bookmarks=p.findall('w:bookmarkStart',NS)
        if bookmarks:
            text=''.join(p.itertext())
            # Only bookmarks on actual Heading paragraphs map to PDF outlines.
            style=p.find('w:pPr/w:pStyle',NS)
            if style is not None and re.fullmatch(r'Heading[1-2]' if native else r'Heading[1-3]',style.get(W+'val','')):
                title=''.join(p.xpath('.//w:t/text()',namespaces=NS))
                for b in bookmarks:result.append((b.get(W+'name'),title))
    return result

def mapping(pdf, expected):
    reader=PdfReader(pdf);count=len(reader.pages);toc=[]
    def flatten(items,level=1):
        for item in items:
            if isinstance(item,list): flatten(item,level+1)
            else: toc.append((level,str(item.title),reader.get_destination_page_number(item)+1))
    flatten(reader.outline)
    with pdfplumber.open(pdf) as visible:
        pages=[p.extract_text() or '' for p in visible.pages]
    result={};cursor=0
    for name,title in expected:
        matches=[i for i in range(cursor,len(toc)) if norm(toc[i][1])==norm(title)]
        if not matches: raise ValueError('Rendered PDF missing heading bookmark: '+title)
        i=matches[0];page=toc[i][2]
        if not 1<=page<=count or norm(title) not in norm(pages[page-1]):
            raise ValueError('Heading outline/page text disagree: '+title)
        result[name]=page;cursor=i+1
    return result,count

def links_check(docx,parts):
    root=ET.fromstring(parts['word/document.xml']);names={b.get(W+'name') for b in root.findall('.//w:bookmarkStart',NS)}
    for link in root.findall('.//w:hyperlink',NS):
        anchor=link.get(W+'anchor')
        if anchor and anchor not in names:raise ValueError('Unresolved internal link: '+anchor)
    rels=ET.fromstring(parts['word/_rels/document.xml.rels']);local=[]
    for rel in rels:
        if rel.get('Type','').endswith('/hyperlink') and rel.get('TargetMode')=='External':
            target=rel.get('Target','');parsed=urlparse(target)
            if parsed.scheme in ('http','https','mailto'):continue
            if parsed.scheme or Path(unquote(parsed.path)).is_absolute():raise ValueError('Nonportable document link: '+target)
            linked=(docx.parent/unquote(parsed.path)).resolve()
            if not linked.is_file():raise ValueError('Missing document attachment: '+target)
            local.append({'target':target,'sha256':sha(linked)})
    return local

def cache_pages(parts,page_map):
    root=ET.fromstring(parts['word/document.xml']);resolved=[]
    for field in root.findall('.//w:fldSimple',NS):
        code=field.get(W+'instr','').strip()
        match=re.fullmatch(r'PAGEREF\s+(\S+)(?:\s+\\h)?',code)
        if not match:raise ValueError('Unsupported body field; use documents field tooling: '+code)
        name=match.group(1)
        if name not in page_map:raise ValueError('Page reference missing heading: '+name)
        text_nodes=field.findall('.//w:t',NS)
        if len(text_nodes)!=1:raise ValueError('Unexpected PAGEREF display structure')
        text_nodes[0].text=str(page_map[name]);resolved.append(name)
    # Complex arbitrary REF/SEQ fields require a separate authoring/update route.
    if root.findall('.//w:instrText',NS):raise ValueError('Complex body fields need documents update route')
    parts['word/document.xml']=ET.tostring(root,xml_declaration=True,encoding='UTF-8',standalone=True)
    return resolved


def toc_container(root):
    nodes=root.xpath('.//w:sdt[w:sdtPr/w:tag[@w:val="report-native-toc"]]/w:sdtContent',namespaces=NS)
    if len(nodes)!=1:raise ValueError('Expected exactly one builder native TOC')
    return nodes[0]


def cache_toc(parts, page_map):
    """Update both TOC entry set and cached page numbers; never flatten the field."""
    root=ET.fromstring(parts['word/document.xml']);container=toc_container(root)
    entries=[]
    for p in root.findall('.//w:p',NS):
        style=p.find('w:pPr/w:pStyle',NS)
        if style is None or style.get(W+'val') not in ('Heading1','Heading2'):continue
        bookmark=next((b.get(W+'name') for b in p.findall('w:bookmarkStart',NS) if b.get(W+'name','').startswith('chapter_')),None)
        if bookmark:entries.append((bookmark,''.join(p.xpath('.//w:t/text()',namespaces=NS)),style.get(W+'val')[-1]))
    if not entries:raise ValueError('Native TOC has no eligible headings')
    container.clear()
    def node(parent,tag,text=None,**attrs):
        child=ET.SubElement(parent,W+tag,{W+k:str(v) for k,v in attrs.items()})
        if text is not None:child.text=text
        return child
    def marker(parent,kind):node(node(parent,'r'),'fldChar',fldCharType=kind)
    for i,(anchor,title,level) in enumerate(entries):
        p=node(container,'p');props=node(p,'pPr');node(props,'pStyle',val='TOC'+level)
        # Explicit tabs survive engines that do not resolve imported TOC styles.
        node(node(props,'tabs'),'tab',val='right',leader='dot',pos='9071')
        if i==0:
            marker(p,'begin');code=node(node(p,'r'),'instrText',' TOC \\o "1-2" \\h \\z ')
            code.set('{http://www.w3.org/XML/1998/namespace}space','preserve');marker(p,'separate')
        link=node(p,'hyperlink',anchor=anchor,history='1')
        node(node(link,'r'),'t',title);node(node(link,'r'),'tab')
        field=node(link,'fldSimple',instr=f' PAGEREF {anchor} \\h ')
        node(node(field,'r'),'t',str(page_map.get(anchor,1)))
        if i==len(entries)-1:marker(p,'end')
    parts['word/document.xml']=ET.tostring(root,xml_declaration=True,encoding='UTF-8',standalone=True)


def verify_native_render(pdf, expected, logical, physical):
    """Check visible TOC numbers and all body PAGE fields against actual pages."""
    with pdfplumber.open(pdf) as visible:
        texts=[p.extract_text() or '' for p in visible.pages]
        first=min(physical.values())
        front='\n'.join(norm(line) for text in texts[:first-1] for line in text.splitlines())
        for anchor,title in expected:
            title_pattern=r'\n?'.join(re.escape(char) for char in norm(title))
            if not re.search(r'(?:^|\n)'+title_pattern+r'[.·…\s]*'+str(logical[anchor])+r'(?=\n|$)',front):
                raise ValueError('Rendered TOC text/page missing: '+title)
        for index,page in enumerate(visible.pages[first-1:],1):
            footer=page.crop((0,float(page.height)-60,float(page.width),float(page.height)))
            if norm(footer.extract_text() or '') != f'Page{index}':
                raise ValueError(f'Body footer does not continue from 1 on body page {index}')
            sizes={round(c['size'],1) for c in footer.chars if c['text'].strip()}
            if sizes!={9.0}:raise ValueError('Footer text/digits must all render at 9 pt: '+str(sizes))

def finalize(args):
    from check_pdf_fonts import preflight, inspect_pdf, parse_substitutions
    docx=args.docx.resolve();qa=args.output_dir.resolve();renderer=args.renderer.resolve()
    runtime=args.runtime_bin.resolve() if args.runtime_bin else None
    if not renderer.is_file():raise ValueError('Missing renderer script')
    if args.renderer_mode == 'codex':
        if runtime is None or not any((runtime/name).is_file() for name in ('soffice','soffice.exe','soffice.cmd')):
            raise ValueError('Codex route requires discovered bundled runtime-bin and soffice')
        if args.soffice:raise ValueError('--soffice is only for the explicit generic route')
    elif not args.soffice:
        raise ValueError('Generic route requires --soffice with the actual local executable')
    else:
        resolved=shutil.which(args.soffice)
        if resolved is None:raise ValueError('Generic LibreOffice executable not found; no document changed')
        args.soffice=str(Path(resolved).resolve())
    if qa.exists():raise ValueError('Use a fresh QA directory; preserve previous evidence')
    receipt_path=docx.with_suffix('.build.json');receipt=json.loads(receipt_path.read_text(encoding='utf-8'))
    if receipt['sha256']!=sha(docx):raise ValueError('DOCX differs from builder receipt')
    expected_fonts = list(dict.fromkeys(receipt.get(k, '') for k in ('body_font', 'heading_font')))
    expected_fonts = [name for name in expected_fonts if name]
    if not expected_fonts:
        raise ValueError('Builder receipt has no expected fonts; rebuild with explicit font metadata')
    substitutes = parse_substitutions(getattr(args, 'font_substitute', []))
    qa.mkdir(parents=True)
    availability = preflight(expected_fonts, substitutes)
    (qa/'font-preflight.json').write_text(json.dumps(availability, ensure_ascii=False, indent=2)+'\n', encoding='utf-8')
    parts=load(docx);original_xml=ET.fromstring(parts['word/document.xml'])
    native=receipt.get('toc','').startswith(('native_toc_', 'verified_native_toc_'))
    expected=headings(original_xml,native)
    if not expected:raise ValueError('No bookmarked Heading paragraphs')
    local=links_check(docx,parts);before=sha(docx);known={};passes=[]
    if native:
        cache_toc(parts,{})
        save(docx,parts)
    env=os.environ.copy()
    env['PYTHONUTF8']='1'
    if runtime:env['PATH']=str(runtime)+os.pathsep+env.get('PATH','')
    if args.font_dir:
        config=ET.Element('fontconfig')
        for folder in args.font_dir:
            if not folder.is_dir():raise ValueError('Missing font directory: '+str(folder))
            ET.SubElement(config,'dir').text=str(folder.resolve())
        ET.SubElement(config,'cachedir').text=str(qa/'font-cache')
        config_path=qa/'fonts.conf'
        config_path.write_bytes(ET.tostring(config,xml_declaration=True,encoding='UTF-8',doctype='<!DOCTYPE fontconfig SYSTEM "urn:fontconfig:fonts.dtd">'))
        env['FONTCONFIG_FILE']=str(config_path)
    for iteration in range(1,5):
        rendered=qa/f'pass-{iteration}'
        command=[sys.executable,str(renderer),str(docx),'--output_dir',str(rendered),'--emit_pdf']
        if args.renderer_mode == 'generic':command += ['--soffice',args.soffice]
        proc=subprocess.run(command,env=env,capture_output=True,text=True,timeout=300, encoding='utf-8')
        (qa/f'render-{iteration}.log').write_text(proc.stdout+'\n'+proc.stderr, encoding='utf-8')
        pdfs=list(rendered.glob('*.pdf'))
        if proc.returncode or len(pdfs)!=1 or not pdfs[0].stat().st_size:raise ValueError('Rendering failed; inspect '+str(qa/f'render-{iteration}.log'))
        physical,count=mapping(pdfs[0],expected)
        offset=min(physical.values())-1 if native else 0
        pages={key:value-offset for key,value in physical.items()}
        pngs=sorted(rendered.glob('page-*.png'),key=lambda p:int(re.search(r'page-(\d+)',p.name).group(1)))
        if len(pngs)!=count:raise ValueError('Missing rendered page images')
        passes.append({'iteration':iteration,'docx_sha256':sha(docx),'page_count':count,'page_map':pages,'physical_page_map':physical})
        if pages==known:
            # The latest DOCX cache, actual heading map and rendered TOC agree.
            reader=PdfReader(pdfs[0]);dest_pages=set()
            page_ids={p.indirect_reference.idnum:i for i,p in enumerate(reader.pages)}
            for page in reader.pages:
                for ann in page.get('/Annots',[]):
                    item=ann.get_object();action=item.get('/A',{})
                    destination=item.get('/Dest') or action.get('/D')
                    if isinstance(destination,list) and destination and hasattr(destination[0],'idnum'):
                        number=page_ids.get(destination[0].idnum)
                        if number is not None: dest_pages.add(number+1)
            if not set(physical.values()).issubset(dest_pages):raise ValueError('PDF internal link target missing')
            if native:verify_native_render(pdfs[0],expected,pages,physical)
            font_check = inspect_pdf(pdfs[0], expected_fonts, substitutes)
            (qa/'pdf-fonts.json').write_text(json.dumps(font_check, ensure_ascii=False, indent=2)+'\n', encoding='utf-8')
            if font_check['status'] not in ('MATCHED', 'SUBSTITUTION_ACCEPTED'):
                raise ValueError('Final PDF fonts require correction or explicit review; inspect pdf-fonts.json and rebuild into a new QA directory')
            receipt['font_availability'] = availability['status']
            receipt['font_verification'] = font_check
            receipt.update(sha256=sha(docx),runtime_profile=args.renderer_mode,status='FIELDS_UPDATED_VISUAL_REVIEW_REQUIRED',toc='verified_native_toc_h1_h2' if native else 'verified_clickable_dot_leader_page_map',field_update={'before_sha256':before,'page_count':count,'page_map':pages,'physical_page_map':physical,'passes':iteration,'method':'native_toc_result_rebuild_from_rendered_heading_pages' if native else 'pageref_cache_update'})
            receipt_path.write_text(json.dumps(receipt,ensure_ascii=False,indent=2)+'\n', encoding='utf-8')
            record={'status':'FIELDS_UPDATED_VISUAL_REVIEW_REQUIRED','docx_sha256':sha(docx),'renderer':str(renderer),'page_count':count,'inspected_pages':[],'passes':passes,'local_links':local,'final_pdf':str(pdfs[0].relative_to(qa)),'page_images':[{'path':str(p.relative_to(qa)),'sha256':sha(p)} for p in pngs],'unresolved_issues':['All final page images require actual visual inspection.']}
            record['runtime_profile']=args.renderer_mode
            record['font_verification']={'status': font_check['status'], 'report': 'pdf-fonts.json', 'sha256': sha(qa/'pdf-fonts.json')}
            (qa/'word-finalization.json').write_text(json.dumps(record,ensure_ascii=False,indent=2)+'\n', encoding='utf-8')
            print(json.dumps({'status':record['status'],'pages':count,'passes':iteration,'report':str(qa/'word-finalization.json')}));return
        parts=load(docx)
        (cache_toc if native else cache_pages)(parts,pages)
        save(docx,parts);known=pages
    raise ValueError('Pagination did not converge in four renders; inspect layout, do not ship stale pages')

def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('--docx',type=Path,required=True);p.add_argument('--output-dir',type=Path,required=True)
    p.add_argument('--renderer',type=Path,required=True);p.add_argument('--runtime-bin',type=Path)
    p.add_argument('--renderer-mode',choices=['codex','generic'],default='codex')
    p.add_argument('--soffice',help='Explicit local LibreOffice executable for generic route')
    p.add_argument('--font-dir',type=Path,action='append',default=[],help='Actual local font folders; creates task-local fontconfig only')
    p.add_argument('--font-substitute', action='append', default=[], help='Explicitly accepted requested-family=actual-family; repeat as needed')
    a=p.parse_args()
    try:finalize(a)
    except (ValueError,OSError,KeyError,subprocess.TimeoutExpired) as ex:p.exit(2,'finalize_word: '+str(ex)+'\n')
if __name__=='__main__':main()
