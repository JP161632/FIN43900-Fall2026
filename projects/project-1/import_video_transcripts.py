"""Import supplied text; preserve uncertain speech and document limited editing."""
import argparse
import hashlib
import json
from pathlib import Path
import re

ROOT=Path(__file__).resolve().parent


def main():
    parser=argparse.ArgumentParser()
    parser.add_argument('--source-dir',type=Path,required=True)
    args=parser.parse_args()
    metadata=json.loads((ROOT/'evidence/video-metadata.json').read_text(encoding='utf-8'))
    prior_path=ROOT/'evidence/video-review.json'
    prior=json.loads(prior_path.read_text(encoding='utf-8')) if prior_path.exists() else {}
    if prior.get('student_confirmed_corrections'):
        raise SystemExit('Reviewed corrections exist; preserve them rather than reimporting source text.')
    records=[]
    for video in metadata['videos']:
        number=video['video']; name=f'transcript-video-{number}.txt'
        raw=(args.source_dir/name).read_bytes()
        text=raw.decode('utf-8-sig').strip()
        text=re.sub(r'(?i)Hi everyone, my name is [^.]+\.', 'Hi everyone. [Speaker introduction omitted for privacy.]',text,count=1)
        text=re.sub(r'(?i)Hi everyone, [^.]+ again\.', 'Hi everyone. [Speaker introduction omitted for privacy.]',text,count=1)
        # Paragraphs improve readability without asserting new words or timings.
        sentences=re.split(r'(?<=[.!?])\s+(?=[A-Z])',text)
        paragraphs=[' '.join(sentences[i:i+5]) for i in range(0,len(sentences),5)]
        body='\n\n'.join(paragraphs)+'\n'
        target=ROOT/'docs'/name
        target.write_text(body,encoding='utf-8',newline='\n')
        records.append({'video':number,'url':video['url'],'duration_seconds':video.get('duration_seconds'),
                        'transcript':f'docs/{name}','provided_source_sha256':hashlib.sha256(raw).hexdigest(),
                        'transcript_sha256':hashlib.sha256(target.read_bytes()).hexdigest(),
                        'editing':'Paragraph breaks and speaker-name omission only; financial wording preserved pending audio confirmation.',
                        'observed_timestamp_index':'PENDING: supplied transcript has no timestamps; caption endpoint returned empty response',
                        'review_status':'TEXT REVIEWED; material caption/speech discrepancies require student audio confirmation'})
    review={'scope':'Text/model comparison and anonymous public metadata; audio and full visual performance not reviewed',
            'student_confirmed_corrections':False,'videos':records,
            'issues':[
                {'video':1,'passage':'base reference is about $190','model_value':'$118.58 (about $119)','status':'UNRESOLVED'},
                {'video':1,'passage':'15.8% WACC; annual weighted donated shares; SCFF; casual range','model_value':'Prior Lab 5 WACC 15.88%; annual weighted diluted shares; FCFF; causal range','status':'UNRESOLVED'},
                {'video':1,'passage':'unrealized investment gains of nonoperating cash generation','model_value':'Unrealized investment gains are not operating cash generation','status':'UNRESOLVED'},
                {'video':2,'passage':'from $1808 to $180.38','model_value':'$118.58 to $108.38 when WACC rises 1 percentage point','status':'UNRESOLVED'},
                {'video':3,'passage':'casual range is about 56 to $200','model_value':'causal range $55.93-$212.08 (about $56-$212)','status':'UNRESOLVED'},
                {'video':3,'passage':'Adding one percentage point to WCC lowers value to about $118','model_value':'WACC increase lowers value to $108.38','status':'UNRESOLVED'},
                {'video':3,'passage':'low case ... value nearly $65','model_value':'Low-case value $55.93 (about $56)','status':'UNRESOLVED'},
                {'video':3,'passage':'Collection days about 95','model_value':'Collection days above 95 is the monitoring threshold','status':'UNRESOLVED'}]}
    (ROOT/'evidence/video-review.json').write_text(json.dumps(review,indent=2)+'\n',encoding='utf-8',newline='\n')
    print('Imported three transcripts; names omitted; uncertain finance wording preserved and flagged.')


if __name__=='__main__':main()
