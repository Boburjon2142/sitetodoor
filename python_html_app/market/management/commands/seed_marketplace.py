from decimal import Decimal
import os

from django.contrib.auth.models import User
from django.core.management.base import BaseCommand

from market.models import Category, NotificationSetting, Product, UserProfile


class Command(BaseCommand):
    help = "Seed marketplace categories, products and staff user"

    def handle(self, *args, **options):
        categories = [
            ("Qum", "qum", "Qurilish qumlari va fraksiyalar"),
            ("G'isht", "gisht", "Har xil o'lchamdagi g'isht mahsulotlari"),
            ("Sement", "sement", "Sement va quruq aralashmalar"),
            ("Asboblar", "asboblar", "Qurilish asbob-uskunalari"),
            ("Santexnika", "santexnika", "Truba, kran va boshqa santexnika mahsulotlari"),
            ("Elektr tovarlari", "elektr-tovarlari", "Kabellar, avtomatlar va aksessuarlar"),
            ("Issiqlik materiallari", "issiqlik-materiallari", "Izolyatsiya mahsulotlari"),
            ("Tom qoplamalari", "tom-qoplamalari", "Tom uchun qoplama va jihozlar"),
            ("Ventilyatsiya", "ventilyatsiya", "Havo almashinuvi jihozlari"),
            ("Bo'yoq va lak materiallari", "boyoq-lak", "Ichki va tashqi bo'yoqlar"),
        ]

        category_map = {}
        for name, slug, description in categories:
            category, _ = Category.objects.get_or_create(
                slug=slug,
                defaults={"name": name, "description": description},
            )
            category_map[slug] = category

        products = [
            ("M400 sement 50kg", "sement", "Bekobod", "Poydevor va beton ishlari uchun sifatli sement", "qop", 78000, 120, "SEM-001"),
            ("M500 sement 50kg", "sement", "Kyzylkum", "Yuqori mustahkam qurilish sementi", "qop", 86000, 70, "SEM-002"),
            ("Qizil g'isht 1-daraja", "gisht", "Qarshi Keramika", "Devor ko'tarish uchun qizil g'isht", "dona", 2200, 2500, "GIS-001"),
            ("Armatura 12mm", "asboblar", "Metall Invest", "Temir-beton ishlari uchun armatura", "metr", 15500, 800, "ARM-012"),
            ("Oq qum yuvilgan", "qum", "Qashqadaryo Qum", "Suvoq va bezak ishlari uchun yuvilgan qum", "m3", 185000, 25, "QUM-001"),
            ("Gazoblok D500", "issiqlik-materiallari", "Usta Blok", "Yengil va issiqlikni saqlovchi blok", "dona", 32000, 420, "BLK-001"),
            ("PPR truba 25mm", "santexnika", "Aqua Plast", "Suv tizimi uchun mustahkam truba", "metr", 12000, 350, "SAN-025"),
            ("NYM kabel 3x2.5", "elektr-tovarlari", "Artel Cable", "Uy ichki elektr montaji uchun kabel", "metr", 8500, 600, "ELK-325"),
            ("Metallocherepitsa", "tom-qoplamalari", "Roof Master", "Tom yopish uchun qoplama", "m2", 98000, 180, "TOM-001"),
            ("Ichki bo'yoq 10kg", "boyoq-lak", "UzColor", "Ichki devorlar uchun yuviladigan bo'yoq", "kg", 65000, 85, "BOY-010"),
            ("Ventilyator kanal 150mm", "ventilyatsiya", "Air Flow", "Oshxona va sexlar uchun ventilyator", "dona", 240000, 35, "VEN-150"),
            ("Perforator 850W", "asboblar", "Ingco", "Ta'mir va qurilish uchun elektr asbob", "dona", 780000, 14, "ASB-850"),
        ]

        for idx, (name, category_slug, brand, short, unit, price, stock, sku) in enumerate(products, start=1):
            Product.objects.get_or_create(
                sku=sku,
                defaults={
                    "name": name,
                    "category": category_map[category_slug],
                    "brand": brand,
                    "description_short": short,
                    "description_full": f"{name} Qarshi bozori va obyektlar uchun qulay yetkazib berish bilan taklif etiladi.",
                    "technical_specs": f"Brend: {brand}\nBirlik: {unit}\nSKU: {sku}\nMos hudud: Qarshi shahri va atrof tumanlar",
                    "price": Decimal(price),
                    "unit": unit,
                    "stock_quantity": stock,
                    "image": f"https://images.unsplash.com/photo-1541888946425-d81bb19240f5?auto=format&fit=crop&w=1200&q=80&sig={idx}",
                    "is_featured": idx <= 8,
                },
            )

        admin_username = os.getenv("DEMO_ADMIN_USERNAME", "admin")
        admin_password = os.getenv("DEMO_ADMIN_PASSWORD", "").strip()

        if admin_password and not User.objects.filter(username=admin_username).exists():
            admin_user = User.objects.create_superuser(admin_username, "admin@example.com", admin_password)
            UserProfile.objects.create(user=admin_user, phone="+998901234567")
            NotificationSetting.objects.create(user=admin_user)
            self.stdout.write(self.style.SUCCESS(f"Admin user created: {admin_username}"))
