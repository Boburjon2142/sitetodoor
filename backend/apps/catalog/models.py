from decimal import Decimal

from django.conf import settings
from django.db import models


class ProductCategory(models.Model):
    name = models.CharField(max_length=120)
    slug = models.SlugField(unique=True)

    def __str__(self):
        return self.name


class Product(models.Model):
    category = models.ForeignKey(ProductCategory, related_name='products', on_delete=models.CASCADE)
    name = models.CharField(max_length=180)
    description = models.TextField(blank=True)
    unit = models.CharField(max_length=30, default='dona')

    def __str__(self):
        return self.name


class SupplierProfile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, related_name='supplier_profile', on_delete=models.CASCADE)
    company_name = models.CharField(max_length=180)
    is_approved = models.BooleanField(default=False)
    latitude = models.FloatField(blank=True, null=True)
    longitude = models.FloatField(blank=True, null=True)
    premium_rank = models.PositiveIntegerField(default=0)

    def __str__(self):
        return self.company_name


class SupplierOffer(models.Model):
    supplier = models.ForeignKey(SupplierProfile, related_name='offers', on_delete=models.CASCADE)
    product = models.ForeignKey(Product, related_name='offers', on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=12, decimal_places=2)
    stock = models.PositiveIntegerField(default=0)
    min_order_qty = models.PositiveIntegerField(default=1)
    delivery_eta_hours = models.PositiveIntegerField(default=24)
    is_active = models.BooleanField(default=True)

    class Meta:
        unique_together = ('supplier', 'product')

    def __str__(self):
        return f'{self.supplier.company_name} - {self.product.name}'

    @property
    def available(self):
        return self.stock > 0 and self.is_active
