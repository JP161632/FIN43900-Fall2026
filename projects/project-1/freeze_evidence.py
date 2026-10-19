"""Freeze stable technical files and assemble truthful required-item manifest."""
import csv
import datetime as dt
import hashlib
import json
from pathlib import Path

ROOT=Path(__file__).resolve().parent
TAG='project-1-nvidia-2026-10-19'
BASE=f'https://github.com/JP161632/FIN43900-Fall2026/blob/{TAG}/projects/project-1/'
EXCLUDE={'file-integrity.json','submission-manifest.csv','evidence/publication-audit.json','outputs/submission-audit.json','outputs/run-receipt.json'}


def stable_files():
    return sorted(p for p in ROOT.rglob('*') if p.is_file() and
                  not any(x in p.relative_to(ROOT).parts for x in ('.build','__pycache__','.venv')) and
                  p.relative_to(ROOT).as_posix() not in EXCLUDE)


def main():
    hashes={p.relative_to(ROOT).as_posix():hashlib.sha256(p.read_bytes()).hexdigest() for p in stable_files()}
    receipt={'scope':'Technical evidence snapshot; human/video submission INCOMPLETE','tag':TAG,
             'created_utc':dt.datetime.now(dt.timezone.utc).isoformat(),'algorithm':'sha256',
             'excluded':sorted(EXCLUDE),'exclusion_reason':'Avoid self-reference and volatile execution/publication/access receipts; Git commit still covers tracked files',
             'files':hashes}
    (ROOT/'file-integrity.json').write_text(json.dumps(receipt,indent=2)+'\n',encoding='utf-8',newline='\n')
    status={
        'technical_package':'EXECUTED / FROZEN; publication checked separately',
        'overall_submission':'INCOMPLETE - authentic student evidence required',
        'edition_a_markdown':'preserved unchanged; original submitted PDF/receipt missing',
        'human_locked_record':'INCOMPLETE; AI-authored directional test is separate',
        'partner_review':'prior Lab12 reported discussion, authenticity/attribution unconfirmed',
        'videos':'NOT RECORDED', 'transcripts':'status markers only',
        'brightspace_final_receipt':'NOT PROVIDED; GitHub is not submission'}
    # Status is intentionally generated before re-freezing so its stable bytes are included on the next call.
    (ROOT/'evidence/submission-status.json').write_text(json.dumps(status,indent=2)+'\n',encoding='utf-8',newline='\n')
    hashes['evidence/submission-status.json']=hashlib.sha256((ROOT/'evidence/submission-status.json').read_bytes()).hexdigest()
    receipt['files']=dict(sorted(hashes.items()))
    (ROOT/'file-integrity.json').write_text(json.dumps(receipt,indent=2)+'\n',encoding='utf-8',newline='\n')
    publication=ROOT/'evidence/publication-audit.json'
    access='PENDING anonymous public check'
    if publication.exists():
        q=json.loads(publication.read_text(encoding='utf-8'))
        if q['status']=='PASS': access=f"yes; anonymous public check {q['checked_utc']}; core hashes verified at {q['commit'][:12]}"
    specs=[('Research-Evolution.pdf','Research-Evolution.pdf','NVIDIA EditionA/B and research evolution'),
           ('Repository',None,'NVIDIA Project1 offline application'),
           ('Visible executed output','outputs/visible-output.md','Executed NVIDIA valuation and statements'),
           ('Decision memo or deck','Decision-Memo.pdf','NVIDIA conditional committee decision'),
           ('Validation-and-AI-Use.pdf','Validation-and-AI-Use.pdf','NVIDIA tests and disclosed AI/human-evidence status')]
    rows=[]
    for title,path,description in specs:
        url=BASE+path if path else f'https://github.com/JP161632/FIN43900-Fall2026/tree/{TAG}/projects/project-1'
        rows.append([title,'yes',url,description,'Valuation2026-09-10; prepared2026-10-19','',access,
                     'sha256:'+hashes[path] if path else TAG,'Technical freeze; not a completed video/human-evidence submission'])
    for i in range(1,4):
        rows.append([f'Video {i}','yes','',f'NVIDIA Video{i} - NOT RECORDED','','','','','Max3:00 for Video1; max5:00 for Video2/3. Planned scripts are not observed timestamps.'])
        rows.append([f'Transcript Video {i}','yes','',f'Corrected actual transcript{i} - NOT AVAILABLE','','','','',f'docs/transcript-video-{i}.txt is a status marker, not a completed transcript'])
    rows.append(['Optional deployed output','no','','Not required','','','','','Local offline interactive output supplied'])
    with (ROOT/'submission-manifest.csv').open('w',encoding='utf-8',newline='') as f:
        writer=csv.writer(f,lineterminator='\n');writer.writerow(['item','required','location_or_url','title','duration_or_as_of','timestamp_index','access_checked','frozen_or_commit_id','notes']);writer.writerows(rows)
    print(f'Frozen {len(hashes)} stable files; manifest11required+1optional; student evidence remains incomplete')


if __name__=='__main__': main()
