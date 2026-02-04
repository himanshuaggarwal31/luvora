# Query Form Setup Guide

## How User Queries Work

**Problem**: Static websites (S3) cannot directly save files or write to databases.

**Solutions**: Use third-party services or AWS serverless backend.

---

## Solution 1: Web3Forms (Recommended - FREE & Easy)

### ✅ Pros:
- 100% FREE (250 submissions/month)
- No backend needed
- Submissions sent to your email
- Access dashboard to view all queries
- 5 minute setup

### Setup Steps:

1. **Get Access Key** (2 minutes)
   - Go to https://web3forms.com/
   - Click "Get Started Free"
   - Enter your email (where queries will be sent)
   - Verify email
   - Copy your **Access Key**

2. **Update query.html** (1 minute)
   ```html
   <!-- Find this line in query.html -->
   <input type="hidden" name="access_key" value="YOUR_WEB3FORMS_ACCESS_KEY">
   
   <!-- Replace with your actual key -->
   <input type="hidden" name="access_key" value="abc123def456...">
   ```

3. **Test Locally** (1 minute)
   ```powershell
   cd C:\Himanshu\REPOS\luvora\static-catalog
   python -m http.server 8080
   start http://localhost:8080/query.html
   ```
   - Fill form and submit
   - Check your email for submission

4. **Upload to S3** (1 minute)
   ```powershell
   aws s3 sync . s3://luvora-catalog --delete
   ```

**✅ Done! You'll receive query emails + can view in Web3Forms dashboard**

---

## Solution 2: EmailJS (Alternative)

### Setup:

1. Go to https://www.emailjs.com/
2. Create account (free 200 emails/month)
3. Connect your Gmail
4. Get Service ID, Template ID, Public Key
5. Update query.html with EmailJS script

**Code for EmailJS:**
```html
<!-- Add before </body> -->
<script src="https://cdn.jsdelivr.net/npm/@emailjs/browser@3/dist/email.min.js"></script>
<script>
    emailjs.init('YOUR_PUBLIC_KEY');
    
    form.addEventListener('submit', (e) => {
        e.preventDefault();
        
        emailjs.sendForm('YOUR_SERVICE_ID', 'YOUR_TEMPLATE_ID', form)
            .then(() => {
                successMessage.style.display = 'block';
                form.reset();
            })
            .catch(() => {
                errorMessage.style.display = 'block';
            });
    });
</script>
```

---

## Solution 3: Formspree (Another Alternative)

1. Go to https://formspree.io/
2. Create account
3. Get form endpoint
4. Change form action:
   ```html
   <form action="https://formspree.io/f/YOUR_FORM_ID" method="POST">
   ```

---

## Solution 4: AWS Serverless (Advanced - Full AWS)

**If you want everything in AWS:**

### Architecture:
```
Static Website (S3)
    ↓ (AJAX POST)
API Gateway
    ↓
Lambda Function (Python/Node.js)
    ↓
DynamoDB (store queries) + SES (send email)
```

### Setup Steps:

1. **Create DynamoDB Table**
   - Table name: `luvora-queries`
   - Primary key: `queryId` (String)

2. **Create Lambda Function**
   ```python
   import json
   import boto3
   import uuid
   from datetime import datetime
   
   dynamodb = boto3.resource('dynamodb')
   table = dynamodb.Table('luvora-queries')
   
   def lambda_handler(event, context):
       # Parse form data
       body = json.loads(event['body'])
       
       # Save to DynamoDB
       query_id = str(uuid.uuid4())
       table.put_item(Item={
           'queryId': query_id,
           'name': body['name'],
           'email': body['email'],
           'phone': body.get('phone', ''),
           'category': body['category'],
           'message': body['message'],
           'timestamp': datetime.now().isoformat(),
           'status': 'new'
       })
       
       return {
           'statusCode': 200,
           'headers': {
               'Access-Control-Allow-Origin': '*',
               'Content-Type': 'application/json'
           },
           'body': json.dumps({'success': True, 'queryId': query_id})
       }
   ```

