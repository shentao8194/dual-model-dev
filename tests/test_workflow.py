import importlib.util
import json
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch

SPEC=importlib.util.spec_from_file_location('workflow',Path(__file__).parents[1]/'skills/dual-model-dev/scripts/workflow.py')
w=importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(w)

class WorkflowTests(unittest.TestCase):
    def setUp(self):
        self.temp=tempfile.TemporaryDirectory()
        self.root=Path(self.temp.name)/'project'; self.root.mkdir()
        self.state=Path(self.temp.name)/'state'; self.state.mkdir()
        self.patches=[patch.object(w,'STATE',self.state),patch.object(w,'RUNS',self.state/'runs'),patch.object(w,'CONFIG',self.state/'config.json')]
        for p in self.patches:p.start()
        self.cfg={'base_url':'https://ark.ap-southeast.bytepluses.com/api/v3','api_key_env':'TEST_MISSING_KEY',
                  'planner':'test-kimi','executor':'test-deepseek','max_calls':48,'max_total_tokens':500000,
                  'max_output_tokens':4096,'timeout_seconds':1800,'max_repairs':0}
        self.job='a'*32
        w.dump(w.CONFIG,self.cfg)
        w.dump(w.RUNS/self.job/'request.json',{'project_dir':str(self.root),'task':'Write an explanation',
                'plan':'Explain addition with one example','mode':'writing','test_commands':[],'config':self.cfg})
        with patch.object(w,'credential',return_value='fake-test-key'):self.r=w.Runner(self.job)
    def tearDown(self):
        for p in self.patches:p.stop()
        self.temp.cleanup()
    def test_writing_model_routing_and_deliverable(self):
        seen=[]
        def agent(stage,model,prompt,writable=False):
            seen.append((stage,model,writable))
            if stage=='writing-draft':self.r.execute('write_file',{'path':'article.md','content':'Addition combines quantities.'},True)
            return 'Checked\nVERDICT: PASS'
        with patch.object(self.r,'agent',side_effect=agent):self.r.run()
        self.assertEqual([x[1] for x in seen],['test-kimi','test-deepseek'])
        self.assertEqual(w.status(self.job)['state'],'completed')
    def test_missing_plan_stops(self):
        self.r.req['plan']=''
        with self.assertRaises(ValueError):self.r.run()
    def test_private_and_escape_paths(self):
        for p in ['../outside','.env','.git/config','secret.key']:
            with self.assertRaises(ValueError):self.r.path(p)
    def test_review_cannot_write(self):
        with self.assertRaises(ValueError):self.r.execute('write_file',{'path':'a','content':'x'},False)
    def test_bad_endpoint_rejected(self):
        self.cfg['base_url']='https://example.com/api/v3'; w.dump(w.CONFIG,self.cfg)
        with self.assertRaises(ValueError):w.config()
    def test_coding_plan_rejects_writing(self):
        self.cfg['base_url']='https://ark.ap-southeast.bytepluses.com/api/coding/v3'; w.dump(w.CONFIG,self.cfg)
        with self.assertRaisesRegex(ValueError,'general-purpose'):
            w.start(str(self.root),'write',[],mode='writing',plan='outline')
    def test_real_test_exit_status(self):
        self.r.req['test_commands']=[[w.sys.executable,'-c','raise SystemExit(2)']]
        self.assertEqual(self.r.tests()[0]['exit_code'],2)
    def test_cancel_boundary(self):
        (self.r.folder/'cancel').touch()
        with self.assertRaises(RuntimeError):self.r.guard()

if __name__=='__main__':unittest.main()
