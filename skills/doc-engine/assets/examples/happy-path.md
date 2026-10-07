# Happy-Path Example — Doc Engine

## Scenario

Developer asks: "Write a README for our new `auth-service`."

## Input Context

- Service: JWT-based authentication microservice, Node.js + Express.
- Endpoints: `POST /login`, `POST /refresh`, `POST /logout`.
- Audience: backend engineers onboarding to the service.
- No existing README.

## Expected Output

```text
doc:
- purpose: enable a backend engineer to install, run, and call auth-service endpoints without prior knowledge of the service
- audience: backend engineer, familiar with REST APIs and Node.js, unfamiliar with this service
- structure:
  1. Overview [explanation] — what the service does and when to use it
  2. Prerequisites [reference] — Node.js version, env vars required
  3. Running locally [tutorial] — install, configure, start commands
  4. Endpoints [reference] — POST /login, POST /refresh, POST /logout with request/response examples
  5. Testing [how-to] — how to run the test suite
  6. Configuration reference [reference] — all env vars with defaults

changes:
- README.md — created from scratch

gaps:
- deployment guide (separate doc needed)
- rate limiting policy not documented in source
```

## Why This Is Correct

- Purpose and audience stated before any content.
- Structure defined before prose is written.
- Gaps identified so the requester knows what is still missing.
- No content invented; gaps listed instead of fabricated.
