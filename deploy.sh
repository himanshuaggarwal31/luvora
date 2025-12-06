#!/bin/bash
# Deployment script for LUVORA

set -e

echo "🚀 Starting LUVORA deployment..."

# Colors for output
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

# Check if .env file exists
if [ ! -f .env ]; then
    echo -e "${RED}Error: .env file not found!${NC}"
    echo "Please create .env file from .env.example"
    exit 1
fi

echo -e "${YELLOW}Building Docker images...${NC}"
docker-compose build

echo -e "${YELLOW}Starting services...${NC}"
docker-compose up -d

echo -e "${YELLOW}Waiting for database to be ready...${NC}"
sleep 10

echo -e "${YELLOW}Running migrations...${NC}"
docker-compose exec web python manage.py migrate

echo -e "${YELLOW}Collecting static files...${NC}"
docker-compose exec web python manage.py collectstatic --noinput

echo -e "${GREEN}✅ Deployment completed successfully!${NC}"
echo -e "${GREEN}Application is running at: http://localhost${NC}"
echo ""
echo "To create a superuser, run:"
echo "  docker-compose exec web python manage.py createsuperuser"
echo ""
echo "To view logs, run:"
echo "  docker-compose logs -f"
