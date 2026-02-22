from rest_framework import serializers

from .models import DriverLocation, TrackingEvent


class TrackingEventSerializer(serializers.ModelSerializer):
    class Meta:
        model = TrackingEvent
        fields = ['id', 'status', 'note', 'created_at']


class DriverLocationSerializer(serializers.ModelSerializer):
    class Meta:
        model = DriverLocation
        fields = ['id', 'order', 'latitude', 'longitude', 'created_at']
        read_only_fields = ['id', 'created_at']
