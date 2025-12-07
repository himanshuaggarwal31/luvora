# LUVORA Production Deployment Guide

## 🚀 Deployment Options

I recommend **Railway.app** for easy production-like deployment with free tier:
- ✓ Free PostgreSQL database included
- ✓ Automatic HTTPS
- ✓ Easy environment variable management
- ✓ GitHub integration for auto-deploy
- ✓ $5 free credit monthly (no credit card needed initially)

**Alternative Options:**
- Render.com (Free tier available)
- Heroku ($7/month minimum)
- DigitalOcean App Platform ($5/month)
- AWS Elastic Beanstalk (Pay as you go)

---

## 📋 Pre-Deployment Checklist

### 1. Generate Production Secrets

```bash
# Generate Django SECRET_KEY
python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"

# Generate Razorpay Webhook Secret
python -c "import secrets; print(secrets.token_urlsafe(32))"
```

### 2. Get Razorpay Live Keys

1. Login to https://dashboard.razorpay.com/
2. Switch to "Live Mode" (toggle in top right)
3. Go to Settings → API Keys
4. Generate Live API Keys
5. Save `rzp_live_*` key ID and secret

### 3. Setup Email (if using Gmail)

1. Enable 2-Factor Authentication on Gmail
2. Generate App Password: https://myaccount.google.com/apppasswords
3. Use this app password in EMAIL_HOST_PASSWORD

---

## 🔧 Railway.app Deployment (Recommended)

### Step 1: Prepare Repository

```bash
# Make sure all files are committed
git add .
git commit -m "chore: prepare for production deployment"
git push origin master
```

### Step 2: Deploy to Railway

1. **Go to** https://railway.app/
2. **Sign up** with GitHub account
3. **Click** "New Project" → "Deploy from GitHub repo"
4. **Select** your `luvora` repository
5. **Wait** for initial build (will fail - that's okay!)

### Step 3: Add PostgreSQL Database

1. In your Railway project, click **"+ New"**
2. Select **"Database" → "Add PostgreSQL"**
3. Railway will create a database and provide connection details
4. Database variables are automatically set

### Step 4: Configure Environment Variables

Click on your web service → "Variables" tab → Add these:

```bash
# Django Core
DEBUG=False
SECRET_KEY=<paste-generated-secret-key>
ALLOWED_HOSTS=<your-railway-domain>.railway.app
CSRF_TRUSTED_ORIGINS=https://<your-railway-domain>.railway.app

# Database (if not auto-set)
DB_ENGINE=django.db.backends.postgresql
DATABASE_URL=<auto-provided-by-railway>

# Razorpay (Use TEST keys first for testing)
RAZORPAY_KEY_ID=rzp_test_Roi0LWTxdDjmMq
RAZORPAY_KEY_SECRET=11qUG3XjLOjEVkf34Qs0Z1Bp
RAZORPAY_WEBHOOK_SECRET=<your-generated-webhook-secret>

# Email
EMAIL_BACKEND=django.core.mail.backends.smtp.EmailBackend
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_USE_TLS=True
EMAIL_HOST_USER=<your-email@gmail.com>
EMAIL_HOST_PASSWORD=<your-app-password>
DEFAULT_FROM_EMAIL=LUVORA <your-email@gmail.com>

# Optional
USE_S3=False
SENTRY_DSN=
```

### Step 5: Deploy

1. Railway will auto-deploy after adding variables
2. Watch the deployment logs
3. Once deployed, note your domain: `https://your-app.railway.app`

### Step 6: Create Superuser

1. In Railway, click on your service
2. Go to "Settings" tab → "Service" → "Enable TCP Proxy"
3. Or use Railway CLI:

```bash
# Install Railway CLI
npm install -g @railway/cli

# Login
railway login

# Link project
railway link

# Run command
railway run python manage.py createsuperuser
```

### Step 7: Configure Razorpay Webhook

1. Go to https://dashboard.razorpay.com/app/webhooks
2. Add New Webhook:
   - URL: `https://your-app.railway.app/shop/webhook/`
   - Secret: <paste-your-webhook-secret>
   - Events: Select `payment.authorized`, `payment.captured`, `payment.failed`, `order.paid`
3. Save

---

## 🧪 Testing Checklist

Once deployed, test these:

- [ ] Homepage loads correctly
- [ ] Static files (CSS/JS) working
- [ ] Images displaying
- [ ] Admin panel accessible: `/django-admin/`
- [ ] Wagtail CMS accessible: `/admin/`
- [ ] Product listing page works
- [ ] Add to cart functionality
- [ ] Checkout page with Razorpay
- [ ] Test payment (use test card: 4111 1111 1111 1111)
- [ ] Webhook received and order updated
- [ ] Email confirmation sent
- [ ] Order visible in admin panel

---

## 🔒 Production Security Checklist

Before going fully live with REAL payments:

- [ ] Change DEBUG to False
- [ ] Use strong SECRET_KEY (not the default)
- [ ] Switch Razorpay to LIVE keys (not TEST)
- [ ] Enable HTTPS only (Railway does this automatically)
- [ ] Review ALLOWED_HOSTS and CSRF_TRUSTED_ORIGINS
- [ ] Set up proper email (not Gmail if high volume expected)
- [ ] Configure Sentry for error monitoring
- [ ] Set up database backups
- [ ] Test webhook signature verification
- [ ] Review Django security settings
- [ ] Set up monitoring/alerting

---

## 📊 Post-Deployment

### Monitor Logs

```bash
# Using Railway CLI
railway logs

# Or view in Railway dashboard
```

### Database Migrations

```bash
railway run python manage.py migrate
```

### Collect Static Files

```bash
railway run python manage.py collectstatic --noinput
```

### Create Sample Data

```bash
# Create superuser
railway run python manage.py createsuperuser

# Or use Django shell
railway run python manage.py shell
```

---

## 🆘 Troubleshooting

### Issue: Static files not loading
**Solution:** Run `python manage.py collectstatic` and check STATIC_ROOT setting

### Issue: Database connection error
**Solution:** Check DATABASE_URL is set correctly, Railway auto-provides this

### Issue: 500 Internal Server Error
**Solution:** Check logs with `railway logs`, likely missing environment variable

### Issue: Webhook not receiving events
**Solution:** 
- Verify webhook URL in Razorpay dashboard
- Check ALLOWED_HOSTS includes your domain
- Verify webhook secret matches

### Issue: Email not sending
**Solution:** 
- Check Gmail app password is correct
- Verify EMAIL_USE_TLS=True
- Check firewall/port 587 is open

---

## 💰 Costs (Approximate)

### Free Tier Testing:
- **Railway**: $5 free credit/month (500 hours)
- **Render**: 750 hours free
- **Database**: Included in free tier

### Production (Paid):
- **Railway**: ~$5-10/month
- **Database**: Included
- **Domain**: ~$10-15/year
- **S3 Storage**: ~$1-5/month (optional)

---

## 🎯 Next Steps After Deployment

1. **Test thoroughly** with test Razorpay keys
2. **Get user feedback** from real users
3. **Monitor errors** and logs
4. **Switch to live keys** when ready for production
5. **Set up custom domain** (optional)
6. **Enable database backups**
7. **Set up monitoring** (Sentry, UptimeRobot, etc.)

---

## 📞 Support

- Railway Docs: https://docs.railway.app/
- Django Deployment: https://docs.djangoproject.com/en/5.0/howto/deployment/
- Razorpay Docs: https://razorpay.com/docs/
- Wagtail Docs: https://docs.wagtail.org/

---

**Ready to deploy?** Follow the steps above and you'll have a production-like environment running in ~30 minutes!
