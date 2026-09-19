#!/usr/bin/env python3
"""Reproduce and repair explicit minicalc C2 MDs; no Docker or remote execution."""
import argparse
import difflib
import hashlib
import json
from pathlib import Path
import re
import shutil
import subprocess
import sys
import tempfile
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT))
import validate as contract


def write_json(p,data):
    p.parent.mkdir(parents=True,exist_ok=True)
    p.write_text(json.dumps(data,ensure_ascii=False,indent=2)+'\n')


def finding_id(repository,configuration,kind,target,dependency):
    # Protocol proposal v1: exact JSON array, UTF-8, no spaces, full SHA-256.
    values=[repository,configuration,kind,target,dependency]
    payload=json.dumps(values,ensure_ascii=False,separators=(',',':')).encode('utf-8')
    return 'finding-'+hashlib.sha256(payload).hexdigest()


def source_check():
    meta=json.loads((ROOT/'fixtures/minicalc/project.json').read_text())
    source=ROOT/'fixtures/minicalc/source'
    actual={str(p.relative_to(source)):hashlib.sha256(p.read_bytes()).hexdigest() for p in source.rglob('*') if p.is_file()}
    if actual!=meta['source_files_sha256']:
        raise ValueError('Pinned source changed: restore snapshot or explicitly review and repin its provenance')
    return meta


def run(args,cwd,expected=0):
    result=subprocess.run(args,cwd=cwd,capture_output=True,text=True,timeout=60)
    if result.returncode!=expected:
        raise ValueError(f'{args}: exit {result.returncode}, expected {expected}\n{result.stdout}{result.stderr}')
    return result.stdout+result.stderr


def scan(project,repo,configuration,evidence_uri):
    lines=(project/'Makefile').read_text().splitlines()
    findings=[];actual_edges=[];declared_edges=[];evidence=[]
    for name in ['main','parser','token','util']:
        target=name+'.o'
        matches=[(i+1,line) for i,line in enumerate(lines) if line.startswith(target+':')]
        if len(matches)!=1:raise ValueError('Only one explicit rule per minicalc object is supported')
        line_no,rule=matches[0]
        tokens=rule.split(':',1)[1].split()
        if not all(re.fullmatch(r'(src|include)/[A-Za-z0-9_.-]+',x) for x in tokens):
            raise ValueError('Macros, pattern rules and nonliteral prerequisites are unsupported')
        declared=set(tokens)
        text=run(['gcc','-std=c11','-Wall','-Wextra','-Iinclude','-g','-MM',f'src/{name}.c'],project)
        lhs,sep,rhs=text.replace('\\\n',' ').partition(':')
        if sep!=':' or lhs.strip()!=target:raise ValueError('Unexpected compiler dependency output')
        deps=rhs.split();external=[d for d in deps if Path(d).is_absolute()]
        actual=set(deps)-set(external)
        if not all(re.fullmatch(r'(src|include)/[A-Za-z0-9_.-]+',x) for x in actual):
            raise ValueError('Unsupported compiler path format')
        evidence.append({'target':target,'command':['gcc','-std=c11','-Wall','-Wextra','-Iinclude','-g','-MM',f'src/{name}.c'],
                         'compiler_output':text,'excluded_external_paths':external,'makefile_rule':rule,'line':line_no})
        actual_edges.extend([target,d] for d in sorted(actual))
        declared_edges.extend([target,d] for d in sorted(declared))
        for kind,paths in [('MISSING',actual-declared),('REDUNDANT',declared-actual)]:
            for dep in sorted(paths):
                findings.append({'finding_id':finding_id(repo['url'],configuration,kind,target,dep),'type':kind,
                    'target':target,'dependency':dep,'commit':repo['commit'],'detector':'COMPILER_MM_LOCAL',
                    'location':{'file':'Makefile','line':line_no},'evidence':{'actual_dependency':dep in actual,
                    'declared_dependency':dep in declared,'description':'本机 gcc -MM 的项目内传递依赖与 minicalc 显式规则比较，非 A 组 Checker 执行结果。','uri':evidence_uri}})
    return findings,actual_edges,declared_edges,evidence


def repair_text(before,findings):
    if not findings or any(f['type']!='MISSING' for f in findings):raise ValueError('Nonempty MD-only input required')
    additions={}
    for f in findings:
        if f['location']['file']!='Makefile' or f['target'] not in ['main.o','parser.o','token.o','util.o']:
            raise ValueError('Out-of-scope repair')
        if not re.fullmatch(r'include/[A-Za-z0-9_.-]+\.h',f['dependency']):raise ValueError('Unsupported dependency')
        additions.setdefault(f['target'],set()).add(f['dependency'])
    lines=before.splitlines(True)
    for target,deps in additions.items():
        matches=[i for i,line in enumerate(lines) if line.startswith(target+':')]
        if len(matches)!=1:raise ValueError('Ambiguous rule')
        i=matches[0];existing=lines[i].split(':',1)[1].split()
        lines[i]=lines[i].rstrip('\n')+''.join(' '+d for d in sorted(deps-set(existing)))+'\n'
    return ''.join(lines)


