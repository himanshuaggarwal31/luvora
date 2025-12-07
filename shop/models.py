"""
Shop models for LUVORA E-commerce
"""
from decimal import Decimal
from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from django.utils import timezone
from django.utils.text import slugify
from django.urls import reverse
from wagtail.models import Page
from wagtail.fields import RichTextField
from wagtail.admin.panels import FieldPanel, MultiFieldPanel
from wagtail.search import index
import uuid


class Category(models.Model):
    """Product categories for organizing products"""
    name = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(max_length=100, unique=True, blank=True)
    description = models.TextField(blank=True)
    image = models.ForeignKey(
        'wagtailimages.Image',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+'
    )
    parent = models.ForeignKey(
        'self',
        null=True,
        blank=True,
        on_delete=models.CASCADE,
        related_name='children'
    )
    is_active = models.BooleanField(default=True)
    display_order = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name_plural = 'Categories'
        ordering = ['display_order', 'name']

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('shop:category_detail', kwargs={'slug': self.slug})


class ProductPage(Page):
    """
    Wagtail Product Page - allows content editors to create products via CMS
    """
    # Basic Information
    sku = models.CharField(
        max_length=50,
        unique=True,
        help_text="Stock Keeping Unit - unique product identifier"
    )
    price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        validators=[MinValueValidator(Decimal('0.01'))]
    )
    compare_price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="Original price for showing discount"
    )
    cost_price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="Cost price (not shown to customers)"
    )
    
    # Product Details
    short_description = models.CharField(max_length=255, blank=True)
    description = RichTextField(blank=True)
    
    # Images
    main_image = models.ForeignKey(
        'wagtailimages.Image',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+'
    )
    
    # Category & Organization
    category = models.ForeignKey(
        Category,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='products'
    )
    
    # Inventory
    stock_quantity = models.IntegerField(
        default=0,
        validators=[MinValueValidator(0)]
    )
    track_inventory = models.BooleanField(default=True)
    allow_backorders = models.BooleanField(default=False)
    
    # Status
    is_featured = models.BooleanField(default=False)
    is_available = models.BooleanField(default=True)
    
    # SEO
    meta_keywords = models.CharField(max_length=255, blank=True)
    
    # Search index configuration
    search_fields = Page.search_fields + [
        index.SearchField('sku'),
        index.SearchField('short_description'),
        index.SearchField('description'),
        index.SearchField('meta_keywords'),
        index.FilterField('category'),
        index.FilterField('is_available'),
        index.FilterField('is_featured'),
    ]
    
    # Admin panels
    content_panels = Page.content_panels + [
        MultiFieldPanel([
            FieldPanel('sku'),
            FieldPanel('category'),
        ], heading="Basic Information"),
        
        MultiFieldPanel([
            FieldPanel('price'),
            FieldPanel('compare_price'),
            FieldPanel('cost_price'),
        ], heading="Pricing"),
        
        MultiFieldPanel([
            FieldPanel('short_description'),
            FieldPanel('description'),
            FieldPanel('main_image'),
        ], heading="Product Details"),
        
        MultiFieldPanel([
            FieldPanel('stock_quantity'),
            FieldPanel('track_inventory'),
            FieldPanel('allow_backorders'),
        ], heading="Inventory"),
        
        MultiFieldPanel([
            FieldPanel('is_available'),
            FieldPanel('is_featured'),
        ], heading="Status"),
    ]
    
    promote_panels = Page.promote_panels + [
        FieldPanel('meta_keywords'),
    ]
    
    template = "shop/product_detail.html"
    parent_page_types = ['shop.ProductIndexPage']
    
    class Meta:
        verbose_name = "Product"
        verbose_name_plural = "Products"
    
    def __str__(self):
        return self.title
    
    @property
    def is_in_stock(self):
        """Check if product is in stock"""
        if not self.track_inventory:
            return True
        return self.stock_quantity > 0 or self.allow_backorders
    
    @property
    def discount_percentage(self):
        """Calculate discount percentage if compare_price exists"""
        if self.compare_price and self.compare_price > self.price:
            discount = ((self.compare_price - self.price) / self.compare_price) * 100
            return round(discount, 0)
        return 0
    
    def can_purchase(self, quantity=1):
        """Check if product can be purchased in given quantity"""
        if not self.is_available:
            return False
        if not self.track_inventory:
            return True
        if self.allow_backorders:
            return True
        return self.stock_quantity >= quantity
    
    def reduce_stock(self, quantity):
        """Reduce stock quantity (called after successful order)"""
        if self.track_inventory:
            self.stock_quantity = max(0, self.stock_quantity - quantity)
            self.save(update_fields=['stock_quantity'])
    
    def get_context(self, request):
        """Add cart form to context"""
        from .forms import CartAddProductForm
        context = super().get_context(request)
        context['cart_product_form'] = CartAddProductForm()
        return context


