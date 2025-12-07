# 🚀 Quick Deployment Guide - Railway.app

## ⏱️ Time Required: 20-30 minutes

---

## 📝 Step-by-Step Instructions

### 1️⃣ Generate Production Secrets (1 min)

```bash
python generate_secrets.py
```

**Save these values** - you'll need them in Step 5!

---

### 2️⃣ Setup Railway.app (3 min)

1. Go to **https://railway.app/**
2. Click **"Login"** → Sign in with **GitHub**
3. Click **"New Project"**
4. Select **"Deploy from GitHub repo"**
5. Choose **`himanshuaggarwal31/luvora`**
6. Click **"Deploy Now"**

⏳ Railway will start building (it will fail - that's normal!)

---

### 3️⃣ Add PostgreSQL Database (2 min)

1. In your Railway project dashboard:
   - Click **"+ New"** button
   - Select **"Database"** → **"Add PostgreSQL"**
2. Wait for PostgreSQL to provision (~30 seconds)

✅ Database connection is automatically configured!

---

### 4️⃣ Get Your App Domain (1 min)

1. Click on your **web service** (not database)
2. Go to **"Settings"** tab
3. Scroll to **"Networking"**
4. Click **"Generate Domain"**
5. **Copy your domain**: `something-random.railway.app`

---

### 5️⃣ Configure Environment Variables (5 min)

Click on **web service** → **"Variables"** tab → **"RAW Editor"**

Paste this (replace values in `< >`):

```bash
# Django Core
DEBUG=False
SECRET_KEY=<paste-from-step-1>
ALLOWED_HOSTS=<your-domain>.railway.app
CSRF_TRUSTED_ORIGINS=https://<your-domain>.railway.app

# Razorpay - TEST MODE (for testing)
RAZORPAY_KEY_ID=rzp_test_Roi0LWTxdDjmMq
RAZORPAY_KEY_SECRET=11qUG3XjLOjEVkf34Qs0Z1Bp
RAZORPAY_WEBHOOK_SECRET=<paste-from-step-1>

# Email (use your own Gmail)
EMAIL_BACKEND=django.core.mail.backends.smtp.EmailBackend
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_USE_TLS=True
EMAIL_HOST_USER=<your-email@gmail.com>
EMAIL_HOST_PASSWORD=<your-gmail-app-password>
DEFAULT_FROM_EMAIL=LUVORA <your-email@gmail.com>

# Optional
USE_S3=False
SENTRY_DSN=
```

Click **"Update Variables"**

---

### 6️⃣ Deploy Application (5 min)

1. Railway will **automatically redeploy** after setting variables
2. Watch the **"Deployments"** tab for progress
3. Wait for ✅ **"Success"** status
4. Visit your domain: `https://your-domain.railway.app`

---

### 7️⃣ Create Admin User (3 min)

**Option A: Using Railway CLI** (Recommended)

```bash
# Install Railway CLI
npm install -g @railway/cli

# Login
railway login

# Link to project
railway link

# Create superuser
railway run python manage.py createsuperuser
```

**Option B: Using Railway Web Terminal**

1. Go to your web service → **"Settings"**
2. Scroll to **"Service"** → Enable **"TCP Proxy"**
3. Use provided connection command

---

### 8️⃣ Setup Razorpay Webhook (3 min)

1. Go to **https://dashboard.razorpay.com/app/webhooks**
2. Click **"+ Add New Webhook"**
3. Fill in:
   - **URL**: `https://your-domain.railway.app/shop/webhook/`
   - **Secret**: `<paste-webhook-secret-from-step-1>`
   - **Active Events**: Check these:
     - ✅ `payment.authorized`
     - ✅ `payment.captured`
     - ✅ `payment.failed`
     - ✅ `order.paid`
4. Click **"Create Webhook"**

---

### 9️⃣ Load Sample Products (Optional - 5 min)

1. Login to Wagtail CMS: `https://your-domain.railway.app/admin/`
2. Go to **"Pages"** → **"Shop"**
3. Add product pages or import from your local database

---

### 🧪 Test Everything (5 min)

Visit your site and test:

✅ **Homepage** - `https://your-domain.railway.app/`
✅ **Django Admin** - `https://your-domain.railway.app/django-admin/`
✅ **Wagtail CMS** - `https://your-domain.railway.app/admin/`
✅ **Products Page** - `https://your-domain.railway.app/shop/products/`
✅ **Test Payment** - Add to cart → checkout → pay with test card
   - **Card**: `4111 1111 1111 1111`
   - **CVV**: Any 3 digits
   - **Expiry**: Any future date
✅ **Check Email** - Order confirmation should arrive
✅ **Check Webhook** - Order should be marked as paid
✅ **View Order** - Check Django admin for order details

---

## ✅ Deployment Complete!

Your production-like test environment is now live at:
**https://your-domain.railway.app**

---

## 🔄 Making Updates

Whenever you push to GitHub master branch:

```bash
git add .
git commit -m "your changes"
git push origin master
```

Railway will **automatically redeploy** in ~2-3 minutes!

---

## 💡 Tips

### View Logs
```bash
railway logs
# Or check Deployments tab in Railway dashboard
```

### Run Commands
```bash
railway run python manage.py <command>
```

### Database Backup
Railway automatically backs up PostgreSQL database

### Switch to Live Razorpay
When ready for production:
1. Get live keys from Razorpay dashboard (Live Mode)
2. Update environment variables in Railway
3. Update webhook URL in Razorpay dashboard

---

## 🆘 Troubleshooting

**Problem**: Static files not loading
**Solution**: Check Deployments logs, should see "Collecting static files..."

**Problem**: Database errors
**Solution**: Check DATABASE_URL is set (Railway auto-sets this)

**Problem**: 500 errors
**Solution**: Check deployment logs with `railway logs`

**Problem**: Webhook not working
**Solution**: Verify webhook URL and secret in Razorpay dashboard

---

## 📚 Full Documentation

See **DEPLOYMENT_GUIDE.md** for detailed information.

---

## 🎯 What's Next?

1. ✅ Test all features thoroughly
2. ✅ Get feedback from users
3. ✅ Monitor logs for errors
4. ✅ When ready, switch to Razorpay live keys
5. ✅ Consider custom domain ($10-15/year)
6. ✅ Set up monitoring (Sentry)

---

**🎉 Happy Deploying!**
