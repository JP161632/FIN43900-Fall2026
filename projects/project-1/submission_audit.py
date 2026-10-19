"""Audit artifact consistency; do not misrepresent missing human evidence as complete."""
import csv
import datetime as dt
import hashlib
import json
from pathlib import Path
import re
import subprocess
import sys

ROOT=Path(__file__).resolve().parent


def main():
    checks=[]
    def check(name,condition,detail):
        checks.append({'check':name,'status':'PASS' if condition else 'FAIL','detail':detail})
    d=json.loads((ROOT/'data/inputs.json').read_text(encoding='utf-8')); r=json.loads((ROOT/'outputs/results.json').read_text(encoding='utf-8'))
    v=json.loads((ROOT/'outputs/validation-results.json').read_text(encoding='utf-8'))
    check('Finance validation',v['status']=='PASS' and len(v['tests'])==15,'15claim-focused tests, actual results in validation-results.json')
    peer=json.loads((ROOT/'outputs/peer-review-checks.json').read_text(encoding='utf-8'))
    peer_status=json.loads((ROOT/'evidence/submission-status.json').read_text(encoding='utf-8'))
    check('Attributed peer challenge and independent follow-up',peer['status']=='PASS' and peer_status['partner_review'].startswith('SUPPLIED') and peer['credit']=='peer challenge' and abs(peer['legacy_margin_trace']['unrounded_reconciliation_error'])<1e-6 and peer['equal_relative_shocks']['gross_margin']['per_share_span']>peer['equal_relative_shocks']['data_center_growth']['per_share_span'] and peer['financial_results_unchanged_sha256']==hashlib.sha256((ROOT/'outputs/results.json').read_bytes()).hexdigest(),'Student-confirmed Antigravity log; named dispositions; independently reproduced legacy trace and equal-relative range challenge; separate from the student terminal-growth record')
    locked=json.loads((ROOT/'evidence/locked-growth-results.json').read_text(encoding='utf-8'))
    artifact_matches=all(hashlib.sha256((ROOT/x['output_path']).read_bytes()).hexdigest()==x['sha256'] and hashlib.sha256((ROOT/x['log_path']).read_bytes()).hexdigest()==x['log_sha256'] and json.loads((ROOT/x['log_path']).read_text(encoding='utf-8'))['return_code']==0 for x in locked['runs'].values())
    spec_committed=subprocess.run(['git','show',locked['prediction_commit']+':projects/project-1/evidence/locked-growth-precommit.json'],cwd=ROOT.parents[1],capture_output=True,text=True,check=True).stdout
    check('Student prediction precommit and executed growth comparison',locked['status']=='EXECUTED / PASS' and dt.datetime.fromisoformat(locked['prediction_commit_time'])<dt.datetime.fromisoformat(locked['started_utc']) and json.loads(spec_committed)==locked['specification'] and artifact_matches and locked['expected_direction_matches'] and locked['expected_action_matches'] and locked['operating_forecast_unchanged'] and locked['financial_results_unchanged_sha256']==hashlib.sha256((ROOT/'outputs/results.json').read_bytes()).hexdigest(),'Student-selected 3% to 2.5%; immutable prediction before run; $118.58 to $116.57 (-1.70%); unchanged WATCH/DEFER; modest magnitude explicitly assessed; assistant execution and instructor-permission basis recorded')
    baseline=hashlib.sha256((ROOT/'evidence/edition-a-existing-nvidia-unchanged.md').read_bytes()).hexdigest()
    check('EditionA byte preservation',baseline.upper()=='FF289D7D83BF56F977D5D3F85F7CDF13125841075D5E8A59AF03FA845D39ED6B','Preservation only; checkpointPDF/receipt still missing')
    cold=json.loads((ROOT/'evidence/cold-run-receipt.json').read_text(encoding='utf-8'))
    check('Fresh no-pip environment',cold['status']=='PASS' and all(x['match'] for x in cold['output_hash_matches'].values()),'Assistant clean run; not student recorded ownership')
    stale=[]
    for path in ROOT.rglob('*'):
        if not path.is_file() or any(x in path.parts for x in ['.build','__pycache__']):continue
        if path.suffix in ['.md','.json','.csv','.txt','.html']:
            if re.search('Sales'+'force|\\b'+'CRM'+'\\b',path.read_text(encoding='utf-8'),re.I):stale.append(path.name)
    check('NVIDIA-only active target',not stale,stale)
    pdf=json.loads((ROOT/'outputs/pdf-qa.json').read_text(encoding='utf-8'))
    check('PDF page/bounds checks',len(pdf['files'])==3 and pdf['total_pages']==sum(f['pages'] for f in pdf['files']) and all(not p['out_of_page_blocks'] for f in pdf['files'] for p in f['page_checks']),f"All{pdf['total_pages']}pages rendered; visual review completed separately")
    for name,stem in [('Decision-Memo','decision-memo'),('Research-Evolution','research-evolution'),('Validation-and-AI-Use','validation-and-ai-use')]:
        actual=hashlib.sha256((ROOT/f'{name}.pdf').read_bytes()).hexdigest(); record=next(x for x in pdf['files'] if x['file']==f'{name}.pdf')
        check(name+' copy/hash',actual==record['sha256'] and (ROOT/f'{name}.pdf').read_bytes()==(ROOT/f'docs/{stem}.pdf').read_bytes(),'Root/docs same PDF; current render receipt hash')
    check('Memo length',next(x for x in pdf['files'] if x['file']=='Decision-Memo.pdf')['pages']<=2,'Maximum2pages')
    quality=json.loads((ROOT/'outputs/document-quality-audit.json').read_text(encoding='utf-8'))
    check('All PDF quality checks',quality['status']=='PASS' and quality['unique_pdf_pages']==13 and all(hashlib.sha256((ROOT/x['file']).read_bytes()).hexdigest()==x['sha256'] for x in quality['files']),'13unique pages: bounds, significant overlaps, glyphs, source text, local evidence targets, result values and identical PDF copies; visual inspection recorded separately')
    visible=(ROOT/'outputs/visible-output.md').read_text(encoding='utf-8')
    check('Visible decision / all statements',all(t in visible for t in ['WATCH / DEFER','five-year income','five-year balance','five-year cash','Market-implied','218.36']), 'Material result viewable without execution')
    for i in [1,2,3]:
        text=(ROOT/f'docs/transcript-video-{i}.txt').read_text(encoding='utf-8')
        review=json.loads((ROOT/'evidence/video-review.json').read_text(encoding='utf-8'))
        item=next(x for x in review['videos'] if x['video']==i)
        check(f'Transcript{i} imported integrity','NOT RECORDED' not in text and len(text.split())>200 and hashlib.sha256((ROOT/item['transcript']).read_bytes()).hexdigest()==item['transcript_sha256'],'Student-requested editorial value corrections logged; audio alignment remains unverified')
    metadata=json.loads((ROOT/'evidence/video-metadata.json').read_text(encoding='utf-8'))
    check('Video links and duration limits',len(metadata['videos'])==3 and all(x.get('player_status')=='OK' and 0<x['duration_seconds']<=(180 if x['video']==1 else 300) for x in metadata['videos']),'Anonymous metadata only; correct video numbering; full playback not reviewed')
    steps=(ROOT/'Student next steps.md').read_text(encoding='utf-8')
    check('Three recording routes and scripts',all(s.lower() in steps.lower() for s in ['Video1 -','Video2 -','Video3 -','Script:','maximum3:00','maximum5:00','Recording-Charts.pdf','--without-pip']), 'Fixed chart routes, timing limits, distinct scripts and actual fresh-environment run instructions; human-history status checked separately')
    recording=json.loads((ROOT/'outputs/recording-script-audit.json').read_text(encoding='utf-8'))
    check('Recording evidence numbers and scripts',recording['status']=='PASS' and recording['financial_result_sha256']==hashlib.sha256((ROOT/'outputs/results.json').read_bytes()).hexdigest() and recording['script_word_counts']['1']<=355,'Question-to-claim-to-readable-evidence mapping; figures independently matched to saved results')
    check('Recording guide single version',steps==(ROOT/'docs/recording-guide.md').read_text(encoding='utf-8'),'Student next steps and audited guide agree; generator preserves current route')
    charts=json.loads((ROOT/'outputs/recording-charts-audit.json').read_text(encoding='utf-8'))
    check('Fixed recording charts',charts['status']=='PASS' and charts['pages']==3 and charts['pdf_sha256']==hashlib.sha256((ROOT/'Recording-Charts.pdf').read_bytes()).hexdigest() and all(hashlib.sha256((ROOT/p['file']).read_bytes()).hexdigest()==p['sha256'] for p in charts['pngs']) and charts['financial_results_unchanged_sha256']==recording['financial_result_sha256'],'Three16:9charts; PDF/1920x1080PNGhashes; saved finance results unchanged')
    with (ROOT/'submission-manifest.csv').open(encoding='utf-8',newline='') as f: rows=list(csv.DictReader(f))
    check('Uniform manifest',len(rows)==12 and sum(x['required']=='yes' for x in rows)==11 and all(x['location_or_url'] for x in rows if x['required']=='yes'),'11required+optionaldeployment; supplied video/transcript links populated; timestamp and speech review pending')
    freeze=json.loads((ROOT/'file-integrity.json').read_text(encoding='utf-8'))
    mismatches=[n for n,h in freeze['files'].items() if not (ROOT/n).is_file() or hashlib.sha256((ROOT/n).read_bytes()).hexdigest()!=h]
    check('Frozen file integrity',not mismatches,mismatches or f"{len(freeze['files'])} stable SHA256matches; exclusions explicit")
    ui=subprocess.run(['node',str(ROOT/'test_dashboard.cjs')],capture_output=True,text=True)
    check('Interactive output controls',ui.returncode==0,ui.stdout.strip()+ui.stderr.strip())
    result={'technical_audit':'PASS' if all(x['status']=='PASS' for x in checks) else 'FAIL',
            'submission_complete':False,'rubric_score':'Not certified; original baseline receipt/PDF and audio/timestamp verification remain unresolved; student growth prediction/run and attributed peer review supplied, with authorship/policy basis documented',
            'checks':checks}
    (ROOT/'outputs/submission-audit.json').write_text(json.dumps(result,indent=2)+'\n',encoding='utf-8',newline='\n')
    print(json.dumps(result,indent=2))
    if result['technical_audit']!='PASS':raise SystemExit(1)


if __name__=='__main__':main()
