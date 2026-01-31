# 📚 LUVORA Complete Commands Reference

> **Complete command reference for running, managing, and deploying LUVORA**  
> Based on full development history and chat context

---

## Table of Contents
1. [Customer-Facing App (Django E-commerce)](#1-customer-facing-app-django-e-commerce)
2. [Backend Management](#2-backend-management)
3. [Static Catalog Version (S3-Ready)](#3-static-catalog-version-s3-ready)
4. [Development Workflows](#4-development-workflows)
5. [Testing & Debugging](#5-testing--debugging)
6. [Production Deployment](#6-production-deployment)
7. [Troubleshooting](#7-troubleshooting)

---

## 1. Customer-Facing App (Django E-commerce)

### Initial Setup (First Time Only)

```powershell
# Clone repository
git clone https://github.com/himanshuaggarwal31/luvora.git
cd luvora

# Run automated setup (Windows)
.\setup.bat

# Activate virtual environment
.venv\Scripts\activate

# Create page structure (Home, Shop, Products)
python setup_pages.py
```

### Starting the Development Server

```powershell
# Activate environment
.venv\Scripts\activate

# Start Django server
python manage.py runserver

# Server runs at: http://127.0.0.1:8000
```

**Customer Access Points:**
- Homepage: `http://127.0.0.1:8000/`
- Shop: `http://127.0.0.1:8000/shop/`
- Cart: `http://127.0.0.1:8000/shop/cart/`
- Checkout: `http://127.0.0.1:8000/shop/checkout/`

### Testing Payments Locally with ngrok

```powershell
# Terminal 1: Start Django server
.venv\Scripts\activate
python manage.py runserver

# Terminal 2: Start ngrok tunnel
.\ngrok http 8000

# Copy the ngrok HTTPS URL (e.g., https://abc123.ngrok-free.dev)
# Update .env file:
# ALLOWED_HOSTS=localhost,127.0.0.1,abc123.ngrok-free.dev
# CSRF_TRUSTED_ORIGINS=https://abc123.ngrok-free.dev
```

**Test Payment Flow:**
1. Access via ngrok URL: `https://abc123.ngrok-free.dev`
2. Add products to cart
3. Go to checkout
4. Complete payment via Razorpay
5. Check order confirmation email

---

## 2. Backend Management

### Django Admin (Order Management)

```powershell
# Access Django admin
# URL: http://127.0.0.1:8000/django-admin/

# Create superuser (first time)
python manage.py createsuperuser
# Username: admin
# Email: admin@luvora.com
# Password: (enter secure password)
```

**Django Admin Features:**
- **View Orders**: `/django-admin/shop/order/`
  - See all orders (paid, pending, processing)
  - Filter by status, date, customer
  - View order details, items, totals
  - Update order status (triggers email notification)

- **Manage Coupons**: `/django-admin/shop/coupon/`
  - Create discount coupons
  - Set percentage or fixed amount
  - Configure validity periods

### Wagtail CMS (Product & Page Management)

```powershell
# Access Wagtail admin
# URL: http://127.0.0.1:8000/admin/

# Use same superuser credentials as Django admin
```

**Wagtail Admin Features:**

#### Adding Products

1. Navigate to: **Pages → Shop → Add child page → Product**
2. Fill in product details:
   - **Title**: Product name (e.g., "Premium Cotton Bedsheet")
   - **Slug**: URL-friendly (e.g., "premium-cotton-bedsheet")
   - **Price**: Product price (e.g., 2999)
   - **Category**: Select or create category
   - **Stock**: Quantity available
   - **Image**: Upload product image
   - **Description**: Rich text product description
   - **SKU**: Stock keeping unit (optional)
3. Click **"Publish"**

#### Managing Pages

```powershell
# Create custom pages via Wagtail admin
# Examples:
# - About Us page
# - Contact page
# - Blog posts
# - Landing pages

# Or use the automated setup script:
python setup_pages.py
```

**Page Management:**
- **Pages → Add child page**: Create new pages
- **Edit**: Click page title to edit content
- **Publish/Unpublish**: Control page visibility
- **Reorder**: Drag and drop pages in tree view

### Checking Orders via Script

```powershell
# Quick order status check
python check_orders.py

# Output shows:
# - Recent 5 orders
# - Payment status (PAID/PENDING)
# - Razorpay transaction IDs
# - Order totals
# - Customer details
```

---

## 3. Static Catalog Version (S3-Ready)

### Local Testing (Development)

```powershell
# Navigate to static catalog folder
cd static-catalog

# Start Python HTTP server
python -m http.server 8080

# Access in browser:
# http://localhost:8080/index.html
```

**Important**: Always use `http://localhost:8080` (not `file://`) to ensure JavaScript can load products.json properly.

**Static Site Pages:**
- Homepage: `http://localhost:8080/index.html`
- Products: `http://localhost:8080/products.html`
- About: `http://localhost:8080/about.html`
- Contact: `http://localhost:8080/contact.html`

### Adding/Editing Products

```powershell
# Edit products file
code static-catalog/data/products.json

# Or use any text editor
notepad static-catalog/data/products.json
```

**Product JSON Structure:**
```json
{
  "id": 1,
  "name": "Premium Cotton Bedsheet",
  "slug": "premium-cotton-bedsheet",
  "price": 2999,
  "category": "Bedsheets",
  "image": "images/bedsheet1.jpg",
  "description": "Luxurious 100% cotton bedsheet with 400 thread count",
  "features": [
    "100% Pure Cotton",
    "400 Thread Count",
    "Machine Washable",
    "Available in Queen & King sizes"
  ],
  "inStock": true
}
```

**Adding a New Product:**
1. Open `static-catalog/data/products.json`
2. Copy an existing product object
3. Update all fields (id, name, price, etc.)
4. Add to array (don't forget comma separator)
5. Save file
6. Refresh browser to see changes

### Deploying to AWS S3

#### Option 1: PowerShell Deployment Script

```powershell
# Navigate to static-catalog
cd static-catalog

# Run deployment script
.\deploy.ps1

# Follow prompts:
# - Enter AWS Profile name (or press Enter for default)
# - Enter S3 bucket name
# - Confirm deployment

# Script automatically:
# - Syncs all files to S3
# - Sets correct content types
# - Configures public read access
# - Outputs website URL
```

#### Option 2: Manual AWS CLI Commands

```powershell
# Install AWS CLI first
# Download from: https://aws.amazon.com/cli/

# Configure AWS credentials
aws configure
# AWS Access Key ID: [your-key]
# AWS Secret Access Key: [your-secret]
# Default region: us-east-1
# Default output format: json

# Create S3 bucket
aws s3 mb s3://luvora-catalog

# Enable static website hosting
aws s3 website s3://luvora-catalog --index-document index.html --error-document index.html

# Upload files
cd static-catalog
aws s3 sync . s3://luvora-catalog --delete

# Set public access
aws s3api put-bucket-policy --bucket luvora-catalog --policy '{
  "Version": "2012-10-17",
  "Statement": [{
    "Sid": "PublicReadGetObject",
    "Effect": "Allow",
    "Principal": "*",
    "Action": "s3:GetObject",
    "Resource": "arn:aws:s3:::luvora-catalog/*"
  }]
}'

# Access your site:
# http://luvora-catalog.s3-website-us-east-1.amazonaws.com
```

#### Update S3 Content

```powershell
# After editing products.json or any files
cd static-catalog

# Sync changes to S3
aws s3 sync . s3://luvora-catalog --delete

# Or use PowerShell script
.\deploy.ps1
```

---

## 4. Development Workflows

### Database Management

```powershell
# Create new migrations (after model changes)
python manage.py makemigrations

# Apply migrations
python manage.py migrate

# Rollback migration
python manage.py migrate shop 0001  # Replace with migration number

# Reset database (careful - deletes all data!)
del db.sqlite3
python manage.py migrate
python setup_pages.py
python manage.py createsuperuser
```

### Static Files Management

```powershell
# Collect static files (for production)
python manage.py collectstatic --noinput

# Clear collected static files
rmdir /s /q staticfiles
mkdir staticfiles
```

### User Management

```powershell
# Create superuser
python manage.py createsuperuser

# Change user password
python manage.py changepassword username

# Create additional staff users via Django admin
# URL: http://127.0.0.1:8000/django-admin/auth/user/add/
```

### Environment Configuration

```powershell
# Copy environment template
copy .env.example .env

# Edit environment variables
code .env

# Key variables:
# DEBUG=True  # Set to False in production
# SECRET_KEY=your-secret-key
# ALLOWED_HOSTS=localhost,127.0.0.1
# RAZORPAY_KEY_ID=rzp_test_xxx
# RAZORPAY_KEY_SECRET=xxx
# EMAIL_HOST_USER=your-email@gmail.com
# EMAIL_HOST_PASSWORD=your-app-password
```

### Generate Production Secrets

```powershell
# Generate SECRET_KEY and WEBHOOK_SECRET
python generate_secrets.py

# Copy output to production .env file
```

---

## 5. Testing & Debugging

### Test Invoice Generation

```powershell
# Generate test invoice and send email
python manage.py test_invoice

# Creates sample order, generates PDF, sends email
# Check terminal for output and email inbox for delivery
```

### Test Webhook Signature

```powershell
# Verify webhook signature verification logic
python test_webhook.py

# Tests:
# - Signature generation
# - Signature verification
# - Invalid signature detection
```

### Check Order Status

```powershell
# View recent orders with payment status
python check_orders.py

# Shows:
# - Last 5 orders
# - Payment status (PAID/PENDING)
# - Razorpay IDs
# - Totals and customer info
```

### View Server Logs

```powershell
# Django development server logs (in terminal)
# Shows:
# - HTTP requests
# - Database queries (if DEBUG=True)
# - Error messages
# - Payment gateway responses

# Access logs via terminal where runserver is running
```

### Django Shell (Interactive Testing)

```powershell
# Open Django shell
python manage.py shell

# Example commands:
>>> from shop.models import Order, Product
>>> Order.objects.all()  # List all orders
>>> Order.objects.filter(status='paid').count()  # Count paid orders
>>> Product.objects.filter(stock__gt=0)  # Products in stock
>>> from shop.cart import Cart
>>> # Test cart operations
```

---

## 6. Production Deployment

### Railway.app Deployment

```powershell
# Prerequisites
# 1. Generate secrets
python generate_secrets.py

# 2. Ensure all files committed to GitHub
git add .
git commit -m "Prepare for Railway deployment"
git push origin main

# 3. Deploy on Railway.app
# - Visit https://railway.app
# - Login with GitHub
# - New Project → Deploy from GitHub repo
# - Select luvora repository
# - Add PostgreSQL database
# - Configure environment variables (see below)
```

**Railway Environment Variables:**
```env
# Django Settings
DEBUG=False
SECRET_KEY=<generated-secret-from-generate_secrets.py>
ALLOWED_HOSTS=.railway.app,your-custom-domain.com
CSRF_TRUSTED_ORIGINS=https://your-app.railway.app,https://your-custom-domain.com

# Database (automatically set by Railway PostgreSQL)
# DATABASE_URL=postgresql://...  # Railway provides this

# Razorpay (Production Keys)
RAZORPAY_KEY_ID=rzp_live_xxxxxxxxxxxxx
RAZORPAY_KEY_SECRET=xxxxxxxxxxxxxxxxxxxxx
RAZORPAY_WEBHOOK_SECRET=<generated-secret>

# Email (Gmail SMTP)
EMAIL_BACKEND=django.core.mail.backends.smtp.EmailBackend
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_USE_TLS=True
EMAIL_HOST_USER=your-email@gmail.com
EMAIL_HOST_PASSWORD=your-app-password
DEFAULT_FROM_EMAIL=LUVORA <your-email@gmail.com>

# Static/Media (Optional - for S3)
USE_S3=False
```

**Post-Deployment Commands (Railway CLI):**
```powershell
# Install Railway CLI
npm install -g @railway/cli

# Login
railway login

# Link to project
railway link

# Run migrations
railway run python manage.py migrate

# Create superuser
railway run python manage.py createsuperuser

# Collect static files
railway run python manage.py collectstatic --noinput

# View logs
railway logs
```

### Render.com Deployment

```powershell
# Similar to Railway, but uses render.yaml or Web UI
# See DEPLOYMENT_GUIDE.md for detailed Render setup

# Key files needed:
# - Procfile
# - build.sh
# - requirements.txt
# - runtime.txt
```

### Heroku Deployment

```powershell
# Install Heroku CLI
# Download from: https://devcenter.heroku.com/articles/heroku-cli

# Login to Heroku
heroku login

# Create new app
heroku create luvora-prod

# Add PostgreSQL addon
heroku addons:create heroku-postgresql:mini

# Set environment variables
heroku config:set DEBUG=False
heroku config:set SECRET_KEY=your-secret-key
heroku config:set RAZORPAY_KEY_ID=rzp_live_xxx
# ... (set all other env vars)

# Deploy
git push heroku main

# Run migrations
heroku run python manage.py migrate

# Create superuser
heroku run python manage.py createsuperuser

# Open app
heroku open

# View logs
heroku logs --tail
```

---

## 7. Troubleshooting

### Common Issues & Solutions

#### Issue: "No module named 'django'"
```powershell
# Solution: Activate virtual environment
.venv\Scripts\activate
pip install -r requirements.txt
```

#### Issue: "CSRF verification failed"
```powershell
# Solution: Update .env with correct domains
# ALLOWED_HOSTS=localhost,127.0.0.1,your-ngrok-url.ngrok-free.dev
# CSRF_TRUSTED_ORIGINS=https://your-ngrok-url.ngrok-free.dev
```

#### Issue: Static files not loading (404 errors)
```powershell
# Development: Django serves static files automatically if DEBUG=True
# Production: Run collectstatic
python manage.py collectstatic --noinput
```

#### Issue: Products not showing in Chrome (static catalog)
```powershell
# Problem: Opening file:// instead of http://
# Solution: Use Python HTTP server
cd static-catalog
python -m http.server 8080
# Then open: http://localhost:8080/index.html
```

#### Issue: Payment webhook not working
```powershell
# Check webhook signature verification
python test_webhook.py

# Verify .env settings:
# RAZORPAY_WEBHOOK_SECRET=your-secret
# ALLOWED_HOSTS includes ngrok domain
# CSRF_TRUSTED_ORIGINS includes https://ngrok-url

# Check ngrok is running and forwarding to port 8000
.\ngrok http 8000
```

#### Issue: Emails not sending
```powershell
# Development: Check console output (console backend)
# Production: Verify Gmail settings in .env
# EMAIL_HOST_USER=your-email@gmail.com
# EMAIL_HOST_PASSWORD=your-app-password  # Not regular password!

# Generate Gmail App Password:
# https://myaccount.google.com/apppasswords
```

#### Issue: "Python 3.14 not compatible"
```powershell
# Solution: Use Python 3.12 or 3.13
# Download Python 3.12 from python.org
# Delete .venv and recreate:
rmdir /s /q .venv
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
```

#### Issue: Database locked (SQLite)
```powershell
# Solution: Close all Django shells and admin pages
# Restart server:
python manage.py runserver
```

#### Issue: Port 8000 already in use
```powershell
# Find process using port 8000
netstat -ano | findstr :8000

# Kill process (replace PID with actual number)
taskkill /PID <PID> /F

# Or use different port
python manage.py runserver 8001
```

---

## Quick Reference Cheat Sheet

### Most Common Commands

```powershell
# 🚀 START APP
.venv\Scripts\activate
python manage.py runserver

# 👤 ADMIN ACCESS
# Django: http://127.0.0.1:8000/django-admin/
# Wagtail: http://127.0.0.1:8000/admin/

# 📦 STATIC CATALOG
cd static-catalog
python -m http.server 8080
# Visit: http://localhost:8080/index.html

# 🧪 TESTING
python check_orders.py           # Check orders
python manage.py test_invoice     # Test invoice/email
python test_webhook.py            # Test webhook

# 🗄️ DATABASE
python manage.py makemigrations
python manage.py migrate
python manage.py createsuperuser

# 🔧 DEVELOPMENT
python manage.py shell            # Django shell
python setup_pages.py             # Setup pages
python generate_secrets.py        # Generate secrets

# 🚢 DEPLOYMENT
python manage.py collectstatic    # Collect static files
git push heroku main              # Deploy to Heroku
railway up                        # Deploy to Railway
```

### File Locations

```
luvora/
├── manage.py                    # Django management
├── .env                         # Environment variables
├── db.sqlite3                   # Database (local)
├── requirements.txt             # Dependencies
├── setup_pages.py               # Page setup script
├── check_orders.py              # Order checker
├── test_webhook.py              # Webhook tester
├── generate_secrets.py          # Secret generator
├── shop/
│   ├── models.py                # Order, Product models
│   ├── views.py                 # Views
│   ├── urls.py                  # URL patterns
│   └── admin.py                 # Django admin config
├── static-catalog/              # Static version (S3)
│   ├── index.html               # Homepage
│   ├── products.html            # Product catalog
│   ├── data/products.json       # Product data
│   ├── deploy.ps1               # S3 deploy script
│   └── README.md                # S3 deployment guide
└── templates/
    └── shop/                    # Django templates
```

---

## Additional Resources

- **Full Documentation**: [README.md](README.md)
- **Quick Start**: [GETTING_STARTED.md](GETTING_STARTED.md)
- **Deployment Guide**: [DEPLOYMENT_GUIDE.md](DEPLOYMENT_GUIDE.md)
- **Quick Deploy**: [QUICK_DEPLOY.md](QUICK_DEPLOY.md)
- **Static Catalog**: [static-catalog/README.md](static-catalog/README.md)
- **Project Structure**: [PROJECT_STRUCTURE.md](PROJECT_STRUCTURE.md)

---

## Support & Contribution

- **Issues**: Report bugs on GitHub Issues
- **Documentation**: See DOCS_INDEX.md for all docs
- **Contributing**: See CONTRIBUTING.md for guidelines

---

**Last Updated**: January 2026  
**Version**: 1.1.0  
**Python**: 3.12 (Required)  
**Django**: 5.1.15  
**Wagtail**: 6.4.2
