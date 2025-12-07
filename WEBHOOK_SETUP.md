# Razorpay Webhook Setup Guide

This guide walks you through setting up Razorpay webhooks for local development and production.

## Overview

Razorpay webhooks notify your server about payment events (e.g., `payment.captured`, `payment.failed`). Your Django app verifies each webhook's signature to ensure it's authentic.

**Webhook endpoint**: `/shop/webhook/`

---

## Local Development Setup

### 1. Expose your local server with ngrok

Razorpay requires an HTTPS URL. Use ngrok to create a tunnel:

```powershell
# Install ngrok from https://ngrok.com (sign up for stable URLs)
ngrok http 8000
```

Copy the HTTPS URL displayed (e.g., `https://abcd-1234.ngrok.io`).

### 2. (Optional) Generate a webhook secret

For signature verification, create a strong secret:

```powershell
# PowerShell one-liner
python -c "import secrets; print(secrets.token_urlsafe(32))"
```

Add it to your **local** `.env` (do NOT commit):

```dotenv
RAZORPAY_WEBHOOK_SECRET=your-generated-secret-here
```

**Dev mode bypass**: If you leave `RAZORPAY_WEBHOOK_SECRET` blank in both your `.env` and Razorpay Dashboard, the webhook will accept requests without signature verification (only when `DEBUG=True`). This is safe for local testing but **never use in production**.

### 3. Configure webhook in Razorpay Dashboard

1. Go to [Razorpay Dashboard → Settings → Webhooks](https://dashboard.razorpay.com/app/website-app-settings/webhooks?action=add-new-webhook)
2. Click **Add New Webhook**
3. Fill in:
   - **Webhook URL**: `https://abcd-1234.ngrok.io/shop/webhook/`
   - **Secret**: (paste the secret from step 2, or leave blank for dev bypass)
   - **Alert Email**: your email
   - **Active Events**: Select events you need:
     - `payment.authorized`
     - `payment.captured`
     - `payment.failed`
     - Others as needed
4. **Create Webhook**

### 4. Start Django server

Keep your Django server running:

```powershell
.venv\Scripts\activate.ps1
python manage.py runserver
```

### 5. Test the webhook

- In Razorpay Dashboard, select your webhook and click **Send Test**
- Choose an event (e.g., `payment.captured`)
- Check:
  - **ngrok inspector** (http://127.0.0.1:4040): shows the POST request and response
  - **Django console**: should log `Razorpay webhook received: payment.captured`
  - Razorpay Dashboard: shows delivery success (HTTP 200)

---

## Production Setup

### 1. Set a strong webhook secret

Generate a secure secret and set it in your production environment (e.g., via environment variables, secrets manager, or hosting platform settings):

```bash
RAZORPAY_WEBHOOK_SECRET=your-production-secret
```

**Do NOT commit this to git.**

### 2. Update webhook URL in Razorpay Dashboard

- Switch to **Live Mode** in Razorpay Dashboard
- Add a new webhook with:
  - **Webhook URL**: `https://yourdomain.com/shop/webhook/`
  - **Secret**: the production secret you generated
  - **Active Events**: same events as test mode

### 3. Ensure HTTPS and signature verification

- Your production site **must** use HTTPS.
- The webhook view will **always** verify signatures when `RAZORPAY_WEBHOOK_SECRET` is set (dev bypass only applies when `DEBUG=True` and secret is blank).

---

## Webhook View Behavior

### Signature Verification

- **Production/Secure Mode**: When `RAZORPAY_WEBHOOK_SECRET` is set, the view computes HMAC-SHA256 of the raw POST body and compares it to the `X-Razorpay-Signature` header. If they don't match, returns HTTP 403.
- **Dev Bypass Mode**: When `DEBUG=True` and `RAZORPAY_WEBHOOK_SECRET` is blank, signature verification is skipped (logs a warning). Only use this locally.

### Handling Events

The webhook view in `shop/views.py` (`razorpay_webhook`) logs all events and includes stub logic for:

- `payment.captured`: Payment succeeded
- `payment.failed`: Payment failed
- `payment.authorized`: Payment authorized (for capture later)

**To-do**: Implement order fulfillment logic (e.g., mark order as paid, reduce stock, send confirmation email) in the webhook handler.

---

## Debugging Tips

### ngrok Inspector

Open http://127.0.0.1:4040 to see:
- Request headers (including `X-Razorpay-Signature`)
- Raw POST body
- Response status and body
- Option to **Replay** requests

### Django Logs

Check your Django console for:
- `Razorpay webhook received: <event_type>`
- Signature verification warnings/errors
- Parsed payment details

### Common Issues

- **403 Forbidden (signature missing)**: Secret is set in `.env` but not in Razorpay Dashboard (or vice versa).
- **403 Forbidden (invalid signature)**: Secrets don't match or webhook URL is incorrect.
- **CSRF token missing**: Ensure `@csrf_exempt` decorator is applied to the webhook view.
- **ngrok URL changes**: Free ngrok URLs change on restart. Update Razorpay Dashboard or sign up for a reserved URL.

---

## Security Best Practices

1. **Always use HTTPS** for webhook URLs (Razorpay requires it).
2. **Always verify signatures** in production (never use dev bypass).
3. **Never commit secrets** to version control (add `.env` to `.gitignore`).
4. **Respond quickly** (HTTP 200) and queue heavy tasks (email, invoice generation) to background workers (e.g., Celery).
5. **Log webhook payloads** for debugging but avoid logging sensitive data (e.g., card numbers) in production.
6. **Limit events** to only what you need in Razorpay Dashboard.

---

## Example: Simulate Webhook with curl

To test locally without Razorpay Dashboard:

```powershell
# Sample payload (save as payload.json)
$payload = @"
{
  "event": "payment.captured",
  "payload": {
    "payment": {
      "entity": {
        "id": "pay_test123",
        "order_id": "order_test456",
        "amount": 50000,
        "notes": {
          "order_id": "LUV202512071234"
        }
      }
    }
  }
}
"@

# Compute HMAC-SHA256 signature (replace <your-secret>)
$secret = "your-secret"
$hmac = [System.Security.Cryptography.HMACSHA256]::new([Text.Encoding]::UTF8.GetBytes($secret))
$hash = $hmac.ComputeHash([Text.Encoding]::UTF8.GetBytes($payload))
$signature = [BitConverter]::ToString($hash).Replace("-", "").ToLower()

# POST to webhook
curl -X POST `
  -H "Content-Type: application/json" `
  -H "X-Razorpay-Signature: $signature" `
  -d $payload `
  http://127.0.0.1:8000/shop/webhook/
```

Expected: HTTP 200 with body `ok`.

---

## References

- [Razorpay Webhooks Documentation](https://razorpay.com/docs/webhooks/)
- [ngrok Documentation](https://ngrok.com/docs)
- Django: `@csrf_exempt` decorator
- HMAC-SHA256 signature verification

---

**Questions?** Check Django logs and ngrok inspector for detailed request/response traces.
