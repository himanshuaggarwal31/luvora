## Running Static Website Locally

### Quick Local Testing (Before Uploading to S3)

**You can test your static website on your computer RIGHT NOW without AWS!**

#### Method 1: Python HTTP Server (Recommended)

```powershell
# Navigate to static-catalog folder
cd C:\Himanshu\REPOS\luvora\static-catalog

# Start Python web server on port 8080
python -m http.server 8080

# Server starts immediately!
# Output: Serving HTTP on :: port 8080 (http://[::]:8080/) ...
```

**Access your website:**
```
http://localhost:8080/index.html
```

**All pages work:**
- Homepage: `http://localhost:8080/index.html`
- Products: `http://localhost:8080/products.html`
- About: `http://localhost:8080/about.html`
- Contact: `http://localhost:8080/contact.html`

**✅ Why use local server?**
- Test changes before uploading to S3
- JavaScript loads products.json correctly (doesn't work with file://)
- See exactly how it will look on S3/CloudFront
- No AWS costs while testing
- Instant feedback on changes

**Stop server:** Press `Ctrl+C` in the terminal

#### Method 2: VS Code Live Server Extension

1. Install "Live Server" extension in VS Code
2. Right-click `index.html` → "Open with Live Server"
3. Website opens automatically in browser
4. Auto-refreshes when you save changes

#### Method 3: Node.js http-server (Alternative)

```powershell
# Install globally (one time)
npm install -g http-server

# Run from static-catalog folder
cd C:\Himanshu\REPOS\luvora\static-catalog
http-server -p 8080

# Access: http://localhost:8080
```

---

## Adding & Managing Products

### How to Add New Products

**Products are stored in a simple JSON file** - easy to edit!

#### Step 1: Edit products.json

```powershell
# Open products file in your editor
code C:\Himanshu\REPOS\luvora\static-catalog\data\products.json

# Or use any text editor
notepad C:\Himanshu\REPOS\luvora\static-catalog\data\products.json
```

#### Step 2: Product Structure

**Each product looks like this:**
```json
{
  "id": 1,
  "name": "Premium Cotton Bedsheet",
  "slug": "premium-cotton-bedsheet",
  "price": 2999,
  "category": "Bedsheets",
  "image": "images/bedsheet1.jpg",
  "description": "Luxurious 100% cotton bedsheet with 400 thread count. Perfect for a comfortable night's sleep.",
  "features": [
    "100% Pure Cotton",
    "400 Thread Count",
    "Machine Washable",
    "Available in Queen & King sizes"
  ],
  "inStock": true
}
```

#### Step 3: Add Your Product

**Copy an existing product and modify:**

```json
[
  {
    "id": 1,
    "name": "Existing Product",
    ...
  },
  {
    "id": 2,
    "name": "Another Product",
    ...
  },
  {
    "id": 3,
    "name": "YOUR NEW PRODUCT NAME",
    "slug": "your-new-product-name",
    "price": 1999,
    "category": "Bedsheets",
    "image": "images/your-product.jpg",
    "description": "Your product description here. Make it compelling!",
    "features": [
      "Feature 1",
      "Feature 2",
      "Feature 3"
    ],
    "inStock": true
  }
]
```

**⚠️ Important:**
- Each product needs a **unique ID** (1, 2, 3, 4...)
- Add **comma** after previous product
- Keep all products inside `[ ]` brackets
- Use **double quotes** for text
- Price is a number (no quotes)

#### Step 4: Add Product Image

```powershell
# Copy your image to images folder
copy C:\path\to\your-product.jpg C:\Himanshu\REPOS\luvora\static-catalog\images\

# Reference it in products.json as:
# "image": "images/your-product.jpg"
```

**Image Requirements:**
- Format: JPG, PNG, WebP
- Recommended size: 800x800px or 1200x1200px
- Keep file size under 500KB for fast loading
- Use descriptive names: `cotton-bedsheet-blue.jpg`

#### Step 5: Test Locally

```powershell
# Start local server
cd C:\Himanshu\REPOS\luvora\static-catalog
python -m http.server 8080

# Open in browser
start http://localhost:8080/products.html

# Check:
# ✅ New product appears
# ✅ Image loads correctly
# ✅ Filtering/search works
# ✅ Price displays properly
```

#### Step 6: Upload to S3

```powershell
# Sync all changes to S3
cd C:\Himanshu\REPOS\luvora\static-catalog
aws s3 sync . s3://luvora-catalog --delete

# Or use PowerShell script
.\deploy.ps1

# If using CloudFront, invalidate cache
aws cloudfront create-invalidation --distribution-id YOUR_ID --paths "/*"
```

**✅ Done! Product is live on your website!**

---

### Quick Product Management

**Edit existing product:**
1. Open `products.json`
2. Find product by ID or name
3. Change any field (name, price, description, etc.)
4. Save file
5. Test locally → Upload to S3

**Remove product:**
1. Open `products.json`
2. Delete entire product object `{ ... }`
3. Remove comma if it's the last item
4. Save → Test → Upload

**Mark as out of stock:**
```json
"inStock": false
```

**Change price:**
```json
"price": 1499  // No quotes, just number
```

**Update image:**
1. Add new image to `images/` folder
2. Change `"image"` field in products.json
3. Upload both to S3

---

## Adding New Pages

### How to Create Additional Pages

**Want to add more pages? (FAQ, Blog, Gallery, etc.)**

#### Step 1: Create HTML File

```powershell
# Navigate to static-catalog folder
cd C:\Himanshu\REPOS\luvora\static-catalog

# Copy existing page as template
copy about.html faq.html

# Or create new file
code faq.html
```

#### Step 2: Basic Page Template

```html
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>FAQ - LUVORA</title>
    <link rel="stylesheet" href="css/style.css">
</head>
<body>
    <!-- Navigation (copy from index.html) -->
    <nav class="navbar">
        <div class="container">
            <div class="logo">LUVORA</div>
            <ul class="nav-menu">
                <li><a href="index.html">Home</a></li>
                <li><a href="products.html">Products</a></li>
                <li><a href="about.html">About</a></li>
                <li><a href="contact.html">Contact</a></li>
                <li><a href="faq.html" class="active">FAQ</a></li>
            </ul>
        </div>
    </nav>

    <!-- Your Content Here -->
    <section class="page-content">
        <div class="container">
            <h1>Frequently Asked Questions</h1>
            <p>Your content here...</p>
        </div>
    </section>

    <!-- Footer (copy from index.html) -->
    <footer>
        <div class="container">
            <p>&copy; 2026 LUVORA. All rights reserved.</p>
        </div>
    </footer>

    <script src="js/main.js"></script>
</body>
</html>
```

#### Step 3: Add to Navigation

**Update ALL pages** (index.html, products.html, about.html, contact.html):

```html
<ul class="nav-menu">
    <li><a href="index.html">Home</a></li>
    <li><a href="products.html">Products</a></li>
    <li><a href="about.html">About</a></li>
    <li><a href="contact.html">Contact</a></li>
    <li><a href="faq.html">FAQ</a></li>  <!-- New page -->
</ul>
```

#### Step 4: Test Locally

```powershell
# Start server
python -m http.server 8080

# Test new page
start http://localhost:8080/faq.html

# Check:
# ✅ Page loads
# ✅ Navigation works
# ✅ Styling applied
# ✅ Links work
```

#### Step 5: Upload to S3

```powershell
# Upload new page
aws s3 cp faq.html s3://luvora-catalog/faq.html

# Or sync entire folder
aws s3 sync . s3://luvora-catalog --delete

# Invalidate CloudFront cache (if using)
aws cloudfront create-invalidation --distribution-id YOUR_ID --paths "/faq.html"
```

---

### Common Page Ideas

**Easy pages to add:**

1. **FAQ Page** (`faq.html`)
   - Common questions and answers
   - Shipping info, returns policy

2. **Gallery** (`gallery.html`)
   - Product showcase
   - Customer photos

3. **Blog** (`blog.html`, `blog/post1.html`)
   - Create `blog/` folder
   - Add individual post HTML files

4. **Terms & Conditions** (`terms.html`)
   - Legal information
   - Privacy policy

5. **Size Guide** (`size-guide.html`)
   - Measurement charts
   - How to choose sizes

**Structure for blog:**
```
static-catalog/
├── blog.html              (blog listing page)
└── blog/
    ├── post1.html         (individual posts)
    ├── post2.html
    └── images/            (blog images)
```

---

## Complete Workflow Example

### Adding a New Product (Full Process)

**Let's add "Silk Pillowcase - Lavender":**

```powershell
# 1. Start local server for testing
cd C:\Himanshu\REPOS\luvora\static-catalog
python -m http.server 8080
# Keep this terminal open

# 2. In NEW terminal, add product image
copy C:\Downloads\silk-pillowcase.jpg C:\Himanshu\REPOS\luvora\static-catalog\images\

# 3. Edit products.json
code C:\Himanshu\REPOS\luvora\static-catalog\data\products.json
```

**Add to products.json:**
```json
{
  "id": 6,
  "name": "Silk Pillowcase - Lavender",
  "slug": "silk-pillowcase-lavender",
  "price": 899,
  "category": "Pillows",
  "image": "images/silk-pillowcase.jpg",
  "description": "Luxurious 100% mulberry silk pillowcase in calming lavender. Gentle on skin and hair.",
  "features": [
    "100% Mulberry Silk",
    "Hypoallergenic",
    "Hidden Zipper Closure",
    "Machine Washable"
  ],
  "inStock": true
}
```

```powershell
# 4. Test in browser (server already running)
start http://localhost:8080/products.html
# Check: ✅ Product appears, image loads, filtering works

# 5. Upload to S3
aws s3 sync . s3://luvora-catalog --delete

# 6. Invalidate CloudFront (if using custom domain)
aws cloudfront create-invalidation --distribution-id E123456 --paths "/*"

# 7. Verify live site
start https://luvora.com/products.html
# Or: start https://d123456.cloudfront.net/products.html
```

**✅ Done! Product is live in 5 minutes!**

---

