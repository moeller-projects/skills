# Rule: Injection Safety

> Impact: critical

## Description

Untrusted input MUST NEVER reach an interpreter — SQL/NoSQL engine, OS shell, LDAP/XPath query, template engine, or `eval`-class construct — as concatenated or interpolated code. Input crosses to interpreters only as bound data.

## Apply When

- Reviewing any code that builds a query, command, or interpreted string from a value that originated outside the current trust boundary — HTTP params, request bodies, headers, cookies, file contents, message-queue payloads, or database values that were themselves user-supplied.

## Checks

- SQL/NoSQL: parameterized queries / prepared statements / bound parameters are used; query text is NEVER built by concatenating or interpolating input.
- OS/shell: commands are invoked with an argument array, NEVER a constructed command string; no shell-interpolation of input (no `shell=True`-equivalent with input in the string).
- Template / dynamic eval: no `eval`, `exec`, `Function()`, or rendering of raw input as executable code or markup.
- ORM escape hatches (`.raw()`, `.query()`, hand-built `WHERE` clauses) are explicitly verified to be parameterized.
- Values that must be *structural* (i.e., identifiers that control query structure — table/column names, sort direction) are validated against an allowlist — escaping is not sufficient for structural elements.

## Anti-Pattern

Avoid examples that execute interpolated shell command strings. For example, passing a filename inside a command string to a shell lets shell syntax in the filename alter the command; pass arguments as a list with shell execution disabled instead.