class ProductIndexPage(Page):
    """Container page for listing all products"""
    intro = RichTextField(blank=True)
    
    content_panels = Page.content_panels + [
        FieldPanel('intro'),
    ]
    
    template = "shop/product_list.html"
    subpage_types = ['shop.ProductPage']
    
    def get_context(self, request):
        context = super().get_context(request)
        # Get all live product pages
        context['products'] = ProductPage.objects.live().public().order_by('-first_published_at')
        return context


class Coupon(models.Model):
    """Discount coupons for promotions"""
    PERCENT = 'percent'
    FIXED = 'fixed'
    DISCOUNT_CHOICES = [
        (PERCENT, 'Percentage Discount'),
        (FIXED, 'Fixed Amount Discount')
    ]
    
    code = models.CharField(
        max_length=50,
        unique=True,
        help_text="Coupon code (case-insensitive)"
    )
    description = models.CharField(max_length=255, blank=True)
    discount_type = models.CharField(max_length=10, choices=DISCOUNT_CHOICES)
    value = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        validators=[MinValueValidator(Decimal('0.01'))]
    )
    
    # Validity
    valid_from = models.DateTimeField()
    valid_to = models.DateTimeField()
    
    # Usage limits
    usage_limit = models.IntegerField(
        default=0,
        help_text="0 = unlimited usage"
    )
    used_count = models.IntegerField(default=0, editable=False)
    
    # Minimum purchase requirement
    minimum_purchase = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=Decimal('0.00'),
        help_text="Minimum cart value required"
    )
    
    # Status
    is_active = models.BooleanField(default=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.code} - {self.get_discount_display()}"
    
    def save(self, *args, **kwargs):
        self.code = self.code.upper()
        super().save(*args, **kwargs)
    
    def is_valid(self, cart_total=None):
        """Check if coupon is valid for use"""
        now = timezone.now()
        
        if not self.is_active:
            return False, "Coupon is not active"
        
        if not (self.valid_from <= now <= self.valid_to):
            return False, "Coupon has expired"
        
        if self.usage_limit and self.used_count >= self.usage_limit:
            return False, "Coupon usage limit reached"
        
        if cart_total and cart_total < self.minimum_purchase:
            return False, f"Minimum purchase of ₹{self.minimum_purchase} required"
        
        return True, "Valid"
    
    def get_discount_display(self):
        """Get human-readable discount display"""
        if self.discount_type == self.PERCENT:
            return f"{self.value}% OFF"
        return f"₹{self.value} OFF"
    
    def calculate_discount(self, total):
        """Calculate discount amount for given total"""
        if self.discount_type == self.PERCENT:
            discount = total * (self.value / Decimal('100'))
        else:
            discount = self.value
        
        # Discount cannot exceed total
        return min(discount, total)
    
    def apply_to_total(self, total):
        """Apply discount and return new total"""
        discount = self.calculate_discount(total)
        return max(total - discount, Decimal('0.00'))
    
    def increment_usage(self):
        """Increment usage count (call after successful order)"""
        self.used_count += 1
        self.save(update_fields=['used_count'])


