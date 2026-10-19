"""Reconcile final edited text with executed finance evidence; never infer audio review."""
import hashlib
import json
from pathlib import Path

ROOT=Path(__file__).resolve().parent


def main():
    results=json.loads((ROOT/'outputs/results.json').read_text(encoding='utf-8'))
    validation=json.loads((ROOT/'outputs/validation-results.json').read_text(encoding='utf-8'))
    changed=next(x['result'] for x in validation['tests'] if x['test']=='Prewritten directional changed input')
    review=json.loads((ROOT/'evidence/video-review.json').read_text(encoding='utf-8'))
    checks=[]
    def check(name,ok,detail):
        checks.append({'check':name,'status':'PASS' if ok else 'FAIL','detail':detail})
    texts={i:(ROOT/'docs'/f'transcript-video-{i}.txt').read_text(encoding='utf-8') for i in [1,2,3]}
    values=[f"{results['cases'][k]['per_share']:.2f}" for k in ['low','base','high']]
    check('Research evolution values',all(x in texts[1] for x in values+['62.72','15.88%','218.36']), 'Earlier/current valuation, range and dated price match saved evidence')
    check('Investment-gain correction','unrealized investment gains are not operating cash generation' in texts[1], 'No unrealized investment gains treated as operating cash')
    check('Code/validation values',all(x in texts[2] for x in ['75 days','191.5','1,624.87','27.50',f"{changed['old_price']:.2f}",f"{changed['new_price']:.2f}"]), 'Driver, FCFF, known answers and WACC test reconciled')
    check('Committee values and triggers',all(x in texts[3] for x in values+['218.36','108.38','above 95','below 70%','below 20%']), 'Range, bridge context, sensitivity and monitoring conditions consistent')
    for item in review['videos']:
        path=ROOT/item['transcript']
        check(f"Transcript {item['video']} edit boundary/hash",texts[item['video']].startswith('EDITED TRANSCRIPT:') and hashlib.sha256(path.read_bytes()).hexdigest()==item['transcript_sha256'], 'Editorially corrected text; no independently verified verbatim audio claim')
    addendum=(ROOT/'docs/post-recording-validation-addendum.md').read_text(encoding='utf-8')
    locked=json.loads((ROOT/'evidence/locked-growth-results.json').read_text(encoding='utf-8'))
    check('Later updates separately labeled',all(x in addendum for x in ['not a transcript','5a9de1d','2.5%','116.56710','1.70%','14.04','8.89']) and locked['expected_direction_matches'] and locked['expected_action_matches'], 'Written addendum covers actual later results without inventing original speech')
    timings=json.loads((ROOT/'evidence/video-timestamp-index.json').read_text(encoding='utf-8'))
    check('Observed caption-cue indices',len(timings['videos'])==3 and all(len(x['chapters'])>=5 and all(0<=t['caption_start_seconds']<x['duration_seconds'] for t in x['chapters']) for x in timings['videos']) and review.get('timestamp_indices_observed') is True,'Actual source-caption topic times replace planned/guessed timing; audio alignment is a separate check')
    grade=json.loads((ROOT/'evidence/rubric-score-estimate.json').read_text(encoding='utf-8'))
    check('Score arithmetic and non-certification',sum(x['points'] for x in grade['criteria'])==grade['estimated_total'] and 100*grade['estimated_total']/grade['maximum']==grade['estimated_percent'] and grade['grade_guaranteed'] is False and grade['audio_edited'] is False, 'Estimate totals correctly; no actual grade or audio modification implied')
    cross=json.loads((ROOT/'evidence/final-source-crosscheck.json').read_text(encoding='utf-8'))
    check('Selected authoritative source comparison',cross['checks'][0]['revenue_millions']==215938 and cross['checks'][1]['cash_plus_marketable_debt_millions']==56586 and cross['checks'][1]['marketable_equity_separate_millions']==42783, 'Fresh SEC/issuer observation record matches model/source-map definitions')
    record={'status':'PASS' if all(x['status']=='PASS' for x in checks) else 'FAIL','checks':checks,
            'scope':'Edited text, addendum, observed caption-cue indices, grade arithmetic and selected historical facts; actual audio alignment remains unverified',
            'financial_results_sha256':hashlib.sha256((ROOT/'outputs/results.json').read_bytes()).hexdigest()}
    (ROOT/'outputs/final-communication-audit.json').write_text(json.dumps(record,indent=2)+'\n',encoding='utf-8',newline='\n')
    print(json.dumps(record,indent=2))
    if record['status']!='PASS':raise SystemExit(1)


if __name__=='__main__':main()
