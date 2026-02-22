from django.conf import settings
from django.db import models
from django.db.models import Avg


class SupplierReview(models.Model):
    supplier = models.ForeignKey('catalog.SupplierProfile', related_name='reviews', on_delete=models.CASCADE)
    customer = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='supplier_reviews', on_delete=models.CASCADE)
    rating = models.PositiveSmallIntegerField()
    comment = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('supplier', 'customer')

    @staticmethod
    def avg_rating_for_supplier(supplier_id):
        value = SupplierReview.objects.filter(supplier_id=supplier_id).aggregate(avg=Avg('rating'))['avg']
        return round(value or 0, 2)


class SupportTicket(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='support_tickets', on_delete=models.CASCADE)
    subject = models.CharField(max_length=180)
    message = models.TextField()
    is_open = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
