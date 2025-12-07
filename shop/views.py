"""
Views for shop app
"""
import time
import hmac
import hashlib
import json
from decimal import Decimal
from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.http import require_POST
from django.contrib import messages
from django.conf import settings
from django.urls import reverse
from django.http import JsonResponse, HttpResponseBadRequest, HttpResponse, HttpResponseForbidden
from django.views.decorators.csrf import csrf_exempt
import razorpay
import logging

from .models import ProductPage, Category, Order, OrderItem, Coupon
from .cart import Cart
from .forms import CartAddProductForm, CouponApplyForm, CheckoutForm

logger = logging.getLogger(__name__)


def product_list(request):
    """Display all products"""
    products = ProductPage.objects.live().public().filter(is_available=True)
    
    # Filter by category if provided
    category_slug = request.GET.get('category')
    if category_slug:
        category = get_object_or_404(Category, slug=category_slug)
        products = products.filter(category=category)
    else:
        category = None
    
    # Get all categories for sidebar
    categories = Category.objects.filter(is_active=True)
    
    context = {
        'products': products,
        'categories': categories,
        'selected_category': category,
    }
    return render(request, 'shop/product_list.html', context)


def product_detail(request, pk, slug):
    """Display product detail"""
    product = get_object_or_404(
        ProductPage.objects.live().public(),
        pk=pk,
        slug=slug
    )
    cart_product_form = CartAddProductForm()
    
    context = {
        'product': product,
        'cart_product_form': cart_product_form,
    }
    return render(request, 'shop/product_detail.html', context)


@require_POST
def cart_add(request, product_id):
    """Add product to cart"""
    cart = Cart(request)
    product = get_object_or_404(ProductPage, id=product_id)
    form = CartAddProductForm(request.POST)
    
    if form.is_valid():
        cd = form.cleaned_data
        quantity = cd['quantity']
        
        # Check if product can be purchased
        if not product.can_purchase(quantity):
            messages.error(request, f"Sorry, {product.title} is out of stock or insufficient quantity available.")
            return redirect('shop:product_detail', pk=product.id, slug=product.slug)
        
        cart.add(
            product=product,
            quantity=quantity,
            override_quantity=cd['override']
        )
        messages.success(request, f"{product.title} added to cart!")
    
    return redirect('shop:cart_detail')


@require_POST
def cart_remove(request, product_id):
    """Remove product from cart"""
    cart = Cart(request)
    product = get_object_or_404(ProductPage, id=product_id)
    cart.remove(product)
    messages.success(request, f"{product.title} removed from cart.")
    return redirect('shop:cart_detail')


def cart_detail(request):
    """Display cart contents"""
    cart = Cart(request)
    
    # Validate cart items
    is_valid, errors = cart.validate_items()
    
    if errors:
        for error in errors:
            messages.warning(request, error)
    
    # Forms
    coupon_form = CouponApplyForm()
    
    # Update cart items with forms for quantity update
    cart_items = []
    for item in cart:
        item['update_quantity_form'] = CartAddProductForm(
            initial={'quantity': item['quantity'], 'override': True}
        )
        cart_items.append(item)
    
    context = {
        'cart': cart,
        'cart_items': cart_items,
        'coupon_form': coupon_form,
        'is_cart_valid': is_valid,
    }
    return render(request, 'shop/cart_detail.html', context)


@require_POST
def coupon_apply(request):
    """Apply coupon code to cart"""
    form = CouponApplyForm(request.POST)
    
    if form.is_valid():
        code = form.cleaned_data['code']
        cart = Cart(request)
        success, message, coupon = cart.apply_coupon(code)
        
        if success:
            messages.success(request, message)
        else:
            messages.error(request, message)
    
    return redirect('shop:cart_detail')


def coupon_remove(request):
    """Remove coupon from cart"""
    cart = Cart(request)
    cart.remove_coupon()
    messages.info(request, "Coupon removed from cart.")
    return redirect('shop:cart_detail')


