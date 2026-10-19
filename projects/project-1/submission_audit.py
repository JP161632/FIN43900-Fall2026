"""Audit bundle completeness honestly; never infer human ownership from file existence."""
import argparse
import csv
import datetime as dt
import hashlib
import json
from pathlib import Path

ROOT=Path(__file__).resolve().parent
TAG='project-1-2026-10-19'
REPO='https://github.com/JP161632/FIN43900-Fall2026'
BASE=f'{REPO}/blob/{TAG}/projects/project-1'
COLUMNS=['item','required','location_or_url','title','duration_or_as_of','timestamp_index','access_checked','frozen_or_commit_id','notes']
VOLATILE={'file-integrity.json','outputs/run-receipt.json','outputs/submission-audit.json'}


def sha(path): return hashlib.sha256(path.read_bytes()).hexdigest()


def write_manifest():
    rows=[]
    items=[('Research-Evolution.pdf','Research-Evolution.pdf','Salesforce Edition B and baseline status','Baseline PDF/receipt missing; company switch disclosed'),
           ('Repository',None,'Project 1 Salesforce corporate finance application','Final tag freezes this package; no GitHub push is a Brightspace submission'),
           ('Visible executed output','outputs/visible-output.md','Executed Salesforce valuation and all statements','Visible without running; optional local HTML viewer also included'),
           ('Decision memo or deck','Decision-Memo.pdf','Salesforce investment committee decision','Two pages; historical valuation and conditional action'),
           ('Validation-and-AI-Use.pdf','Validation-and-AI-Use.pdf','Validation and named AI use','Missing human lock and recorded ownership evidence remain disclosed')]
    for item,path,title,notes in items:
        rows.append(dict(item=item,required='yes',location_or_url=(f'{REPO}/tree/{TAG}/projects/project-1' if path is None else BASE+'/'+path),
                         title=title,duration_or_as_of='2026-08-27 valuation; prepared2026-10-19',timestamp_index='',
                         access_checked='',frozen_or_commit_id=TAG if path is None else 'sha256:'+sha(ROOT/path),
                         notes=notes+'; local file verified; anonymous instructional access check pending'))
    for i,title in [(1,'Research evolution and AI-output check'),(2,'Codebase and validation'),(3,'Committee defense and live demonstration')]:
        rows.append(dict(item=f'Video {i}',required='yes',location_or_url='',title=title,duration_or_as_of='',timestamp_index='',
                         access_checked='',frozen_or_commit_id='',notes='NOT RECORDED; maximum '+('3:00' if i==1 else '5:00')+'; planned indices are not observed timestamps'))
        rows.append(dict(item=f'Transcript Video {i}',required='yes',location_or_url='',title=f'Corrected actual transcript video{i}',
                         duration_or_as_of='',timestamp_index='',access_checked='',frozen_or_commit_id='',
                         notes=f'docs/transcript-video-{i}.txt is an explicit NOT RECORDED status, not a completed transcript'))
    rows.append(dict(item='Optional deployed output',required='no',location_or_url='',title='',duration_or_as_of='',
                     timestamp_index='',access_checked='',frozen_or_commit_id='',notes='Not required; locally runnable engine and offline visible output supplied'))
    with (ROOT/'submission-manifest.csv').open('w',encoding='utf-8',newline='') as f:
        writer=csv.DictWriter(f,fieldnames=COLUMNS,lineterminator='\n'); writer.writeheader(); writer.writerows(rows)


def freeze():
    entries={}
    for path in sorted(ROOT.rglob('*')):
        if not path.is_file(): continue
        relative=path.relative_to(ROOT)
        if any(p in ('.build','__pycache__','.venv') for p in relative.parts): continue
        name=relative.as_posix()
        if name in VOLATILE: continue
        entries[name]=sha(path)
    payload={'version_tag':TAG,'frozen_utc':dt.datetime.now(dt.timezone.utc).isoformat(),
             'scope':'all project files except this self-referential inventory, volatile run/audit receipt and ignored build/cache files',
             'files':entries}
    (ROOT/'file-integrity.json').write_text(json.dumps(payload,indent=2)+'\n',encoding='utf-8',newline='\n')