def verify_program(project):
    logs=[]
    for expr,expected in [('1+2*3','7'),('10-4/2','8'),('3*(4+5)','27'),('--version','minicalc 1.0.0')]:
        got=run([str(project/'minicalc'),expr],project).strip()
        if got!=expected:raise ValueError(f'{expr}: output {got!r}, expected {expected!r}')
        logs.append(f'PASS {expr!r}: {got}')
    return '\n'.join(logs)+'\n'


def generate(out):
    meta=source_check();repo={'url':meta['repository_url'],'commit':meta['commits']['C2']}
    configuration=meta['configuration_id'];records=[]
    uri='artifact://minicalc/c2/'
    def save(name,kind,content,job):
        p=out/'artifacts/minicalc/c2'/name;p.parent.mkdir(parents=True,exist_ok=True)
        if isinstance(content,str):p.write_text(content)
        else:write_json(p,content)
        records.append({'artifact_id':'minicalc-c2-'+name,'type':kind,'uri':uri+name,
                        'media_type':'application/json' if name.endswith('.json') else 'text/plain',
                        'producer_job_id':job,'repository':repo,'configuration_id':configuration,
                        'sha256':hashlib.sha256(p.read_bytes()).hexdigest()})
        return uri+name
    before_job='job-minicalc-c2-local-check';repair_job='job-minicalc-c2-local-repair';recheck_job='job-minicalc-c2-local-recheck'
    with tempfile.TemporaryDirectory(prefix='minicalc-b-') as tmp:
        project=Path(tmp)/'source';shutil.copytree(ROOT/'fixtures/minicalc/source',project)
        clean_log=run(['make','clean'],project)+run(['make','-j2'],project)
        test_log=verify_program(project)
        findings,actual,declared,evidence=scan(project,repo,configuration,uri+'evidence.json')
        counts={kind:sum(f['type']==kind for f in findings) for kind in ['MISSING','REDUNDANT']}
        if counts!=meta['expected']['C2']:raise ValueError(f'Unexpected C2 findings: {counts}')
        md=[f for f in findings if f['type']=='MISSING']
        report={'schema_version':'1.0','repository':repo,'configuration_id':configuration,'producer_job_id':before_job,'findings':findings}
        save('evidence.json','EVIDENCE',{'method':'gcc -MM; explicit rules','compiler_version':run(['gcc','--version'],project),'records':evidence},before_job)
        graph_base={'schema_version':'1.0','commit':repo['commit'],'configuration_id':configuration}
        for name,edges,kind in [('actual.json',actual,'ACTUAL_GRAPH'),('declared.json',declared,'DECLARED_GRAPH')]:
            save(name,kind,{**graph_base,'edges':edges},before_job)
        save('error-report.json','ERROR_REPORT',report,before_job)
        save('md-report.json','ERROR_REPORT',{**report,'findings':md},before_job)
        save('build-before.log','BUILD_LOG',clean_log.replace(str(project),'<source>'),before_job)
        save('test-before.log','BUILD_LOG',test_log,before_job)
        for f in md:run(['make','-q','-W',f['dependency'],f['target']],project,expected=0)
        before=(project/'Makefile').read_text();after=repair_text(before,md)
        patch=''.join(difflib.unified_diff(before.splitlines(True),after.splitlines(True),fromfile='a/Makefile',tofile='b/Makefile'))
        patch_path=Path(tmp)/'fix.patch';patch_path.write_text(patch)
        run(['git','apply','--check',str(patch_path)],project)
        run(['git','apply',str(patch_path)],project)
        build_after=run(['make','clean'],project)+run(['make','-j2'],project)
        test_after=verify_program(project)
        for f in md:run(['make','-q','-W',f['dependency'],f['target']],project,expected=1)
        remaining,_,_,after_evidence=scan(project,repo,configuration,uri+'recheck-evidence.json')
        if remaining:raise ValueError('Repair left dependency findings')
        patch_hash=hashlib.sha256(patch.encode()).hexdigest()
        save('fix.patch','PATCH',patch,repair_job)
        save('build-after.log','BUILD_LOG',build_after.replace(str(project),'<source>'),repair_job)
        save('test-after.log','BUILD_LOG',test_after,repair_job)
        save('recheck-report.json','ERROR_REPORT',{**report,'producer_job_id':recheck_job,'findings':remaining},recheck_job)
        save('recheck-evidence.json','EVIDENCE',{'base_commit':repo['commit'],'patch_sha256':patch_hash,'method':'LOCAL gcc -MM recheck; not A-group Checker','records':after_evidence},recheck_job)
    build={'command':'make -j2','clean_command':'make clean && make -j2','verify_command':'python3 /opt/b-group/verify_minicalc.py .','working_directory':'/workspace/minicalc'}
    env={'image':'minicalc-devops:c2-NOT-BUILT','configuration_id':configuration,'project_root':'/workspace/minicalc'}
    base={'schema_version':'1.0','trace_id':'trace-minicalc-c2','execution':{'timeout_seconds':600}}
    full={**base,'job_type':'FULL_CHECK','idempotency_key':'minicalc-c2-full','input':{'repository':repo,'environment':env,'build':build}}
    draft={**base,'job_type':'DRAFT','idempotency_key':'minicalc-c2-draft','input':{'repository':repo,'build':build,'max_iterations':5}}
    repair={**base,'job_type':'REPAIR','idempotency_key':'minicalc-c2-repair','input':{**full['input'],'md_report_uri':uri+'md-report.json','makefiles':['Makefile'],'finding_types':['MISSING'],'recheck':{'job_type':'FULL_CHECK','required':True}}}
    result=lambda log:{'passed':True,'exit_code':0,'log_uri':uri+log}
    response={k:v for k,v in full.items() if k!='idempotency_key'}
    response.update(job_id=before_job,status='SUCCEEDED',error=None,output={'actual_graph_uri':uri+'actual.json','declared_graph_uri':uri+'declared.json','error_report_uri':uri+'error-report.json','evidence_uri':uri+'evidence.json'})
    repaired={k:v for k,v in repair.items() if k!='idempotency_key'}
    repaired.update(job_id=repair_job,status='SUCCEEDED',error=None,output={'patch_uri':uri+'fix.patch','declaration_style':'EXPLICIT','accepted':True,'rejection_reason':None,'build_result':result('build-after.log'),'test_result':result('test-after.log'),'recheck_result':{'passed':True,'error_report_uri':uri+'recheck-report.json','remaining_missing_count':0}})
    # These are contract mappings of local evidence, never runnable Docker job claims.
    examples={'draft-request':draft,'full-request':full,'full-response-local':response,'repair-request':repair,'repair-response-local':repaired,'md-report':{**report,'findings':md}}
    for name,data in examples.items():write_json(out/'contracts/minicalc'/(name+'.json'),data)
    write_json(out/'artifacts/index.json',records)
    write_json(out/'contracts/minicalc/manifest.json',{'examples':list(examples),'scope':'LOCAL evidence mapped to contracts; environment.image NOT BUILT; API not executed; requires A-group acceptance'})
    summary={'source_commit_from_zip':repo['commit'],'remote_commit_verified':meta.get('remote_commit_verified',False),'before':counts,'after':{'MISSING':0,'REDUNDANT':0},'patch_sha256':patch_hash,'four_cases_asserted_before_and_after':True,'four_missing_edges_incremental_rebuild_checked':True,'docker':'NOT_RUN','a_group_checker':'NOT_RUN','mode':'LOCAL_EXPLICIT_REPAIR_DEMO'}
    write_json(out/'summary.json',summary)
    validate_suite(out)
    return summary


