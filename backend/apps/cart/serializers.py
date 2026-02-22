from collections import defaultdict
from decimal import Decimal

from rest_framework import serializers

from apps.common.utils import haversine_km
from apps.users.models import UserAddress
from .models import Cart, CartItem


class CartItemSerializer(serializers.ModelSerializer):
    offer_id = serializers.IntegerField(source='supplier_offer_id', read_only=True)
    product_name = serializers.CharField(source='supplier_offer.product.name', read_only=True)
    supplier_name = serializers.CharField(source='supplier_offer.supplier.company_name', read_only=True)
    unit_price = serializers.DecimalField(source='supplier_offer.price', max_digits=12, decimal_places=2, read_only=True)
    line_total = serializers.SerializerMethodField()

    class Meta:
        model = CartItem
        fields = ['id', 'offer_id', 'product_name', 'supplier_name', 'quantity', 'unit_price', 'line_total']

    def get_line_total(self, obj):
        return obj.quantity * obj.supplier_offer.price


class CartSerializer(serializers.ModelSerializer):
    items = CartItemSerializer(many=True, read_only=True)
    items_subtotal = serializers.SerializerMethodField()

    class Meta:
        model = Cart
        fields = ['id', 'items', 'items_subtotal']

    def get_items_subtotal(self, obj):
        total = sum(item.quantity * item.supplier_offer.price for item in obj.items.select_related('supplier_offer'))
        return Decimal(total).quantize(Decimal('1.00'))


class AddCartItemSerializer(serializers.Serializer):
    supplier_offer_id = serializers.IntegerField()
    quantity = serializers.IntegerField(min_value=1)


class CheckoutSerializer(serializers.Serializer):
    address_id = serializers.IntegerField()
    delivery_slot = serializers.DateTimeField()
    payment_method = serializers.ChoiceField(choices=[('cash', 'Cash'), ('mockpay', 'MockPay'), ('payme', 'Payme'), ('click', 'Click'), ('uzum', 'Uzum')])

    def validate_address_id(self, value):
        user = self.context['request'].user
        if not UserAddress.objects.filter(id=value, user=user).exists():
            raise serializers.ValidationError('Address not found')
        return value


def estimate_delivery_fee(cart: Cart, address: UserAddress, base_fee: int, per_km_fee: int):
    by_supplier = defaultdict(list)
    for item in cart.items.select_related('supplier_offer__supplier'):
        by_supplier[item.supplier_offer.supplier_id].append(item)

    total = Decimal('0')
    for supplier_id, items in by_supplier.items():
        supplier = items[0].supplier_offer.supplier
        km = haversine_km(address.latitude, address.longitude, supplier.latitude, supplier.longitude)
        total += Decimal(base_fee + int(km * per_km_fee))
    return total.quantize(Decimal('1.00'))