class Order(models.Model):
    """Customer orders"""
    STATUS_CHOICES = [
        ('pending', 'Pending Payment'),
        ('paid', 'Paid'),
        ('processing', 'Processing'),
        ('shipped', 'Shipped'),
        ('delivered', 'Delivered'),
        ('cancelled', 'Cancelled'),
        ('refunded', 'Refunded'),
    ]
    
    # Order identification
    order_id = models.CharField(max_length=50, unique=True, editable=False)
    
    # Customer information
    customer_name = models.CharField(max_length=255)
    customer_email = models.EmailField()
    customer_phone = models.CharField(max_length=20)
    
    # Shipping address
    shipping_address_line1 = models.CharField(max_length=255)
    shipping_address_line2 = models.CharField(max_length=255, blank=True)
    shipping_city = models.CharField(max_length=100)
    shipping_state = models.CharField(max_length=100)
    shipping_pincode = models.CharField(max_length=10)
    shipping_country = models.CharField(max_length=100, default='India')
    
    # Order totals
    subtotal = models.DecimalField(max_digits=10, decimal_places=2)
    discount_amount = models.DecimalField(max_digits=10, decimal_places=2, default=Decimal('0.00'))
    shipping_cost = models.DecimalField(max_digits=10, decimal_places=2, default=Decimal('0.00'))
    tax_amount = models.DecimalField(max_digits=10, decimal_places=2, default=Decimal('0.00'))
    total = models.DecimalField(max_digits=10, decimal_places=2)
    
    # Coupon
    coupon = models.ForeignKey(
        Coupon,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='orders'
    )
    coupon_code = models.CharField(max_length=50, blank=True)
    
    # Payment
    payment_method = models.CharField(max_length=50, default='razorpay')
    razorpay_order_id = models.CharField(max_length=100, blank=True)
    razorpay_payment_id = models.CharField(max_length=100, blank=True)
    razorpay_signature = models.CharField(max_length=255, blank=True)
    
    # Status
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    
    # Notes
    customer_notes = models.TextField(blank=True)
    admin_notes = models.TextField(blank=True)
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    paid_at = models.DateTimeField(null=True, blank=True)
    
    class Meta:
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['-created_at']),
            models.Index(fields=['status']),
            models.Index(fields=['customer_email']),
        ]
    
    def __str__(self):
        return f"Order {self.order_id}"
    
    def save(self, *args, **kwargs):
        if not self.order_id:
            self.order_id = self.generate_order_id()
        super().save(*args, **kwargs)
    
    @staticmethod
    def generate_order_id():
        """Generate unique order ID"""
        timestamp = timezone.now().strftime('%Y%m%d%H%M%S')
        random_str = str(uuid.uuid4())[:8].upper()
        return f"LUV{timestamp}{random_str}"
    
    def mark_as_paid(self, payment_id, signature):
        """Mark order as paid and send confirmation email"""
        self.status = 'paid'
        self.razorpay_payment_id = payment_id
        self.razorpay_signature = signature
        self.paid_at = timezone.now()
        self.save()
        
        # Increment coupon usage if applicable
        if self.coupon:
            self.coupon.increment_usage()
        
        # Reduce stock for all items
        for item in self.items.all():
            if item.product:
                item.product.reduce_stock(item.quantity)
        
        # Send order confirmation email with invoice
        from .email_utils import send_order_confirmation_email
        send_order_confirmation_email(self)


class OrderItem(models.Model):
    """Individual items in an order"""
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey(
        ProductPage,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='order_items'
    )
    
    # Product snapshot (preserve details even if product changes)
    product_sku = models.CharField(max_length=50)
    product_name = models.CharField(max_length=255)
    product_price = models.DecimalField(max_digits=10, decimal_places=2)
    
    quantity = models.IntegerField(validators=[MinValueValidator(1)])
    line_total = models.DecimalField(max_digits=10, decimal_places=2)
    
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['id']
    
    def __str__(self):
        return f"{self.product_name} x {self.quantity}"
    
    def save(self, *args, **kwargs):
        self.line_total = self.product_price * self.quantity
        super().save(*args, **kwargs)
