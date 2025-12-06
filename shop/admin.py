"""
Django admin configuration for Shop models
"""
from django.contrib import admin
from .models import Category, Coupon, Order, OrderItem


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug', 'parent', 'is_active', 'display_order']
    list_filter = ['is_active', 'parent']
    search_fields = ['name', 'description']
    prepopulated_fields = {'slug': ('name',)}
    list_editable = ['display_order', 'is_active']


@admin.register(Coupon)
class CouponAdmin(admin.ModelAdmin):
    list_display = ['code', 'discount_type', 'value', 'valid_from', 'valid_to', 
                    'used_count', 'usage_limit', 'is_active']
    list_filter = ['discount_type', 'is_active', 'valid_from', 'valid_to']
    search_fields = ['code', 'description']
    readonly_fields = ['used_count', 'created_at', 'updated_at']
    fieldsets = (
        ('Basic Information', {
            'fields': ('code', 'description', 'is_active')
        }),
        ('Discount Settings', {
            'fields': ('discount_type', 'value', 'minimum_purchase')
        }),
        ('Validity Period', {
            'fields': ('valid_from', 'valid_to')
        }),
        ('Usage Limits', {
            'fields': ('usage_limit', 'used_count')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )


class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0
    readonly_fields = ['product_sku', 'product_name', 'product_price', 'quantity', 'line_total']
    can_delete = False


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['order_id', 'customer_name', 'customer_email', 'total', 
                    'status', 'created_at', 'paid_at']
    list_filter = ['status', 'created_at', 'paid_at']
    search_fields = ['order_id', 'customer_name', 'customer_email', 'customer_phone']
    readonly_fields = ['order_id', 'subtotal', 'discount_amount', 'total', 
                       'created_at', 'updated_at', 'paid_at', 'razorpay_order_id',
                       'razorpay_payment_id', 'razorpay_signature']
    inlines = [OrderItemInline]
    
    fieldsets = (
        ('Order Information', {
            'fields': ('order_id', 'status', 'created_at', 'updated_at', 'paid_at')
        }),
        ('Customer Information', {
            'fields': ('customer_name', 'customer_email', 'customer_phone')
        }),
        ('Shipping Address', {
            'fields': ('shipping_address_line1', 'shipping_address_line2', 
                      'shipping_city', 'shipping_state', 'shipping_pincode', 'shipping_country')
        }),
        ('Order Totals', {
            'fields': ('subtotal', 'discount_amount', 'shipping_cost', 'tax_amount', 'total')
        }),
        ('Coupon', {
            'fields': ('coupon', 'coupon_code'),
            'classes': ('collapse',)
        }),
        ('Payment Information', {
            'fields': ('payment_method', 'razorpay_order_id', 'razorpay_payment_id', 
                      'razorpay_signature')
        }),
        ('Notes', {
            'fields': ('customer_notes', 'admin_notes'),
            'classes': ('collapse',)
        }),
    )
    
    def get_readonly_fields(self, request, obj=None):
        """Make most fields readonly after order is created"""
        if obj:  # Editing existing order
            return self.readonly_fields + ['customer_name', 'customer_email', 
                                          'customer_phone', 'coupon']
        return self.readonly_fields
