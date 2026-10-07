# Rule: Secrets in Source

> Impact: critical

## Description

Credentials, keys, and tokens MUST NEVER be hardcoded in source or committed to the repository. Secrets MUST be supplied at runtime from environment variables or a secret manager.

## Apply When

- Reviewing any code, config file, test fixture, example file, or comment that contains or references a credential — API keys, database connection strings, private keys, OAuth client secrets, signing keys, passwords, or bearer tokens.

## Checks

- No literal high-entropy strings or recognizable key formats in tracked files (such as `AKIA…`, `-----BEGIN … PRIVATE KEY-----`, `ghp_…`, `xox…`, JWT-shaped strings).
- Connection strings or URLs with embedded credentials are flagged.
- Secrets are read from environment variables or a secret manager at runtime — NEVER assigned as literals in code.
- Test fixtures and example files use obvious placeholders (`REPLACE_ME`, `example-key`), never real-looking values.
- Secret-bearing files (`.env`, key files, cert files) are gitignored; any committed `*.example` sample contains no real values.
- A secret found already committed MUST be treated as compromised — the finding MUST say *rotate the credential*, not merely *remove it*.

## Anti-Pattern

`const API_KEY = "sk-live-9f3c…"` committed to the repo. A config file containing `postgres://user:realPassw0rd@host:5432/db`.
