"""
Forms for shop app
"""
from django import forms
from .models import Order


class CartAddProductForm(forms.Form):
    """Form for adding products to cart"""
    quantity = forms.IntegerField(
        min_value=1,
        initial=1,
        widget=forms.NumberInput(attrs={
            'class': 'form-control',
            'style': 'width: 80px;'
        })
    )
    override = forms.BooleanField(
        required=False,
        initial=False,
        widget=forms.HiddenInput
    )


class CouponApplyForm(forms.Form):
    """Form for applying coupon code"""
    code = forms.CharField(
        max_length=50,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter coupon code'
        })
    )


class CheckoutForm(forms.ModelForm):
    """Form for checkout process"""
    
    class Meta:
        model = Order
        fields = [
            'customer_name', 'customer_email', 'customer_phone',
            'shipping_address_line1', 'shipping_address_line2',
            'shipping_city', 'shipping_state', 'shipping_pincode',
            'customer_notes'
        ]
        widgets = {
            'customer_name': forms.TextInput(attrs={'class': 'form-control'}),
            'customer_email': forms.EmailInput(attrs={'class': 'form-control'}),
            'customer_phone': forms.TextInput(attrs={'class': 'form-control'}),
            'shipping_address_line1': forms.TextInput(attrs={'class': 'form-control'}),
            'shipping_address_line2': forms.TextInput(attrs={'class': 'form-control'}),
            'shipping_city': forms.TextInput(attrs={'class': 'form-control'}),
            'shipping_state': forms.TextInput(attrs={'class': 'form-control'}),
            'shipping_pincode': forms.TextInput(attrs={'class': 'form-control'}),
            'customer_notes': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        }
        labels = {
            'customer_name': 'Full Name',
            'customer_email': 'Email Address',
            'customer_phone': 'Phone Number',
            'shipping_address_line1': 'Address Line 1',
            'shipping_address_line2': 'Address Line 2 (Optional)',
            'shipping_city': 'City',
            'shipping_state': 'State',
            'shipping_pincode': 'PIN Code',
            'customer_notes': 'Order Notes (Optional)',
        }
