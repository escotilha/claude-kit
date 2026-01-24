# Security Rules

Security guidelines to follow in all projects.

## Secrets Management

- NEVER commit secrets, API keys, passwords, or credentials
- Use environment variables for sensitive configuration
- Add `.env` files to `.gitignore`
- Use secret management services in production (AWS Secrets Manager, Vault, etc.)
- Rotate credentials if accidentally exposed

## Input Validation

- Validate and sanitize ALL user input
- Use parameterized queries - never concatenate SQL
- Escape output to prevent XSS
- Validate file uploads (type, size, content)
- Implement rate limiting on public endpoints

## Authentication & Authorization

- Use established auth libraries, don't roll your own
- Hash passwords with bcrypt, argon2, or scrypt
- Implement proper session management
- Use HTTPS everywhere
- Apply principle of least privilege

## OWASP Top 10 Awareness

Avoid these common vulnerabilities:

1. Injection (SQL, NoSQL, OS command)
2. Broken Authentication
3. Sensitive Data Exposure
4. XML External Entities (XXE)
5. Broken Access Control
6. Security Misconfiguration
7. Cross-Site Scripting (XSS)
8. Insecure Deserialization
9. Using Components with Known Vulnerabilities
10. Insufficient Logging & Monitoring

## Dependencies

- Keep dependencies updated
- Review security advisories regularly
- Use `npm audit`, `pip-audit`, or equivalent
- Pin dependency versions in production
- Verify package integrity before installation

## Code Review Security Checklist

Before approving PRs, verify:

- [ ] No hardcoded secrets
- [ ] User input is validated
- [ ] SQL queries are parameterized
- [ ] Output is properly escaped
- [ ] Error messages don't leak sensitive info
- [ ] Authentication/authorization is correct
- [ ] New dependencies are reviewed

## Incident Response

If a security issue is discovered:

1. Don't panic, but act quickly
2. Assess the scope and impact
3. Contain the issue (revoke credentials, patch, etc.)
4. Document what happened
5. Notify affected parties if required
6. Post-mortem and implement preventive measures
