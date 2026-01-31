    # 🌐 Complete S3 Static Website Hosting Guide with Custom Domain

    > **Step-by-step guide to host your LUVORA static catalog on AWS S3 with a custom domain**

    ---

    ## 📋 Table of Contents

### Core Setup (Required)
1. [What You Need](#what-you-need)
2. [Files & Folders Required](#files--folders-required)
3. [AWS Account Setup](#aws-account-setup)
4. [S3 Bucket Creation & Configuration](#s3-bucket-creation--configuration)
5. [Upload Website Files](#upload-website-files)
6. [Testing Without Domain](#testing-without-domain-first)
7. [CloudFront CDN Setup for HTTPS](#cloudfront-cdn-setup-for-https-optional)

### Domain Setup (Optional - Can Do Later)
8. [Domain Purchase & Setup](#domain-purchase--setup-optional)
9. [SSL Certificate for Custom Domain](#ssl-certificate-for-custom-domain)
10. [DNS Configuration](#dns-configuration-point-domain-to-website)
11. [Final Testing with Domain](#final-testing-with-custom-domain)

### Maintenance & Support
12. [Updating Your Website](#updating-your-website)
13. [Cost Estimation](#cost-estimation)
14. [Troubleshooting](#troubleshooting)

    ## What You Need

    ### Prerequisites Checklist

**Required (To Get Started):**
- [ ] AWS Account (free tier available)
- [ ] Credit/debit card for AWS (required even for free tier)
- [ ] AWS CLI installed (optional but recommended for updates)
- [ ] Product images ready to upload

**Optional (Can Add Later):**
- [ ] Custom domain name (e.g., luvora.com) - *You can use AWS URLs first!*
- [ ] Domain registrar account (GoDaddy, Namecheap, AWS Route 53, etc.)

| Service | Cost (Monthly) | When Needed |
|---------|---------------|-------------|
| S3 Storage (1GB) | ~$0.023 | ✅ Always (Required) |
| S3 Requests (10,000 requests) | ~$0.005 | ✅ Always (Required) |
| CloudFront (HTTPS) | First 1TB free | ⚡ Optional (for better performance) |
| Route 53 (DNS) | $0.50 per hosted zone | 🌐 Optional (only with custom domain) |
| SSL Certificate | **FREE** (AWS) | 🌐 Optional (only with custom domain) |
| **Total WITHOUT Domain** | **~$0.03/month** | Just S3 |
| **Total WITH Domain** | **~$0.50-3/month** | S3 + CloudFront + Domain |

    ## Files & Folders Required

    ### What to Upload from Your Project

    Only the `static-catalog` folder and its contents are needed. Here's the complete structure:

    ```
    static-catalog/
    ├── index.html              ✅ Required - Homepage
    ├── products.html           ✅ Required - Product catalog
    ├── about.html              ✅ Required - About page
    ├── contact.html            ✅ Required - Contact page
    ├── css/
    │   └── style.css          ✅ Required - Styling
    ├── js/
    │   ├── main.js            ✅ Required - Navigation
    │   ├── products.js        ✅ Required - Product loading
    │   ├── catalog.js         ✅ Required - Filtering/search
    │   └── contact.js         ✅ Required - Contact form
    ├── data/
    │   └── products.json      ✅ Required - Product database
    └── images/                 ✅ Required - Product images
        ├── bedsheet1.jpg
        ├── bedsheet2.jpg
        └── ... (your product images)
    ```

    ### What NOT to Upload

    ❌ Do NOT upload these Django-related files:
    - `.venv/` folder
    - `shop/` folder
    - `luvora_project/` folder
    - `manage.py`
    - `db.sqlite3`
    - `.env` file
    - `requirements.txt`
    - Any Python files

    **Only upload the `static-catalog` folder contents!**

    ---

    ## AWS Account Setup

    ### Step 1: Create AWS Account

    1. Go to https://aws.amazon.com/
    2. Click **"Create an AWS Account"**
    3. Fill in:
    - Email address
    - Password
    - AWS account name (e.g., "LUVORA Production")
    4. Choose **"Personal"** account type
    5. Enter payment information (required for verification)
    6. Select **"Free Tier"** plan
    7. Complete phone verification
    8. Choose **"Basic Support - Free"** plan

    ### Step 2: Enable MFA (Multi-Factor Authentication) - Recommended

    1. Login to AWS Console: https://console.aws.amazon.com/
    2. Click your account name (top right) → **Security credentials**
    3. Scroll to **Multi-factor authentication (MFA)**
    4. Click **"Assign MFA device"**
    5. Follow setup wizard (use Google Authenticator app)

    ### Step 3: Create IAM User (Recommended for Security)

    Instead of using root account:

    1. Go to **IAM** service in AWS Console
    2. Click **"Users"** → **"Add users"**
    3. Username: `luvora-admin`
    4. Select **"Provide user access to the AWS Management Console"**
    5. Choose **"I want to create an IAM user"**
    6. Set custom password
    7. Click **"Next"**
    8. Attach policies:
    - `AmazonS3FullAccess`
    - `CloudFrontFullAccess`
    - `AWSCertificateManagerFullAccess`
    - `AmazonRoute53FullAccess`
    9. Click **"Create user"**
    10. Save credentials securely

    **Use this IAM user for all future operations.**

    ---

    ## S3 Bucket Creation & Configuration

    ### Step 1: Create S3 Bucket

    1. Login to AWS Console with IAM user
    2. Go to **S3** service (search "S3" in top search bar)
    3. Click **"Create bucket"**

    **Bucket Settings:**
    - **Bucket name**: `luvora-catalog` (must be globally unique)
    - If taken, try: `luvora-shop`, `luvora-products`, `luvora-store-2026`
    - **Important**: Use lowercase letters, numbers, and hyphens only
    - This bucket name will be part of your temporary URL
    - **AWS Region**: Choose closest to your target audience
    - India: `ap-south-1` (Mumbai)
    - US East: `us-east-1` (N. Virginia) - required for Route 53
    - Europe: `eu-west-1` (Ireland)
    - **Object Ownership**: Select **"ACLs enabled"** → **"Bucket owner preferred"**
    - **Block Public Access settings**: 
    - ✅ **UNCHECK** "Block all public access"
    - ✅ **CHECK** the acknowledgment box (I acknowledge that these settings might make my bucket public)
    - **Bucket Versioning**: Disabled (to save costs)
    - **Tags**: Optional (e.g., `Project: LUVORA`)
    - **Default encryption**: Server-side encryption with Amazon S3 managed keys (SSE-S3) - Enabled by default
    - Click **"Create bucket"**

    ### Step 2: Enable Static Website Hosting

    1. Click on your bucket name: `luvora-catalog`
    2. Go to **"Properties"** tab
    3. Scroll to **"Static website hosting"** section
    4. Click **"Edit"**
    5. Configure:
    - **Static website hosting**: **Enable**
    - **Hosting type**: **Host a static website**
    - **Index document**: `index.html`
    - **Error document**: `index.html` (redirects 404s to homepage)
    6. Click **"Save changes"**
    7. **Copy the Bucket website endpoint** (e.g., `http://luvora-catalog.s3-website-ap-south-1.amazonaws.com`)
    - Save this URL - you'll test with it first!

    ### Step 3: Configure Bucket Policy (Public Access)

    1. Stay in your bucket, go to **"Permissions"** tab
    2. Scroll to **"Bucket policy"** section
    3. Click **"Edit"**
    4. Paste this policy (replace `luvora-catalog` with your actual bucket name):

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

    **What this does**: Allows anyone to read (download) files from your bucket, making your website publicly accessible.

    ### Step 4: Configure CORS (Optional but Recommended)

    If you plan to load resources from other domains:

    1. Go to **"Permissions"** tab
    2. Scroll to **"Cross-origin resource sharing (CORS)"**
    3. Click **"Edit"**
    4. Paste this configuration:

    ```json
    [
    {
        "AllowedHeaders": ["*"],
        "AllowedMethods": ["GET", "HEAD"],
        "AllowedOrigins": ["*"],
        "ExposeHeaders": [],
        "MaxAgeSeconds": 3000
    }
    ]
    ```

    5. Click **"Save changes"**

    ---

    ## Upload Website Files

    ### Option 1: AWS Console (Manual Upload - Good for First Time)

    1. Open your bucket: `luvora-catalog`
    2. Click **"Upload"**
    3. Click **"Add files"** and **"Add folder"**
    4. Navigate to your project: `C:\Himanshu\REPOS\luvora\static-catalog`
    5. Select ALL files and folders:
    - `index.html`
    - `products.html`
    - `about.html`
    - `contact.html`
    - `css/` folder (and its contents)
    - `js/` folder (and its contents)
    - `data/` folder (and its contents)
    - `images/` folder (and its contents)
    6. Click **"Upload"**
    7. Wait for upload to complete (progress bar shows status)
    8. Click **"Close"** when done

    **Verify Upload:**
    - You should see files listed in your bucket
    - Check that folder structure is maintained:
    ```
    css/style.css
    js/main.js
    js/products.js
    js/catalog.js
    js/contact.js
    data/products.json
    images/...
    index.html
    products.html
    about.html
    contact.html
    ```

    ### Option 2: AWS CLI (Automated - Better for Updates)

    #### Install AWS CLI (First Time Only)

    **Windows:**
    1. Download installer: https://awscli.amazonaws.com/AWSCLIV2.msi
    2. Run installer, follow prompts
    3. Open new PowerShell window
    4. Verify installation:
    ```powershell
    aws --version
    # Output: aws-cli/2.x.x ...
    ```

    #### Configure AWS CLI

    ```powershell
    # Run configuration wizard
    aws configure

    # Enter when prompted:
    # AWS Access Key ID: (from IAM user creation)
    # AWS Secret Access Key: (from IAM user creation)
    # Default region name: ap-south-1  (or your chosen region)
    # Default output format: json
    ```

    **To get Access Keys if you don't have them:**
    1. AWS Console → IAM → Users → `luvora-admin`
    2. Click **"Security credentials"** tab
    3. Scroll to **"Access keys"**
    4. Click **"Create access key"**
    5. Choose **"Command Line Interface (CLI)"**
    6. Check acknowledgment, click **"Next"**
    7. Click **"Create access key"**
    8. **Copy and save both keys immediately** (you can't view secret key again)

    #### Upload Files with AWS CLI

    ```powershell
    # Navigate to static-catalog folder
    cd C:\Himanshu\REPOS\luvora\static-catalog

    # Upload all files to S3 bucket
    aws s3 sync . s3://luvora-catalog --delete

    # Flags explained:
    # . = current directory (static-catalog)
    # s3://luvora-catalog = your bucket
    # --delete = removes files from S3 that don't exist locally
    ```

    **Expected Output:**
    ```
    upload: ./index.html to s3://luvora-catalog/index.html
    upload: ./products.html to s3://luvora-catalog/products.html
    upload: ./about.html to s3://luvora-catalog/about.html
    upload: ./contact.html to s3://luvora-catalog/contact.html
    upload: ./css/style.css to s3://luvora-catalog/css/style.css
    upload: ./js/main.js to s3://luvora-catalog/js/main.js
    ...
    ```

    ### Option 3: PowerShell Deployment Script (Easiest)

    Use the included deployment script:

    ```powershell
    cd C:\Himanshu\REPOS\luvora\static-catalog

    # Run deployment script
    .\deploy.ps1

    # Follow prompts:
    # Enter AWS Profile name: (press Enter for default)
    # Enter S3 bucket name: luvora-catalog
    # Confirm deployment: Y
    ```

    The script automatically:
    - Syncs all files
    - Sets correct content types (HTML, CSS, JS, JSON, images)
    - Displays website URL

    ---

## Testing Without Domain First

### ✅ Your Website is Already Live!

After uploading files to S3, **your website is immediately accessible** without any domain. You have a working URL right now!

### Option 1: S3 Static Website URL (HTTP Only)

**Your Current URL:**
```
http://luvora-catalog.s3-website-ap-south-1.amazonaws.com
```

**How to Find It:**
1. AWS Console → S3 → Your bucket (`luvora-catalog`)
2. Go to **Properties** tab
3. Scroll to **Static website hosting** section
4. Copy the **Bucket website endpoint**

**✅ Use This URL To:**
- Test your website immediately
- Share with team/clients for preview
- Verify everything works before buying domain
- Use temporarily while domain propagates

**⚠️ Limitations:**
- Only HTTP (not HTTPS) - no green padlock
- Long, hard-to-remember URL
- No custom branding

**Example Testing:**
```
Homepage:  http://luvora-catalog.s3-website-ap-south-1.amazonaws.com
Products:  http://luvora-catalog.s3-website-ap-south-1.amazonaws.com/products.html
About:     http://luvora-catalog.s3-website-ap-south-1.amazonaws.com/about.html
```

**Perfect for:** Development, testing, internal use, temporary deployment

---

### Option 2: CloudFront URL (HTTPS - No Domain Needed!)

If you want HTTPS **without buying a domain**, you can use CloudFront's free URL:

#### Quick CloudFront Setup (Without Custom Domain)

1. **AWS Console → CloudFront → Create distribution**

2. **Origin Settings:**
   - Origin domain: `luvora-catalog.s3-website-ap-south-1.amazonaws.com` (your S3 website endpoint)
   - Protocol: HTTP only
   - Name: (auto-fills)

3. **Default Cache Behavior:**
   - Viewer protocol policy: **Redirect HTTP to HTTPS**
   - Allowed HTTP methods: GET, HEAD
   - Cache policy: CachingOptimized

4. **Settings:**
   - Price class: Use only North America and Europe (cheaper)
   - Alternate domain names (CNAMEs): **Leave BLANK** (no custom domain)
   - Custom SSL certificate: **Default CloudFront Certificate**
   - Default root object: `index.html`
   - IPv6: On

5. **Create distribution** → Wait 15-20 minutes

6. **Your HTTPS URL:**
   ```
   https://d123456abcdef.cloudfront.net
   ```
   Copy from CloudFront console → Distribution domain name

**✅ CloudFront URL Benefits:**
- ✅ **HTTPS enabled** (secure, green padlock)
- ✅ **No domain purchase needed**
- ✅ **Faster loading** (global CDN)
- ✅ **Free SSL certificate** (automatic)
- ✅ **No additional cost** (first 1TB free)

**Example URLs:**
```
Homepage:  https://d123456abcdef.cloudfront.net
Products:  https://d123456abcdef.cloudfront.net/products.html
About:     https://d123456abcdef.cloudfront.net/about.html
```

**Perfect for:** Production use without domain, professional testing, secure sharing

---

### Decision Time: Do You Need a Custom Domain?

**✅ Use AWS URLs (S3 or CloudFront) if:**
- You want to test before committing to domain
- It's for internal/development use
- Budget is very tight ($0.03/month vs $0.50+/month)
- You're fine sharing the CloudFront URL
- Domain purchase can wait

**✅ Get Custom Domain if:**
- You want professional branding (luvora.com)
- Need easy-to-remember URL
- Planning to market/advertise the site
- Want email addresses (info@luvora.com)
- This is customer-facing production site

**💡 Recommended Approach:**
1. **Start with CloudFront URL** (free HTTPS)
2. **Test everything thoroughly**
3. **Use it for a few days/weeks**
4. **Buy domain later when ready**
5. **Point domain to existing CloudFront** (takes 5 minutes)

---

## Domain Purchase & Setup (OPTIONAL)

> **⚠️ NOTE: This section is OPTIONAL. Your website already works with CloudFront URL!**  
> Only proceed if you want a custom domain like `luvora.com`

**Already Happy with CloudFront URL?** → Skip to [Updating Your Website](#updating-your-website)

---

### When to Add a Custom Domain

**Right now, your website works perfectly at:**
- S3 URL: `http://your-bucket.s3-website-region.amazonaws.com`
- CloudFront URL: `https://d123456abcdef.cloudfront.net` ✅ **HTTPS enabled!**

**Add a custom domain when:**
- ✅ You're ready to go fully public
- ✅ You want professional branding
- ✅ You need an easy-to-remember URL
- ✅ You want custom email (info@yourdomain.com)
- ✅ Marketing/advertising requires branded domain

**Don't need it yet?** → Use CloudFront URL for now, add domain anytime later!

---

### Step 1: Choose a Domain Registrar

**Recommended Options:**

    | Registrar | .com Price | Pros | Cons |
    |-----------|-----------|------|------|

    **Recommendation**: Use **AWS Route 53** for simplest integration, or **Namecheap** for best value.

    ### Step 2A: Purchase Domain via AWS Route 53 (Easiest)

    1. AWS Console → Search **"Route 53"**
    2. Click **"Registered domains"** → **"Register domain"**
    3. Search for your domain: `luvora.com`
    4. If available, click **"Add to cart"**
    5. Choose registration period: **1 year** (can renew later)
    6. Enter contact information:
    - Full name
    - Email address
    - Phone number
    - Address
    7. **Privacy Protection**: **Enable** (hides your personal info from WHOIS)
    8. Review and click **"Complete Order"**
    9. Confirm email verification (check inbox/spam)
    10. **Wait 10-15 minutes** for domain registration to complete

    **✅ Advantage**: DNS is automatically set up in Route 53. Skip to [Step 3: Create Hosted Zone](#step-3-create-hosted-zone-route-53).

    ### Step 2B: Purchase Domain via Namecheap

    1. Go to https://www.namecheap.com/
    2. Search for your domain: `luvora.com`
    3. If available, click **"Add to Cart"**
    4. Review cart:
    - Domain: $8.88/year
    - WhoisGuard (privacy): **FREE first year** ✓
    5. Click **"Confirm Order"**
    6. Create account or login
    7. Enter payment information
    8. Complete purchase
    9. Verify email (check inbox)

    ### Step 2C: Purchase Domain via GoDaddy

    1. Go to https://www.godaddy.com/
    2. Search for domain: `luvora.com`
    3. Add to cart (⚠️ uncheck upsells: website builder, email, etc.)
    4. Proceed to checkout
    5. Create account/login
    6. Enter payment details
    7. Complete purchase
    8. Verify email

    ### Step 3: Create Hosted Zone (Route 53)

    Even if you bought domain elsewhere, create hosted zone in Route 53 for easy management:

    1. AWS Console → **Route 53**
    2. Click **"Hosted zones"** → **"Create hosted zone"**
    3. **Domain name**: `luvora.com` (exact match to your domain)
    4. **Type**: **Public hosted zone**
    5. Click **"Create hosted zone"**
    6. **Copy the 4 nameserver (NS) records**:
    ```
    ns-123.awsdns-12.com
    ns-456.awsdns-45.net
    ns-789.awsdns-78.org
    ns-012.awsdns-01.co.uk
    ```

    **Cost**: $0.50/month per hosted zone

    ### Step 4: Update Nameservers (If Bought Domain Outside AWS)

    #### For Namecheap:
    1. Login to Namecheap
    2. Go to **Domain List** → Click **"Manage"** next to your domain
    3. Find **"Nameservers"** section
    4. Select **"Custom DNS"**
    5. Paste the 4 AWS nameservers (from Step 3)
    6. Click **"Save"**
    7. **Wait 24-48 hours** for propagation (usually 1-4 hours)

    #### For GoDaddy:
    1. Login to GoDaddy
    2. Go to **My Products** → **Domains**
    3. Click **"DNS"** next to your domain
    4. Scroll to **"Nameservers"** → Click **"Change"**
    5. Select **"I'll use my own nameservers"**
    6. Paste the 4 AWS nameservers
    7. Click **"Save"**
    8. **Wait 24-48 hours** for propagation

    **Check Propagation Status:**
    ```powershell
    # Check nameservers
    nslookup -type=ns luvora.com

    # Should show AWS nameservers after propagation
    ```

    Or use online tool: https://www.whatsmydns.net/

    ---

    ## CloudFront CDN Setup (HTTPS)

    **Why CloudFront?**
    - ✅ **HTTPS/SSL** (S3 static hosting only supports HTTP)
    - ✅ **Global CDN** (faster load times worldwide)
    - ✅ **Free SSL certificate** (via AWS Certificate Manager)
    - ✅ **DDoS protection**
    - ✅ **Better performance**

    ### Step 1: Request SSL Certificate (Must Do First)

    1. AWS Console → Search **"Certificate Manager"** (ACM)
    2. **⚠️ IMPORTANT**: Change region to **US East (N. Virginia) us-east-1** (top right dropdown)
    - CloudFront requires certificates in us-east-1
    3. Click **"Request certificate"** → **"Request a public certificate"** → **"Next"**
    4. **Domain names**:
    - Add: `luvora.com`
    - Click **"Add another name to this certificate"**
    - Add: `www.luvora.com`
    - (This covers both with and without www)
    5. **Validation method**: **DNS validation** (easier)
    6. **Key algorithm**: **RSA 2048**
    7. Click **"Request"**
    8. Click on your certificate (Status: Pending validation)
    9. Expand both domains, click **"Create records in Route 53"** for each
    10. Click **"Create records"** (adds CNAME records automatically)
    11. **Wait 5-30 minutes** for validation (refresh page to check)
    12. Status should change to **"Issued"** ✅

    **Troubleshooting Certificate Validation:**
    - Ensure Route 53 hosted zone exists for your domain
    - Check that nameservers are propagated (can take 24-48 hours)
    - CNAME records should appear in Route 53 hosted zone automatically

    ### Step 2: Create CloudFront Distribution

    1. AWS Console → **CloudFront**
    2. Click **"Create distribution"**

    **Origin Settings:**
    - **Origin domain**: 
    - ⚠️ **DO NOT** select from dropdown (it will use S3 REST API endpoint)
    - **Manually type** your S3 website endpoint: 
        - `luvora-catalog.s3-website-ap-south-1.amazonaws.com`
        - (Get this from S3 bucket → Properties → Static website hosting)
    - **Protocol**: **HTTP only** (S3 static hosting endpoint only supports HTTP)
    - **Name**: Auto-fills (leave as is)

    **Default Cache Behavior Settings:**
    - **Viewer protocol policy**: **Redirect HTTP to HTTPS** ✅
    - **Allowed HTTP methods**: **GET, HEAD**
    - **Cache policy**: **CachingOptimized** (recommended)
    - **Origin request policy**: None
    - **Response headers policy**: Optional (leave blank)

    **Settings:**
    - **Price class**: **Use only North America and Europe** (cheaper) or **Use all edge locations** (faster globally)
    - **Alternate domain names (CNAMEs)**: 
    - Add: `luvora.com`
    - Add: `www.luvora.com`
    - **Custom SSL certificate**: Select your certificate (from Step 1)
    - If not visible, ensure certificate is in **us-east-1** region and **Status: Issued**
    - **Default root object**: `index.html`
    - **Description**: `LUVORA Static Catalog`
    - **Logging**: Off (to save costs)
    - **IPv6**: On (recommended)

    **Error Pages (Recommended):**
    3. After creation, click on your distribution
    4. Go to **"Error pages"** tab → **"Create custom error response"**
    5. Create two custom error responses:

    **Response 1 (404 errors):**
    - HTTP error code: **404: Not Found**
    - Customize error response: **Yes**
    - Response page path: `/index.html`
    - HTTP response code: **200: OK**
    - Click **"Create custom error response"**

    **Response 2 (403 errors):**
    - HTTP error code: **403: Forbidden**
    - Customize error response: **Yes**
    - Response page path: `/index.html`
    - HTTP response code: **200: OK**
    - Click **"Create custom error response"**

    **Why?** This ensures clean URLs work (e.g., `/products` loads `/products.html`)

    6. Click **"Create distribution"**
    7. **Wait 15-30 minutes** for deployment (Status: "Deploying" → "Enabled")
    8. **Copy the Distribution domain name**: `d123456abcdef.cloudfront.net`
    9. **Test it**: Open `https://d123456abcdef.cloudfront.net` in browser
    - ✅ Should load your website with HTTPS!

    ---

    ## DNS Configuration

    Now point your domain to CloudFront:

    ### Create DNS Records in Route 53

    1. AWS Console → **Route 53** → **Hosted zones**
    2. Click your hosted zone: `luvora.com`
    3. Click **"Create record"**

    **Record 1: Root domain (luvora.com)**
    - **Record name**: Leave blank (creates root domain record)
    - **Record type**: **A - Routes traffic to an IPv4 address and some AWS resources**
    - **Alias**: **✅ Enable** (toggle on)
    - **Route traffic to**: 
    - Choose **"Alias to CloudFront distribution"**
    - Select your distribution from dropdown (the `d123456abcdef.cloudfront.net`)
    - **Routing policy**: **Simple routing**
    - **Evaluate target health**: **No**
    - Click **"Create records"**

    **Record 2: WWW subdomain (www.luvora.com)**
    - Click **"Create record"** again
    - **Record name**: `www`
    - **Record type**: **A**
    - **Alias**: **✅ Enable**
    - **Route traffic to**:
    - Choose **"Alias to CloudFront distribution"**
    - Select same distribution
    - Click **"Create records"**

    ### Verify DNS Records

    ```powershell
    # Wait 5-10 minutes, then check DNS propagation
    nslookup luvora.com
    nslookup www.luvora.com

    # Should return CloudFront IP addresses
    ```

    Online checker: https://www.whatsmydns.net/ (check worldwide propagation)

    ---

    ## Testing & Verification

    ### Step-by-Step Testing Checklist

    1. **✅ S3 Bucket Test** (HTTP):
    ```
    http://luvora-catalog.s3-website-ap-south-1.amazonaws.com
    ```
    - Should load your website
    - If not, check bucket policy and static hosting settings

    2. **✅ CloudFront Test** (HTTPS):
    ```
    https://d123456abcdef.cloudfront.net
    ```
    - Should load with HTTPS (green padlock)
    - If not, wait longer (can take 30 minutes)

    3. **✅ Domain Test** (Your Custom Domain):
    ```
    https://luvora.com
    https://www.luvora.com
    ```
    - Both should load your website with HTTPS
    - If not working:
        - Check DNS propagation (can take 24-48 hours)
        - Verify Route 53 records are correct
        - Check SSL certificate is validated

    4. **✅ Page Navigation Test**:
    - Homepage: `https://luvora.com`
    - Products: `https://luvora.com/products.html`
    - About: `https://luvora.com/about.html`
    - Contact: `https://luvora.com/contact.html`
    - All should load without errors

    5. **✅ Product Loading Test**:
    - Open products page
    - Check browser console (F12) for errors
    - Verify products display correctly
    - Test filtering and search

    6. **✅ Mobile Test**:
    - Open on mobile device
    - Check responsive design
    - Test navigation menu

    7. **✅ Browser Cache Test**:
    - Clear browser cache (Ctrl+Shift+Delete)
    - Reload website
    - Verify latest content loads

    8. **✅ Security Headers Test**:
    - Go to: https://securityheaders.com/
    - Enter your domain: `https://luvora.com`
    - Check security rating

    9. **✅ SSL Certificate Test**:
    - Go to: https://www.ssllabs.com/ssltest/
    - Enter your domain
    - Should get A or A+ rating

    10. **✅ Performance Test**:
        - Go to: https://pagespeed.web.dev/
        - Enter your domain
        - Check performance scores

    ---

    ## Updating Your Website

    ### When You Add/Edit Products

    ```powershell
    # 1. Edit products.json locally
    code C:\Himanshu\REPOS\luvora\static-catalog\data\products.json

    # 2. Save changes

    # 3. Upload to S3
    cd C:\Himanshu\REPOS\luvora\static-catalog
    aws s3 sync . s3://luvora-catalog --delete

    # 4. Invalidate CloudFront cache (so changes appear immediately)
    aws cloudfront create-invalidation --distribution-id YOUR_DISTRIBUTION_ID --paths "/*"

    # Get Distribution ID:
    # CloudFront Console → Your distribution → ID (e.g., E1234ABCDEFGHI)
    ```

    **Or use PowerShell script:**

    ```powershell
    cd static-catalog
    .\deploy.ps1

    # Then manually invalidate CloudFront:
    # AWS Console → CloudFront → Your distribution → Invalidations tab
    # Click "Create invalidation"
    # Object paths: /*
    # Click "Create invalidation"
    # Wait 3-5 minutes
    ```

    ### When You Update HTML/CSS/JS Files

    Same process as above:

    1. Edit files locally
    2. Save changes
    3. Sync to S3: `aws s3 sync . s3://luvora-catalog --delete`
    4. Invalidate CloudFront cache: `aws cloudfront create-invalidation --distribution-id XXXXXXX --paths "/*"`

    **CloudFront Cache Behavior:**
    - Without invalidation: Changes may take 24 hours to appear (default TTL)
    - With invalidation: Changes appear in 3-5 minutes
    - First 1000 invalidation paths per month are free

    ### Adding New Product Images

    ```powershell
    # 1. Add images to local folder
    copy path\to\new-product.jpg C:\Himanshu\REPOS\luvora\static-catalog\images\

    # 2. Upload to S3
    cd C:\Himanshu\REPOS\luvora\static-catalog
    aws s3 sync images/ s3://luvora-catalog/images/

    # 3. Update products.json with image path
    # "image": "images/new-product.jpg"

    # 4. Upload products.json
    aws s3 cp data/products.json s3://luvora-catalog/data/products.json

    # 5. Invalidate cache
    aws cloudfront create-invalidation --distribution-id XXXXXXX --paths "/data/products.json" "/images/*"
    ```

    ---

    ## Cost Estimation

    ### Real Monthly Cost Examples

    **Scenario 1: Small Business (500 visitors/month)**
    - S3 Storage (1GB): $0.023
    - S3 GET Requests (10,000): $0.004
    - CloudFront Data Transfer (10GB): $0 (free tier)
    - Route 53 Hosted Zone: $0.50
    - **Total: ~$0.53/month** 💰

    **Scenario 2: Growing Business (5,000 visitors/month)**
    - S3 Storage (2GB): $0.046
    - S3 GET Requests (100,000): $0.04
    - CloudFront Data Transfer (50GB): $0 (free tier)
    - Route 53 Hosted Zone: $0.50
    - **Total: ~$0.59/month** 💰

    **Scenario 3: Established Business (20,000 visitors/month)**
    - S3 Storage (5GB): $0.115
    - S3 GET Requests (500,000): $0.20
    - CloudFront Data Transfer (200GB): $0 (free tier)
    - Route 53 Hosted Zone: $0.50
    - **Total: ~$0.82/month** 💰

    **Scenario 4: Popular Site (100,000 visitors/month)**
    - S3 Storage (10GB): $0.23
    - S3 GET Requests (2M): $0.80
    - CloudFront Data Transfer (1TB+): $0 (free tier, then $85/TB)
    - Route 53 Hosted Zone: $0.50
    - **Total: ~$1.53/month** (within free tier) 💰

    ### AWS Free Tier (First 12 Months)
    - S3: 5GB storage, 20,000 GET requests
    - CloudFront: 1TB data transfer, 10M HTTP/HTTPS requests
    - Certificate Manager: **Always free**
    - Route 53: **Not** in free tier ($0.50/month)

    ---

    ## Troubleshooting

    ### Issue: "Access Denied" when accessing S3 URL

    **Solution:**
    ```powershell
    # Check bucket policy allows public read
    aws s3api get-bucket-policy --bucket luvora-catalog

    # If missing, apply policy:
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
    ```

    ### Issue: Products not loading (products.json returns 404)

    **Solution:**
    ```powershell
    # Verify products.json exists in S3
    aws s3 ls s3://luvora-catalog/data/

    # Should show: products.json

    # If missing, upload:
    aws s3 cp data/products.json s3://luvora-catalog/data/products.json

    # Check browser console (F12) for actual error
    ```

    ### Issue: SSL certificate not validating

    **Solutions:**
    1. Ensure certificate is in **us-east-1** region
    2. Check Route 53 has CNAME records for validation
    3. Wait 30 minutes (can take up to 24 hours)
    4. Verify nameservers are propagated: `nslookup -type=ns luvora.com`

    ### Issue: Domain not resolving to CloudFront

    **Solutions:**
    ```powershell
    # Check DNS records
    nslookup luvora.com

    # Should return CloudFront IPs, not S3 or nothing

    # If wrong, check Route 53:
    # 1. Hosted zone exists for luvora.com
    # 2. A records point to CloudFront distribution (Alias)
    # 3. Nameservers at registrar match Route 53 NS records
    ```

    ### Issue: Changes not appearing on website

    **Solution:**
    ```powershell
    # Invalidate CloudFront cache
    aws cloudfront create-invalidation \
    --distribution-id E1234ABCDEFGHI \
    --paths "/*"

    # Wait 3-5 minutes, then clear browser cache and reload
    ```

    ### Issue: "Certificate doesn't match domain"

    **Solution:**
    - Ensure SSL certificate includes both `luvora.com` AND `www.luvora.com`
    - Certificate status must be "Issued" (not Pending)
    - CloudFront alternate domain names (CNAMEs) must match certificate

    ### Issue: Images not displaying

    **Solutions:**
    ```powershell
    # Check image paths in products.json
    # Should be: "images/product.jpg" (not "/images/..." or "C:\...")

    # Verify images uploaded to S3
    aws s3 ls s3://luvora-catalog/images/

    # Check browser console for 404 errors
    # Re-upload missing images:
    aws s3 sync images/ s3://luvora-catalog/images/ --acl public-read
    ```

    ### Issue: Website loads but styling broken

    **Solution:**
    ```powershell
    # Check CSS path in HTML files
    # Should be: "css/style.css" (relative path)

    # Verify CSS uploaded
    aws s3 ls s3://luvora-catalog/css/

    # Check browser console for CSS 404 errors
    # Re-upload CSS:
    aws s3 cp css/style.css s3://luvora-catalog/css/style.css
    ```

    ### Issue: High AWS bill

    **Check costs:**
    1. AWS Console → Billing → Bills
    2. Check by service:
    - S3: Should be ~$0.02-0.50
    - CloudFront: Should be $0 (free tier) or minimal
    - Route 53: $0.50/month
    3. If unexpectedly high:
    - Check for unexpected CloudFront data transfer
    - Look for S3 storage accumulation (old files)
    - Check CloudFront cache hit ratio

    **Reduce costs:**
    ```powershell
    # Remove old/unused files from S3
    aws s3 rm s3://luvora-catalog/old-images/ --recursive

    # Enable CloudFront compression
    # CloudFront Console → Distribution → Behaviors → Edit
    # Compress objects automatically: Yes
    ```

    ---

    ## Quick Reference Commands

    ### Daily Operations

    ```powershell
    # Upload changes to S3
    cd C:\Himanshu\REPOS\luvora\static-catalog
    aws s3 sync . s3://luvora-catalog --delete

    # Invalidate CloudFront cache
    aws cloudfront create-invalidation --distribution-id E123456 --paths "/*"

    # Check what's in S3 bucket
    aws s3 ls s3://luvora-catalog --recursive

    # Download backup from S3
    aws s3 sync s3://luvora-catalog ./backup/
    ```

    ### AWS Console URLs

    - **S3 Buckets**: https://s3.console.aws.amazon.com/s3/buckets
    - **CloudFront**: https://console.aws.amazon.com/cloudfront/
    - **Route 53**: https://console.aws.amazon.com/route53/
    - **Certificate Manager**: https://console.aws.amazon.com/acm/ (us-east-1)
    - **IAM Users**: https://console.aws.amazon.com/iam/
    - **Billing**: https://console.aws.amazon.com/billing/

    ---

    ## Next Steps After Deployment

    1. **✅ Test Everything**: Go through testing checklist above
    2. **✅ Set Up Billing Alert**:
    - AWS Console → Billing → Budgets
    - Create budget: $5/month threshold
    - Email alert when 80% reached
    3. **✅ Enable CloudWatch Monitoring** (optional):
    - Track website traffic
    - Monitor errors
    - Set up alarms
    4. **✅ Add Google Analytics** (optional):
    - Track visitor behavior
    - Measure conversions
    - Understand audience
    5. **✅ Submit to Search Engines**:
    - Google Search Console: https://search.google.com/search-console
    - Bing Webmaster Tools: https://www.bing.com/webmasters
    6. **✅ Create Backup Strategy**:
    - Export S3 bucket regularly
    - Store products.json in version control
    - Keep local copy of all images

    ---

    ## Additional Resources

    - **AWS S3 Documentation**: https://docs.aws.amazon.com/s3/
    - **CloudFront Documentation**: https://docs.aws.amazon.com/cloudfront/
    - **Route 53 Documentation**: https://docs.aws.amazon.com/route53/
    - **AWS Free Tier Details**: https://aws.amazon.com/free/
    - **AWS Pricing Calculator**: https://calculator.aws/
    - **AWS Support**: https://console.aws.amazon.com/support/

    ---

    ## Support

    If you encounter issues:
    1. Check this troubleshooting section
    2. Review AWS CloudWatch logs
    3. Check browser console (F12) for JavaScript errors
    4. Contact AWS Support (if you have a support plan)

    ---

    **Last Updated**: January 2026  
    **Estimated Setup Time**: 2-3 hours (including DNS propagation)  
    **Monthly Cost**: $1-3 for typical small business traffic  
    **Difficulty**: Medium (requires careful attention to detail)

    **Good luck with your deployment! 🚀**
