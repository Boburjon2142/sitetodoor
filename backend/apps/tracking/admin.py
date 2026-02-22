from django.contrib import admin

from .models import DriverLocation, TrackingEvent

admin.site.register(TrackingEvent)
admin.site.register(DriverLocation)
