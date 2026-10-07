# Rule: Authorization Enforcement

> Impact: critical

## Description

Every operation that exposes or mutates a protected resource MUST enforce a server-side authorization check, scoped to both the acting principal and the specific resource. Authentication is not authorization, and client-side checks are never sufficient.

## Apply When

- Reviewing any endpoint, request handler, RPC method, or service function that reads, lists, creates, updates, or deletes a resource that is not equally public to all users.

## Checks

- Authorization is enforced as distinct from authentication — being logged in MUST NOT be treated as being permitted.
- The check is object-scoped: it confirms this principal may act on *this specific resource id*. Fetching `/orders/{id}` MUST verify the order belongs to (or is visible to) the caller — guarding against IDOR (Insecure Direct Object Reference).
- Enforcement is server-side. Hidden UI elements, disabled buttons, and client-side role checks do not count as authorization.
- New routes and handlers are NEVER authorized by omission — the absence of a check is a finding, not a pass.
- Privileged operations (admin, cross-tenant, bulk) explicitly verify the elevated role or permission.
- Authorization is default-deny: an unmatched role or permission MUST fall through to denied.

## Anti-Pattern

`app.get("/api/orders/:id", authenticated, (req) => db.orders.find(req.params.id))` — authenticated but never checks the order belongs to `req.user`. Relying on the frontend hiding an admin button instead of enforcing the role on the server.
