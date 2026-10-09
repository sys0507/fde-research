#!/usr/bin/env python3
"""Optional HTML/CSS screen builder. Authors supply scenario-specific ui states and business content."""
import argparse,json,re
from pathlib import Path

def main():
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('input',type=Path);p.add_argument('--overwrite',action='store_true');a=p.parse_args()
    base=a.input.resolve().parent;data=json.loads(a.input.read_text(encoding='utf-8'));template=(Path(__file__).resolve().parents[1]/'assets/screen-template.html').read_text(encoding='utf-8')
    outputs=[]
    for scene in data['scenes']:
        ui=scene['ui'];sid=scene['id']
        for key in ['product','organization','module','person','role','object','task','basis','time']:
            if not isinstance(ui.get(key),str) or not ui[key].strip():raise ValueError(sid+': Missing ui.'+key)
        if not ui.get('navigation'):raise ValueError(sid+': Missing navigation')
        phases=['before','after']+(['result'] if scene.get('result_required') else [])
        if not set(phases)<=ui['states'].keys():raise ValueError(sid+': Missing page state')
        for phase,state in ui['states'].items():
            if phase not in ['before','after','result'] or not state.get('title') or not state.get('blocks'):raise ValueError(sid+': Invalid page')
            if phase=='after' and scene.get('result_required') and state.get('action',{}).get('target')!='result':raise ValueError(sid+': after main action must transition to result')
            if state.get('action') and state['action']['target'] not in ui['states']:raise ValueError(sid+': Action targets a nonexistent state')
            for b in state['blocks']:
                if b.get('type') not in ['facts','table','document','text','messages','timeline'] or not b.get('title'):raise ValueError(sid+': Unsupported block')
        dest=(base/scene['demo']).resolve()
        if not dest.is_relative_to(base) or dest.suffix!='.html':raise ValueError('demo must be inside the delivery directory and be HTML')
        if dest.exists() and not a.overwrite:raise ValueError('Page exists; preserve manual edits before using --overwrite: '+str(dest))
        label=ui.get('simulation_label','Simulation · Not a production system')
        if not isinstance(label,str) or not label.strip():raise ValueError(sid+': simulation_label must identify the simulation')
        payload=dict(ui,id=sid,title=scene['title'],simulation_label=label)
        encoded=json.dumps(payload,ensure_ascii=False).replace('<','\\u003c').replace('>','\\u003e').replace('&','\\u0026')
        outputs.append((dest,template.replace('__SCENE_DATA__',encoded)))
    for dest,text in outputs:
        dest.parent.mkdir(parents=True,exist_ok=True);dest.write_text(text, encoding='utf-8')
    print(json.dumps({'screens':len(outputs),'output':[str(x.relative_to(base)) for x,_ in outputs]},ensure_ascii=False))
if __name__=='__main__':main()
