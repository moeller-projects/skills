#!/usr/bin/env python3
"""Create an Azure DevOps work item through a guarded dry-run-first POST.

Purpose: Create work items.
Inputs: CLI flags and ADO_ORGANIZATION/ADO_PROJECT environment variables.
Outputs: Dry-run JSON or guarded API response.
Side effects: POSTs to Azure DevOps only with --confirm.
Requires Python 3.9+, standard library only. Run with: python scripts/create-work-item.py
"""
import json, os, sys
from pathlib import Path
from urllib.parse import quote
sys.path.insert(0, str(Path(__file__).resolve().parent))
import _ado_lib as lib

def main():
    organization=os.environ.get('ADO_ORGANIZATION',''); project=os.environ.get('ADO_PROJECT',''); typ=''; title=''; description=''; fields='{}'; confirm=False
    args=sys.argv[1:]; i=0
    names={'--organization':'organization','--project':'project','--type':'typ','--title':'title','--description':'description','--fields-json':'fields'}
    vals=locals()
    while i<len(args):
        a=args[i]
        if a=='--confirm': confirm=True; i+=1; continue
        if a in names:
            if i+1>=len(args): val=''; i+=1
            else: val=args[i+1]; i+=2
            if names[a]=='organization': organization=val
            elif names[a]=='project': project=val
            elif names[a]=='typ': typ=val
            elif names[a]=='title': title=val
            elif names[a]=='description': description=val
            else: fields=val
            continue
        print(f'Unknown argument: {a}', file=sys.stderr); return 1
    missing=[n for n,v in [('organization',organization),('project',project),('type',typ),('title',title)] if not v]
    if missing: lib.emit_blocker('MISSING_INPUT',missing,'Provide the missing values before creating a work item.')
    try: extra=json.loads(fields)
    except Exception: lib.emit_error('PARSE_FAILED','parse','--fields-json must be a JSON object.','Pass fields as \'{"System.Tags":"tag"}\' or omit --fields-json.')
    if not isinstance(extra,dict): lib.emit_error('PARSE_FAILED','parse','--fields-json must be a JSON object.','Pass fields as \'{"System.Tags":"tag"}\' or omit --fields-json.')
    if confirm: lib.require_pat()
    url=f'https://dev.azure.com/{organization}/{project}/_apis/wit/workitems/${quote(typ,safe="")}?api-version=7.1'
    body=[{'op':'add','path':'/fields/System.Title','value':title}]
    if description:
        field='Microsoft.VSTS.TCM.ReproSteps' if typ=='Bug' else 'System.Description'
        body.append({'op':'add','path':'/fields/'+field,'value':description})
    body += [{'op':'add','path':'/fields/'+k,'value':v} for k,v in extra.items()]
    if not confirm:
        print(json.dumps({'action_type':'create-work-item','dry_run':True,'requires_confirmation':True,'risk':'high','method':'POST','url':url,'content_type':'application/json-patch+json','required_scopes':['Work Items: Read & write','OAuth: vso.work_write'],'body':body})); return 0
    out=lib.http_write_json('POST','application/json-patch+json',url,json.dumps(body).encode(),label='create work item'); print(out); return 0
if __name__=='__main__': sys.exit(main())
