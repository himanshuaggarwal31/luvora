# LUVORA - Premium E-commerce Platform

A complete, production-ready e-commerce platform built with **Django** and **Wagtail CMS**, featuring integrated payment processing, inventory management, and a modern Bootstrap-based UI.

![Python](https://img.shields.io/badge/Python-3.11-blue)
![Django](https://img.shields.io/badge/Django-4.2-green)
![Wagtail](https://img.shields.io/badge/Wagtail-5.2-teal)
![License](https://img.shields.io/badge/License-MIT-yellow)

## 🌟 Features

### Core Functionality
- **🛍️ Product Management**: Full CRUD with Wagtail CMS integration
- **🛒 Shopping Cart**: Session-based cart with real-time updates
- **💳 Payment Gateway**: Razorpay integration for secure payments
- **🎟️ Coupon System**: Percentage and fixed-amount discounts
- **📦 Order Management**: Complete order tracking and history
- **📊 Inventory Tracking**: Real-time stock management
- **🔍 Search & Filter**: Category-based product filtering
- **📱 Responsive Design**: Mobile-first Bootstrap 5 UI

### Technical Features
- **🗄️ Oracle Database Support**: Native Oracle DB integration (or PostgreSQL)
- **🐳 Docker Ready**: Complete containerization with Docker Compose
- **🔒 Security**: HTTPS, CSRF protection, secure payment verification
- **📧 Email Notifications**: Order confirmation emails
- **🔧 Environment-based Config**: 12-factor app methodology
- **📝 Comprehensive Logging**: Application and payment logging
- **🚀 Production Ready**: Gunicorn + Nginx deployment

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

- **Python 3.10+** (3.11 recommended)
- **pip** and **virtualenv**
- **Git**
- **Oracle Instant Client** (if using Oracle DB)
- **Docker & Docker Compose** (for containerized deployment)
- **Razorpay Account** (for payment processing)

---

## 🚀 Quick Start

### Option 1: Local Development (Virtual Environment)

```powershell
# Clone the repository
cd c:\Himanshu\REPOS\luvora

# Create virtual environment
python -m venv .venv
.venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Copy environment file
copy .env.example .env

# Edit .env with your configurations
# (Use notepad, VS Code, or any text editor)

# Run migrations
python manage.py migrate

# Create superuser
python manage.py createsuperuser

# Collect static files
python manage.py collectstatic

# Run development server
python manage.py runserver
```

Visit: **http://localhost:8000**

### Option 2: Docker Deployment (Recommended for Production)

```powershell
# Copy environment file
copy .env.example .env

# Edit .env with your configurations

# Run deployment script
.\deploy.bat

# Create superuser (in container)
docker-compose exec web python manage.py createsuperuser
```

Visit: **http://localhost**

---

## 🗄️ Database Setup

### PostgreSQL (Recommended for Development)

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

# Database (choose one)
# PostgreSQL
DB_ENGINE=django.db.backends.postgresql
DB_NAME=luvora_db
DB_USER=luvora_user
DB_PASSWORD=your_password
DB_HOST=localhost
DB_PORT=5432

# Oracle
# DB_ENGINE=django.db.backends.oracle
# DB_NAME=hostname:1521/service_name
# DB_USER=oracle_user
# DB_PASSWORD=oracle_password

# Razorpay
RAZORPAY_KEY_ID=rzp_test_xxxxxxxxxxxxx
RAZORPAY_KEY_SECRET=your_razorpay_secret
RAZORPAY_WEBHOOK_SECRET=your_webhook_secret

# Email
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_USE_TLS=True
EMAIL_HOST_USER=your-email@gmail.com
EMAIL_HOST_PASSWORD=your-app-password
DEFAULT_FROM_EMAIL=LUVORA <noreply@luvora.com>

# AWS S3 (Production Media Storage)
USE_S3=False
# AWS_ACCESS_KEY_ID=your_access_key
# AWS_SECRET_ACCESS_KEY=your_secret_key
# AWS_STORAGE_BUCKET_NAME=your_bucket_name
# AWS_S3_REGION_NAME=ap-south-1

# Site
SITE_URL=http://localhost:8000
WAGTAIL_SITE_NAME=LUVORA
```

### Razorpay Setup

1. Sign up at https://razorpay.com
2. Get API keys from Dashboard → Settings → API Keys
3. Add keys to `.env` file
4. For webhooks: Dashboard → Webhooks → Add webhook URL
   - URL: `https://yourdomain.com/shop/payment/callback/`
   - Events: `payment.authorized`, `payment.failed`

---

## 💻 Development Workflow

### Creating Products

1. Access Wagtail admin: http://localhost:8000/admin/
2. Login with superuser credentials
3. Navigate to Pages → Add child page → Product Index Page
4. Under Product Index, add Product Pages

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
│   ├── admin.py           # Admin configuration
│   └── urls.py            # Shop URLs
├── home/                   # Wagtail home app
│   └── models.py          # HomePage model
├── templates/              # HTML templates
│   ├── base.html          # Base template
│   ├── home/              # Home templates
│   └── shop/              # Shop templates
├── static/                 # Static files (CSS, JS, images)
├── media/                  # User-uploaded files
├── staticfiles/            # Collected static files
├── nginx/                  # Nginx configuration
├── requirements.txt        # Python dependencies
├── Dockerfile             # Docker configuration
├── docker-compose.yml     # Docker Compose setup
├── .env.example           # Environment variables template
└── README.md              # This file
```

---

## 🔌 API & Integrations

### Razorpay Integration

The platform uses Razorpay for payment processing:

1. **Order Creation**: When checkout is completed, a Razorpay order is created
2. **Payment Popup**: User completes payment in Razorpay modal
3. **Verification**: Payment signature is verified server-side
4. **Confirmation**: Order status is updated, stock reduced, email sent

### Webhook Handling

Add webhook endpoint in Razorpay dashboard:
- URL: `https://yourdomain.com/shop/payment/callback/`
- Secret: Set in `.env` as `RAZORPAY_WEBHOOK_SECRET`

---

## 🐛 Troubleshooting

### Common Issues

**1. cx_Oracle Import Error**
```bash
# Install Oracle Instant Client
# Add to PATH/LD_LIBRARY_PATH
# Reinstall cx_Oracle
pip uninstall cx_Oracle
pip install cx_Oracle
```

**2. Static Files Not Loading**
```bash
python manage.py collectstatic --clear
python manage.py collectstatic
```

**3. Migration Issues**
```bash
python manage.py makemigrations
python manage.py migrate --run-syncdb
```

**4. Razorpay Payment Fails**
- Check API keys in `.env`
- Verify webhook signature
- Check logs: `docker-compose logs web`

**5. Docker Port Already in Use**
```powershell
# Windows
netstat -ano | findstr :8000
taskkill /PID <PID> /F

# Or change port in docker-compose.yml
```

---

## 📞 Support & Contributing

- **Issues**: Open an issue on GitHub
- **Documentation**: See `/docs` folder
- **Contributing**: Pull requests welcome!

---

## 📄 License

This project is licensed under the MIT License.

---

## 🎯 Roadmap

- [ ] Email marketing integration
- [ ] Product reviews & ratings
- [ ] Wishlist functionality
- [ ] Multi-currency support
- [ ] Advanced analytics dashboard
- [ ] Mobile app (React Native)
- [ ] Inventory alerts
- [ ] Bulk product import

---

## 👥 Credits

Built with ❤️ for LUVORA by Himanshu

**Tech Stack:**
- Django 4.2
- Wagtail CMS 5.2
- Bootstrap 5
- Razorpay
- PostgreSQL/Oracle
- Docker & Nginx

---

**Happy Selling! 🚀**
