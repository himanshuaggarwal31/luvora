#!/bin/bash
# Build script for deployment platforms

echo "🚀 Starting build process..."

# Install Python dependencies
echo "📦 Installing dependencies..."
pip install -r requirements.txt

# Collect static files
echo "📁 Collecting static files..."
python manage.py collectstatic --noinput

# Run migrations
echo "🗄️  Running database migrations..."
python manage.py migrate --noinput

# Create cache table
echo "💾 Creating cache table..."
python manage.py createcachetable || true

echo "✅ Build complete!"
