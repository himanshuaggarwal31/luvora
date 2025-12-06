# Security Policy

## Supported Versions

| Version | Supported          |
| ------- | ------------------ |
| 1.0.x   | :white_check_mark: |

## Reporting a Vulnerability

If you discover a security vulnerability in LUVORA, please report it responsibly:

1. **DO NOT** open a public issue
2. Email security concerns to: himanshu@luvora.com (replace with your email)
3. Include:
   - Description of the vulnerability
   - Steps to reproduce
   - Potential impact
   - Suggested fix (if any)

We will respond within 48 hours and work with you to address the issue.

## Security Best Practices

### For Deployment

1. **Always use HTTPS in production**
   - Set `DEBUG=False`
   - Use SSL certificates (Let's Encrypt recommended)

2. **Protect sensitive credentials**
   - Never commit `.env` file
   - Use environment variables for all secrets
   - Rotate API keys regularly

3. **Database Security**
   - Use strong passwords
   - Restrict database access to application only
   - Enable encryption at rest (if available)

4. **Payment Gateway**
   - Use Razorpay webhook secrets
   - Verify all payment signatures server-side
   - Never trust client-side payment data

5. **Regular Updates**
   - Keep dependencies updated: `pip list --outdated`
   - Monitor security advisories for Django, Wagtail
   - Apply security patches promptly

### For Development

1. Never use production credentials in development
2. Use separate Razorpay test keys
3. Keep `.env` files out of version control
4. Sanitize any data before logging

## Known Security Considerations

1. **CSRF Protection**: Enabled by default in Django
2. **XSS Protection**: Django templates auto-escape by default
3. **SQL Injection**: Use Django ORM (avoid raw SQL)
4. **Session Security**: Secure cookies in production
5. **Rate Limiting**: Consider adding rate limiting for production

## Security Headers (Nginx)

The included `nginx.conf` sets these security headers:
- X-Frame-Options: SAMEORIGIN
- X-Content-Type-Options: nosniff
- X-XSS-Protection: 1; mode=block

For production, consider adding:
- Content-Security-Policy
- Strict-Transport-Security (HSTS)

## Compliance

- **PCI DSS**: Payment data is handled by Razorpay (PCI compliant)
- **GDPR**: Minimal PII collected; implement data export/deletion as needed
- **Data Retention**: Configure according to your privacy policy
