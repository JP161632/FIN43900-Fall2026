"""Execute the student's committed terminal-growth specification, preserving receipts."""
import datetime as dt
import hashlib
import json
from pathlib import Path
import subprocess
import sys

ROOT=Path(__file__).resolve().parent
REPO=ROOT.parents[1]


def digest(path):return hashlib.sha256(path.read_bytes()).hexdigest()


def git(*args):
    return subprocess.run(['git',*args],cwd=REPO,capture_output=True,text=True,check=True).stdout.strip()


def main():
    spec_path=ROOT/'evidence/locked-growth-precommit.json'
    rel=spec_path.relative_to(REPO).as_posix()
    spec=json.loads(spec_path.read_text(encoding='utf-8'))
    assert spec['old_value']==0.03 and spec['new_value']==0.025
    assert not git('status','--porcelain','--',rel),'Prediction must be committed before execution'
    commit=git('log','-1','--format=%H','--',rel)
    committed=json.loads(git('show',commit+':'+rel));assert committed==spec
    commit_time=git('show','-s','--format=%cI',commit)
    started=dt.datetime.now(dt.timezone.utc)
    assert dt.datetime.fromisoformat(commit_time)<started
    frozen_before=digest(ROOT/'outputs/results.json');input_before=digest(ROOT/'data/inputs.json')
    target=ROOT/'evidence/locked-growth'
    runs={}
    for name,value in [('baseline',spec['old_value']),('changed',spec['new_value'])]:
        out=target/name
        if out.exists():raise SystemExit('Run artifacts already exist; preserve them. Use the saved receipt rather than rerunning this historical exercise.')
        command=[sys.executable,str(ROOT/'run.py'),'--growth',str(value),'--output',str(out)]
        begin=dt.datetime.now(dt.timezone.utc).isoformat()
        completed=subprocess.run(command,cwd=ROOT,capture_output=True,text=True)
        out.mkdir(parents=True,exist_ok=True)
        log={'started_utc':begin,'ended_utc':dt.datetime.now(dt.timezone.utc).isoformat(),
             'command_from_project_folder':f'python run.py --growth {value} --output evidence/locked-growth/{name}',
             'return_code':completed.returncode,'stdout':completed.stdout,'stderr':completed.stderr}
        log_path=out/'execution-log.json';log_path.write_text(json.dumps(log,indent=2)+'\n',encoding='utf-8',newline='\n')
        if completed.returncode:raise SystemExit('Locked run failed; inspect preserved '+str(log_path))
        result_path=out/'scenario.json';r=json.loads(result_path.read_text(encoding='utf-8'))
        runs[name]={'output_path':result_path.relative_to(ROOT).as_posix(),'sha256':digest(result_path),
                    'log_path':log_path.relative_to(ROOT).as_posix(),'log_sha256':digest(log_path),
                    'growth':r['growth'],'per_share':r['per_share'],'enterprise_value_millions':r['enterprise_value'],
                    'equity_value_millions':r['equity_value'],'terminal_fcff_millions':r['terminal_fcff'],
                    'pv_terminal_millions':r['pv_terminal'],'terminal_share':r['terminal_share'],
                    'entry_ceiling':r['entry_ceiling'],'action':r['action']}
    old=json.loads((ROOT/runs['baseline']['output_path']).read_text(encoding='utf-8'))
    new=json.loads((ROOT/runs['changed']['output_path']).read_text(encoding='utf-8'))
    assert old['forecast']==new['forecast'],'Operating forecast changed in terminal-only test'
    for key in ['wacc','terminal_roic','diluted_shares','bridge']:assert old[key]==new[key],key
    assert frozen_before==digest(ROOT/'outputs/results.json') and input_before==digest(ROOT/'data/inputs.json')
    assert abs(old['per_share']-json.loads((ROOT/'outputs/results.json').read_text(encoding='utf-8'))['cases']['base']['per_share'])<1e-9
    direction='lower' if new['per_share']<old['per_share'] else 'higher' if new['per_share']>old['per_share'] else 'unchanged'
    record={'status':'EXECUTED / PASS','prediction_commit':commit,'prediction_commit_time':commit_time,
            'prediction_specification_sha256':digest(spec_path),'started_utc':started.isoformat(),
            'ended_utc':dt.datetime.now(dt.timezone.utc).isoformat(),'operator':'Assistant executing the student-authored, committed prediction',
            'specification':spec,'runs':runs,'actual_direction':direction,
            'expected_direction_matches':direction==spec['student_expected_valuation_direction'],
            'expected_action_matches':new['action']==spec['student_expected_action'],
            'per_share_change':new['per_share']-old['per_share'],
            'per_share_percentage_change':100*(new['per_share']/old['per_share']-1),
            'operating_forecast_unchanged':True,'held_fixed_checks':['wacc','terminal_roic','diluted_shares','bridge'],
            'original_inputs_unchanged_sha256':input_before,'financial_results_unchanged_sha256':frozen_before,
            'magnitude_assessment':'Student predicted much lower without a numerical threshold. Report observed size rather than claiming a quantified magnitude target passed.',
            'no_change_reason':'Market price $218.36 remains above changed intrinsic value and the 20%-discount entry ceiling; lower terminal growth reinforces deferral.',
            'mechanism':'Lower terminal g lowers the growth multiplier and increases WACC-minus-g, while lower g/ROIC reinvestment partly offsets the valuation decline. Explicit five-year forecasts stay fixed.',
            'authorship_boundary':'Student supplied original prediction, exact rate and expected action before this run. Assistant recorded/executed. Instructor AI-wording permission is student-reported; no independent AI-off attestation is invented.'}
    assert record['expected_direction_matches'] and record['expected_action_matches']
    (ROOT/'evidence/locked-growth-results.json').write_text(json.dumps(record,indent=2)+'\n',encoding='utf-8',newline='\n')
    print(json.dumps({k:record[k] for k in ['status','prediction_commit','actual_direction','per_share_change','per_share_percentage_change','expected_action_matches']},indent=2))
    print(json.dumps(runs,indent=2))


if __name__=='__main__':main()
