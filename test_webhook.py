#!/usr/bin/env python
"""
Test script to verify Razorpay webhook signature verification
"""
import os
import sys
import django
import hmac
import hashlib
import json
import requests

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'luvora_project.settings')
django.setup()

from decouple import config

# Get the webhook secret
WEBHOOK_SECRET = config('RAZORPAY_WEBHOOK_SECRET', default='')
WEBHOOK_URL = 'https://unalleviated-vicente-clownishly.ngrok-free.dev/shop/webhook/'

if not WEBHOOK_SECRET:
    print("❌ RAZORPAY_WEBHOOK_SECRET is not set in .env file!")
    sys.exit(1)

print(f"✓ Webhook Secret: {WEBHOOK_SECRET[:10]}... (loaded)")
print(f"✓ Webhook URL: {WEBHOOK_URL}")
print()

# Sample webhook payload
payload = {
    "entity": "event",
    "account_id": "acc_test123",
    "event": "payment.captured",
    "contains": ["payment"],
    "payload": {
        "payment": {
            "entity": {
                "id": "pay_test123",
                "entity": "payment",
                "amount": 50000,
                "currency": "INR",
                "status": "captured",
                "order_id": "order_test123",
                "method": "card",
                "captured": True
            }
        }
    },
    "created_at": 1638360000
}

# Convert to JSON string
payload_json = json.dumps(payload, separators=(',', ':'))

# Generate signature
signature = hmac.new(
    WEBHOOK_SECRET.encode('utf-8'),
    payload_json.encode('utf-8'),
    hashlib.sha256
).hexdigest()

print("📦 Test Payload:")
print(json.dumps(payload, indent=2))
print()
print(f"🔐 Generated Signature: {signature}")
print()

# Test with correct signature
print("Testing webhook with CORRECT signature...")
try:
    response = requests.post(
        WEBHOOK_URL,
        json=payload,
        headers={
            'X-Razorpay-Signature': signature,
            'Content-Type': 'application/json'
        },
        timeout=10
    )
    
    if response.status_code == 200:
        print(f"✅ SUCCESS: Webhook accepted (Status: {response.status_code})")
        print(f"   Response: {response.text[:200]}")
    else:
        print(f"❌ FAILED: Unexpected status code {response.status_code}")
        print(f"   Response: {response.text[:500]}")
except Exception as e:
    print(f"❌ ERROR: {e}")

print()
print("-" * 60)
print()

# Test with incorrect signature
print("Testing webhook with INCORRECT signature...")
try:
    response = requests.post(
        WEBHOOK_URL,
        json=payload,
        headers={
            'X-Razorpay-Signature': 'invalid_signature_12345',
            'Content-Type': 'application/json'
        },
        timeout=10
    )
    
    if response.status_code == 403:
        print(f"✅ SUCCESS: Webhook correctly rejected invalid signature (Status: {response.status_code})")
        print(f"   Response: {response.text[:200]}")
    else:
        print(f"⚠️  WARNING: Expected 403, got {response.status_code}")
        print(f"   Response: {response.text[:500]}")
except Exception as e:
    print(f"❌ ERROR: {e}")

print()
print("=" * 60)
print("✓ Webhook signature verification test completed!")
print()
print("📋 Next Steps:")
print("1. Go to Razorpay Dashboard: https://dashboard.razorpay.com/app/webhooks")
print("2. Click on your webhook or create a new one")
print(f"3. Set URL: {WEBHOOK_URL}")
print(f"4. Set Secret: {WEBHOOK_SECRET}")
print("5. Enable events: payment.authorized, payment.captured, payment.failed, order.paid")
print("6. Click 'Send Test Webhook' to verify")
