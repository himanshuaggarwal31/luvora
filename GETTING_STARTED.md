# LUVORA - Complete Setup & Getting Started

## 🎯 What You've Built

Congratulations! You now have a **complete, production-ready e-commerce platform** with:

✅ Product management via Wagtail CMS  
✅ Shopping cart & checkout system  
✅ Razorpay payment integration (test mode ready)
✅ **Professional PDF invoice generation**
✅ **Automated email notifications with attachments**
✅ Coupon system with validation
✅ Order management & tracking 
✅ Real-time inventory tracking
✅ Responsive Bootstrap 5 UI  
✅ Docker deployment ready  
✅ SQLite/PostgreSQL/Oracle support

---

## 🚀 Getting Started (3 Minutes - Windows)

### Automated Setup (Recommended)

```powershell
# Clone repository
git clone https://github.com/himanshuaggarwal31/luvora.git
cd luvora

# Run setup script (installs everything automatically)
.\setup.bat

# After setup completes:
.venv\Scripts\activate
python setup_pages.py
python manage.py runserver
```

🎉 **Done!** Open http://127.0.0.1:8000

---

## 📝 Manual Setup (Alternative)

### Step 1: Python Environment

**Important**: Use Python 3.12 (Python 3.14 not yet supported by Django/Wagtail)

```powershell
# Check Python version
python --version  # Should show 3.12.x

# Create virtual environment
python -m venv .venv
.venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

### Step 2: Database Configuration

**SQLite (Default - No setup needed!)**  
The `.env` file is already configured for SQLite:
```env
DB_ENGINE=django.db.backends.sqlite3
DB_NAME=db.sqlite3
```

### Step 3: Initialize Application
```powershell
# Run migrations
python manage.py migrate

# Create superuser (admin account)
python manage.py createsuperuser
# Enter: username, email, password

# Create page structure and sample products
python setup_pages.py
```

The `setup_pages.py` script creates:
- Home page (site root)
- Shop page (`/shop/`)
- 2 sample products with images

### Step 4: Start Server
```powershell
python manage.py runserver
```

🎉 **Application ready!**

**Visit:**
- **Shop**: http://127.0.0.1:8000/shop/
- **Admin**: http://127.0.0.1:8000/admin/
- **Django Admin**: http://127.0.0.1:8000/django-admin/

---

## 🎨 Your First Steps

### 1. Access Admin Panels

**Wagtail CMS** (Content & Products)  
→ http://127.0.0.1:8000/admin/  
→ Manage pages, products, images  
→ Pages → Shop → Add child page → Product

**Django Admin** (Orders & Settings)  
→ http://127.0.0.1:8000/django-admin/  
→ View orders, create coupons, manage categories

### 2. Browse the Shop
→ http://127.0.0.1:8000/shop/  
→ View sample products  
→ Clean URLs: `/shop/product-name/`  
→ Responsive design for all devices

### 3. Test the Complete Flow
1. **Add products** to cart
2. **View cart**: http://127.0.0.1:8000/shop/cart/
3. **Go to checkout**: http://127.0.0.1:8000/shop/checkout/
4. **Fill shipping details**
5. **Payment page**: Works in test mode (no API keys needed)
6. **Check terminal**: Email with invoice appears in console
4. Fill shipping info
5. Payment page (test mode if Razorpay not configured)

---

## 💳 Setup Razorpay (Optional)

1. **Sign up**: https://razorpay.com
2. **Get Test Keys**: Dashboard → Settings → API Keys
3. **Update .env**:
```env
RAZORPAY_KEY_ID=rzp_test_xxxxxxxxxxxxx
RAZORPAY_KEY_SECRET=your_secret_key_here
```
4. **Test Payment**: Use test card `4111 1111 1111 1111`

---

## 📝 Managing Content

### Add Products (CMS)
1. Wagtail Admin → Pages → Shop
2. Add child page → Product
3. Fill: Title, SKU, Price, Description, Image
4. Check "Live" and "Is available"
5. Publish

### Create Categories
```python
# In shell: python manage.py shell
from shop.models import Category

Category.objects.create(
    name="Your Category",
    description="Category description"
)
```

### Create Coupons
Django Admin → Shop → Coupons → Add Coupon
- Code: SUMMER20
- Type: Percentage
- Value: 20
- Valid dates
- Save

---

## 🐳 Docker Deployment

```powershell
# Setup environment
copy .env.example .env
# Edit .env with production settings

# Deploy
.\deploy.bat

# Create superuser
docker-compose exec web python manage.py createsuperuser

