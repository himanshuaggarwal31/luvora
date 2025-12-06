"""
Management command to populate database with sample data for testing
"""
from django.core.management.base import BaseCommand
from django.utils import timezone
from datetime import timedelta
from decimal import Decimal
from wagtail.models import Page, Site

from shop.models import Category, ProductPage, Coupon, ProductIndexPage
from home.models import HomePage


class Command(BaseCommand):
    help = 'Populate database with sample data for testing'

    def add_arguments(self, parser):
        parser.add_argument(
            '--clear',
            action='store_true',
            help='Clear existing data before populating',
        )

    def handle(self, *args, **options):
        if options['clear']:
            self.stdout.write('Clearing existing data...')
            ProductPage.objects.all().delete()
            Category.objects.all().delete()
            Coupon.objects.all().delete()

        self.stdout.write('Creating sample data...')

        # Create categories
        categories = self._create_categories()
        self.stdout.write(self.style.SUCCESS(f'✓ Created {len(categories)} categories'))

        # Create products
        products = self._create_products(categories)
        self.stdout.write(self.style.SUCCESS(f'✓ Created {len(products)} products'))

        # Create coupons
        coupons = self._create_coupons()
        self.stdout.write(self.style.SUCCESS(f'✓ Created {len(coupons)} coupons'))

        # Setup homepage
        self._setup_homepage()
        self.stdout.write(self.style.SUCCESS('✓ Homepage configured'))

        self.stdout.write(self.style.SUCCESS('\n🎉 Sample data created successfully!'))
        self.stdout.write('\nTest coupons:')
        for coupon in coupons:
            self.stdout.write(f'  - {coupon.code}: {coupon.get_discount_display()}')

    def _create_categories(self):
        categories = [
            {'name': 'Electronics', 'description': 'Electronic devices and gadgets'},
            {'name': 'Fashion', 'description': 'Clothing and accessories'},
            {'name': 'Home & Living', 'description': 'Home essentials and decor'},
            {'name': 'Books', 'description': 'Books and educational materials'},
            {'name': 'Sports', 'description': 'Sports equipment and gear'},
        ]

        created = []
        for cat_data in categories:
            cat, _ = Category.objects.get_or_create(
                name=cat_data['name'],
                defaults={'description': cat_data['description'], 'is_active': True}
            )
            created.append(cat)

        return created

    def _create_products(self, categories):
        # Get or create ProductIndexPage
        home_page = Page.objects.get(depth=2)
        
        try:
            product_index = ProductIndexPage.objects.first()
            if not product_index:
                product_index = ProductIndexPage(
                    title='Shop',
                    intro='Browse our collection of products'
                )
                home_page.add_child(instance=product_index)
                product_index.save_revision().publish()
        except Exception as e:
            self.stdout.write(self.style.WARNING(f'Could not create ProductIndexPage: {e}'))
            return []

        products_data = [
            {
                'title': 'Wireless Bluetooth Headphones',
                'sku': 'ELEC001',
                'price': Decimal('2499.00'),
                'compare_price': Decimal('3499.00'),
                'category': categories[0],
                'short_description': 'Premium wireless headphones with noise cancellation',
                'description': '<p>High-quality wireless headphones with active noise cancellation, 30-hour battery life, and premium sound quality.</p>',
                'stock_quantity': 50,
                'is_featured': True,
            },
            {
                'title': 'Cotton T-Shirt - Black',
                'sku': 'FASH001',
                'price': Decimal('499.00'),
                'compare_price': Decimal('799.00'),
                'category': categories[1],
                'short_description': '100% cotton comfortable t-shirt',
                'description': '<p>Premium quality cotton t-shirt. Soft, breathable, and durable. Available in multiple sizes.</p>',
                'stock_quantity': 100,
                'is_featured': True,
            },
            {
                'title': 'Smart LED Desk Lamp',
                'sku': 'HOME001',
                'price': Decimal('1299.00'),
                'category': categories[2],
                'short_description': 'Adjustable LED desk lamp with USB charging',
                'description': '<p>Energy-efficient LED desk lamp with adjustable brightness, color temperature control, and built-in USB charging port.</p>',
                'stock_quantity': 30,
                'is_featured': False,
            },
            {
                'title': 'Python Programming Book',
                'sku': 'BOOK001',
                'price': Decimal('599.00'),
                'compare_price': Decimal('799.00'),
                'category': categories[3],
                'short_description': 'Learn Python programming from scratch',
                'description': '<p>Comprehensive guide to Python programming covering basics to advanced topics. Perfect for beginners and intermediate learners.</p>',
                'stock_quantity': 75,
                'is_featured': False,
            },
            {
                'title': 'Yoga Mat - Premium',
                'sku': 'SPORT001',
                'price': Decimal('899.00'),
                'category': categories[4],
                'short_description': 'Non-slip premium yoga mat',
                'description': '<p>Eco-friendly premium yoga mat with excellent grip and cushioning. Perfect for all types of yoga and fitness exercises.</p>',
                'stock_quantity': 40,
                'is_featured': True,
            },
        ]

        created = []
        for prod_data in products_data:
            try:
                product = ProductPage(
                    title=prod_data['title'],
                    sku=prod_data['sku'],
                    price=prod_data['price'],
                    compare_price=prod_data.get('compare_price'),
                    category=prod_data['category'],
                    short_description=prod_data['short_description'],
                    description=prod_data['description'],
                    stock_quantity=prod_data['stock_quantity'],
                    is_featured=prod_data['is_featured'],
                    is_available=True,
                    track_inventory=True,
                )
                product_index.add_child(instance=product)
                product.save_revision().publish()
                created.append(product)
            except Exception as e:
                self.stdout.write(self.style.WARNING(f'Could not create product {prod_data["title"]}: {e}'))

        return created

    def _create_coupons(self):
        now = timezone.now()
        coupons_data = [
            {
                'code': 'WELCOME10',
                'description': 'Welcome discount for new customers',
                'discount_type': 'percent',
                'value': Decimal('10.00'),
                'valid_from': now,
                'valid_to': now + timedelta(days=30),
            },
            {
                'code': 'SAVE500',
                'description': 'Save ₹500 on orders above ₹2000',
                'discount_type': 'fixed',
                'value': Decimal('500.00'),
                'minimum_purchase': Decimal('2000.00'),
                'valid_from': now,
                'valid_to': now + timedelta(days=30),
            },
            {
                'code': 'FLASH25',
                'description': 'Flash sale - 25% off',
                'discount_type': 'percent',
                'value': Decimal('25.00'),
                'valid_from': now,
                'valid_to': now + timedelta(days=7),
                'usage_limit': 100,
            },
        ]

        created = []
        for coupon_data in coupons_data:
            coupon, _ = Coupon.objects.get_or_create(
                code=coupon_data['code'],
                defaults=coupon_data
            )
            created.append(coupon)

        return created

    def _setup_homepage(self):
        """Configure homepage with sample content"""
        try:
            home = HomePage.objects.first()
            if home:
                home.hero_title = "Welcome to LUVORA"
                home.hero_subtitle = "Discover premium products curated just for you"
                home.hero_cta_text = "Shop Now"
                home.featured_title = "Featured Products"
                home.featured_description = "<p>Check out our handpicked selection of amazing products</p>"
                home.about_title = "About LUVORA"
                home.about_content = """<p>LUVORA is your destination for quality products at great prices. 
                We curate the best products across categories to bring you an exceptional shopping experience.</p>
                <p>Shop with confidence with our secure payment system and hassle-free returns.</p>"""
                home.save_revision().publish()
        except Exception as e:
            self.stdout.write(self.style.WARNING(f'Could not setup homepage: {e}'))
