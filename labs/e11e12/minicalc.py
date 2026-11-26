"""Explicit adapter for the unmodified upstream Minicalc C0/C1 history."""
import hashlib
import json
import shutil
import time
from pathlib import Path
from lab import run, save, patch

TARGETS = {name+'.o':'src/'+name+'.c' for name in ('main','parser','token','util')}

def scan(project, old=None):
    # GNU Make expands := variables and conditionals; use the compiler's actual
    # local header dependencies, rather than the two-file classroom oracle.
    database=run(['make','-pn'],project)
    declared={}
    import re
    for target in TARGETS:
        lines=re.findall(r'^'+re.escape(target)+r':\s*(.*)$',database,re.M)
        if not lines:raise ValueError('UNSUPPORTED_RULE '+target)
        declared[target]=sorted(set(lines[0].split()))
    sources=sorted(list((project/'src').glob('*.c'))+list((project/'include').glob('*.h')))
    key={'files':{str(p.relative_to(project)):hashlib.sha256(p.read_bytes()).hexdigest() for p in sources},
         'makefile':hashlib.sha256((project/'Makefile').read_bytes()).hexdigest(),
         'compiler':run(['gcc','--version'],project).splitlines()[0]}
    actual={};reused=[];refreshed=[]
    for target,source in TARGETS.items():
        if old and old['key']==key:
            actual[target]=old['actual'][target];reused.append(target)
        else:
            text=run(['gcc','-std=c11','-Wall','-Wextra','-Iinclude','-g','-MM','-MT',target,source],project)
            actual[target]=sorted(set(text.replace('\\\n',' ').split(':',1)[1].split()))
            refreshed.append(target)
    findings=[]
    for target in TARGETS:
        for kind,edges in [('MISSING',set(actual[target])-set(declared[target])),('REDUNDANT',set(declared[target])-set(actual[target]))]:
            findings.extend(dict(type=kind,target=target,dependency=p) for p in sorted(edges))
    current={(f['type'],f['target'],f['dependency']) for f in findings}
    previous={(f['type'],f['target'],f['dependency']) for f in old['findings']} if old else set()
    return dict(schema_version='e8e10-1',profile='MINICALC_C0_C1_EXPLICIT',commit=run(['git','rev-parse','HEAD'],project).strip(),
                actual=actual,declared=declared,key=key,findings=findings,reused=reused,refreshed=refreshed,
                added=[list(x) for x in sorted(current-previous)],resolved=[list(x) for x in sorted(previous-current)])

def validate(project, patchfile, evidence, fail_test=False):
    evidence.mkdir(parents=True)
    before=(project/'Makefile').read_bytes()
    sandbox=evidence/'sandbox'
    shutil.copytree(project,sandbox,ignore=shutil.ignore_patterns('.git','*.o','minicalc'))
    checks={};error=None
    try:
        run(['git','init','-b','main'],sandbox)
        run(['git','config','user.name','ValidationSandbox'],sandbox)
        run(['git','config','user.email','fixture@localhost'],sandbox)
        from lab import commit
        commit(sandbox,'original Minicalc validation input')
        run(['git','apply','--check',str(patchfile.resolve())],sandbox);checks['patch_applies']=True
        run(['git','apply',str(patchfile.resolve())],sandbox)
        (evidence/'build.log').write_text(run(['make','clean'],sandbox)+run(['make'],sandbox));checks['build']=True
        outputs={expr:run(['./minicalc',expr],sandbox).strip() for expr in ('1+2*3','10-4/2','3*(4+5)')}
        save(evidence/'program-outputs.json',outputs)
        checks['test']=outputs=={'1+2*3':'7','10-4/2':'8','3*(4+5)':'27'} and not fail_test
        old_mtime=(sandbox/'main.o').stat().st_mtime_ns
        time.sleep(1.05)
        header=sandbox/'include/config.h';header.write_bytes(header.read_bytes()+b'\n/* B03 header-change probe */\n')
        (evidence/'incremental.log').write_text(run(['make'],sandbox))
        checks['header_change']=(sandbox/'main.o').stat().st_mtime_ns>old_mtime
        current=scan(sandbox);save(evidence/'recheck.json',current)
        checks['no_missing']=not any(f['type']=='MISSING' for f in current['findings'])
    except (ValueError,OSError) as exc:error=str(exc)
    accepted=bool(checks) and all(checks.values()) and error is None
    if accepted:(project/'Makefile').write_bytes((sandbox/'Makefile').read_bytes())
    unchanged=before==(project/'Makefile').read_bytes()
    result=dict(accepted=accepted,checks=checks,error=error,source_unchanged=unchanged,rollback=not accepted and unchanged)
    save(evidence/'validation.json',result);return result
