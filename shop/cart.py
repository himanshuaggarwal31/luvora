"""
Shopping cart functionality using Django sessions
"""
from decimal import Decimal
from django.conf import settings
from .models import ProductPage, Coupon


class Cart:
    """Session-based shopping cart"""
    
    def __init__(self, request):
        """Initialize the cart"""
        self.session = request.session
        cart = self.session.get(settings.CART_SESSION_ID if hasattr(settings, 'CART_SESSION_ID') else 'cart')
        
        if not cart:
            # Initialize empty cart
            cart = self.session['cart'] = {}
        
        self.cart = cart
        self._coupon_id = self.session.get('coupon_id')
    
    def add(self, product, quantity=1, override_quantity=False):
        """
        Add a product to the cart or update its quantity.
        
        Args:
            product: ProductPage instance
            quantity: Quantity to add
            override_quantity: If True, set quantity instead of incrementing
        """
        product_id = str(product.id)
        
        if product_id not in self.cart:
            self.cart[product_id] = {
                'quantity': 0,
                'price': str(product.price),
                'sku': product.sku,
                'title': product.title,
            }
        
        if override_quantity:
            self.cart[product_id]['quantity'] = quantity
        else:
            self.cart[product_id]['quantity'] += quantity
        
        self.save()
    
    def remove(self, product):
        """Remove a product from the cart"""
        product_id = str(product.id)
        
        if product_id in self.cart:
            del self.cart[product_id]
            self.save()
    
    def save(self):
        """Mark session as modified to ensure it's saved"""
        self.session.modified = True
    
    def clear(self):
        """Remove cart from session"""
        del self.session['cart']
        if 'coupon_id' in self.session:
            del self.session['coupon_id']
        self.save()
    
    def get_total_price(self):
        """Calculate total price of all items in cart"""
        return sum(
            Decimal(item['price']) * item['quantity']
            for item in self.cart.values()
        )
    
    def get_total_quantity(self):
        """Get total number of items in cart"""
        return sum(item['quantity'] for item in self.cart.values())
    
    def __iter__(self):
        """
        Iterate over items in cart and get products from database
        """
        product_ids = self.cart.keys()
        # Get products from database
        products = ProductPage.objects.filter(id__in=product_ids)
        cart = self.cart.copy()
        
        for product in products:
            cart[str(product.id)]['product'] = product
        
        for item in cart.values():
            item['price'] = Decimal(item['price'])
            item['total_price'] = item['price'] * item['quantity']
            yield item
    
    def __len__(self):
        """Count all items in cart"""
        return sum(item['quantity'] for item in self.cart.values())
    
    @property
    def coupon(self):
        """Get applied coupon if exists"""
        if self._coupon_id:
            try:
                return Coupon.objects.get(id=self._coupon_id)
            except Coupon.DoesNotExist:
                pass
        return None
    
    @coupon.setter
    def coupon(self, coupon):
        """Set coupon for cart"""
        if coupon:
            self.session['coupon_id'] = coupon.id
        else:
            if 'coupon_id' in self.session:
                del self.session['coupon_id']
        self.save()
    
    def get_discount(self):
        """Get discount amount from coupon"""
        if self.coupon:
            total = self.get_total_price()
            is_valid, message = self.coupon.is_valid(total)
            if is_valid:
                return self.coupon.calculate_discount(total)
        return Decimal('0.00')
    
    def get_total_price_after_discount(self):
        """Get total price after applying discount"""
        return self.get_total_price() - self.get_discount()
    
    def apply_coupon(self, coupon_code):
        """
        Apply coupon to cart
        
        Returns:
            tuple: (success: bool, message: str, coupon: Coupon or None)
        """
        try:
            coupon = Coupon.objects.get(code=coupon_code.upper())
        except Coupon.DoesNotExist:
            return False, "Invalid coupon code", None
        
        total = self.get_total_price()
        is_valid, message = coupon.is_valid(total)
        
        if is_valid:
            self.coupon = coupon
            discount = self.get_discount()
            return True, f"Coupon applied! You saved ₹{discount}", coupon
        else:
            return False, message, None
    
    def remove_coupon(self):
        """Remove applied coupon"""
        self.coupon = None
    
    def validate_items(self):
        """
        Validate all items in cart (stock, availability, etc.)
        
        Returns:
            tuple: (is_valid: bool, errors: list)
        """
        errors = []
        product_ids = self.cart.keys()
        products = {str(p.id): p for p in ProductPage.objects.filter(id__in=product_ids)}
        
        for product_id, item in self.cart.items():
            if product_id not in products:
                errors.append(f"Product {item['title']} is no longer available")
                continue
            
            product = products[product_id]
            
            if not product.is_available:
                errors.append(f"{product.title} is currently unavailable")
            
            if not product.can_purchase(item['quantity']):
                errors.append(
                    f"{product.title}: Only {product.stock_quantity} items available "
                    f"(you have {item['quantity']} in cart)"
                )
        
        return len(errors) == 0, errors


def get_cart(request):
    """Helper function to get cart instance"""
    return Cart(request)
