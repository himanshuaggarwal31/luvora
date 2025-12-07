"""
Custom middleware for shop app
"""
from django.utils.deprecation import MiddlewareMixin


class DisableCSRFForPaymentCallbackMiddleware(MiddlewareMixin):
    """
    Disable CSRF origin checking for Razorpay payment callback.
    Razorpay's JavaScript form submission creates a null origin,
    which Django's CSRF middleware rejects when CSRF_TRUSTED_ORIGINS is set.
    The payment callback uses Razorpay's signature verification for security.
    """
    
    def process_request(self, request):
        if request.path == '/shop/payment/callback/':
            setattr(request, '_dont_enforce_csrf_checks', True)
        return None
