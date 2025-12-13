# PowerShell deployment script for AWS S3

# Configuration
$BUCKET_NAME = "luvora-catalog"
$REGION = "ap-south-1"
$CLOUDFRONT_DIST_ID = ""  # Optional: Add if using CloudFront

Write-Host "🚀 Deploying LUVORA Static Catalog to S3..." -ForegroundColor Cyan
Write-Host "================================================" -ForegroundColor Cyan

# Check if AWS CLI is installed
try {
    aws --version | Out-Null
    Write-Host "✓ AWS CLI configured" -ForegroundColor Green
} catch {
    Write-Host "❌ AWS CLI not found. Please install it first:" -ForegroundColor Red
    Write-Host "   Download from: https://aws.amazon.com/cli/" -ForegroundColor Yellow
    Write-Host "   Then run: aws configure" -ForegroundColor Yellow
    exit 1
}

# Check if AWS credentials are configured
try {
    aws sts get-caller-identity 2>&1 | Out-Null
    if ($LASTEXITCODE -ne 0) { throw }
} catch {
    Write-Host "❌ AWS credentials not configured. Run:" -ForegroundColor Red
    Write-Host "   aws configure" -ForegroundColor Yellow
    exit 1
}

# Sync files to S3
Write-Host ""
Write-Host "📤 Uploading files to S3..." -ForegroundColor Cyan
aws s3 sync . "s3://$BUCKET_NAME/" `
    --exclude ".git/*" `
    --exclude "*.sh" `
    --exclude "*.ps1" `
    --exclude "README.md" `
    --exclude ".DS_Store" `
    --delete `
    --region $REGION

if ($LASTEXITCODE -eq 0) {
    Write-Host "✅ Files uploaded successfully!" -ForegroundColor Green
} else {
    Write-Host "❌ Upload failed!" -ForegroundColor Red
    exit 1
}

# Set proper content types
Write-Host ""
Write-Host "🔧 Setting content types..." -ForegroundColor Cyan

# HTML files
aws s3 cp "s3://$BUCKET_NAME/" "s3://$BUCKET_NAME/" `
    --exclude "*" `
    --include "*.html" `
    --content-type "text/html" `
    --metadata-directive REPLACE `
    --recursive `
    --region $REGION

# CSS files
aws s3 cp "s3://$BUCKET_NAME/" "s3://$BUCKET_NAME/" `
    --exclude "*" `
    --include "*.css" `
    --content-type "text/css" `
    --metadata-directive REPLACE `
    --recursive `
    --region $REGION

# JavaScript files
aws s3 cp "s3://$BUCKET_NAME/" "s3://$BUCKET_NAME/" `
    --exclude "*" `
    --include "*.js" `
    --content-type "application/javascript" `
    --metadata-directive REPLACE `
    --recursive `
    --region $REGION

# JSON files
aws s3 cp "s3://$BUCKET_NAME/" "s3://$BUCKET_NAME/" `
    --exclude "*" `
    --include "*.json" `
    --content-type "application/json" `
    --metadata-directive REPLACE `
    --recursive `
    --region $REGION

Write-Host "✅ Content types set!" -ForegroundColor Green

# Invalidate CloudFront cache (if using)
if ($CLOUDFRONT_DIST_ID) {
    Write-Host ""
    Write-Host "🔄 Invalidating CloudFront cache..." -ForegroundColor Cyan
    aws cloudfront create-invalidation `
        --distribution-id $CLOUDFRONT_DIST_ID `
        --paths "/*"
    
    if ($LASTEXITCODE -eq 0) {
        Write-Host "✅ CloudFront cache invalidated!" -ForegroundColor Green
    } else {
        Write-Host "⚠️  CloudFront invalidation failed (non-critical)" -ForegroundColor Yellow
    }
}

Write-Host ""
Write-Host "================================================" -ForegroundColor Cyan
Write-Host "🎉 Deployment Complete!" -ForegroundColor Green
Write-Host ""
Write-Host "Your site is live at:" -ForegroundColor Cyan
Write-Host "http://$BUCKET_NAME.s3-website-$REGION.amazonaws.com" -ForegroundColor Yellow
Write-Host ""
Write-Host "If using CloudFront, check your distribution URL." -ForegroundColor Gray
Write-Host "================================================" -ForegroundColor Cyan
