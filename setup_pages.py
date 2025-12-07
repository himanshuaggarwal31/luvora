#!/usr/bin/env python
"""Script to create the initial Wagtail page structure"""
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'luvora_project.settings')
django.setup()

from wagtail.models import Page, Site
from home.models import HomePage
from shop.models import ProductIndexPage, ProductPage
from django.utils.text import slugify

def create_pages():
    """Create the initial page hierarchy"""
    
    # Get root page
    root = Page.objects.get(id=1)
    
    # Check if home already exists
    if HomePage.objects.exists():
        print("Home page already exists, skipping...")
        home = HomePage.objects.first()
    else:
        # Create Home page
        print('Creating Home page...')
        home = HomePage(
            title='Home',
            slug='home',
            show_in_menus=True
        )
        root.add_child(instance=home)
        home.save_revision().publish()
        print(f'✅ Home page created: {home.title} (ID: {home.id})')
        
        # Update or create the default site to point to our new home page
        site, created = Site.objects.get_or_create(
            is_default_site=True,
            defaults={
                'hostname': 'localhost',
                'port': 8000,
                'site_name': 'LUVORA',
                'root_page': home
            }
        )
        if not created:
            site.root_page = home
            site.save()
        print(f'✅ Site root updated to Home page')
    
    # Check if Shop already exists
    if ProductIndexPage.objects.exists():
        print("Shop page already exists, skipping...")
        shop = ProductIndexPage.objects.first()
    else:
        # Create Shop page (ProductIndexPage)
        print('Creating Shop page...')
        shop = ProductIndexPage(
            title='Shop',
            slug='shop',
            intro='<p>Browse our premium bedsheet collection</p>',
            show_in_menus=True
        )
        home.add_child(instance=shop)
        shop.save_revision().publish()
        print(f'✅ Shop page created: {shop.title} (ID: {shop.id})')
    
    # Create sample products if none exist
    if ProductPage.objects.exists():
        print(f"Products already exist ({ProductPage.objects.count()} found), skipping...")
    else:
        products_data = [
            {
                'title': 'Premium Cotton Bedsheet',
                'sku': 'BED-001',
                'price': 2599.00,
                'compare_price': 4999.00,
                'short_description': 'Luxurious 100% cotton bedsheet with superior comfort',
                'description': '<p>Experience ultimate comfort with our premium cotton bedsheets. Made from the finest quality cotton, these sheets are soft, breathable, and durable.</p>',
                'stock_quantity': 50,
                'is_available': True,
                'is_featured': True
            },
            {
                'title': 'Floral Print Bedsheet Set',
                'sku': 'BED-002',
                'price': 3999.00,
                'compare_price': 4599.00,
                'short_description': 'Beautiful floral design with matching pillowcases',
                'description': '<p>Add elegance to your bedroom with this stunning floral print bedsheet set. Includes one bedsheet and two matching pillowcases.</p>',
                'stock_quantity': 30,
                'is_available': True,
                'is_featured': False
            }
        ]
        
        for product_data in products_data:
            print(f'Creating product: {product_data["title"]}...')
            product = ProductPage(
                title=product_data['title'],
                slug=slugify(product_data['title']),
                sku=product_data['sku'],
                price=product_data['price'],
                compare_price=product_data.get('compare_price'),
                short_description=product_data['short_description'],
                description=product_data['description'],
                stock_quantity=product_data['stock_quantity'],
                is_available=product_data['is_available'],
                is_featured=product_data['is_featured'],
                show_in_menus=False
            )
            shop.add_child(instance=product)
            product.save_revision().publish()
            print(f'✅ Product created: {product.title} (ID: {product.id})')
    
    print('\n' + '='*60)
    print('✅ ALL PAGES CREATED SUCCESSFULLY!')
    print('='*60)
    print(f'\nSite structure:')
    print(f'  Root (ID: 1)')
    print(f'  └── Home (ID: {home.id}) ← Site Root')
    print(f'      └── Shop (ID: {shop.id}) → URL: /shop/')
    
    for product in ProductPage.objects.all():
        print(f'          └── {product.title} (ID: {product.id}) → URL: /shop/{product.slug}/')
    
    print(f'\n🌐 Visit: http://127.0.0.1:8000/')
    print(f'🛍️  Shop: http://127.0.0.1:8000/shop/')
    print(f'⚙️  Admin: http://127.0.0.1:8000/admin/')

if __name__ == '__main__':
    create_pages()
