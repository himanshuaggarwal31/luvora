#!/usr/bin/env python
"""Quick script to check order status"""
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'luvora_project.settings')
django.setup()

from shop.models import Order

recent = Order.objects.order_by('-created_at')[:5]

print("\n" + "="*80)
print("RECENT ORDERS STATUS")
print("="*80)

for o in recent:
    paid_status = "✓ PAID" if o.paid_at else "○ PENDING"
    print(f"\n{paid_status} | {o.order_id}")
    print(f"   Customer: {o.customer_name}")
    print(f"   Status: {o.status}")
    print(f"   Total: ₹{o.total}")
    print(f"   Razorpay Order: {o.razorpay_order_id or 'N/A'}")
    print(f"   Razorpay Payment: {o.razorpay_payment_id or 'N/A'}")
    print(f"   Created: {o.created_at.strftime('%Y-%m-%d %H:%M:%S')}")
    if o.paid_at:
        print(f"   Paid At: {o.paid_at.strftime('%Y-%m-%d %H:%M:%S')}")

print("\n" + "="*80)
print(f"Total Orders: {Order.objects.count()}")
print(f"Paid Orders: {Order.objects.filter(status='paid').count()}")
print(f"Pending Orders: {Order.objects.filter(status='pending').count()}")
print("="*80 + "\n")
