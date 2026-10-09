#!/usr/bin/env python3
"""Check configurable simulation labels and safe HTML payload construction."""
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

SCRIPT=Path(__file__).with_name('build_screens.py')


class ScreenLabelTests(unittest.TestCase):
    def build(self, label=None):
        temp=tempfile.TemporaryDirectory(prefix='fde-screen-test-')
        self.addCleanup(temp.cleanup)
        root=Path(temp.name)
        ui={key:'Example' for key in ['product','organization','module','person','role','object','task','basis','time']}
        ui['navigation']=['List']
        ui['states']={phase:{'title':phase,'blocks':[{'type':'facts','title':'Record','items':[]}]} for phase in ['before','after']}
        if label is not None:
            ui['simulation_label']=label
        data={'scenes':[{'id':'S01','title':'Test scenario','demo':'screens/S01.html','ui':ui}]}
        source=root/'input.json'
        source.write_text(json.dumps(data,ensure_ascii=False),encoding='utf-8')
        proc=subprocess.run([sys.executable,'-X','utf8',str(SCRIPT),str(source)],capture_output=True,text=True,encoding='utf-8')
        return proc, root/'screens/S01.html'

    def test_default_is_project_neutral_and_explicitly_simulated(self):
        proc,path=self.build()
        self.assertEqual(proc.returncode,0,proc.stderr)
        html=path.read_text(encoding='utf-8')
        self.assertIn('Simulation · Not a production system',html)
        self.assertNotIn('Teaching simulation · Local demo',html)

    def test_label_payload_cannot_inject_html_script(self):
        proc,path=self.build('Simulation </script><script>alert(1)</script>')
        self.assertEqual(proc.returncode,0,proc.stderr)
        html=path.read_text(encoding='utf-8')
        self.assertNotIn('</script><script>alert(1)',html)
        self.assertIn('\\u003c/script\\u003e',html)

    def test_empty_label_is_rejected(self):
        proc,path=self.build(' ')
        self.assertNotEqual(proc.returncode,0)
        self.assertFalse(path.exists())


if __name__=='__main__':
    unittest.main()
