"""
URL configuration for shop app
"""
from django.urls import path
from . import views

app_name = 'shop'

urlpatterns = [
    # Product URLs
    path('', views.product_list, name='product_list'),
    path('product/<int:pk>/<slug:slug>/', views.product_detail, name='product_detail'),
    path('category/<slug:slug>/', views.category_detail, name='category_detail'),
    
    # Cart URLs
    path('cart/', views.cart_detail, name='cart_detail'),
    path('cart/add/<int:product_id>/', views.cart_add, name='cart_add'),
    path('cart/remove/<int:product_id>/', views.cart_remove, name='cart_remove'),
    
    # Coupon URLs
    path('cart/coupon/apply/', views.coupon_apply, name='coupon_apply'),
    path('cart/coupon/remove/', views.coupon_remove, name='coupon_remove'),
    
    # Checkout URLs
    path('checkout/', views.checkout, name='checkout'),
    path('payment/<str:order_id>/', views.payment, name='payment'),
    path('payment/callback/', views.payment_callback, name='payment_callback'),
    path('test-payment/<str:order_id>/', views.test_payment, name='test_payment'),  # Dev mode only
    path('order/success/<str:order_id>/', views.order_success, name='order_success'),
    path('payment/failed/', views.payment_failed, name='payment_failed'),
    
    # Razorpay webhook
    path('webhook/', views.razorpay_webhook, name='razorpay_webhook'),
]
