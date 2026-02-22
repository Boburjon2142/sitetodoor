from django.conf import settings
from django.db import models


class TrackingEvent(models.Model):
    order = models.ForeignKey('orders.Order', related_name='tracking_events', on_delete=models.CASCADE)
    status = models.CharField(max_length=20)
    note = models.CharField(max_length=255, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)


class DriverLocation(models.Model):
    order = models.ForeignKey('orders.Order', related_name='driver_locations', on_delete=models.CASCADE)
    driver = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='location_logs', on_delete=models.CASCADE)
    latitude = models.FloatField()
    longitude = models.FloatField()
    created_at = models.DateTimeField(auto_now_add=True)
