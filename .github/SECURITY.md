# Security Policy

## Reporting a Vulnerability

**Please do not open a public GitHub issue for security vulnerabilities.**

If you discover a security issue — especially anything related to credential handling, token exposure, or data privacy — please report it privately:

1. Go to the **[Security tab](https://github.com/TanaTTV/Discord-Archiver/security)** of this repo
2. Click **"Report a vulnerability"**
3. Fill in the details

We'll acknowledge your report within 48 hours and work on a fix as quickly as possible.

## What counts as a security issue?

- Bot token exposure or logging
- User data leaking outside localhost
- Path traversal in file output
- CORS misconfiguration allowing external access
- Any vulnerability that could affect a user's Discord account

## What doesn't count

- Issues caused by users misconfiguring their own `.env` or running the app on a public network (the tool is designed for localhost only)
- Discord API rate limiting or account issues from high concurrency settings (these are covered in the README warnings)
