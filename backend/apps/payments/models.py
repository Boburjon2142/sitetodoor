from django.db import models


class PaymentProviderType(models.TextChoices):
    CASH = 'cash', 'Cash'
    MOCK = 'mockpay', 'MockPay'
    PAYME = 'payme', 'Payme'
    CLICK = 'click', 'Click'
    UZUM = 'uzum', 'Uzum'


class PaymentStatus(models.TextChoices):
    PENDING = 'pending', 'Pending'
    SUCCESS = 'success', 'Success'
    FAILED = 'failed', 'Failed'


class PaymentIntent(models.Model):
    order = models.ForeignKey('orders.Order', related_name='payment_intents', on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=12, decimal_places=2)
    provider = models.CharField(max_length=20, choices=PaymentProviderType.choices)
    status = models.CharField(max_length=20, choices=PaymentStatus.choices, default=PaymentStatus.PENDING)
    external_id = models.CharField(max_length=120, blank=True, null=True)
    idempotency_key = models.CharField(max_length=120, blank=True, null=True, unique=True)
    raw_payload = models.JSONField(default=dict, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
