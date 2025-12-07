# LUVORA Project Structure

```
luvora/
│
├── luvora_project/                 # Main Django project
│   ├── __init__.py
│   ├── settings.py                 # Project settings (environment-based)
│   ├── urls.py                     # Main URL configuration
│   ├── wsgi.py                     # WSGI application
│   └── asgi.py                     # ASGI application
│
├── shop/                           # E-commerce application
│   ├── management/
│   │   └── commands/
│   │       ├── populate_sample_data.py  # Sample data loader
│   │       └── test_invoice.py          # Invoice testing tool
│   ├── migrations/                 # Database migrations
│   ├── __init__.py
│   ├── admin.py                    # Django admin configuration
│   ├── apps.py                     # App configuration
│   ├── cart.py                     # Shopping cart logic
│   ├── context_processors.py      # Template context processors
│   ├── forms.py                    # Django forms
│   ├── models.py                   # Data models (Product, Order, Coupon)
│   ├── urls.py                     # Shop URL patterns
│   ├── views.py                    # View controllers
│   ├── invoice.py                  # PDF invoice generation
│   └── email_utils.py              # Email notification system
│
├── home/                           # Wagtail home app
│   ├── migrations/
│   ├── __init__.py
│   ├── apps.py
│   └── models.py                   # HomePage model
│
├── templates/                      # HTML templates
│   ├── base.html                   # Base template
│   ├── home/
│   │   └── home_page.html         # Homepage template
│   └── shop/
│       ├── product_list.html       # Product listing
│       ├── product_detail.html     # Product detail
│       ├── cart_detail.html        # Shopping cart
│       ├── checkout.html           # Checkout form
│       ├── payment.html            # Payment page
│       ├── order_success.html      # Order confirmation
│       ├── payment_failed.html     # Payment failure
│       ├── category_detail.html    # Category view
│       └── emails/                 # Email templates
│           ├── order_confirmation.html      # Order email (HTML)
│           ├── order_confirmation.txt       # Order email (text)
│           ├── order_status_update.html     # Status email (HTML)
│           └── order_status_update.txt      # Status email (text)
│
├── static/                         # Static files (CSS, JS, images)
│   ├── css/
│   ├── js/
│   └── images/
│
├── media/                          # User-uploaded files
│   ├── images/                     # Product images
│   └── documents/                  # Documents
│
├── staticfiles/                    # Collected static files (production)
│
├── logs/                           # Application logs
│   └── django.log
│
├── nginx/                          # Nginx configuration
│   └── nginx.conf                  # Nginx config file
│
├── .venv/                          # Virtual environment (not in git)
│
├── requirements.txt                # Python dependencies
├── .env                            # Environment variables (not in git)
├── .env.example                    # Environment template
├── .gitignore                      # Git ignore rules
│
├── Dockerfile                      # Docker image definition
├── docker-compose.yml              # Docker Compose configuration
├── deploy.sh                       # Linux/Mac deployment script
├── deploy.bat                      # Windows deployment script
├── setup.sh                        # Linux/Mac setup script
├── setup.bat                       # Windows setup script
│
├── manage.py                       # Django management script
├── setup_pages.py                  # Automated page structure setup
│
├── README.md                       # Main documentation
├── QUICKSTART.md                   # Quick setup guide
├── GETTING_STARTED.md              # First steps guide
├── CHANGELOG.md                    # Version history
├── CONTRIBUTING.md                 # Contribution guidelines
├── SECURITY.md                     # Security policy
├── PAYMENT_SETUP.md                # Payment integration guide
├── INTEGRATION_COMPLETE.md         # Integration summary
├── PYTHON_VERSION_ISSUE.md         # Python compatibility notes
├── LICENSE                         # MIT license
└── PROJECT_STRUCTURE.md           # This file
```

## Key Directories Explained

### `/luvora_project` - Main Project
- **settings.py**: Environment-based configuration (database, security, apps)
- **urls.py**: Root URL routing (includes shop and Wagtail URLs)
- **wsgi.py/asgi.py**: Server interface for deployment

### `/shop` - E-commerce Logic
- **models.py**: Product, Order, Coupon, Category models
- **views.py**: Business logic (cart, checkout, payment)
- **cart.py**: Session-based shopping cart implementation
- **invoice.py**: PDF invoice generation with ReportLab
- **email_utils.py**: Email notifications (order confirmations, status updates)
- **forms.py**: User input forms (checkout, coupon)
- **admin.py**: Django admin customization

### `/home` - CMS Pages
- **models.py**: Wagtail page models (HomePage, etc.)
- Used for content-managed pages

### `/templates` - HTML Templates
- **base.html**: Master template (navbar, footer, shared styles)
- **shop/**: Product and cart templates
- **home/**: Homepage template

### `/static` - Static Assets
- CSS, JavaScript, images
- Collected to `/staticfiles` in production

### `/media` - User Uploads
- Product images uploaded via CMS
- Served by Nginx in production

### `/nginx` - Web Server Config
- Reverse proxy configuration
- Static/media file serving
- Security headers

## Configuration Files

| File | Purpose |
|------|---------|
| `requirements.txt` | Python package dependencies |
| `.env` | Environment variables (secrets, config) |
| `Dockerfile` | Container image definition |
| `docker-compose.yml` | Multi-container orchestration |
| `.gitignore` | Files to exclude from Git |

## Entry Points

| Command | Purpose |
|---------|---------|
| `python manage.py runserver` | Development server |
| `gunicorn luvora_project.wsgi` | Production server |
| `python manage.py migrate` | Database migrations |
| `python manage.py createsuperuser` | Create admin user |
| `python manage.py populate_sample_data` | Load test data |

## Important Notes

1. **Never commit `.env`** - Contains secrets
2. **Virtual environment** (`.venv`) - Local to each developer
3. **Migrations** - Track in Git, run before deployment
4. **Static files** - Collect before production deploy
5. **Media files** - Backup regularly, use S3 in production

## Data Flow

1. **Request** → Nginx → Gunicorn → Django
2. **Static files** → Nginx (direct serve)
3. **Media files** → Nginx (or S3 in production)
4. **Database** → PostgreSQL/Oracle
5. **Sessions** → Database (cart stored in session)
6. **Payments** → Razorpay API → Webhook callback

## Development Workflow

```
1. Edit code in /shop or /templates
2. Test locally: python manage.py runserver
3. Make migrations if models changed
4. Commit changes to Git
5. Deploy: docker-compose up -d
```

## Production Deployment

```
1. Set DEBUG=False in .env
2. Configure production database
3. Set up Razorpay production keys
4. Configure S3 for media (optional)
5. Build Docker image
6. Deploy with docker-compose or K8s
7. Set up SSL (Let's Encrypt)
8. Configure backups
```

---

For more details, see **README.md** and **QUICKSTART.md**
