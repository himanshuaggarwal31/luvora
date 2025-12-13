# LUVORA Static Catalog - Quick Start

## ✅ What's Included

A complete static website with:
- ✅ Homepage with hero and features
- ✅ Products catalog page with filtering
- ✅ About page
- ✅ Contact page
- ✅ Responsive design (mobile-friendly)
- ✅ Product search and filters
- ✅ No shopping cart / No payments

## 🚀 Quick Deploy to S3 (30 minutes)

### 1. Test Locally (2 min)
```bash
# Windows
cd static-catalog
start index.html

# Mac/Linux
cd static-catalog
open index.html
```

### 2. Install AWS CLI (5 min - if not installed)
```bash
pip install awscli
aws configure
```

Enter your AWS credentials:
- AWS Access Key ID
- AWS Secret Access Key  
- Default region: `ap-south-1`
- Output format: `json`

### 3. Deploy to S3 (5 min)

**Windows:**
```powershell
cd static-catalog
.\deploy.ps1
```

**Mac/Linux:**
```bash
cd static-catalog
chmod +x deploy.sh
./deploy.sh
```

### 4. Done! 🎉

Your site is live at:
```
http://luvora-catalog.s3-website-ap-south-1.amazonaws.com
```

## 📝 Update Products

1. Edit `data/products.json`
2. Run deploy script again
3. Changes live instantly!

## 💰 Cost: ~$1-3/month

See `README.md` for full documentation.