def checkout(request):
    """Checkout page"""
    cart = Cart(request)
    
    if len(cart) == 0:
        messages.warning(request, "Your cart is empty.")
        return redirect('shop:product_list')
    
    # Validate cart
    is_valid, errors = cart.validate_items()
    if not is_valid:
        for error in errors:
            messages.error(request, error)
        return redirect('shop:cart_detail')
    
    if request.method == 'POST':
        form = CheckoutForm(request.POST)
        
        if form.is_valid():
            # Create order
            order = form.save(commit=False)
            
            # Calculate totals
            subtotal = cart.get_total_price()
            discount = cart.get_discount()
            total = cart.get_total_price_after_discount()
            
            order.subtotal = subtotal
            order.discount_amount = discount
            order.total = total
            
            # Apply coupon if exists
            if cart.coupon:
                order.coupon = cart.coupon
                order.coupon_code = cart.coupon.code
            
            order.save()
            
            # Create order items
            for item in cart:
                OrderItem.objects.create(
                    order=order,
                    product=item['product'],
                    product_sku=item['sku'],
                    product_name=item['title'],
                    product_price=float(item['price']),  # Convert Decimal to float for JSON serialization
                    quantity=item['quantity']
                )
            
            # Store order id in session for payment
            request.session['order_id'] = order.id
            
            # Redirect to payment
            return redirect('shop:payment', order_id=order.order_id)
    else:
        form = CheckoutForm()
    
    context = {
        'form': form,
        'cart': cart,
    }
    return render(request, 'shop/checkout.html', context)


def payment(request, order_id):
    """Payment page with Razorpay integration"""
    order = get_object_or_404(Order, order_id=order_id)
    
    # Check if order belongs to current session
    if request.session.get('order_id') != order.id:
        messages.error(request, "Invalid order access.")
        return redirect('shop:product_list')
    
    # Initialize Razorpay client
    if settings.RAZORPAY_KEY_ID and settings.RAZORPAY_KEY_SECRET:
        client = razorpay.Client(
            auth=(settings.RAZORPAY_KEY_ID, settings.RAZORPAY_KEY_SECRET)
        )
        
        # Create Razorpay order
        try:
            razorpay_order = client.order.create({
                'amount': int(order.total * 100),  # Amount in paise
                'currency': 'INR',
                'receipt': order.order_id,
                'payment_capture': 1
            })
            
            order.razorpay_order_id = razorpay_order['id']
            order.save()
            
            context = {
                'order': order,
                'razorpay_order_id': razorpay_order['id'],
                'razorpay_key_id': settings.RAZORPAY_KEY_ID,
                'amount': int(order.total * 100),
                'currency': 'INR',
                'callback_url': request.build_absolute_uri(reverse('shop:payment_callback')),
            }
            return render(request, 'shop/payment.html', context)
        
        except Exception as e:
            logger.error(f"Razorpay order creation failed: {str(e)}")
            messages.error(request, "Payment gateway error. Please try again.")
            return redirect('shop:checkout')
    else:
        # Razorpay not configured - show test mode
        context = {
            'order': order,
            'test_mode': True,
            'test_payment_url': request.build_absolute_uri(
                reverse('shop:test_payment', kwargs={'order_id': order.order_id})
            ),
        }
        return render(request, 'shop/payment.html', context)


def test_payment(request, order_id):
    """
    Test mode payment - bypasses Razorpay for development
    Only works when DEBUG=True and Razorpay keys are not configured
    """
    if not settings.DEBUG or (settings.RAZORPAY_KEY_ID and settings.RAZORPAY_KEY_SECRET):
        messages.error(request, "Test payment is only available in development mode.")
        return redirect('shop:product_list')
    
    order = get_object_or_404(Order, order_id=order_id)
    
    # Check if order belongs to current session
    if request.session.get('order_id') != order.id:
        messages.error(request, "Invalid order access.")
        return redirect('shop:product_list')
    
    if request.method == 'POST':
        # Simulate successful payment
        test_payment_id = f"test_pay_{order.order_id}_{int(time.time())}"
        test_signature = f"test_sig_{order.order_id}"
        
        # Mark order as paid (this triggers email and invoice generation)
        order.mark_as_paid(test_payment_id, test_signature)
        
        # Clear cart
        cart = Cart(request)
        cart.clear()
        
        # Clear order from session
        if 'order_id' in request.session:
            del request.session['order_id']
        
        messages.success(request, "✅ TEST PAYMENT: Your order has been placed successfully!")
        return redirect('shop:order_success', order_id=order.order_id)
    
    # Show test payment confirmation page
    context = {
        'order': order,
    }
    return render(request, 'shop/test_payment.html', context)


