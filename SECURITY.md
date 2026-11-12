# Security Policy

## Supported versions

| Version | Supported |
|---|---|
| 0.1.x | Yes |

## Reporting a vulnerability

Please use GitHub's private vulnerability reporting (Security tab → "Report a vulnerability"). Do not open a public issue for security problems.

I acknowledge reports within 72 hours and aim to ship a fix or mitigation within 14 days.

## Scope

- Code in `src/`, the CI workflow, and the data loader.
- Data integrity issues (a clause that misstates a policy) are not security issues: open a "Clause update" issue instead.

## Design notes

- Standard library only at runtime; no network calls in the checker.
- The data file is read as JSON, never executed.