# Load sample data
docker-compose exec web python manage.py populate_sample_data
```

Visit: http://localhost

---

## 📊 Sample Data Included

After running `python manage.py populate_sample_data`:

**Products:**
- Wireless Bluetooth Headphones (₹2,499)
- Cotton T-Shirt (₹499)
- Smart LED Desk Lamp (₹1,299)
- Python Programming Book (₹599)
- Yoga Mat (₹899)

**Coupons:**
- `WELCOME10` - 10% off
- `SAVE500` - ₹500 off on orders above ₹2,000
- `FLASH25` - 25% off (limited 100 uses)

**Categories:**
- Electronics
- Fashion
- Home & Living
- Books
- Sports

---

## 🔧 Customization

### Change Colors
Edit `templates/base.html`:
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
1. Place logo at `static/images/logo.png`
2. Update navbar in `templates/base.html`

---

## 📁 Project Structure

```
luvora/
├── shop/               # E-commerce logic
│   ├── models.py       # Product, Order, Coupon
│   ├── views.py        # Cart, Checkout, Payment
│   └── cart.py         # Shopping cart
├── templates/          # HTML templates
│   ├── base.html       # Master template
│   └── shop/           # Product pages
├── static/             # CSS, JS, images
├── media/              # Uploaded images
├── .env               # Configuration
└── manage.py          # Django commands
```

Full details: **PROJECT_STRUCTURE.md**

---

## 🎓 Learning Resources

### Documentation
- **README.md** - Complete guide
- **QUICKSTART.md** - Quick setup
- **PROJECT_STRUCTURE.md** - Code organization
- **SECURITY.md** - Security best practices

### Django/Wagtail
- Django Docs: https://docs.djangoproject.com
- Wagtail Docs: https://docs.wagtail.org
- Razorpay Docs: https://razorpay.com/docs/

---

## 🛠️ Useful Commands

```powershell
# Development
python manage.py runserver          # Start server
python manage.py makemigrations     # Create migrations
python manage.py migrate            # Apply migrations
python manage.py createsuperuser    # Create admin
python manage.py shell              # Python shell

# Data
python manage.py populate_sample_data        # Load test data
python manage.py populate_sample_data --clear  # Clear & reload

# Production
python manage.py collectstatic      # Collect static files
python manage.py check --deploy     # Check production readiness

# Docker
docker-compose up -d                # Start containers
docker-compose logs -f              # View logs
docker-compose down                 # Stop containers
docker-compose exec web python manage.py migrate  # Run in container
```

---

## 🐛 Troubleshooting

### Port already in use
```powershell
netstat -ano | findstr :8000
taskkill /PID <PID> /F
```

### Module not found
```powershell
.venv\Scripts\activate
pip install -r requirements.txt
```

### Database errors
```powershell
# Reset database (WARNING: deletes data)
del db.sqlite3
python manage.py migrate
```

### Static files not loading
```powershell
python manage.py collectstatic --clear
```

---

## 🚀 Deployment Checklist

Before going live:

- [ ] Update `.env` with production values
- [ ] Set `DEBUG=False`
- [ ] Configure production database (PostgreSQL/Oracle)
- [ ] Set up Razorpay production keys
- [ ] Configure email (SMTP)
- [ ] Set up SSL certificate (Let's Encrypt)
- [ ] Configure media storage (S3/Object Storage)
- [ ] Set up backups
- [ ] Test payment flow end-to-end
- [ ] Set up monitoring (Sentry)

See **README.md** → Deployment section

---

## 📈 Next Steps

1. **Customize Design**
   - Update colors and branding
   - Add your logo
   - Customize templates

2. **Add Products**
   - Upload real products via CMS
   - Add product images
   - Set up categories

3. **Configure Payments**
   - Set up Razorpay production account
   - Test payment flow
   - Configure webhooks

4. **Marketing**
   - Create coupons for promotions
   - Set up email notifications
   - Add SEO metadata

5. **Deploy**
   - Choose hosting (Oracle Cloud, DigitalOcean, AWS)
   - Deploy with Docker
   - Set up SSL
   - Go live! 🎉

---

## 💡 Pro Tips

1. **Backup regularly**: Database and media files
2. **Test payments** thoroughly before going live
3. **Monitor logs** for errors and issues
4. **Use sample data** to demo to clients
5. **Read SECURITY.md** before production deployment
6. **Join communities**: Django, Wagtail, Python forums
7. **Version control**: Commit code to Git regularly

---

## 🆘 Need Help?

- **Documentation**: Read README.md and QUICKSTART.md
- **Logs**: Check `logs/django.log` for errors
- **Community**: Stack Overflow, Django forum
- **Issues**: Open issue on GitHub

---

## 🎉 You're Ready!

You now have a **fully functional e-commerce platform**. Start customizing, add your products, and launch your store!

**Good luck with your business! 🚀**

---

## Quick Reference Card

| Task | Command |
|------|---------|
| Start server | `python manage.py runserver` |
| Add products | Go to http://localhost:8000/admin/ |
| View orders | Go to http://localhost:8000/django-admin/ |
| Test coupons | Use `WELCOME10`, `SAVE500`, `FLASH25` |
| Shop frontend | http://localhost:8000/shop/ |
| Reset database | `del db.sqlite3` + `python manage.py migrate` |
| Docker deploy | `.\deploy.bat` |
| Get help | Check README.md |

---

**Built with ❤️ for LUVORA**
