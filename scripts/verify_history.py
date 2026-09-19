#!/usr/bin/env python3
"""Replay verified upstream c0/c1/c2 locally, without network or Docker."""
import hashlib
import json
from pathlib import Path
import shutil
import sys
import tempfile
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
from scripts import minicalc as m


def generate(out):
    meta=m.source_check();bundle=m.ROOT/meta['history_bundle']
    if hashlib.sha256(bundle.read_bytes()).hexdigest()!=meta['history_bundle_sha256']:raise ValueError('Git bundle hash mismatch')
    index=[];summary={};previous=None;previous_label=None;examples=[]
    with tempfile.TemporaryDirectory(prefix='minicalc-history-') as tmp:
        source=Path(tmp)/'source';m.run(['git','clone','--quiet',str(bundle),str(source)],m.ROOT)
        for label,sha in meta['commits'].items():
            m.run(['git','checkout','--quiet','--detach',label.lower()],source)
            if m.run(['git','rev-parse','HEAD'],source).strip()!=sha:raise ValueError('Tag SHA mismatch')
            log=m.run(['make','clean'],source)+m.run(['make','-j2'],source)
            test=m.verify_program(source)
            repo={'url':meta['repository_url'],'commit':sha};config=meta['configuration_id']
            prefix=f'artifact://minicalc-history/{label.lower()}/';job=f'job-minicalc-{label.lower()}-history-local'
            findings,actual,declared,evidence=m.scan(source,repo,config,prefix+'evidence.json')
            counts={kind:sum(f['type']==kind for f in findings) for kind in ['MISSING','REDUNDANT']}
            if counts!=meta['expected'][label]:raise ValueError(f'{label} unexpected counts: {counts}')
            report={'schema_version':'1.0','repository':repo,'configuration_id':config,'producer_job_id':job,'findings':findings}
            content={'actual.json':('ACTUAL_GRAPH',{'schema_version':'1.0','commit':sha,'configuration_id':config,'edges':actual}),
                     'declared.json':('DECLARED_GRAPH',{'schema_version':'1.0','commit':sha,'configuration_id':config,'edges':declared}),
                     'error-report.json':('ERROR_REPORT',report),
                     'md-report.json':('ERROR_REPORT',{**report,'findings':[f for f in findings if f['type']=='MISSING']}),
                     'evidence.json':('EVIDENCE',{'compiler_version':m.run(['gcc','--version'],source),'method':'local compiler scan; full rescan at each commit','records':evidence}),
                     'build.log':('BUILD_LOG',log.replace(str(source),'<source>')),'test.log':('BUILD_LOG',test)}
            for name,(kind,value) in content.items():
                path=out/'artifacts/minicalc-history'/label.lower()/name;path.parent.mkdir(parents=True,exist_ok=True)
                if isinstance(value,str):path.write_text(value)
                else:m.write_json(path,value)
                index.append({'artifact_id':f'minicalc-history-{label}-{name}','type':kind,'uri':prefix+name,'media_type':'application/json' if name.endswith('.json') else 'text/plain','producer_job_id':job,'repository':repo,'configuration_id':config,'sha256':hashlib.sha256(path.read_bytes()).hexdigest()})
            current={f['finding_id'] for f in findings}
            delta={'added_finding_ids':sorted(current-previous),'resolved_finding_ids':sorted(previous-current)} if previous is not None else None
            summary[label]={'commit':sha,'counts':counts,'build_and_assertions_passed':True,'delta':delta}
            template=json.loads((m.ROOT/'contracts/minicalc/full-request.json').read_text())
            template['input']['repository']=repo
            template['idempotency_key']='minicalc-history-'+label
            output={'actual_graph_uri':prefix+'actual.json','declared_graph_uri':prefix+'declared.json','error_report_uri':prefix+'error-report.json','evidence_uri':prefix+'evidence.json'}
            if previous_label:
                template['job_type']='INCREMENTAL_CHECK'
                template['input']['base_commit']=meta['commits'][previous_label]
                template['input']['baseline']={'actual_graph_uri':f'artifact://minicalc-history/{previous_label.lower()}/actual.json','declared_graph_uri':f'artifact://minicalc-history/{previous_label.lower()}/declared.json','commit':meta['commits'][previous_label],'configuration_id':config}
                output.update(delta)
            response={k:v for k,v in template.items() if k!='idempotency_key'}
            response.update(job_id=job,status='SUCCEEDED',output=output,error=None)
            for suffix,data in [('request',template),('response-local',response)]:
                name=f'{label.lower()}-{suffix}.json';m.write_json(out/'contracts/minicalc-history'/name,data);examples.append(name)
            previous=current;previous_label=label
    if len(summary['C1']['delta']['added_finding_ids'])!=1 or summary['C1']['delta']['resolved_finding_ids']:raise ValueError('C0-C1 delta mismatch')
    if summary['C2']['delta']['added_finding_ids'] or len(summary['C2']['delta']['resolved_finding_ids'])!=1:raise ValueError('C1-C2 delta mismatch')
    m.write_json(out/'contracts/minicalc-history/manifest.json',{'examples':examples,'mode':'LOCAL_FULL_RESCAN_COMPARISON; NOT_BUILT image; not actual EChecker execution'});m.write_json(out/'artifacts/index.json',index);m.write_json(out/'summary.json',summary)
    old=m.contract.ROOT;m.contract.ROOT=out
    try:
        for name in examples:m.contract.validate(json.loads((out/'contracts/minicalc-history'/name).read_text()))
        for record in index:
            m.contract.check(record,m.contract.SCHEMA['$defs']['artifact']);path,_=m.contract.read_artifact(record['uri'])
            if record['type']=='ERROR_REPORT':m.contract.validate(json.loads(path.read_text()))
    finally:m.contract.ROOT=old
    return summary


if __name__=='__main__':
    print(json.dumps(generate(m.ROOT/'work/minicalc-history'),ensure_ascii=False,indent=2))
