# Happy-Path Example — Debugging

## Scenario

A local test started failing after a parser refactor with `KeyError: 'token'`.

## Expected Output

```text
status: fixed
root_cause:
- finding: the refactor renamed the parser output key to `access_token`, but the request builder still reads `token`
- evidence: the bottom stack frame points to request_builder.py; a minimal fixture reproduces the KeyError, and commit bisect identifies the rename commit
repro_steps:
- run `pytest tests/test_request_builder.py -q` with fixture `valid_auth_response.json`
- observe `KeyError: 'token'` in the request builder
fix:
- update the request builder to consume the parser's `access_token` field and preserve the public request shape
verification:
- the original test command passes; an adjacent malformed-response test still returns the expected validation error
regression_check:
- added a fixture test asserting the parser-to-request-builder field contract; it fails against the pre-fix commit and passes after the fix
open_risks:
- none
```
