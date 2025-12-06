# Python Version Compatibility Issue

## Problem
The LUVORA project is currently running on **Python 3.14.2**, which has compatibility issues with Django and Wagtail.

### Error Details
```
AttributeError: 'super' object has no attribute 'dicts' and no __dict__ for setting new attributes
```

This error occurs in Django's template context copying mechanism and is caused by breaking changes in Python 3.14's `copy` module.

## Tested Versions
- **Django 4.2.27**: ❌ Not compatible with Python 3.14
- **Django 5.1.15**: ❌ Not compatible with Python 3.14
- **Wagtail 6.4.2**: ❌ Requires Django, also affected

## Solution

### Option 1: Use Python 3.12 or 3.13 (RECOMMENDED)
Python 3.12 or 3.13 are fully supported by both Django and Wagtail and will work without issues.

**Steps:**
1. Install Python 3.12 or 3.13 from https://www.python.org/downloads/
2. Delete the existing virtual environment:
   ```powershell
   Remove-Item -Recurse -Force .venv
   ```
3. Create a new virtual environment with Python 3.12/3.13:
   ```powershell
   python3.12 -m venv .venv
   # or
   python3.13 -m venv .venv
   ```
4. Activate and reinstall dependencies:
   ```powershell
   .venv\Scripts\activate.ps1
   pip install -r requirements.txt
   python manage.py migrate
   python manage.py createsuperuser
   python manage.py runserver
   ```

### Option 2: Wait for Django 5.2+ (NOT YET AVAILABLE)
Django 5.2 is expected to have full Python 3.14 support, but it hasn't been released yet.

## Current Status
- ✅ All dependencies installed
- ✅ Database migrations completed
- ✅ Code committed to GitHub
- ❌ Admin panel fails due to Python 3.14 incompatibility
- ❌ Template rendering fails

## Recommended Action
**Switch to Python 3.12 or 3.13 to continue development.**

Until then, the project structure, code, migrations, and configuration are all complete and pushed to GitHub at:
`https://github.com/himanshuaggarwal31/luvora.git`
