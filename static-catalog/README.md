# LUVORA Static Catalog - S3 Deployment Guide

## 🌟 Overview

This is a **static catalog website** for LUVORA - no shopping cart, no payment processing. Perfect for hosting on **AWS S3** for ~$1-3/month.

---

## 📁 Folder Structure

```
static-catalog/
├── index.html          # Homepage
├── products.html       # Products catalog with filters
├── about.html          # About page
├── contact.html        # Contact page
├── css/
│   └── style.css       # All styles
├── js/
│   ├── main.js         # Navigation & common
│   ├── products.js     # Product display
│   ├── catalog.js      # Filtering & search
│   └── contact.js      # Contact form
├── data/
│   └── products.json   # Product catalog data
└── images/
    └── (add your images here)
```

---

## 🚀 Deployment to AWS S3

### Step 1: Prepare Your Files

1. **Add Product Images** (optional):
   - Place product images in `images/products/`
   - Update `products.json` image paths

2. **Test Locally**:
   ```bash
   # Windows
   start index.html
   
   # Mac/Linux
   open index.html
   ```

### Step 2: Create S3 Bucket

1. **Login to AWS Console**: https://console.aws.amazon.com/s3/
2. Click **"Create bucket"**
3. **Bucket name**: `luvora-catalog` (must be globally unique)
4. **Region**: Choose closest to your users (e.g., `ap-south-1` for India)
5. **Uncheck** "Block all public access"
6. Acknowledge the warning
7. Click **"Create bucket"**

### Step 3: Enable Static Website Hosting

1. Click on your bucket
2. Go to **"Properties"** tab
3. Scroll to **"Static website hosting"**
4. Click **"Edit"**
5. Select **"Enable"**
6. **Index document**: `index.html`
7. **Error document**: `index.html`
8. Click **"Save changes"**
9. **Note the website URL** (e.g., `http://luvora-catalog.s3-website-ap-south-1.amazonaws.com`)

### Step 4: Upload Files

1. Go to **"Objects"** tab
2. Click **"Upload"**
3. **Drag and drop** entire `static-catalog` folder contents
4. Click **"Upload"**

### Step 5: Set Bucket Policy (Make Public)

1. Go to **"Permissions"** tab
2. Scroll to **"Bucket policy"**
3. Click **"Edit"**
4. Paste this policy (replace `luvora-catalog` with your bucket name):

```json
{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Sid": "PublicReadGetObject",
            "Effect": "Allow",
            "Principal": "*",
            "Action": "s3:GetObject",
            "Resource": "arn:aws:s3:::luvora-catalog/*"
        }
    ]
}
```

5. Click **"Save changes"**

### Step 6: Test Your Website

Visit your S3 website URL:
```
http://luvora-catalog.s3-website-ap-south-1.amazonaws.com
```

---

## 🌐 Optional: Custom Domain with CloudFront

### Benefits:
- HTTPS support
- Custom domain (www.luvora.com)
- Faster loading (CDN)
- Only $0.50-2/month extra

### Setup:

1. **Create CloudFront Distribution**:
   - Go to CloudFront console
   - Click "Create Distribution"
   - **Origin Domain**: Your S3 bucket
   - **Origin Path**: Leave blank
   - **Viewer Protocol Policy**: Redirect HTTP to HTTPS
   - **Alternate Domain Names (CNAMEs)**: www.luvora.com
   - **SSL Certificate**: Request from ACM or use default
   - Click "Create Distribution"

2. **Update DNS**:
   - In your domain registrar, add CNAME:
   - `www` → `[your-cloudfront-domain].cloudfront.net`

---

## 💰 Cost Estimate

### S3 Only:
- **Storage**: $0.023/GB/month (first 50TB)
- **Requests**: $0.0004/1000 requests
- **Data Transfer**: $0.09/GB (first 10TB)
- **Estimated**: **$1-3/month** for small sites

### With CloudFront:
- **Data Transfer**: $0.085/GB
- **Requests**: $0.01/10,000 requests
- **Estimated**: **$2-5/month**

---

## 🔧 Updating Your Site

### Method 1: AWS Console
1. Go to S3 bucket
2. Upload new/updated files
3. Changes reflect immediately

### Method 2: AWS CLI (Recommended)

```bash
# Install AWS CLI
pip install awscli

# Configure credentials
aws configure

# Sync folder to S3
cd static-catalog
aws s3 sync . s3://luvora-catalog/ --delete

# Invalidate CloudFront cache (if using)
aws cloudfront create-invalidation --distribution-id YOUR_DIST_ID --paths "/*"
```

---

## 📝 Updating Products

1. **Edit** `data/products.json`
2. **Add** product images to `images/products/`
3. **Upload** to S3

Example product entry:
```json
{
    "id": 4,
    "name": "New Product",
    "slug": "new-product",
    "price": 4999,
    "category": "Bedsheets",
    "image": "images/products/new-product.jpg",
    "description": "Product description here",
    "features": ["Feature 1", "Feature 2"],
    "inStock": true
}
```

---

## 🔒 Security Best Practices

1. **Never commit AWS credentials** to git
2. **Use IAM roles** for programmatic access
3. **Enable CloudFront** for HTTPS
4. **Regular backups** of S3 bucket
5. **Monitor costs** in AWS Billing Dashboard

---

## 🆘 Troubleshooting

### Issue: 404 Not Found
**Solution**: Check file paths are correct and files are uploaded

### Issue: Access Denied
**Solution**: Verify bucket policy is set correctly

### Issue: CSS/JS not loading
**Solution**: Check file paths in HTML files, ensure case-sensitive paths match

### Issue: Products not showing
**Solution**: 
- Check browser console for errors
- Verify `products.json` is valid JSON
- Ensure file is uploaded to S3

---

## 📊 Features Included

✅ **Homepage** - Hero, features, featured products
✅ **Products Page** - Full catalog with filtering & search
✅ **Category Filter** - Filter by product category
✅ **Price Filter** - Filter by price range
✅ **Search** - Search products by name/description
✅ **Sort** - Sort by price or name
✅ **Responsive Design** - Works on mobile, tablet, desktop
✅ **About Page** - Company information
✅ **Contact Page** - Contact form (mailto)

❌ **Not Included** (by design):
- Shopping cart
- Payment processing
- User accounts
- Order management
- Database

---

## 🎯 Next Steps

1. ✅ Test locally first
2. ✅ Add your product images
3. ✅ Update `products.json` with real products
4. ✅ Deploy to S3
5. ✅ Test S3 website
6. ⬜ (Optional) Setup CloudFront
7. ⬜ (Optional) Add custom domain

---

## 📞 Support

For questions about:
- **AWS S3**: https://docs.aws.amazon.com/s3/
- **CloudFront**: https://docs.aws.amazon.com/cloudfront/
- **This catalog**: Contact your developer

---

**Ready to deploy?** Follow the steps above and your catalog will be live in ~30 minutes!
