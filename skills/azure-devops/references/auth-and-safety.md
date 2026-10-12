# Auth and Safety

- Read `AZURE_DEVOPS_PAT` from the environment. Never echo it, place it in generated artifacts, or persist it in examples.
- Read flows use GET requests only.
- Write flows are limited to dedicated Python scripts for work items, work item comments, pull requests, and PR comments.
- Every write script defaults to dry-run and requires `--confirm` before network mutation.
- Run the scripts with Python 3.9+; they use only the standard library.
- Do not include raw thread payloads unless the caller explicitly requests them.
- If required input or authentication is missing, return structured blocker output rather than attempting a degraded network call.
- PAT scopes should be least-privilege: Work Items read/write for work item creation, Code read/write for pull request and PR comment creation.
