# LUVORA Quick Setup Guide

## 🚀 3-Minute Quick Start (Windows)

### Automated Setup (Recommended)

```powershell
# Clone repository
git clone https://github.com/himanshuaggarwal31/luvora.git
cd luvora

# Run setup script
.\setup.bat

# The script automatically:
# - Creates Python 3.12 virtual environment
# - Installs all dependencies (Django 5.1, Wagtail 6.4, ReportLab, etc.)
# - Configures SQLite database
# - Runs migrations
# - Creates static directory
# - Prompts for superuser creation
```

After setup completes:

```powershell
# Activate environment
.venv\Scripts\activate

# Create page structure (Home, Shop, Products)
python setup_pages.py

# Start server
python manage.py runserver
```

**Visit**: http://127.0.0.1:8000

**Admin**: http://127.0.0.1:8000/admin/ (use superuser credentials)

---

## 📝 Manual Setup (If Needed)

### Step 1: Environment Setup

```powershell
# Create virtual environment (Python 3.12 required)
python -m venv .venv
.venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

### Step 2: Database Configuration

**SQLite (Default - No configuration needed!)**
```env
DB_ENGINE=django.db.backends.sqlite3
DB_NAME=db.sqlite3
```

The `.env` file is already configured for SQLite.

### Step 3: Initialize Database & Pages

```powershell
# Run migrations
python manage.py migrate

# Create superuser
python manage.py createsuperuser

# Create page structure (Home, Shop, Sample Products)
python setup_pages.py
```

The `setup_pages.py` script creates:
- ✅ Home page (site root)
- ✅ Shop page (`/shop/`)
- ✅ 2 sample products with pricing

### Step 4: Run Development Server

```powershell
python manage.py runserver
```

**Visit**: http://127.0.0.1:8000

---

## 📝 What You Get Out of the Box

### ✅ Pre-configured Features
- **SQLite Database**: Ready to use, no setup needed
- **Sample Products**: 2 products with images and pricing
- **Shopping Cart**: Session-based cart system
- **Payment Integration**: Razorpay (works in test mode without keys)
- **Invoice Generation**: Professional PDF invoices with ReportLab
- **Email Notifications**: Console backend (prints to terminal)
- **Admin Panel**: Wagtail CMS + Django Admin
- **Bootstrap 5 UI**: Responsive, mobile-first design

---

## 🛍️ Adding More Products

### Via Wagtail CMS (Recommended)

1. Visit: http://127.0.0.1:8000/admin/
2. Login with superuser credentials
3. Pages → Shop → Add child page → Product
4. Fill in product details:
   - **Title**: Product name
   - **SKU**: Unique code (e.g., "BED-001")
   - **Price**: Selling price
   - **Compare Price**: Original price (for discount display)
   - **Short Description**: Brief product summary
   - **Description**: Detailed product information (rich text)
   - **Main Image**: Upload product image
   - **Category**: Select or create category
   - **Stock Quantity**: Available units
   - **Is Available**: ✓ (make product visible)
   - **Is Featured**: ✓ (optional, for featured products)
5. Save and publish

### Managing Products

- **Edit**: Pages → Shop → Click product → Edit
- **Delete**: Pages → Shop → Click product → Delete
- **Unpublish**: Uncheck "Live" to hide without deleting
- **Reorder**: Drag and drop in page list

---

## 🧪 Testing Features

### Test the Shop
1. Visit: http://127.0.0.1:8000/shop/
2. Browse products
3. Click on a product to view details
4. Product shows: price, stock status, description, image

### Test Shopping Cart
1. Add product to cart
2. Visit cart: http://127.0.0.1:8000/shop/cart/
3. Update quantities
4. See real-time price calculations

### Test Checkout Flow
1. Fill in shipping information
2. Review order summary
3. Click "Proceed to Payment"
4. **Test Mode** (no Razorpay keys):
   - Payment page shows test mode message
   - Order created but not paid
5. **Production Mode** (with keys):
   - Razorpay payment modal opens
   - Complete payment with test card

### Test Payment & Invoices
After placing an order:

```powershell
# View orders in Django admin
# Visit: http://127.0.0.1:8000/django-admin/shop/order/

