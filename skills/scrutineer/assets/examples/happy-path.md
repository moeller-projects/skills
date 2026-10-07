# Happy-Path Example — Scrutineer: Feature PR Review

## Input

Pull request: "Add password reset via email token". Diff touches `src/auth/reset.ts` (new), `src/auth/routes.ts` (route registration), `tests/auth/reset.spec.ts` (new tests).

## Process

1. Read the full diff before opening any file.
2. Open `src/auth/token-store.ts` only to confirm how `issueToken()` expires tokens.
3. Verify the suspected defect: the reset endpoint does not invalidate existing sessions after password change — confirmed by tracing `changePassword()` in `src/auth/password.ts`.
4. Sort findings, fence scope, issue verdict.

## Output

```text
verdict: request-changes
summary: Email-token password reset flow is well structured and tested, but sessions survive the password change.

findings:
- [blocker] src/auth/reset.ts:58 — existing sessions are not revoked after password change
  why: a hijacked session stays valid after the victim resets their password, defeating the reset
  suggestion: call `sessionStore.revokeAll(userId)` inside the reset handler before returning success
- [major] src/auth/reset.ts:23 — reset token accepted twice within its expiry window
  why: token replay allows a second password change from the same link
  suggestion: mark the token consumed in `tokenStore` before changing the password
- [nit] src/auth/routes.ts:17 — route is `/reset-password` while sibling routes use verbs (`/login`, `/logout`)
  why: consistency with the existing route vocabulary
  suggestion: consider `/reset` or document the naming choice

out-of-scope:
- `src/auth/password.ts` uses a deprecated hash work factor — pre-existing, hand to mechanic

risk:
- Token expiry is 24h; even with replay fixed, a leaked link has a long window — consider shortening in a follow-up
```
