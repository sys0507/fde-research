#!/usr/bin/env python3
"""Bind an agent-authored source selection to original-file hashes (standard library)."""
import argparse, hashlib, json
from pathlib import Path

def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('--root',type=Path,required=True)
    p.add_argument('--selection',type=Path,required=True)
    p.add_argument('--output',type=Path,required=True)
    p.add_argument('--previous',type=Path)
    args=p.parse_args()
    try:
        root=args.root.resolve();records=json.loads(args.selection.read_text(encoding='utf-8'));seen=set();out=[]
        if not isinstance(records,list) or not records:raise ValueError('selection must be a nonempty list')
        for record in records:
            for k in ('id','path','title','version','status','use','decision'):
                if not isinstance(record.get(k),str) or not record[k].strip():raise ValueError('Source needs '+k)
            if record['id'] in seen:raise ValueError('Duplicate source id')
            seen.add(record['id']);path=(root/record['path']).resolve()
            if not path.is_relative_to(root) or not path.is_file():raise ValueError('Source missing or outside input root: '+record['path'])
            if record['decision'] not in ('adopted','reference','superseded'):raise ValueError('Unknown source decision')
            out.append(dict(record,path=path.relative_to(root).as_posix(),bytes=path.stat().st_size,sha256=hashlib.sha256(path.read_bytes()).hexdigest()))
        result={'schema_version':1,'sources':out,'note':'Selection, version and status are agent judgments grounded in the cited original; hashing does not imply approval.'}
        if args.previous:
            previous={x['id']:x for x in json.loads(args.previous.read_text(encoding='utf-8'))['sources']};current={x['id']:x for x in out}
            result['changes']=[{'id':i,'before':previous.get(i),'after':current.get(i)} for i in sorted(set(previous)|set(current)) if previous.get(i)!=current.get(i)]
        if args.output.exists():raise ValueError('Output exists; choose a new version')
        args.output.parent.mkdir(parents=True,exist_ok=True);args.output.write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n', encoding='utf-8')
        print('PASS input-index '+str(len(out)))
    except (ValueError,OSError,KeyError,TypeError) as e:p.exit(2,'index_inputs: '+str(e)+'\n')
if __name__=='__main__':main()