def validate_suite(root):
    old=contract.ROOT;contract.ROOT=root
    try:
        manifest=json.loads((root/'contracts/minicalc/manifest.json').read_text())
        for name in manifest['examples']:
            contract.validate(json.loads((root/'contracts/minicalc'/(name+'.json')).read_text()))
        for rec in json.loads((root/'artifacts/index.json').read_text()):
            contract.check(rec,contract.SCHEMA['$defs']['artifact']);contract.read_artifact(rec['uri'])
        for name in ['actual.json','declared.json']:
            g=json.loads((root/'artifacts/minicalc/c2'/name).read_text())
            if set(g)!={'schema_version','commit','configuration_id','edges'} or g['schema_version']!='1.0':raise ValueError('graph shape mismatch')
            report=json.loads((root/'contracts/minicalc/md-report.json').read_text())
            if g['commit']!=report['repository']['commit'] or g['configuration_id']!=report['configuration_id']:raise ValueError('graph/report identity mismatch')
            if len(g['edges'])!=len({tuple(e) for e in g['edges']}):raise ValueError('duplicate graph edges')
            if not all(len(e)==2 and all(isinstance(p,str) and p and not p.startswith('/') and '..' not in Path(p).parts for p in e) for e in g['edges']):raise ValueError('invalid edge')
    finally:contract.ROOT=old


if __name__=='__main__':
    parser=argparse.ArgumentParser(description=__doc__);parser.add_argument('--validate',action='store_true');args=parser.parse_args()
    try:
        if args.validate:source_check();validate_suite(ROOT);print('PASS minicalc pinned source, 6 examples and artifacts')
        else:print(json.dumps(generate(ROOT/'work/minicalc-run'),ensure_ascii=False,indent=2))
    except (ValueError,OSError,subprocess.SubprocessError) as e:sys.exit('FAIL: '+str(e))
