"""Freeze stable technical files and assemble truthful required-item manifest."""
import csv
import datetime as dt
import hashlib
import json
from pathlib import Path

ROOT=Path(__file__).resolve().parent
TAG='project-1-nvidia-pdf-polish-2026-10-19'
BASE=f'https://github.com/JP161632/FIN43900-Fall2026/blob/{TAG}/projects/project-1/'
EXCLUDE={'file-integrity.json','submission-manifest.csv','evidence/publication-audit.json','outputs/submission-audit.json','outputs/run-receipt.json'}


def stable_files():
    return sorted(p for p in ROOT.rglob('*') if p.is_file() and
                  not any(x in p.relative_to(ROOT).parts for x in ('.build','__pycache__','.venv')) and
                  p.relative_to(ROOT).as_posix() not in EXCLUDE)


def main():
    status_path=ROOT/'evidence/submission-status.json'
    status=json.loads(status_path.read_text(encoding='utf-8'))
    metadata=json.loads((ROOT/'evidence/video-metadata.json').read_text(encoding='utf-8'))
    review=json.loads((ROOT/'evidence/video-review.json').read_text(encoding='utf-8'))
    status['videos']='Three supplied YouTube links; titles/durations/player metadata checked; audiovisual performance not reviewed'
    status['transcripts']='Three transcripts editorially corrected to model values at student request; audio alignment and observed timestamp indices unverified'
    status['overall_submission']='INCOMPLETE - final evidence and transcript/audio reconciliation required'
    status_path.write_text(json.dumps(status,indent=2)+'\n',encoding='utf-8',newline='\n')
    hashes={p.relative_to(ROOT).as_posix():hashlib.sha256(p.read_bytes()).hexdigest() for p in stable_files()}
    receipt={'scope':'Technical evidence and supplied video/transcript snapshot; final evidence review INCOMPLETE','tag':TAG,
             'created_utc':dt.datetime.now(dt.timezone.utc).isoformat(),'algorithm':'sha256',
             'excluded':sorted(EXCLUDE),'exclusion_reason':'Avoid self-reference and volatile execution/publication/access receipts; Git commit still covers tracked files',
             'files':hashes}
    (ROOT/'file-integrity.json').write_text(json.dumps(receipt,indent=2)+'\n',encoding='utf-8',newline='\n')
    publication=ROOT/'evidence/publication-audit.json'
    access='PENDING anonymous public check'
    if publication.exists():
        q=json.loads(publication.read_text(encoding='utf-8'))
        if q['status']=='PASS' and q.get('frozen_file_sha256')==hashes: access=f"yes; anonymous public check {q['checked_utc']}; core hashes verified at {q['commit'][:12]}"
    specs=[('Research-Evolution.pdf','Research-Evolution.pdf','NVIDIA EditionA/B and research evolution'),
           ('Repository',None,'NVIDIA Project1 offline application'),
           ('Visible executed output','outputs/visible-output.md','Executed NVIDIA valuation and statements'),
           ('Decision memo or deck','Decision-Memo.pdf','NVIDIA conditional committee decision'),
           ('Validation-and-AI-Use.pdf','Validation-and-AI-Use.pdf','NVIDIA tests and disclosed AI/human-evidence status')]
    rows=[]
    for title,path,description in specs:
        url=BASE+path if path else f'https://github.com/JP161632/FIN43900-Fall2026/tree/{TAG}/projects/project-1'
        rows.append([title,'yes',url,description,'Valuation2026-09-10; prepared2026-10-19','',access,
                     'sha256:'+hashes[path] if path else TAG,'Evidence snapshot; unresolved requirements documented in evidence/submission-status.json'])
    for i in range(1,4):
        video=next(x for x in metadata['videos'] if x['video']==i)
        transcript=next(x for x in review['videos'] if x['video']==i)
        seconds=video.get('duration_seconds')
        duration=f'{seconds//60}:{seconds%60:02d}' if seconds is not None else 'PENDING'
        video_access=f"Anonymous metadata {video.get('player_status','UNVERIFIED')}; {video['checked_utc']}; full playback not reviewed"
        rows.append([f'Video {i}','yes',video['url'],video.get('title',f'NVIDIA Video {i}'),duration,
                     transcript['observed_timestamp_index'],video_access,'YouTube video ID: '+video['url'].split('=')[-1],
                     'Transcript model values editorially corrected at student request; audio alignment unverified; see docs/video-review.md'])
        path=transcript['transcript']
        rows.append([f'Transcript Video {i}','yes',BASE+path,f'Editorially corrected transcript {i} - model values reconciled',duration,
                     transcript['observed_timestamp_index'],access,'sha256:'+hashes[path],
                     'Student-requested value corrections logged in evidence/video-review.json; audio and actual timing unverified'])
    rows.append(['Optional deployed output','no','','Not required','','','','','Local offline interactive output supplied'])
    with (ROOT/'submission-manifest.csv').open('w',encoding='utf-8',newline='') as f:
        writer=csv.writer(f,lineterminator='\n');writer.writerow(['item','required','location_or_url','title','duration_or_as_of','timestamp_index','access_checked','frozen_or_commit_id','notes']);writer.writerows(rows)
    print(f'Frozen {len(hashes)} stable files; 3video URLs and transcripts included; final evidence review incomplete')


if __name__=='__main__': main()
