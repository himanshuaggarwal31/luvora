#!/usr/bin/env python
"""
Generate secrets for production deployment
"""
from django.core.management.utils import get_random_secret_key
import secrets

print("=" * 80)
print("PRODUCTION SECRETS GENERATOR")
print("=" * 80)
print()
print("Copy these values to your .env.production file or hosting platform:")
print()
print("-" * 80)
print(f"SECRET_KEY={get_random_secret_key()}")
print()
print(f"RAZORPAY_WEBHOOK_SECRET={secrets.token_urlsafe(32)}")
print("-" * 80)
print()
print("⚠️  IMPORTANT: Never commit these secrets to git!")
print("=" * 80)
