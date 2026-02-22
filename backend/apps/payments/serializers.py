from rest_framework import serializers

from .models import PaymentIntent


class PaymentIntentSerializer(serializers.ModelSerializer):
    class Meta:
        model = PaymentIntent
        fields = ['id', 'order', 'amount', 'provider', 'status', 'external_id', 'raw_payload', 'created_at']
