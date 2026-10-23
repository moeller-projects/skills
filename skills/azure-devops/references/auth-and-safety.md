# Auth and Safety

- Git remote URLs can embed credentials. Pipe a remote URL directly to `parse-git-remote.py`; never place it in command arguments, logs, or output.
- Read `AZURE_DEVOPS_PAT` from the environment. Never echo it, place it in generated artifacts, or persist it in examples. Redact the literal current PAT and supported bearer/plain PAT forms recursively from every emitted field and write response.
- Read flows use GET requests only; GET retries are bounded.
- Write flows are limited to dedicated Python scripts for work items, work item comments, pull requests, and PR comments. A transport/server failure on a write is never replayed because its outcome is unknown; check Azure DevOps before retrying.
- Every write script defaults to dry-run and requires `--confirm` before network mutation.
- Run the scripts with Python 3.9+; they use only the standard library.
- Do not include raw thread payloads unless the caller explicitly requests them; even then, redact recursively.
- If required input or authentication is missing, return structured blocker output rather than attempting a degraded network call.
- Partial combined fetches preserve the successful source and emit a partial handoff with missing source fields and warnings; input/auth blockers remain fatal.
- PAT scopes should be least-privilege: Work Items read/write for work item creation, Code read/write for pull request and PR comment creation.
