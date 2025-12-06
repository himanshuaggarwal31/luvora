# LUVORA - Complete Setup & Getting Started

## 🎯 What You've Built

Congratulations! You now have a **complete, production-ready e-commerce platform** with:

✅ Product management via Wagtail CMS  
✅ Shopping cart & checkout system  
✅ Razorpay payment integration  
✅ Coupon system  
✅ Order management  
✅ Inventory tracking  
✅ Responsive Bootstrap UI  
✅ Docker deployment ready  
✅ Oracle/PostgreSQL support  

---

## 🚀 Getting Started (5 Minutes)

### Step 1: Install Dependencies
```powershell
# Run the setup script
.\setup.bat

# OR manually:
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
copy .env.example .env
```

### Step 2: Configure Database
Edit `.env` file - Choose one:

**Option A: SQLite (Quickest)**
```env
DEBUG=True
SECRET_KEY=your-secret-key-change-in-production
DB_ENGINE=django.db.backends.sqlite3
DB_NAME=db.sqlite3
```

**Option B: PostgreSQL (Recommended)**
```env
DEBUG=True
SECRET_KEY=your-secret-key-change-in-production
DB_ENGINE=django.db.backends.postgresql
DB_NAME=luvora_db
DB_USER=postgres
DB_PASSWORD=your_password
DB_HOST=localhost
DB_PORT=5432
```

### Step 3: Initialize Database
```powershell
# Create database tables
python manage.py migrate

# Create admin user
python manage.py createsuperuser
# Enter: username, email, password

# Load sample products & coupons
python manage.py populate_sample_data
```

### Step 4: Run Server
```powershell
python manage.py runserver
```

🎉 **Done!** Open http://localhost:8000

---

## 🎨 Your First Steps

### 1. Access Admin Panels

**Wagtail CMS** (Manage Products & Pages)  
→ http://localhost:8000/admin/  
→ Login with superuser credentials  
→ Go to Pages → Shop → Add Product

**Django Admin** (Manage Orders & Coupons)  
→ http://localhost:8000/django-admin/  
→ View orders, create coupons, manage categories

### 2. Browse Shop
→ http://localhost:8000/shop/  
→ See sample products  
→ Add to cart  
→ Try coupon code: **WELCOME10**

### 3. Test Checkout
1. Add products to cart
2. Apply coupon: **WELCOME10** (10% off)
3. Go to checkout
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
