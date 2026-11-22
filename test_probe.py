import contextlib
import io
import json
import unittest
from unittest.mock import patch
from probe import main

class ProbePolicy(unittest.TestCase):
    def run_probe(self,args,result):
        output=io.StringIO()
        with patch('sys.argv',['probe.py','http://localhost/healthz','--count','1','--interval','0']+args), patch('probe.probe',return_value=result), contextlib.redirect_stdout(output):
            code=main()
        return code,json.loads(output.getvalue().splitlines()[-1])
    def test_default_requires_success(self):
        code,summary=self.run_probe([],{'ok':False,'error':'exercise'})
        self.assertEqual(code,1)
        self.assertEqual(summary['successes'],0)
    def test_explicit_failure_allowance(self):
        code,_=self.run_probe(['--max-failure-percent','100'],{'ok':False,'error':'exercise'})
        self.assertEqual(code,0)
    def test_successful_observation(self):
        code,summary=self.run_probe([],{'ok':True,'status':200})
        self.assertEqual(code,0)
        self.assertEqual(summary['sample_availability_percent'],100)
