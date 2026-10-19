"""Anonymous GitHub access and byte verification; no credentials, private data or mutation."""
import argparse
import concurrent.futures
import datetime as dt
import hashlib
import json
from pathlib import Path
import subprocess
import urllib.request

ROOT=Path(__file__).resolve().parent
REPO=ROOT.parents[1]
OWNER='JP161632/FIN43900-Fall2026'


def get(url):
    req=urllib.request.Request(url,headers={'User-Agent':'Course-Project1-NVIDIA-Public-Integrity-Check','Accept':'application/vnd.github+json'})
    with urllib.request.urlopen(req,timeout=45) as response:return response.read()


def main():
    p=argparse.ArgumentParser();p.add_argument('--ref',default='main');p.add_argument('--verify-only',action='store_true');args=p.parse_args()
    c=json.loads(get(f'https://api.github.com/repos/{OWNER}/commits/{args.ref}'));commit=c['sha']
    tree=json.loads(get(f'https://api.github.com/repos/{OWNER}/git/trees/{commit}?recursive=1'))
    remote={x['path']:x['sha'] for x in tree['tree'] if x['type']=='blob' and x['path'].startswith('projects/project-1/')}
    local=subprocess.run(['git','ls-tree','-r','HEAD','--','projects/project-1'],cwd=REPO,capture_output=True,text=True,check=True).stdout
    wrong=[];count=0
    for line in local.splitlines():
        meta,path=line.split('\t');sha=meta.split()[2];count+=1
        if remote.get(path)!=sha:wrong.append(path)
    assert not wrong,wrong
    frozen=json.loads((ROOT/'file-integrity.json').read_text(encoding='utf-8'))
    def verify(pair):
        name,h=pair
        url=f'https://raw.githubusercontent.com/{OWNER}/{commit}/projects/project-1/'+urllib.parse.quote(name)
        actual=hashlib.sha256(get(url)).hexdigest()
        assert actual==h,(name,h,actual)
        return name
    with concurrent.futures.ThreadPoolExecutor(max_workers=6) as pool:
        checked=list(pool.map(verify,frozen['files'].items()))
    result={'status':'PASS','checked_utc':dt.datetime.now(dt.timezone.utc).isoformat(),'access':'Anonymous public GitHub API and raw file requests; no credentials',
            'ref':args.ref,'commit':commit,'git_blob_files_verified':count,'sha256_frozen_files_verified':len(checked),
            'frozen_files':checked,'scope':'Published technical package, supplied transcript bytes and video-link records; audiovisual, timestamp and human-evidence review remains incomplete'}
    if not args.verify_only:(ROOT/'evidence/publication-audit.json').write_text(json.dumps(result,indent=2)+'\n',encoding='utf-8',newline='\n')
    print(json.dumps({k:z for k,z in result.items() if k!='frozen_files'},indent=2))


if __name__=='__main__':main()
