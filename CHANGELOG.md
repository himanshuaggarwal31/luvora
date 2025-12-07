# Changelog

All notable changes to LUVORA will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [1.1.0] - 2025-12-07

### Added
- **PDF Invoice Generation**: Professional branded invoices using ReportLab
- **Email Notifications**: Automated order confirmation emails with PDF attachments
- **Order Status Emails**: Notifications when order status changes
- **Test Mode for Payments**: Razorpay integration works without API keys for development
- **Management Command**: `test_invoice` command for testing invoice and email generation
- **Automated Setup Script**: `setup.bat` for Windows one-click installation
- **Page Creation Script**: `setup_pages.py` for automatic page structure setup
- Email templates (HTML and plain text versions)
- Console email backend for development testing
- Comprehensive payment integration documentation (PAYMENT_SETUP.md)
- Quick reference guide (INTEGRATION_COMPLETE.md)

### Changed
- **Upgraded Django**: 4.2 → 5.1.15
- **Upgraded Wagtail**: 5.2 → 6.4.2
- **Updated Pillow**: For compatibility with Wagtail 6.x and Python 3.12
- **Python Requirement**: Now requires Python 3.12+ (3.14 not yet supported)
- **Database Default**: Changed to SQLite for easier development setup
- **Product Template**: Fixed to use `page` context variable instead of `product`
- **URL Structure**: Products now use clean `/shop/product-name/` URLs
- Order model: Added automatic email sending on payment success
- Cart handling: Improved decimal serialization for session storage

### Fixed
- Python 3.14 compatibility issues (documented workaround: use Python 3.12)
- Wagtail page template context bug in product detail pages
- Product page hierarchy for proper URL generation
- Stock reduction and coupon usage tracking on payment
- Session serialization issues with Decimal types

### Security
- Payment signature verification
- Secure session handling
- CSRF protection maintained

### Documentation
- Updated README.md with current tech stack and features
- Updated QUICKSTART.md with automated setup instructions
- Updated GETTING_STARTED.md with Python version requirements
- Added PYTHON_VERSION_ISSUE.md for compatibility notes
- Added PAYMENT_SETUP.md for payment integration guide
- Added INTEGRATION_COMPLETE.md for feature overview
- Updated all .md files to reflect Django 5.1 and Wagtail 6.4

## [1.0.0] - 2025-12-06

### Added
- Initial release of LUVORA e-commerce platform
- Django 4.2 and Wagtail 5.2 integration
- Product management with Wagtail CMS
- Shopping cart functionality (session-based)
- Razorpay payment gateway integration
- Coupon system (percentage and fixed discounts)
- Order management system
- Inventory tracking
- Category-based product filtering
- Responsive Bootstrap 5 UI
- Oracle and PostgreSQL database support
- Docker containerization
- Nginx reverse proxy configuration
- Comprehensive documentation
- Admin panels (Wagtail + Django)
- Security features (CSRF, XSS protection)
- Gunicorn production server setup

### Features
- ✅ Full product CRUD via CMS
- ✅ Real-time cart updates
- ✅ Secure payment processing
- ✅ Order tracking
- ✅ Stock management
- ✅ Discount coupons
- ✅ Mobile-responsive design
- ✅ Production-ready deployment

## [Unreleased]

### Planned Features
- Email marketing integration
- Product reviews and ratings
- Wishlist functionality
- Multi-currency support
- Advanced analytics dashboard
- Inventory alerts
- Bulk product import/export
- Mobile app (React Native)
- Multi-language support
- Advanced shipping calculations

---

## Version History

- **1.1.0** (2025-12-07): Payment integration upgrade, invoice generation, email notifications
- **1.0.0** (2025-12-06): Initial release

---

For older changes, see [GitHub Releases](https://github.com/himanshuaggarwal31/luvora/releases).
