#!/usr/bin/env python3
"""Create an Azure DevOps pull request through a guarded dry-run-first POST.

Purpose: Create pull requests.
Inputs: CLI flags and ADO environment variables.
Outputs: Dry-run JSON or guarded API response.
Side effects: POSTs to Azure DevOps only with --confirm.
Requires Python 3.9+, standard library only. Run with: python scripts/create-pull-request.py
"""
import json, os, sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parent))
import _ado_lib as lib

def main():
    organization=os.environ.get('ADO_ORGANIZATION',''); project=os.environ.get('ADO_PROJECT',''); repo=os.environ.get('ADO_REPOSITORY_ID',''); source=''; target='main'; title=''; description=''; reviewers='[]'; confirm=False
    args=sys.argv[1:]; i=0
    while i<len(args):
        a=args[i]
        if a=='--confirm': confirm=True; i+=1; continue
        mapping={'--organization':'o','--project':'p','--repository-id':'r','--source-branch':'s','--target-branch':'t','--title':'i','--description':'d','--reviewers-json':'v'}
        if a in mapping:
            val=args[i+1] if i+1<len(args) else ''; i+=2; k=mapping[a]
            if k=='o': organization=val
            elif k=='p': project=val
            elif k=='r': repo=val
            elif k=='s': source=val
            elif k=='t': target=val
            elif k=='i': title=val
            elif k=='d': description=val
            else: reviewers=val
            continue
        print(f'Unknown argument: {a}',file=sys.stderr); return 1
    missing=[n for n,v in [('organization',organization),('project',project),('repository_id',repo),('source_branch',source),('target_branch',target),('title',title)] if not v]
    if missing: lib.emit_blocker('MISSING_INPUT',missing,'Provide the missing values before creating a pull request.')
    try: rv=json.loads(reviewers)
    except Exception: lib.emit_error('PARSE_FAILED','parse','--reviewers-json must be a JSON array.','Pass reviewers as \'[{"id":"..."}]\' or omit --reviewers-json.')
    if not isinstance(rv,list): lib.emit_error('PARSE_FAILED','parse','--reviewers-json must be a JSON array.','Pass reviewers as \'[{"id":"..."}]\' or omit --reviewers-json.')
    if confirm: lib.require_pat()
    def ref(x): return x if x.startswith('refs/heads/') else 'refs/heads/'+x
    url=f'https://dev.azure.com/{organization}/{project}/_apis/git/repositories/{repo}/pullrequests?api-version=7.1'
    body={'sourceRefName':ref(source),'targetRefName':ref(target),'title':title,'description':description}
    if rv: body['reviewers']=rv
    if not confirm:
        print(json.dumps({'action_type':'create-pull-request','dry_run':True,'requires_confirmation':True,'risk':'high','method':'POST','url':url,'content_type':'application/json','required_scopes':['Code: Read & write','OAuth: vso.code_write'],'body':body})); return 0
    out=lib.http_write_json('POST','application/json',url,json.dumps(body).encode(),label='create pull request'); print(out); return 0
if __name__=='__main__': sys.exit(main())
