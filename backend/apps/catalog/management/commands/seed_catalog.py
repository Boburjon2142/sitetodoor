from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand

from apps.catalog.models import Product, ProductCategory, SupplierOffer, SupplierProfile

User = get_user_model()


class Command(BaseCommand):
    help = 'Seed demo catalog, suppliers and offers'

    def handle(self, *args, **options):
        categories = [
            ('Sement', 'cement'),
            ('Armatura', 'rebar'),
            ('Quruq aralashmalar', 'dry-mixes'),
        ]
        category_map = {}
        for name, slug in categories:
            category_map[slug], _ = ProductCategory.objects.get_or_create(slug=slug, defaults={'name': name})

        products_data = [
            ('M400 sement 50kg', 'cement', 'Qopda sement', 'qop'),
            ('M500 sement 50kg', 'cement', 'Yuqori mustahkam sement', 'qop'),
            ('Armatura 12mm', 'rebar', 'Metall armatura', 'metr'),
            ('Gips suvoq 25kg', 'dry-mixes', 'Ichki ishlar uchun', 'qop'),
        ]

        products = {}
        for name, slug, desc, unit in products_data:
            product, _ = Product.objects.get_or_create(
                name=name,
                defaults={'category': category_map[slug], 'description': desc, 'unit': unit},
            )
            products[name] = product

        supplier_users = [
            ('998900000002', 'supplier', 'Temir Market'),
            ('998900000005', 'supplier', 'Sement Usta'),
        ]

        supplier_profiles = []
        for phone, role, company in supplier_users:
            user, _ = User.objects.get_or_create(phone=phone, defaults={'role': role})
            profile, _ = SupplierProfile.objects.get_or_create(
                user=user,
                defaults={'company_name': company, 'is_approved': True, 'latitude': 41.3111, 'longitude': 69.2797},
            )
            supplier_profiles.append(profile)

        offer_data = [
            (supplier_profiles[0], products['M400 sement 50kg'], 78000, 220, 1, 6),
            (supplier_profiles[1], products['M400 sement 50kg'], 76000, 120, 1, 9),
            (supplier_profiles[0], products['Armatura 12mm'], 14500, 5000, 10, 5),
            (supplier_profiles[1], products['Gips suvoq 25kg'], 42000, 300, 1, 7),
        ]
        for supplier, product, price, stock, min_qty, eta in offer_data:
            SupplierOffer.objects.update_or_create(
                supplier=supplier,
                product=product,
                defaults={
                    'price': price,
                    'stock': stock,
                    'min_order_qty': min_qty,
                    'delivery_eta_hours': eta,
                    'is_active': True,
                },
            )

        self.stdout.write(self.style.SUCCESS('Catalog seeded successfully'))
