"""Render readable course records from templates and executed evidence."""
import hashlib
import json
from pathlib import Path
import re
import subprocess

ROOT=Path(__file__).resolve().parent
REPO=ROOT.parents[1]


def write(path,text):
    (ROOT/path).write_text(text.strip()+'\n',encoding='utf-8',newline='\n')


def main():
    r=json.loads((ROOT/'outputs/results.json').read_text(encoding='utf-8'))
    v=json.loads((ROOT/'outputs/validation-results.json').read_text(encoding='utf-8'))
    b=r['cases']['base'];lo=r['cases']['low'];hi=r['cases']['high']
    baseline=(ROOT/'evidence/edition-a-existing-nvidia-unchanged.md').read_bytes()
    digest=hashlib.sha256(baseline).hexdigest().upper()
    assert digest=='FF289D7D83BF56F977D5D3F85F7CDF13125841075D5E8A59AF03FA845D39ED6B'
    changed=next(x['result'] for x in v['tests'] if x['test']=='Prewritten directional changed input')
    values={'base':f"{b['per_share']:.2f}",'low':f"{lo['per_share']:.2f}",'high':f"{hi['per_share']:.2f}",
            'entry':f"{b['entry_ceiling']:.2f}",'wacc':f"{b['wacc']:.2%}",'terminal_share':f"{b['terminal_share']:.1%}",
            'changed_value':f"{changed['new_price']:.2f}",'tests':str(len(v['tests'])),
            'ev_billions':f"{b['enterprise_value']/1000:,.2f}",'equity_billions':f"{b['equity_value']/1000:,.2f}",
            'bridge_billions':f"{sum(b['bridge'].values())/1000:,.2f}",
            'reverse_shift':f"{r['reverse_dcf']['constant_increment_to_each_dc_growth']*100:.2f}",
            'edition_a_text':baseline.decode('utf-8').strip(),'baseline_hash_1':digest[:32],'baseline_hash_2':digest[32:]}
    prior=[]
    for name in ['lab-05-nvda-dcf','lab-08-nvda-pe','lab-10-nvda-proforma','lab-11-nvda-sensitivity','lab-12-nvda-review']:
        for file in sorted((REPO/'projects'/name).glob('*')):
            if file.suffix not in ['.md','.py']:continue
            relative=file.relative_to(REPO).as_posix()
            commit=subprocess.run(['git','log','-1','--format=%H','--',relative],cwd=REPO,capture_output=True,text=True,check=True).stdout.strip()
            prior.append({'path':relative,'sha256':hashlib.sha256(file.read_bytes()).hexdigest(),'last_commit':commit,
                          'use':'Historical research trail, not unqualified final valuation evidence'})
    write('evidence/prior-lab-index.json',json.dumps(prior,indent=2))
    for name in ['research-evolution','decision-memo','validation-and-ai-use']:
        text=(ROOT/'docs/templates'/f'{name}.md').read_text(encoding='utf-8')
        for key,value in values.items():text=text.replace('{{'+key+'}}',value)
        assert not re.search(r'\{\{[a-z_]+\}\}',text),name
        write(f'docs/{name}.md',text)
    write('Student next steps.md',(ROOT/'docs/recording-guide.md').read_text(encoding='utf-8'))
    print('Built readable records; preserved original baseline and supplied transcripts.')


if __name__=='__main__':main()
