# Payment Integration & Invoice Generation Guide

## 🎉 Features Implemented

✅ **Razorpay Payment Gateway Integration**
✅ **PDF Invoice Generation** (using ReportLab)
✅ **Automated Email Notifications** with invoice attachment
✅ **Order Confirmation Emails**
✅ **Order Status Update Emails**

## 🔧 Setup Instructions

### 1. Razorpay Setup (For Production)

1. **Create Razorpay Account**
   - Go to https://dashboard.razorpay.com/signup
   - Sign up for a free account

2. **Get API Keys**
   - Go to Settings → API Keys
   - Generate Test/Live keys
   - Copy `Key ID` and `Key Secret`

3. **Update `.env` File**
   ```env
   RAZORPAY_KEY_ID=rzp_test_xxxxxxxxxxxx
   RAZORPAY_KEY_SECRET=xxxxxxxxxxxxxxxx
   ```

### 2. Email Setup

#### Development (Console Backend - Default)
Emails will be printed to the terminal where Django is running.
```env
EMAIL_BACKEND=django.core.mail.backends.console.EmailBackend
```

#### Production (Gmail SMTP)
1. Enable 2-Factor Authentication in your Gmail
2. Create an App Password: https://myaccount.google.com/apppasswords
3. Update `.env`:
   ```env
   EMAIL_BACKEND=django.core.mail.backends.smtp.EmailBackend
   EMAIL_HOST=smtp.gmail.com
   EMAIL_PORT=587
   EMAIL_USE_TLS=True
   EMAIL_HOST_USER=your-email@gmail.com
   EMAIL_HOST_PASSWORD=your-16-char-app-password
   DEFAULT_FROM_EMAIL=LUVORA <noreply@luvora.com>
   ```

## 📝 Testing the Integration

### Test Mode (Without Razorpay Keys)
When Razorpay keys are not configured, the system runs in TEST MODE:
- Payment page shows a test mode message
- No actual payment is processed
- You can still test the checkout flow

### Test with Sample Order

1. **Create a test order** by going through checkout
2. **Test invoice generation**:
   ```bash
   python manage.py test_invoice ORDER_ID_HERE --save
   ```
   This creates `invoice_ORDER_ID.pdf`

3. **Test email with invoice**:
   ```bash
   python manage.py test_invoice ORDER_ID_HERE --email
   ```
   Check terminal (console backend) or your inbox

## 🛍️ Customer Experience Flow

### 1. Shopping
- Browse products at `/shop/`
- Add items to cart
- Apply coupon codes (if any)

### 2. Checkout
- Enter shipping details
- Review order summary
- Click "Proceed to Payment"

### 3. Payment
**With Razorpay (Production):**
- Razorpay payment modal opens
- Choose payment method:
  - Credit/Debit Card
  - UPI
  - Net Banking
  - Wallets
- Complete payment
- Redirected to success page

**Test Mode (Development):**
- See test mode message
- Order created but not paid

### 4. Order Confirmation
After successful payment:
1. ✅ Order status updated to "Paid"
2. 📧 Email sent with invoice PDF attached
3. 📦 Stock reduced for purchased items
4. 🎟️ Coupon usage incremented (if used)

### 5. Email Contents
Customer receives:
- Order confirmation message
- Complete order details
- Shipping address
- Itemized list of products
- Price breakdown with discounts
- **PDF Invoice attachment**

## 📄 Invoice Features

The generated invoice includes:
- LUVORA branding
- Invoice number (Order ID)
- Customer details
- Shipping address
- Itemized product list with SKU
- Price breakdown:
  - Subtotal
  - Discount (if applied)
  - Shipping cost
  - Tax
  - Total
- Payment information
- Professional formatting with colors and styling

## 🔄 Order Status Updates

Admins can update order status from Django admin. When status changes:
- Automatic email sent to customer
- Email contains:
  - New status
  - Order details
  - Optional custom message

## 💡 Tips for Testing

### Test Razorpay in Test Mode
Use these test card details:
- **Card Number**: 4111 1111 1111 1111
- **CVV**: Any 3 digits
- **Expiry**: Any future date
- **OTP**: 123456

### Test UPI
Use: `success@razorpay`

### View Console Emails
When using console email backend, emails appear in the terminal where `runserver` is running.

## 🚀 Going Live

1. **Switch to Live Razorpay Keys**
   - Get Live API keys from Razorpay dashboard
   - Update `.env` with live keys

2. **Configure Production Email**
   - Set up Gmail SMTP or use a service like SendGrid
   - Update `.env` with production email settings

3. **Test Everything**
   - Place test orders
   - Verify emails arrive
   - Check invoice PDFs
   - Test payment flow end-to-end

## 📞 Support

For any issues:
- Check Django logs
- Check Razorpay dashboard for payment logs
- Test invoice generation separately using management command
- Verify email settings with Django's `send_mail` function

## 🎨 Customization

### Customize Invoice
Edit `shop/invoice.py` to:
- Add company logo
- Change colors (currently brown #8B4513)
- Modify layout
- Add terms & conditions
- Include GST/tax numbers

### Customize Emails
Edit templates in `templates/shop/emails/`:
- `order_confirmation.html` - Main confirmation email
- `order_confirmation.txt` - Plain text version
- `order_status_update.html` - Status update email
- `order_status_update.txt` - Plain text version

## ✅ What's Working

✓ Complete checkout flow
✓ Razorpay integration with test mode fallback
✓ PDF invoice generation with professional styling
✓ Email sending with attachment
✓ Automatic emails on payment success
✓ Order status tracking
✓ Stock management
✓ Coupon validation and usage tracking