def audit():
    problems=[]; checks=[]
    required=['README.md','requirements.txt','model.py','run.py','tests.py','data/inputs.json','data/sources.json',
              'outputs/results.json','outputs/visible-output.md','outputs/validation-results.json','outputs/dashboard.html',
              'Research-Evolution.pdf','Decision-Memo.pdf','Validation-and-AI-Use.pdf','docs/research-evolution.pdf',
              'docs/decision-memo.pdf','docs/validation-and-ai-use.md','docs/validation-and-ai-use.pdf',
              'docs/rubric-audit.md','evidence/cold-run-log.md','evidence/assumption-challenges.md',
              'evidence/peer-policy.md','evidence/data-lineage.md','evidence/project1-credit-check.md','submission-manifest.csv']
    for name in required:
        if not (ROOT/name).is_file(): problems.append('Missing artifact '+name)
    if not problems: checks.append('Required analysis/artifact paths exist')
    for stem,rootname in [('research-evolution','Research-Evolution'),('decision-memo','Decision-Memo'),('validation-and-ai-use','Validation-and-AI-Use')]:
        if (ROOT/f'{rootname}.pdf').exists() and (ROOT/'docs'/f'{stem}.pdf').exists():
            if sha(ROOT/f'{rootname}.pdf')!=sha(ROOT/'docs'/f'{stem}.pdf'): problems.append('PDF copies differ '+stem)
    checks.append('Root and repository PDF copies checked')
    if (ROOT/'outputs/validation-results.json').exists():
        v=json.loads((ROOT/'outputs/validation-results.json').read_text(encoding='utf-8'))
        if v['failed']: problems.append('Finance checks failed')
        else: checks.append(f"{v['passed']} finance tests passed")
    if (ROOT/'evidence/cold-run-receipt.json').exists():
        cold=json.loads((ROOT/'evidence/cold-run-receipt.json').read_text(encoding='utf-8'))
        if cold['status']!='PASS' or not all(x['match'] for x in cold['output_hash_matches'].values()): problems.append('Clean run mismatch')
        else: checks.append('Fresh environment and all four deterministic hashes match')
    if (ROOT/'submission-manifest.csv').exists():
        with (ROOT/'submission-manifest.csv').open(encoding='utf-8',newline='') as f:
            reader=csv.DictReader(f); rows=list(reader)
            if set(reader.fieldnames or [])!=set(COLUMNS) or len(rows)!=12: problems.append('Manifest must have exact shared columns and12 rows')
            else: checks.append('Shared12-row manifest schema matches course template')
        for row in rows:
            if row['required']=='yes':
                fields=['location_or_url','access_checked','frozen_or_commit_id']
                if row['item'].startswith('Video '): fields+=['duration_or_as_of','timestamp_index']
                missing=[field for field in fields if not row.get(field,'').strip()]
                if missing: problems.append(row['item']+': missing '+', '.join(missing))
    for i in range(1,4):
        path=ROOT/'docs'/f'transcript-video-{i}.txt'
        if not path.exists() or 'NOT RECORDED' in path.read_text(encoding='utf-8'):
            problems.append(f'Video{i}: actual corrected transcript unavailable')
    status=json.loads((ROOT/'evidence/submission-status.json').read_text(encoding='utf-8'))
    for key,value in status.items():
        if key not in ('status_as_of','note') and value in ('MISSING','NOT PROVIDED','PENDING','NOT SUBMITTED'):
            problems.append('Human/external evidence '+key+': '+value)
    if (ROOT/'file-integrity.json').exists():
        inventory=json.loads((ROOT/'file-integrity.json').read_text(encoding='utf-8'))
        mismatches=[name for name,expected in inventory['files'].items() if not (ROOT/name).exists() or sha(ROOT/name)!=expected]
        if mismatches: problems.append('Frozen hashes differ: '+', '.join(mismatches))
        else: checks.append(f"All {len(inventory['files'])} frozen artifact hashes match")
    else: problems.append('No frozen integrity inventory')
    output={'status':'READY FOR HUMAN REVIEW' if not problems else 'NOT READY FOR FINAL SUBMISSION',
            'mechanical_checks':checks,'open_items':problems,
            'limitation':'File existence and passing arithmetic cannot certify authorship, access, financial judgment or points.'}
    (ROOT/'outputs/submission-audit.json').write_text(json.dumps(output,indent=2)+'\n',encoding='utf-8',newline='\n')
    print(json.dumps(output,indent=2))
    return output


if __name__=='__main__':
    p=argparse.ArgumentParser(description=__doc__); p.add_argument('--freeze',action='store_true'); p.add_argument('--write-manifest',action='store_true')
    a=p.parse_args()
    if a.write_manifest: write_manifest()
    if a.freeze: freeze()
    audit()
