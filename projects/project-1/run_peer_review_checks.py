"""Independent follow-up to the attributed peer challenge; not a human locked test."""
import copy
import datetime as dt
import hashlib
import importlib.util
import json
from pathlib import Path
import subprocess
import sys
from model import valuation

ROOT=Path(__file__).resolve().parent
REPO=ROOT.parents[1]


def main():
    before=hashlib.sha256((ROOT/'outputs/results.json').read_bytes()).hexdigest()
    module_path=REPO/'projects/lab-11-nvda-sensitivity/nvda_sensitivity.py'
    spec=importlib.util.spec_from_file_location('legacy_lab11',module_path)
    legacy=importlib.util.module_from_spec(spec)
    original_bytecode_setting=sys.dont_write_bytecode
    try:
        sys.dont_write_bytecode=True
        spec.loader.exec_module(legacy)
    finally:
        sys.dont_write_bytecode=original_bytecode_setting
    base=legacy.run(legacy.BASE_INPUTS)
    high=legacy.run(legacy.BASE_INPUTS,'GROSS_MARGIN',legacy.DRIVERS[1]['higher'])
    low=legacy.run(legacy.BASE_INPUTS,'REVENUE_GROWTH',legacy.DRIVERS[0]['lower'])
    assert all(x['valid'] for x in [base,high,low])
    b=base['statements'][2031];h=high['statements'][2031];l=low['statements'][2031]
    op=h['Operating income']-b['Operating income'];tax=h['Tax']-b['Tax']
    wc=-(h['Change in inventory']-b['Change in inventory'])+(h['Change in accounts payable']-b['Change in accounts payable'])
    cash=h['FCFE before shareholder payouts']-b['FCFE before shareholder payouts']
    assert abs(op-tax+wc-cash)<1e-6
    assert round(cash,2)==8952.95 and round(b['FCFE before shareholder payouts'],2)==242008.19
    d=json.loads((ROOT/'data/inputs.json').read_text(encoding='utf-8'))
    historical_margin=d['history']['FY26']['gross_profit']/d['history']['FY26']['revenue']
    assert d['history']['FY26']['revenue']==215938 and round(100*historical_margin,1)==71.1
    current=valuation(d)
    groups={}
    for driver in ['data_center_growth','gross_margin']:
        group={}
        for label,factor in [('lower',0.95),('higher',1.05)]:
            changed=copy.deepcopy(d)
            changed['cases']['base'][driver]=[x*factor for x in d['cases']['base'][driver]]
            result=valuation(changed)
            group[label]={'factor':factor,'input_path':'cases.base.'+driver,
                          'old_path':d['cases']['base'][driver],'new_path':changed['cases']['base'][driver],
                          'per_share':result['per_share'],'action':result['action'],
                          'year5_ebit_millions':result['forecast'][-1]['income_statement']['ebit'],
                          'year5_fcff_millions':result['forecast'][-1]['fcff'],
                          'max_articulation_error_millions':max(abs(e) for year in result['forecast'] for e in year['checks'].values())}
        assert group['lower']['per_share']<current['per_share']<group['higher']['per_share']
        group['per_share_span']=group['higher']['per_share']-group['lower']['per_share']
        group['year5_ebit_span_millions']=group['higher']['year5_ebit_millions']-group['lower']['year5_ebit_millions']
        group['year5_fcff_span_millions']=group['higher']['year5_fcff_millions']-group['lower']['year5_fcff_millions']
        groups[driver]=group
    after=hashlib.sha256((ROOT/'outputs/results.json').read_bytes()).hexdigest();assert before==after
    commit=subprocess.run(['git','log','-1','--format=%H','--','projects/project-1/evidence/peer-followup-precommit.md'],cwd=REPO,capture_output=True,text=True,check=True).stdout.strip()
    result={'status':'PASS','executed_utc':dt.datetime.now(dt.timezone.utc).isoformat(),
            'operator':'Assistant; follow-up executed October19, not claimed as the October1 joint event or student lock',
            'prediction_commit':commit,'credit':'peer challenge','discussion_date':'2026-10-01',
            'legacy_model_sha256':hashlib.sha256(module_path.read_bytes()).hexdigest(),
            'historical_source_check':{'revenue_millions':215938,'gross_profit_millions':153463,'gaap_gross_margin':historical_margin},
            'legacy_margin_trace':{'operating_income_change':op,'tax_change':tax,'net_wc_contribution':wc,'fcfe_increase':cash,
                                   'base_fcfe':b['FCFE before shareholder payouts'],'higher_margin_fcfe':h['FCFE before shareholder payouts'],
                                   'rounded_components_sum':round(op,2)-round(tax,2)+round(wc,2),
                                   'unrounded_reconciliation_error':op-tax+wc-cash},
            'legacy_lower_growth':{'ebit_delta':l['Operating income']-b['Operating income'],
                                   'fcfe_delta':l['FCFE before shareholder payouts']-b['FCFE before shareholder payouts'],
                                   'fcfe':l['FCFE before shareholder payouts']},
            'equal_relative_shocks':groups,'baseline_per_share':current['per_share'],'baseline_action':current['action'],
            'range_interpretation':'Equal relative driver shocks do not equate economic plausibility, risk or probability; output ranking is conditional on metric and horizon',
            'financial_results_unchanged_sha256':after}
    (ROOT/'outputs/peer-review-checks.json').write_text(json.dumps(result,indent=2)+'\n',encoding='utf-8',newline='\n')
    print(json.dumps(result,indent=2))


if __name__=='__main__':main()
