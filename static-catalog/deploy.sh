#!/bin/bash
# Deployment script for AWS S3

# Configuration
BUCKET_NAME="luvora-catalog"
REGION="ap-south-1"
CLOUDFRONT_DIST_ID=""  # Optional: Add if using CloudFront

echo "🚀 Deploying LUVORA Static Catalog to S3..."
echo "================================================"

# Check if AWS CLI is installed
if ! command -v aws &> /dev/null; then
    echo "❌ AWS CLI not found. Please install it first:"
    echo "   pip install awscli"
    echo "   aws configure"
    exit 1
fi

# Check if AWS credentials are configured
if ! aws sts get-caller-identity &> /dev/null; then
    echo "❌ AWS credentials not configured. Run:"
    echo "   aws configure"
    exit 1
fi

echo "✓ AWS CLI configured"

# Sync files to S3
echo ""
echo "📤 Uploading files to S3..."
aws s3 sync . s3://$BUCKET_NAME/ \
    --exclude ".git/*" \
    --exclude "*.sh" \
    --exclude "README.md" \
    --exclude ".DS_Store" \
    --delete \
    --region $REGION

if [ $? -eq 0 ]; then
    echo "✅ Files uploaded successfully!"
else
    echo "❌ Upload failed!"
    exit 1
fi

# Set proper content types
echo ""
echo "🔧 Setting content types..."
aws s3 cp s3://$BUCKET_NAME/ s3://$BUCKET_NAME/ \
    --exclude "*" \
    --include "*.html" \
    --content-type "text/html" \
    --metadata-directive REPLACE \
    --recursive \
    --region $REGION

aws s3 cp s3://$BUCKET_NAME/ s3://$BUCKET_NAME/ \
    --exclude "*" \
    --include "*.css" \
    --content-type "text/css" \
    --metadata-directive REPLACE \
    --recursive \
    --region $REGION

aws s3 cp s3://$BUCKET_NAME/ s3://$BUCKET_NAME/ \
    --exclude "*" \
    --include "*.js" \
    --content-type "application/javascript" \
    --metadata-directive REPLACE \
    --recursive \
    --region $REGION

aws s3 cp s3://$BUCKET_NAME/ s3://$BUCKET_NAME/ \
    --exclude "*" \
    --include "*.json" \
    --content-type "application/json" \
    --metadata-directive REPLACE \
    --recursive \
    --region $REGION

echo "✅ Content types set!"

# Invalidate CloudFront cache (if using)
if [ -n "$CLOUDFRONT_DIST_ID" ]; then
    echo ""
    echo "🔄 Invalidating CloudFront cache..."
    aws cloudfront create-invalidation \
        --distribution-id $CLOUDFRONT_DIST_ID \
        --paths "/*"
    
    if [ $? -eq 0 ]; then
        echo "✅ CloudFront cache invalidated!"
    else
        echo "⚠️  CloudFront invalidation failed (non-critical)"
    fi
fi

echo ""
echo "================================================"
echo "🎉 Deployment Complete!"
echo ""
echo "Your site is live at:"
echo "http://$BUCKET_NAME.s3-website-$REGION.amazonaws.com"
echo ""
echo "If using CloudFront, check your distribution URL."
echo "================================================"
