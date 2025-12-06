"""
Context processor to make cart available in all templates
"""
from .cart import Cart


def cart_context(request):
    """Add cart to template context"""
    return {
        'cart': Cart(request)
    }