@csrf_exempt
@require_POST
def payment_callback(request):
    """Handle Razorpay payment callback"""
    try:
        # Get payment details
        razorpay_payment_id = request.POST.get('razorpay_payment_id')
        razorpay_order_id = request.POST.get('razorpay_order_id')
        razorpay_signature = request.POST.get('razorpay_signature')
        
        # Get order
        order = get_object_or_404(Order, razorpay_order_id=razorpay_order_id)
        
        # Verify signature
        client = razorpay.Client(
            auth=(settings.RAZORPAY_KEY_ID, settings.RAZORPAY_KEY_SECRET)
        )
        
        params_dict = {
            'razorpay_order_id': razorpay_order_id,
            'razorpay_payment_id': razorpay_payment_id,
            'razorpay_signature': razorpay_signature
        }
        
        client.utility.verify_payment_signature(params_dict)
        
        # Payment successful - mark order as paid
        order.mark_as_paid(razorpay_payment_id, razorpay_signature)
        
        # Clear cart
        cart = Cart(request)
        cart.clear()
        
        # Clear order from session
        if 'order_id' in request.session:
            del request.session['order_id']
        
        messages.success(request, "Payment successful! Your order has been placed.")
        return redirect('shop:order_success', order_id=order.order_id)
    
    except razorpay.errors.SignatureVerificationError:
        logger.error("Razorpay signature verification failed")
        messages.error(request, "Payment verification failed. Please contact support.")
        return redirect('shop:payment_failed')
    
    except Exception as e:
        logger.error(f"Payment callback error: {str(e)}")
        messages.error(request, "Payment processing error. Please contact support.")
        return redirect('shop:payment_failed')


def order_success(request, order_id):
    """Order success page"""
    order = get_object_or_404(Order, order_id=order_id)
    
    context = {
        'order': order,
    }
    return render(request, 'shop/order_success.html', context)


def payment_failed(request):
    """Payment failed page"""
    return render(request, 'shop/payment_failed.html')


def category_detail(request, slug):
    """Display products in a category"""
    category = get_object_or_404(Category, slug=slug, is_active=True)
    products = ProductPage.objects.live().public().filter(
        category=category,
        is_available=True
    )
    
    context = {
        'category': category,
        'products': products,
    }
    return render(request, 'shop/category_detail.html', context)


@csrf_exempt
def razorpay_webhook(request):
    """
    Handle Razorpay webhooks.
    Verifies signature when RAZORPAY_WEBHOOK_SECRET is set.
    Dev mode: allows unverified webhooks if DEBUG=True and secret is blank.
    """
    if request.method != 'POST':
        return HttpResponseBadRequest("Only POST allowed")
    
    # Read raw body
    payload = request.body or b""
    signature = request.headers.get("X-Razorpay-Signature") or request.META.get("HTTP_X_RAZORPAY_SIGNATURE")
    
    secret = getattr(settings, "RAZORPAY_WEBHOOK_SECRET", "") or ""
    
    # Dev mode bypass: if no secret and DEBUG=True, allow processing without verification
    if not secret and settings.DEBUG:
        logger.warning(
            "Razorpay webhook signature verification SKIPPED (DEBUG=True, no secret set). "
            "This is ONLY safe for local development."
        )
    else:
        # Production/secure mode: require signature and verify it
        if not signature:
            logger.warning("Razorpay webhook missing signature header")
            return HttpResponseForbidden("signature missing")
        
        if not secret:
            logger.error("RAZORPAY_WEBHOOK_SECRET not configured but signature provided")
            return HttpResponseForbidden("webhook secret not configured")
        
        # Compute HMAC-SHA256 and compare
        computed_hmac = hmac.new(
            key=secret.encode("utf-8"),
            msg=payload,
            digestmod=hashlib.sha256
        ).hexdigest()
        
        if not hmac.compare_digest(computed_hmac, signature):
            logger.warning("Invalid Razorpay webhook signature")
            return HttpResponseForbidden("invalid signature")
    
    # Parse JSON payload
    try:
        event = json.loads(payload.decode("utf-8"))
    except Exception as e:
        logger.exception("Invalid JSON in webhook payload")
        return HttpResponseBadRequest("invalid json")
    
    event_type = event.get("event")
    payload_data = event.get("payload", {})
    logger.info(f"Razorpay webhook received: {event_type}")
    
    # Handle specific events
    if event_type == "payment.captured":
        payment = payload_data.get("payment", {}).get("entity", {})
        payment_id = payment.get("id")
        order_id = payment.get("notes", {}).get("order_id") or payment.get("order_id")
        amount = payment.get("amount")  # in paise
        
        logger.info(f"Payment captured: payment_id={payment_id}, order_id={order_id}, amount={amount}")
        
        # TODO: Look up Order by order_id or razorpay_order_id and mark as paid if needed
        # Example:
        # try:
        #     order = Order.objects.get(order_id=order_id)
        #     if order.paid:
        #         logger.info(f"Order {order_id} already marked as paid")
        #     else:
        #         order.mark_as_paid(payment_id, signature or "")
        #         logger.info(f"Order {order_id} marked as paid via webhook")
        # except Order.DoesNotExist:
        #     logger.warning(f"Order {order_id} not found for payment.captured webhook")
    
    elif event_type == "payment.failed":
        payment = payload_data.get("payment", {}).get("entity", {})
        logger.info(f"Payment failed: {payment.get('id')}")
    
    elif event_type == "payment.authorized":
        payment = payload_data.get("payment", {}).get("entity", {})
        logger.info(f"Payment authorized: {payment.get('id')}")
    
    # Add other event handlers as needed
    
    # Respond with 200 to acknowledge receipt
    return HttpResponse("ok")


