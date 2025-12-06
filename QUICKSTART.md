# LUVORA Quick Setup Guide

## 🚀 5-Minute Quick Start

### Step 1: Setup Environment

```powershell
# Navigate to project
cd c:\Himanshu\REPOS\luvora

# Create virtual environment
python -m venv .venv
.venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

### Step 2: Configure Database

**Option A: SQLite (Easiest - for testing)**
```powershell
# Copy .env file
copy .env.example .env

# Edit .env - Use SQLite (default)
# DB_ENGINE=django.db.backends.sqlite3
# DB_NAME=db.sqlite3
```

**Option B: PostgreSQL (Recommended)**
```powershell
# Install PostgreSQL from https://www.postgresql.org/download/

# Create database
psql -U postgres
CREATE DATABASE luvora_db;
\q

# Update .env
# DB_ENGINE=django.db.backends.postgresql
# DB_NAME=luvora_db
# DB_USER=postgres
# DB_PASSWORD=your_password
```

### Step 3: Initialize Database

```powershell
# Run migrations
python manage.py migrate

# Create superuser
python manage.py createsuperuser
# Enter username, email, password when prompted

# Create logs directory
mkdir logs
```

### Step 4: Run Development Server

```powershell
# Start server
python manage.py runserver

# Open browser: http://localhost:8000
```

---

## 📝 Initial Setup

### Create Home Page (Wagtail)

1. Visit: http://localhost:8000/admin/
2. Login with superuser credentials
3. Click "Pages" → "Welcome to your new Wagtail site!"
4. Click "..." → "Delete"
5. Click "Pages" → "Home" → "Add child page" → "Home Page"
6. Fill in hero section and save
7. Set as homepage if prompted

### Create Product Index

1. In Wagtail admin: Pages → Home → Add child page → Product Index Page
2. Title: "Shop" or "Products"
3. Save and publish

### Add First Product

1. Pages → Shop → Add child page → Product
2. Fill in:
   - Title: Your product name
   - SKU: Unique code (e.g., "PROD001")
   - Price: Product price
   - Category: Create one first (see below)
   - Stock quantity: Available units
   - Short description
   - Full description
   - Upload image
3. Check "Is available" and "Live" checkbox
4. Save and publish

### Create Categories

```powershell
python manage.py shell
```

```python
from shop.models import Category

# Create categories
electronics = Category.objects.create(
    name="Electronics",
    description="Electronic devices and accessories"
)

fashion = Category.objects.create(
    name="Fashion",
    description="Clothing and accessories"
)

print("Categories created!")
exit()
```

### Create Test Coupon

1. Visit: http://localhost:8000/django-admin/
2. Shop → Coupons → Add Coupon
3. Fill in:
   - Code: WELCOME10
   - Discount type: Percentage
   - Value: 10
   - Valid from: Today's date
   - Valid to: Future date
   - Active: ✓
4. Save

---

## 🧪 Test the Application

### Test Products
1. Visit: http://localhost:8000/shop/
2. Browse products
3. Click on a product to view details

### Test Shopping Cart
1. Add product to cart
2. Update quantity
3. Apply coupon code: WELCOME10
4. Proceed to checkout

### Test Checkout (Without Payment)
1. Fill in shipping information
2. Submit form
3. You'll see payment page (Razorpay test mode if not configured)

---

## 💳 Configure Razorpay (Optional)

### Get Razorpay Test Keys

1. Sign up at: https://razorpay.com
2. Go to Dashboard → Settings → API Keys
3. Click "Generate Test Key"
4. Copy Key ID and Key Secret

### Update .env

```env
RAZORPAY_KEY_ID=rzp_test_xxxxxxxxxxxxx
RAZORPAY_KEY_SECRET=your_secret_key_here
```

### Test Payment

1. Restart server: `python manage.py runserver`
2. Go through checkout process
3. Use Razorpay test cards:
   - Card: 4111 1111 1111 1111
   - CVV: Any 3 digits
   - Expiry: Any future date

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