# Test invoice generation
python manage.py test_invoice ORDER_ID_HERE --save

# Test email with invoice (check terminal for output)
python manage.py test_invoice ORDER_ID_HERE --email
```

---

## 💳 Payment Integration (Optional)

### Test Mode (Default - No Setup Needed)
- Checkout works without Razorpay API keys
- Payment page shows test mode message
- Perfect for development and testing
- No actual payment processing

### Production Mode (With Razorpay)

1. **Sign up**: https://razorpay.com
2. **Get Keys**: Dashboard → Settings → API Keys → Generate Test Key
3. **Update .env**:
   ```env
   RAZORPAY_KEY_ID=rzp_test_xxxxxxxxxxxxx
   RAZORPAY_KEY_SECRET=your_secret_key_here
   ```
4. **Restart server**: `python manage.py runserver`

### Test Payment (With Keys)
Use Razorpay test credentials:
- **Card**: 4111 1111 1111 1111
- **CVV**: Any 3 digits
- **Expiry**: Any future date
- **OTP**: 123456
- **UPI**: success@razorpay

See [PAYMENT_SETUP.md](PAYMENT_SETUP.md) for detailed payment guide.

---

## 🐳 Docker Quick Start (Alternative)

```powershell
# Copy environment file
copy .env.example .env

# Edit .env with your settings

# Start with Docker
docker-compose up -d

# Wait 10 seconds for services to start

# Run migrations
docker-compose exec web python manage.py migrate

# Create superuser
docker-compose exec web python manage.py createsuperuser

# Visit: http://localhost
```

---

## 📊 Admin Access

- **Wagtail Admin** (CMS): http://localhost:8000/admin/
  - Manage pages, products, images
  
- **Django Admin**: http://localhost:8000/django-admin/
  - Manage orders, coupons, categories

---

## 🔍 Useful Commands

```powershell
# Create new app
python manage.py startapp app_name

# Make migrations
python manage.py makemigrations

# Apply migrations
python manage.py migrate

# Collect static files
python manage.py collectstatic

# Create superuser
python manage.py createsuperuser

# Run shell
python manage.py shell

# Check for issues
python manage.py check

# Run tests
python manage.py test
```

---

## 🛠️ Troubleshooting

### Port 8000 already in use
```powershell
# Find process
netstat -ano | findstr :8000

# Kill process
taskkill /PID <PID_NUMBER> /F

# Or run on different port
python manage.py runserver 8080
```

### Module not found errors
```powershell
# Ensure virtual environment is activated
.venv\Scripts\activate

# Reinstall requirements
pip install -r requirements.txt
```

### Database errors
```powershell
# Reset database (WARNING: deletes all data)
del db.sqlite3
python manage.py migrate
python manage.py createsuperuser
```

### Static files not loading
```powershell
python manage.py collectstatic --clear
python manage.py collectstatic
```

---

## 📚 Next Steps

1. ✅ Add more products via Wagtail admin
2. ✅ Customize homepage content
3. ✅ Configure email settings for order confirmations
4. ✅ Set up Razorpay for real payments
5. ✅ Deploy to production (see README.md)

---

## 🎨 Customization

### Change Colors (templates/base.html)
```css
:root {
    --primary-color: #8B4513;    /* Your brand color */
    --secondary-color: #D2691E;
    --accent-color: #F4A460;
}
```

### Update Site Name
Edit `.env`:
```env
WAGTAIL_SITE_NAME=Your Store Name
```

### Add Logo
1. Upload logo to `static/images/logo.png`
2. Update `templates/base.html` navbar section

---

## 📞 Need Help?

- Check README.md for detailed documentation
- Check logs: `docker-compose logs` or `python manage.py runserver` output
- Open an issue on GitHub

**Happy Building! 🚀**