@csrf_exempt
def razorpay_webhook(request):
    """
    Handle Razorpay webhooks.
    Verifies signature when RAZORPAY_WEBHOOK_SECRET is set.
    Dev mode: allows unverified webhooks if DEBUG=True and secret is blank.
    """
    if request.method != 'POST':
        return HttpResponseBadRequest("Only POST allowed")
    
    # Read raw body
    payload = request.body or b""
    signature = request.headers.get("X-Razorpay-Signature") or request.META.get("HTTP_X_RAZORPAY_SIGNATURE")
    
    secret = getattr(settings, "RAZORPAY_WEBHOOK_SECRET", "") or ""
    
    # Dev mode bypass: if no secret and DEBUG=True, allow processing without verification
    if not secret and settings.DEBUG:
        logger.warning(
            "Razorpay webhook signature verification SKIPPED (DEBUG=True, no secret set). "
            "This is ONLY safe for local development."
        )
    else:
        # Production/secure mode: require signature and verify it
        if not signature:
            logger.warning("Razorpay webhook missing signature header")
            return HttpResponseForbidden("signature missing")
        
        if not secret:
            logger.error("RAZORPAY_WEBHOOK_SECRET not configured but signature provided")
            return HttpResponseForbidden("webhook secret not configured")
        
        # Compute HMAC-SHA256 and compare
        computed_hmac = hmac.new(
            key=secret.encode("utf-8"),
            msg=payload,
            digestmod=hashlib.sha256
        ).hexdigest()
        
        if not hmac.compare_digest(computed_hmac, signature):
            logger.warning("Invalid Razorpay webhook signature")
            return HttpResponseForbidden("invalid signature")
    
    # Parse JSON payload
    try:
        event = json.loads(payload.decode("utf-8"))
    except Exception as e:
        logger.exception("Invalid JSON in webhook payload")
        return HttpResponseBadRequest("invalid json")
    
    event_type = event.get("event")
    payload_data = event.get("payload", {})
    logger.info(f"Razorpay webhook received: {event_type}")
    
    # Handle specific events
    if event_type == "payment.captured":
        payment = payload_data.get("payment", {}).get("entity", {})
        payment_id = payment.get("id")
        order_id = payment.get("notes", {}).get("order_id") or payment.get("order_id")
        amount = payment.get("amount")  # in paise
        
        logger.info(f"Payment captured: payment_id={payment_id}, order_id={order_id}, amount={amount}")
        
        # TODO: Look up Order by order_id or razorpay_order_id and mark as paid if needed
        # Example:
        # try:
        #     order = Order.objects.get(order_id=order_id)
        #     if order.paid:
        #         logger.info(f"Order {order_id} already marked as paid")
        #     else:
        #         order.mark_as_paid(payment_id, signature or "")
        #         logger.info(f"Order {order_id} marked as paid via webhook")
        # except Order.DoesNotExist:
        #     logger.warning(f"Order {order_id} not found for payment.captured webhook")
    
    elif event_type == "payment.failed":
        payment = payload_data.get("payment", {}).get("entity", {})
        logger.info(f"Payment failed: {payment.get('id')}")
    
    elif event_type == "payment.authorized":
        payment = payload_data.get("payment", {}).get("entity", {})
        logger.info(f"Payment authorized: {payment.get('id')}")
    
    # Add other event handlers as needed
    
    # Respond with 200 to acknowledge receipt
    return HttpResponse("ok")
