# LUVORA - Premium E-commerce Platform

A complete, production-ready e-commerce platform built with **Django 5.1** and **Wagtail CMS 6.4**, featuring integrated payment processing, automated invoice generation, email notifications, and a modern Bootstrap-based UI.

![Python](https://img.shields.io/badge/Python-3.12-blue)
![Django](https://img.shields.io/badge/Django-5.1-green)
![Wagtail](https://img.shields.io/badge/Wagtail-6.4-teal)
![License](https://img.shields.io/badge/License-MIT-yellow)

## 🌟 Features

### Core E-commerce
- **🛍️ Product Management**: Full CRUD with Wagtail CMS integration
- **🛒 Shopping Cart**: Session-based cart with real-time updates
- **💳 Payment Gateway**: Razorpay integration for secure payments (UPI, Cards, Net Banking)
- **📄 Invoice Generation**: Professional PDF invoices with ReportLab
- **📧 Email Notifications**: Automated order confirmations with invoice attachments
- **🎟️ Coupon System**: Percentage and fixed-amount discounts with validation
- **📦 Order Management**: Complete order tracking and status updates
- **📊 Inventory Tracking**: Real-time stock management with backorder support
- **🔍 Search & Filter**: Category-based product filtering
- **📱 Responsive Design**: Mobile-first Bootstrap 5 UI

### Technical Features
- **🗄️ Database Support**: SQLite (dev), PostgreSQL, Oracle
- **🐳 Docker Ready**: Complete containerization with Docker Compose
- **🔒 Security**: HTTPS, CSRF protection, secure payment verification
- **📝 Comprehensive Logging**: Application and payment logging
- **🚀 Production Ready**: Gunicorn + Nginx + WhiteNoise deployment
- **🔧 Environment-based Config**: 12-factor app methodology
- **🎨 CMS-Powered**: Wagtail CMS for content management

---

## 📋 Table of Contents

1. [Prerequisites](#prerequisites)
2. [Quick Start](#quick-start)
3. [Database Setup](#database-setup)
4. [Configuration](#configuration)
5. [Development Workflow](#development-workflow)
6. [Deployment](#deployment)
7. [Project Structure](#project-structure)
8. [API & Integrations](#api--integrations)
9. [Troubleshooting](#troubleshooting)

---

## 🔧 Prerequisites

- **Python 3.12+** (Python 3.14 not yet supported - see [PYTHON_VERSION_ISSUE.md](PYTHON_VERSION_ISSUE.md))
- **pip** and **virtualenv**
- **Git**
- **Oracle Instant Client** (optional, if using Oracle DB)
- **Docker & Docker Compose** (optional, for containerized deployment)
- **Razorpay Account** (optional, for payment processing - works in test mode without)

---

## 🚀 Quick Start

### Windows Quick Setup (Recommended)

```powershell
# Clone the repository
git clone https://github.com/himanshuaggarwal31/luvora.git
cd luvora

# Run the automated setup script
.\setup.bat

# The script will:
# - Create virtual environment with Python 3.12
# - Install all dependencies
# - Configure SQLite database
# - Run migrations
# - Create static directory
# - Prompt for superuser creation
```

After setup completes:
```powershell
# Activate virtual environment
.venv\Scripts\activate

# Create page structure (Home, Shop, Products)
python setup_pages.py

# Run development server
python manage.py runserver
```

Visit: **http://127.0.0.1:8000**

Admin Panel: **http://127.0.0.1:8000/admin/**

### Manual Setup

```powershell
# Create virtual environment
python -m venv .venv
.venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Copy environment file
copy .env.example .env

# Run migrations
python manage.py migrate

# Create superuser
python manage.py createsuperuser

# Create page structure
python setup_pages.py

# Run development server
python manage.py runserver
```

---

## 🗄️ Database Setup

### SQLite (Default - Recommended for Development)

No configuration needed! SQLite is pre-configured in `.env` and works out of the box.

```env
DB_ENGINE=django.db.backends.sqlite3
DB_NAME=db.sqlite3
```

### PostgreSQL (Recommended for Production)

```bash
# Install PostgreSQL
# Download from: https://www.postgresql.org/download/

# Create database
psql -U postgres
CREATE DATABASE luvora_db;
CREATE USER luvora_user WITH PASSWORD 'your_password';
GRANT ALL PRIVILEGES ON DATABASE luvora_db TO luvora_user;
\q
```

Update `.env`:
```env
DB_ENGINE=django.db.backends.postgresql
DB_NAME=luvora_db
DB_USER=luvora_user
DB_PASSWORD=your_password
DB_HOST=localhost
DB_PORT=5432
```

### Oracle Database

1. **Install Oracle Instant Client**
   - Download from: https://www.oracle.com/database/technologies/instant-client/downloads.html
   - Add to PATH (Windows) or LD_LIBRARY_PATH (Linux)

2. **Install cx_Oracle**
   ```bash
   pip install cx_Oracle
   ```

3. **Update .env**
   ```env
   DB_ENGINE=django.db.backends.oracle
   DB_NAME=hostname:1521/service_name
   DB_USER=your_oracle_user
   DB_PASSWORD=your_oracle_password
   ```

---

## ⚙️ Configuration

### Environment Variables (.env)

```env
# Django Settings
DEBUG=True
SECRET_KEY=your-secret-key-here
ALLOWED_HOSTS=localhost,127.0.0.1

# Database (SQLite - Default)
DB_ENGINE=django.db.backends.sqlite3
DB_NAME=db.sqlite3

# Database (PostgreSQL - Alternative)
# DB_ENGINE=django.db.backends.postgresql
# DB_NAME=luvora_db
# DB_USER=luvora_user
# DB_PASSWORD=your_password
# DB_HOST=localhost
# DB_PORT=5432

# Razorpay (Optional - Works in test mode without keys)
RAZORPAY_KEY_ID=
RAZORPAY_KEY_SECRET=
RAZORPAY_WEBHOOK_SECRET=

# Email (Console backend for development)
EMAIL_BACKEND=django.core.mail.backends.console.EmailBackend
DEFAULT_FROM_EMAIL=noreply@luvora.com

# Email (Gmail SMTP for production)
# EMAIL_BACKEND=django.core.mail.backends.smtp.EmailBackend
# EMAIL_HOST=smtp.gmail.com
# EMAIL_PORT=587
# EMAIL_USE_TLS=True
# EMAIL_HOST_USER=your-email@gmail.com
# EMAIL_HOST_PASSWORD=your-app-password

# Site
SITE_URL=http://127.0.0.1:8000
WAGTAIL_SITE_NAME=LUVORA
```

### Razorpay Setup

**For Development/Testing:**
- No API keys needed! The system works in test mode
- Checkout flow works, but no actual payment processing
- Perfect for testing the complete e-commerce flow

**For Production:**
1. Sign up at https://razorpay.com
2. Get API keys from Dashboard → Settings → API Keys
3. Add keys to `.env` file:
   ```env
   RAZORPAY_KEY_ID=rzp_test_xxxxxxxxxxxxx
   RAZORPAY_KEY_SECRET=your_razorpay_secret
   ```
4. For webhooks: Dashboard → Webhooks → Add webhook URL
   - URL: `https://yourdomain.com/shop/payment/callback/`
   - Events: `payment.authorized`, `payment.failed`

See [PAYMENT_SETUP.md](PAYMENT_SETUP.md) for detailed payment integration guide.

---

## 💻 Development Workflow

### Initial Page Setup

After installing, create the page structure:

```bash
python setup_pages.py
```

This creates:
- Home page (site root)
- Shop page (product listing)
- Sample products with images and pricing

### Creating Products via CMS

1. Access Wagtail admin: http://127.0.0.1:8000/admin/
2. Login with superuser credentials
3. Navigate to Pages → Shop
4. Click "Add child page" → Product
5. Fill in product details:
   - Title, SKU, Price
   - Description and images
   - Stock quantity
   - Category (optional)

### Testing Payments & Invoices

```bash
# Place an order through the website, then test invoice generation:
python manage.py test_invoice ORDER_ID_HERE --save

# Test email with invoice:
python manage.py test_invoice ORDER_ID_HERE --email
```

The invoice will be:
- Saved as PDF (with `--save`)
- Sent via email (with `--email`)
- Displayed in terminal if using console email backend

### Creating Categories

```bash
python manage.py shell
```

```python
from shop.models import Category

# Create main categories
Category.objects.create(name="Electronics", description="Electronic items")
Category.objects.create(name="Clothing", description="Fashion & apparel")
Category.objects.create(name="Home & Garden", description="Home essentials")
```

### Creating Coupons

1. Access Django admin: http://localhost:8000/django-admin/
2. Navigate to Shop → Coupons → Add Coupon
3. Set code, discount type, value, and validity period

### Running Tests

```bash
# Run all tests
python manage.py test

# Run specific app tests
python manage.py test shop

# With coverage
pip install coverage
coverage run --source='.' manage.py test
coverage report
```

---

## 🚀 Deployment

### Docker Deployment (Recommended)

```bash
# Production deployment
docker-compose -f docker-compose.yml up -d

# View logs
docker-compose logs -f

# Stop services
docker-compose down

# Rebuild after code changes
docker-compose build
docker-compose up -d
```

### Manual Deployment (VPS/Cloud)

1. **Server Setup**
   ```bash
   # Update system
   sudo apt update && sudo apt upgrade -y
   
   # Install dependencies
   sudo apt install python3.11 python3-pip nginx postgresql git -y
   ```

2. **Clone & Setup**
   ```bash
   git clone https://github.com/yourusername/luvora.git
   cd luvora
   python3 -m venv .venv
   source .venv/bin/activate
   pip install -r requirements.txt
   ```

3. **Configure Nginx**
   ```bash
   sudo cp nginx/nginx.conf /etc/nginx/sites-available/luvora
   sudo ln -s /etc/nginx/sites-available/luvora /etc/nginx/sites-enabled/
   sudo systemctl reload nginx
   ```

4. **Setup Systemd Service**
   ```bash
   sudo nano /etc/systemd/system/luvora.service
   ```
   
   ```ini
   [Unit]
   Description=LUVORA E-commerce
   After=network.target
   
   [Service]
   User=www-data
   WorkingDirectory=/path/to/luvora
   Environment="PATH=/path/to/luvora/.venv/bin"
   ExecStart=/path/to/luvora/.venv/bin/gunicorn --workers 3 --bind 0.0.0.0:8000 luvora_project.wsgi:application
   
   [Install]
   WantedBy=multi-user.target
   ```
   
   ```bash
   sudo systemctl start luvora
   sudo systemctl enable luvora
   ```

5. **SSL Certificate (Let's Encrypt)**
   ```bash
   sudo apt install certbot python3-certbot-nginx
   sudo certbot --nginx -d yourdomain.com
   ```

---

## 📁 Project Structure

```
luvora/
├── luvora_project/         # Main Django project
│   ├── settings.py         # Project settings
│   ├── urls.py             # URL configuration
│   ├── wsgi.py            # WSGI application
│   └── asgi.py            # ASGI application
├── shop/                   # Shop application
│   ├── models.py          # Product, Order, Coupon models
│   ├── views.py           # View logic
│   ├── forms.py           # Django forms
│   ├── cart.py            # Cart functionality
│   ├── invoice.py         # PDF invoice generation (NEW)
│   ├── email_utils.py     # Email sending utilities (NEW)
│   ├── admin.py           # Admin configuration
│   ├── urls.py            # Shop URLs
│   └── management/
│       └── commands/
│           ├── populate_sample_data.py
│           └── test_invoice.py  # Invoice testing tool (NEW)
├── home/                   # Wagtail home app
│   └── models.py          # HomePage model
├── templates/              # HTML templates
│   ├── base.html          # Base template
│   ├── home/              # Home templates
│   └── shop/              # Shop templates
│       ├── emails/        # Email templates (NEW)
│       │   ├── order_confirmation.html
│       │   ├── order_confirmation.txt
│       │   ├── order_status_update.html
│       │   └── order_status_update.txt
│       ├── product_detail.html
│       ├── product_list.html
│       ├── cart_detail.html
│       ├── checkout.html
│       └── payment.html
├── static/                 # Static files (CSS, JS, images)
├── media/                  # User-uploaded files
├── staticfiles/            # Collected static files
├── nginx/                  # Nginx configuration
├── setup_pages.py         # Page structure creation (NEW)
├── requirements.txt        # Python dependencies
├── setup.bat              # Windows setup script
├── Dockerfile             # Docker configuration
├── docker-compose.yml     # Docker Compose setup
├── .env                   # Environment variables
├── .env.example           # Environment template
├── PAYMENT_SETUP.md       # Payment integration guide (NEW)
├── INTEGRATION_COMPLETE.md # Quick reference (NEW)
├── PYTHON_VERSION_ISSUE.md # Python compatibility notes (NEW)
└── README.md              # This file
```

---

## 🔌 API & Integrations

### Razorpay Payment Integration

The platform uses Razorpay for secure payment processing:

1. **Test Mode** (No API keys): 
   - Checkout works, payment page shows test mode message
   - Perfect for development and testing

2. **Production Mode** (With API keys):
   - Order creation: Razorpay order created on checkout
   - Payment popup: User completes payment in Razorpay modal
   - Verification: Payment signature verified server-side
   - Confirmation: Order marked paid, stock reduced, email sent

### Invoice Generation

Automated PDF invoice generation with:
- Professional branding and styling
- Complete order details and customer info
- Itemized product list with SKU codes
- Price breakdown (subtotal, discount, shipping, tax, total)
- Payment information
- Attached to confirmation emails

### Email Notifications

Automated emails sent on:
- **Order Confirmation**: Sent when payment succeeds
  - Includes full order details
  - PDF invoice attached
  - Beautiful HTML template
- **Order Status Updates**: Sent when admin changes order status
  - Status change notification
  - Optional custom message

Email backends:
- **Development**: Console (emails printed to terminal)
- **Production**: SMTP (Gmail, SendGrid, etc.)

---

## 🐛 Troubleshooting

### Common Issues

**1. Python 3.14 Compatibility**
```bash
# Django/Wagtail not yet compatible with Python 3.14
# Use Python 3.12 or 3.13
# See PYTHON_VERSION_ISSUE.md for details
```

**2. ModuleNotFoundError: No module named 'django'**
```bash
# Virtual environment not activated
.venv\Scripts\activate  # Windows
source .venv/bin/activate  # Linux/Mac
```

**3. Static Files Not Loading**
```bash
python manage.py collectstatic --clear
python manage.py collectstatic
```

**4. Migration Issues**
```bash
python manage.py makemigrations
python manage.py migrate --run-syncdb
```

**5. Payment Test Mode Issues**
- Razorpay keys not needed for test mode
- Test mode shows on payment page automatically
- Check logs in terminal for details

**6. Invoice Generation Fails**
```bash
# Install PDF libraries
pip install reportlab weasyprint
```

**7. Email Not Sending**
```bash
# Check terminal for console backend output
# For production, verify SMTP settings in .env
# Test with: python manage.py test_invoice ORDER_ID --email
```

**8. No Products Showing**
```bash
# Run page setup script
python setup_pages.py

# Or create pages manually in Wagtail admin
```

---

## 📞 Support & Contributing

- **Issues**: Open an issue on [GitHub](https://github.com/himanshuaggarwal31/luvora/issues)
- **Documentation**: 
  - [PAYMENT_SETUP.md](PAYMENT_SETUP.md) - Payment integration guide
  - [INTEGRATION_COMPLETE.md](INTEGRATION_COMPLETE.md) - Feature overview
  - [PYTHON_VERSION_ISSUE.md](PYTHON_VERSION_ISSUE.md) - Python compatibility
  - [GETTING_STARTED.md](GETTING_STARTED.md) - Detailed setup guide
- **Contributing**: Pull requests welcome! See [CONTRIBUTING.md](CONTRIBUTING.md)

---

## 📄 License

This project is licensed under the MIT License. See [LICENSE](LICENSE) for details.

---

## 🎯 Roadmap

- [x] Razorpay payment integration
- [x] PDF invoice generation
- [x] Email notifications with attachments
- [x] Automated order processing
- [ ] Email marketing integration
- [ ] Product reviews & ratings
- [ ] Wishlist functionality
- [ ] Multi-currency support
- [ ] Advanced analytics dashboard
- [ ] Mobile app (React Native)
- [ ] Inventory alerts
- [ ] Bulk product import/export

---

## 👥 Credits

Built with ❤️ by Himanshu Aggarwal

**Tech Stack:**
- Django 5.1.15
- Wagtail CMS 6.4.2
- Python 3.12
- Bootstrap 5
- Razorpay
- ReportLab (PDF generation)
- SQLite/PostgreSQL/Oracle
- Docker & Nginx

---

**Happy Selling! 🚀**
