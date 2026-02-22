from rest_framework import serializers

from apps.payments.serializers import PaymentIntentSerializer
from .models import Delivery, Order, OrderItem


class OrderItemSerializer(serializers.ModelSerializer):
    product_name = serializers.CharField(source='product.name', read_only=True)

    class Meta:
        model = OrderItem
        fields = ['id', 'product_name', 'quantity', 'unit_price', 'line_total']


class DeliverySerializer(serializers.ModelSerializer):
    class Meta:
        model = Delivery
        fields = ['scheduled_time', 'distance_km', 'fee', 'driver']


class OrderSerializer(serializers.ModelSerializer):
    items = OrderItemSerializer(many=True, read_only=True)
    delivery = DeliverySerializer(read_only=True)

    class Meta:
        model = Order
        fields = [
            'id', 'status', 'payment_method', 'subtotal', 'delivery_fee',
            'total_amount', 'delivery_slot', 'created_at', 'items', 'delivery',
        ]


class OrderAdminSerializer(OrderSerializer):
    payment_intents = PaymentIntentSerializer(many=True, read_only=True)

    class Meta(OrderSerializer.Meta):
        fields = OrderSerializer.Meta.fields + ['commission_amount', 'payment_intents']