3. **Create API Gateway**
   - REST API
   - Create resource: `/submit-query`
   - Method: POST
   - Integration: Lambda function
   - Enable CORS

4. **Update query.html**
   ```javascript
   form.addEventListener('submit', async (e) => {
       e.preventDefault();
       
       const formData = {
           name: document.getElementById('name').value,
           email: document.getElementById('email').value,
           phone: document.getElementById('phone').value,
           category: document.getElementById('category').value,
           message: document.getElementById('message').value
       };
       
       const response = await fetch('https://YOUR_API_ID.execute-api.region.amazonaws.com/prod/submit-query', {
           method: 'POST',
           headers: { 'Content-Type': 'application/json' },
           body: JSON.stringify(formData)
       });
       
       if (response.ok) {
           successMessage.style.display = 'block';
           form.reset();
       }
   });
   ```

**Cost**: ~$0.20/month for 1000 queries (Lambda + DynamoDB free tier)

---

## Solution 5: Google Forms (Simplest - No Code)

1. Create Google Form
2. Add link to your website
3. Queries go to Google Sheets automatically

**HTML:**
```html
<a href="https://forms.gle/YOUR_FORM_ID" class="btn">Submit Query</a>
```

**Pros**: Zero setup, free, automatic spreadsheet  
**Cons**: Users leave your website

---

## Recommendation

**For your use case, I recommend Web3Forms:**
- ✅ FREE forever (250/month)
- ✅ Professional appearance (users stay on your site)
- ✅ Email notifications
- ✅ Dashboard to view queries
- ✅ No backend maintenance
- ✅ 5 minute setup

---

## Adding to Navigation

Update all pages (index.html, products.html, about.html, contact.html):

```html
<ul class="nav-menu">
    <li><a href="index.html">Home</a></li>
    <li><a href="products.html">Products</a></li>
    <li><a href="about.html">About</a></li>
    <li><a href="contact.html">Contact</a></li>
    <li><a href="query.html">Submit Query</a></li>
</ul>
```

---

## Testing Checklist

```powershell
# 1. Test locally
cd C:\Himanshu\REPOS\luvora\static-catalog
python -m http.server 8080
start http://localhost:8080/query.html

# 2. Submit test query
# 3. Check your email
# 4. Upload to S3
aws s3 sync . s3://luvora-catalog --delete

# 5. Test live
start https://d123456.cloudfront.net/query.html
```

---

## Viewing Submitted Queries

### Web3Forms:
- Login to https://web3forms.com/dashboard
- View all submissions
- Export as CSV
- Email notifications automatic

### AWS DynamoDB:
- AWS Console → DynamoDB → Tables → luvora-queries
- Click "Explore table items"
- View/search/filter queries

### EmailJS:
- Login to EmailJS dashboard
- View sent emails
- Check Gmail inbox

---

## Security Notes

1. **Spam Protection**: Web3Forms includes honeypot + reCAPTCHA
2. **Rate Limiting**: Built into all services
3. **Email Verification**: Users can't fake sender
4. **Data Privacy**: Submissions are secure (HTTPS)

---

## Cost Comparison

| Solution | Free Tier | Cost After |
|----------|-----------|------------|
| Web3Forms | 250/month | $9/month for 1000 |
| EmailJS | 200/month | $13/month for 1000 |
| Formspree | 50/month | $10/month for 1000 |
| AWS Serverless | 1M requests | ~$0.20 per 1000 |
| Google Forms | Unlimited | FREE |

---

## Next Steps

1. Choose solution (I recommend Web3Forms)
2. Get access key
3. Update query.html
4. Test locally
5. Upload to S3
6. Share query page: `https://luvora.com/query.html`

**Need help?** Let me know which solution you choose and I'll help set it up!
