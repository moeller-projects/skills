#!/usr/bin/env python3
"""Create an Azure DevOps work item comment through a guarded dry-run-first POST.

Purpose: Create work item comments.
Inputs: CLI flags and ADO_ORGANIZATION/ADO_PROJECT environment variables.
Outputs: Dry-run JSON or guarded API response.
Side effects: POSTs to Azure DevOps only with --confirm.
Requires Python 3.9+, standard library only. Run with: python scripts/create-work-item-comment.py
"""
import json, os, re, sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parent))
import _ado_lib as lib

def main():
    organization=os.environ.get('ADO_ORGANIZATION',''); project=os.environ.get('ADO_PROJECT',''); wid=''; text=''; confirm=False
    args=sys.argv[1:]; i=0; names={'--organization':'o','--project':'p','--work-item-id':'w','--text':'t'}
    while i<len(args):
        a=args[i]
        if a=='--confirm': confirm=True; i+=1; continue
        if a in names:
            val=args[i+1] if i+1<len(args) else ''; i+=2
            if names[a]=='o': organization=val
            elif names[a]=='p': project=val
            elif names[a]=='w': wid=val
            else: text=val
            continue
        print(f'Unknown argument: {a}',file=sys.stderr); return 1
    missing=[n for n,v in [('organization',organization),('project',project),('work_item_id',wid),('text',text)] if not v]
    if missing: lib.emit_blocker('MISSING_INPUT',missing,'Provide the missing values before creating a work item comment.')
    if not re.fullmatch(r'[0-9]+',wid): lib.emit_error('PARSE_FAILED','parse','--work-item-id must be an integer.','Provide a numeric work item id.')
    if confirm: lib.require_pat()
    url=f'https://dev.azure.com/{organization}/{project}/_apis/wit/workItems/{wid}/comments?api-version=7.1-preview.4'; body={'text':text}
    if not confirm:
        print(json.dumps({'action_type':'create-work-item-comment','dry_run':True,'requires_confirmation':True,'risk':'high','method':'POST','url':url,'content_type':'application/json','required_scopes':['Work Items: Read & write','OAuth: vso.work_write'],'body':body})); return 0
    out=lib.http_write_json('POST','application/json',url,json.dumps(body).encode(),label='create work item comment'); print(out); return 0
if __name__=='__main__': sys.exit(main())
