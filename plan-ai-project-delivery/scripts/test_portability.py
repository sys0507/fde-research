#!/usr/bin/env python3
"""Unicode output under strict encoding warnings and an injected GBK text default.

Child processes override only omitted/locale text encodings. Explicit UTF-8 reads
remain intact. This tests deterministic legacy-encoding behavior, not a claim
that every OS locale has been exercised. No package or customer file is modified.
"""
from pathlib import Path
import json
import os
import subprocess
import sys
import tempfile
import unittest

ROOT=Path(__file__).resolve().parents[1]
PACKAGE=ROOT.parent
LABEL='\u62a5\u4ef7 \u7532\u65b9\u53e6\u4ed8'
CHILD="""import builtins,io,runpy,sys
from pathlib import Path
sys.path.insert(0,str(Path(sys.argv[1]).resolve().parent))
def wrap(original):
    def opened(file,mode='r',buffering=-1,encoding=None,errors=None,newline=None,closefd=True,opener=None):
        if 'b' not in mode and encoding in (None,'locale'):
            encoding='gbk'
        return original(file,mode,buffering,encoding,errors,newline,closefd,opener)
    return opened
io.open=wrap(io.open)
builtins.open=wrap(builtins.open)
sys.argv=sys.argv[1:]
runpy.run_path(sys.argv[0],run_name='__main__')
"""


class PortabilityTests(unittest.TestCase):
    def setUp(self):
        temp=tempfile.TemporaryDirectory(prefix='fde-encoding-')
        self.addCleanup(temp.cleanup)
        self.root=Path(temp.name)

    def json(self,name,data):
        path=self.root/name
        path.write_text(json.dumps(data,ensure_ascii=False),encoding='utf-8')
        return path

    def run_script(self,path,*args):
        command=[sys.executable,'-B','-X','utf8=0','-X','warn_default_encoding',
                 '-W','error::EncodingWarning','-c',CHILD,str(path),*map(str,args)]
        result=subprocess.run(command,capture_output=True,
                              env=dict(os.environ,PYTHONUTF8='0',PYTHONDONTWRITEBYTECODE='1'))
        self.assertEqual(result.returncode,0,result.stderr.decode('utf-8',errors='backslashreplace'))

    def test_scenario_input_template_and_output(self):
        ui={key:LABEL for key in ['product','organization','module','person','role','object','task','basis','time']}
        ui['navigation']=[LABEL]
        ui['states']={phase:{'title':LABEL,'blocks':[{'type':'facts','title':LABEL,'items':[]}]} for phase in ['before','after']}
        source=self.json('scenes.json',{'scenes':[{'id':'S01','title':LABEL,'demo':'screens/S01.html','ui':ui}]})
        self.run_script(PACKAGE/'fde-ai-scenario-design/scripts/build_screens.py',source)
        self.assertIn(LABEL,(self.root/'screens/S01.html').read_text(encoding='utf-8'))

    def test_source_index_and_previous_version(self):
        (self.root/'original.md').write_text(LABEL,encoding='utf-8')
        selection=self.json('selection.json',[{'id':'S1','path':'original.md','title':LABEL,'version':'V1','status':LABEL,'use':LABEL,'decision':'adopted'}])
        first=self.root/'first.json';second=self.root/'second.json'
        script=ROOT/'scripts/index_inputs.py'
        self.run_script(script,'--root',self.root,'--selection',selection,'--output',first)
        self.run_script(script,'--root',self.root,'--selection',selection,'--previous',first,'--output',second)
        data=json.loads(second.read_text(encoding='utf-8'))
        self.assertEqual(data['sources'][0]['title'],LABEL)
        self.assertEqual(data['changes'],[])

    def test_inherited_baseline_manifest_and_render(self):
        (self.root/'original.txt').write_text(LABEL+' 123.45',encoding='utf-8')
        data={'adoption_instruction':LABEL,'sources':[{'id':'S1','path':'original.txt'}],
              'facts':{'price':{'source_id':'S1','locator':LABEL,'visibility':'client','status':'adopted_estimate','unit':'CNY','value':'123.45'}},
              'scope_review':{'conclusion':LABEL,'changes':[],'conflicts':[],'missing_details':[]}}
        source=self.json('adopt.json',data);output=self.root/'inherited'
        script=ROOT/'scripts/inherit_baseline.py'
        self.run_script(script,'adopt','--input',source,'--source-root',self.root,'--output',output)
        (output/'internal/source.md').write_text(LABEL+' {{baseline.price}}',encoding='utf-8')
        self.run_script(script,'render','--root',output,'--template','internal/source.md','--output','client/report.md')
        self.run_script(script,'check','--root',output)
        self.assertEqual((output/'client/report.md').read_text(encoding='utf-8'),LABEL+' 123.45')

    def test_delivery_index_preserves_unicode_paths_and_metadata(self):
        from test_runtime import RuntimeTests
        fixture=RuntimeTests()
        fixture.setUp()
        self.addCleanup(fixture.doCleanups)
        args=fixture.prepare_delivery()
        extra=args.root/'client'/('\u9644\u4ef6.md')
        extra.write_text(LABEL,encoding='utf-8')
        receipt=args.root/'client/report.build.json'
        data=json.loads(receipt.read_text(encoding='utf-8'));data['note']=LABEL
        receipt.write_text(json.dumps(data,ensure_ascii=False),encoding='utf-8')
        self.run_script(ROOT/'scripts/check_delivery.py','--root',args.root,'--markdown',args.markdown,'--docx',args.docx)
        result=json.loads((args.root/'delivery-index.json').read_text(encoding='utf-8'))
        self.assertIn('client/\u9644\u4ef6.md',[r['path'] for r in result['artifacts']])


if __name__=='__main__':
    unittest.main()
