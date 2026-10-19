"""Run a fresh copy in a new Python venv, without installing any model packages."""
import datetime as dt
import hashlib
import json
from pathlib import Path
import shutil
import subprocess
import sys
import time
import uuid

ROOT=Path(__file__).resolve().parent


def main():
    start=time.perf_counter()
    target=(ROOT/'.build'/('cold-'+uuid.uuid4().hex[:10])).resolve()
    assert target.is_relative_to((ROOT/'.build').resolve())
    target.mkdir(parents=True)
    source=target/'project'
    shutil.copytree(ROOT,source,ignore=shutil.ignore_patterns('.build','__pycache__','.venv'))
    envdir=target/'venv'
    setup=subprocess.run([sys.executable,'-m','venv','--without-pip',str(envdir)],capture_output=True,text=True)
    python=envdir/('Scripts/python.exe' if sys.platform=='win32' else 'bin/python')
    result={'timestamp_utc':dt.datetime.now(dt.timezone.utc).isoformat(),'operator':'Codex assistant, not a recorded student run',
            'environment':'new venv with no pip or third-party model packages; copied project; no network/credentials',
            'setup_exit':setup.returncode,'setup_stderr':setup.stderr,
            'command':'<fresh-venv-python> <copied-project>/run.py --all --output <fresh-output>',
            'first_failure':None,'resolution':'not needed if no failure','output_hash_matches':{}}
    if setup.returncode:
        result['first_failure']='Fresh virtual environment setup failed'
        result['resolution']='Unresolved; do not claim clean run'
    else:
        version=subprocess.run([str(python),'-c','import sys; print(sys.version)'],capture_output=True,text=True)
        run=subprocess.run([str(python),str(source/'run.py'),'--all','--output',str(target/'fresh-output')],cwd=target,capture_output=True,text=True)
        result.update(python=version.stdout.strip(),exit_code=run.returncode,stdout=run.stdout,stderr=run.stderr)
        if run.returncode:
            result['first_failure']='End-to-end model execution failed'
            result['resolution']='Unresolved; preserve stderr and diagnose before claiming reproduction'
        else:
            for name in ('results.json','validation-results.json','visible-output.md','dashboard.html'):
                a=hashlib.sha256((ROOT/'outputs'/name).read_bytes()).hexdigest()
                b=hashlib.sha256((target/'fresh-output'/name).read_bytes()).hexdigest()
                result['output_hash_matches'][name]={'reference':a,'fresh':b,'match':a==b}
            if not all(x['match'] for x in result['output_hash_matches'].values()):
                result['first_failure']='Deterministic output hash mismatch'
                result['resolution']='Unresolved; do not claim reproduction'
    result['elapsed_seconds']=round(time.perf_counter()-start,3)
    result['status']='PASS' if result['first_failure'] is None else 'FAIL'
    (ROOT/'evidence'/'cold-run-receipt.json').write_text(json.dumps(result,indent=2)+'\n',encoding='utf-8',newline='\n')
    log=f'''# Assistant clean-environment cold run

Run UTC: {result['timestamp_utc']}. Operator: Codex assistant. Status: **{result['status']}**.

Isolation: a new temporary project copy and a new Python virtual environment created with `python -m venv --without-pip`. No model package installation, credentials or data fetches. The current workspace's site-packages are not inherited.

Exact logical command: `{result['command']}`. Temporary absolute paths are deliberately omitted from the public record.

First failure: {result['first_failure'] or 'None observed'}. Resolution: {result['resolution']}. Measured setup and execution time: {result['elapsed_seconds']} seconds. Runtime and byte-for-byte output hashes are in `cold-run-receipt.json`.

Console output:

```
{result.get('stdout','')}{result.get('stderr','')}
```

All four deterministic financial/output files must match the frozen reference. The volatile run receipt is expected to have a new timestamp and is not compared. The course known answers, source checks, accounting/terminal/bridge checks, highest-risk SBC failure and decision-altering downside run inside this clean execution.

**No recording was made of a student performing this run.** This is useful technical reproduction evidence; it does not substitute for the student's Video2/code ownership or human AI-off locked changed-input exercise. Follow the README in a genuinely clean environment and record the required defense.
'''
    (ROOT/'evidence'/'cold-run-log.md').write_text(log,encoding='utf-8',newline='\n')
    print(json.dumps({'status':result['status'],'elapsed_seconds':result['elapsed_seconds'],
                      'all_four_outputs_match':all(x['match'] for x in result['output_hash_matches'].values())},indent=2))
    if result['status']!='PASS': raise SystemExit(1)


if __name__=='__main__': main()
