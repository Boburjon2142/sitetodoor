from decimal import Decimal

from django.conf import settings
from django.db import models


class OrderStatus(models.TextChoices):
    PREPARING = 'preparing', 'tayyorlanyapti'
    ON_THE_WAY = 'on_the_way', 'yo`lda'
    DELIVERED = 'delivered', 'yetkazildi'


class Order(models.Model):
    customer = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='orders', on_delete=models.CASCADE)
    supplier = models.ForeignKey('catalog.SupplierProfile', related_name='orders', on_delete=models.CASCADE)
    address = models.ForeignKey('users.UserAddress', related_name='orders', on_delete=models.PROTECT)
    status = models.CharField(max_length=20, choices=OrderStatus.choices, default=OrderStatus.PREPARING)
    payment_method = models.CharField(max_length=20)
    subtotal = models.DecimalField(max_digits=12, decimal_places=2)
    delivery_fee = models.DecimalField(max_digits=12, decimal_places=2)
    commission_amount = models.DecimalField(max_digits=12, decimal_places=2, default=Decimal('0.00'))
    total_amount = models.DecimalField(max_digits=12, decimal_places=2)
    delivery_slot = models.DateTimeField()
    created_at = models.DateTimeField(auto_now_add=True)


class OrderItem(models.Model):
    order = models.ForeignKey(Order, related_name='items', on_delete=models.CASCADE)
    product = models.ForeignKey('catalog.Product', on_delete=models.PROTECT)
    supplier_offer = models.ForeignKey('catalog.SupplierOffer', on_delete=models.PROTECT)
    quantity = models.PositiveIntegerField()
    unit_price = models.DecimalField(max_digits=12, decimal_places=2)
    line_total = models.DecimalField(max_digits=12, decimal_places=2)


class Delivery(models.Model):
    order = models.OneToOneField(Order, related_name='delivery', on_delete=models.CASCADE)
    scheduled_time = models.DateTimeField()
    distance_km = models.FloatField(default=0)
    fee = models.DecimalField(max_digits=12, decimal_places=2)
    driver = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='deliveries', null=True, blank=True, on_delete=models.SET_NULL)
