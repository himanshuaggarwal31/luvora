#!/bin/bash
# LUVORA Setup Script for Linux/Mac
# This script sets up the development environment

set -e

echo "========================================"
echo "LUVORA E-commerce Platform Setup"
echo "========================================"
echo

# Colors
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

# Check Python version
if ! command -v python3 &> /dev/null; then
    echo -e "${RED}[ERROR] Python 3 is not installed${NC}"
    echo "Please install Python 3.10+ from https://www.python.org/downloads/"
    exit 1
fi

echo -e "${GREEN}[1/8] Checking Python version...${NC}"
python3 --version

echo
echo -e "${GREEN}[2/8] Creating virtual environment...${NC}"
if [ -d ".venv" ]; then
    echo "Virtual environment already exists"
else
    python3 -m venv .venv
    echo "Virtual environment created"
fi

echo
echo -e "${GREEN}[3/8] Activating virtual environment...${NC}"
source .venv/bin/activate

echo
echo -e "${GREEN}[4/8] Upgrading pip...${NC}"
pip install --upgrade pip

echo
echo -e "${GREEN}[5/8] Installing dependencies...${NC}"
pip install -r requirements.txt

echo
echo -e "${GREEN}[6/8] Setting up environment file...${NC}"
if [ -f ".env" ]; then
    echo ".env file already exists"
else
    cp .env.example .env
    echo ".env file created - Please update with your credentials"
fi

echo
echo -e "${GREEN}[7/8] Creating logs directory...${NC}"
mkdir -p logs

echo
echo -e "${GREEN}[8/8] Running database migrations...${NC}"
python manage.py migrate

echo
echo "========================================"
echo -e "${GREEN}Setup Complete!${NC}"
echo "========================================"
echo
echo "Next steps:"
echo "  1. Update .env file with your database credentials"
echo "  2. Create a superuser: python manage.py createsuperuser"
echo "  3. Load sample data: python manage.py populate_sample_data"
echo "  4. Run server: python manage.py runserver"
echo
echo "For detailed instructions, see QUICKSTART.md"
echo
