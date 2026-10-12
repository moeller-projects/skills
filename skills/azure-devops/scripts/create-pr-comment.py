#!/usr/bin/env python3
"""Create an Azure DevOps PR comment thread or reply through a guarded POST.

Purpose: Create PR comment threads and replies.
Inputs: CLI flags and ADO environment variables.
Outputs: Dry-run JSON or guarded API response.
Side effects: POSTs to Azure DevOps only with --confirm.
Requires Python 3.9+, standard library only. Run with: python scripts/create-pr-comment.py
"""
import json, os, re, sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parent))
import _ado_lib as lib

def err(msg,recovery): lib.emit_error('PARSE_FAILED','parse',msg,recovery)
def main():
    mode='thread'; pr_url=''; org=os.environ.get('ADO_ORGANIZATION',''); project=os.environ.get('ADO_PROJECT',''); repo=os.environ.get('ADO_REPOSITORY_ID',''); pr=os.environ.get('ADO_PULL_REQUEST_ID',''); thread=''; content=''; path=''; side='right'; line=''; end=''; confirm=False
    args=sys.argv[1:]; i=0; mapping={'--mode':'mode','--pull-request-url':'pr_url','--organization':'org','--project':'project','--repository-id':'repo','--pull-request-id':'pr','--thread-id':'thread','--content':'content','--file-path':'path','--side':'side','--line':'line','--end-line':'end'}
    while i<len(args):
        a=args[i]
        if a=='--confirm': confirm=True; i+=1; continue
        if a in mapping:
            v=args[i+1] if i+1<len(args) else ''; i+=2; k=mapping[a]
            if k=='mode': mode=v
            elif k=='pr_url': pr_url=v
            elif k=='org': org=v
            elif k=='project': project=v
            elif k=='repo': repo=v
            elif k=='pr': pr=v
            elif k=='thread': thread=v
            elif k=='content': content=v
            elif k=='path': path=v
            elif k=='side': side=v
            elif k=='line': line=v
            else: end=v
            continue
        print(f'Unknown argument: {a}',file=sys.stderr); return 1
    if pr_url:
        parsed=lib.parse_pull_request_url(pr_url)
        if parsed is None: err('Invalid pull request URL.','Provide a URL such as '+lib.PR_URL_HINT+'.')
        if not org: org=parsed['organization']
        if not project: project=parsed['project']
        if not repo: repo=parsed['repository_id']
        if not pr: pr=parsed['pull_request_id']
    if mode not in ('thread','reply'): err("--mode must be 'thread' or 'reply'.",'Use --mode thread for a new thread or --mode reply for an existing thread.')
    if side not in ('left','right'): err("--side must be 'left' or 'right'.",'Omit --side for right-side comments or pass left/right.')
    if mode=='reply' and thread and not re.fullmatch(r'[0-9]+',thread): err('--thread-id must be an integer.','Provide a numeric thread id for --mode reply.')
    if path:
        if re.match(r'^[\\/]{2}',path): err(r'--file-path must be repo-root-relative and start with a single \'/\'; UNC-style paths (\\server\share or //server/share) are not allowed.','Provide a repository path such as /src/order.ts.')
        if re.match(r'^[A-Za-z]:[\\/]',path): err("--file-path must be repo-root-relative and start with '/'.",'Provide a repository path such as /src/order.ts.')
        collapsed=re.sub(r'/+','/',path.replace('\\','/'))
        segments=[s for s in collapsed.lstrip('/').split('/') if s]
        if any(s in ('.','..') for s in segments): err('--file-path must stay within the repository root.','Remove path traversal segments and provide a repo-root-relative path.')
        path=lib.normalize_repo_root_path(collapsed)
        if not path or path=='/': err('--file-path must include a file path under the repository root.','Provide a repository path such as /src/order.ts.')
    if end and mode!='thread': err('--end-line is only valid with --mode thread.','Remove --end-line or switch to --mode thread.')
    if end and not path: err('--end-line requires --file-path.','Supply --file-path to create an inline thread, or remove --end-line.')
    missing=[n for n,v in [('organization',org),('project',project),('repository_id',repo),('pull_request_id',pr),('content',content)] if not v]
    if mode=='reply' and not thread: missing.append('thread_id')
    if missing: lib.emit_blocker('MISSING_INPUT',missing,'Provide the missing values before creating the PR comment.')
    if confirm: lib.require_pat()
    base=f'https://dev.azure.com/{org}/{project}/_apis/git/repositories/{repo}/pullRequests/{pr}/threads'
    if mode=='reply': url=base+'/'+thread+'/comments?api-version=7.1'; action='reply-pr-comment'; body={'content':content,'commentType':1}
    else:
        url=base+'?api-version=7.1'; action='create-pr-comment-thread'
        if path:
            if not line: lib.emit_blocker('MISSING_INPUT',['line'],'Provide --line for inline PR comments or omit --file-path for a general thread.')
            if not re.fullmatch(r'[0-9]+',line): err('--line must be an integer.','Provide a numeric line number for inline comments.')
            if end:
                if not re.fullmatch(r'[0-9]+',end): err('--end-line must be an integer.','Provide a numeric end line number, or omit --end-line to anchor to a single line.')
                if int(end)<int(line): err('--end-line must be greater than or equal to --line.','Set --end-line to a line number >= --line.')
            else: end=line
            ctx={'filePath':path, ('rightFileStart' if side=='right' else 'leftFileStart'):{'line':int(line),'offset':1}, ('rightFileEnd' if side=='right' else 'leftFileEnd'):{'line':int(end),'offset':1}}
            body={'comments':[{'parentCommentId':0,'content':content,'commentType':1}],'status':'active','threadContext':ctx}
        else: body={'comments':[{'parentCommentId':0,'content':content,'commentType':1}],'status':'active'}
    if not confirm:
        print(json.dumps({'action_type':action,'dry_run':True,'requires_confirmation':True,'risk':'high','method':'POST','url':url,'content_type':'application/json','required_scopes':['Code: Read & write','OAuth: vso.code_write'],'body':body})); return 0
    out=lib.http_write_json('POST','application/json',url,json.dumps(body).encode(),label=action); print(out); return 0
if __name__=='__main__': sys.exit(main())
