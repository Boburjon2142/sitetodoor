from collections import defaultdict
from decimal import Decimal

from django.db import transaction

from apps.cart.models import Cart
from apps.common.utils import haversine_km
from apps.payments.providers import create_payment_intent
from apps.tracking.models import TrackingEvent
from .models import Delivery, Order, OrderItem, OrderStatus


@transaction.atomic
def create_orders_from_cart(user, cart: Cart, address, delivery_slot, payment_method, delivery_fee, commission_percent):
    grouped = defaultdict(list)
    for item in cart.items.select_related('supplier_offer__supplier', 'supplier_offer__product'):
        grouped[item.supplier_offer.supplier_id].append(item)

    orders = []
    supplier_count = max(len(grouped.keys()), 1)
    per_supplier_delivery = (delivery_fee / supplier_count).quantize(Decimal('1.00'))

    for supplier_id, items in grouped.items():
        subtotal = sum(i.quantity * i.supplier_offer.price for i in items)
        subtotal = Decimal(subtotal).quantize(Decimal('1.00'))
        commission_amount = (subtotal * Decimal(commission_percent) / Decimal('100')).quantize(Decimal('1.00'))
        total = subtotal + per_supplier_delivery

        order = Order.objects.create(
            customer=user,
            supplier_id=supplier_id,
            address=address,
            payment_method=payment_method,
            subtotal=subtotal,
            delivery_fee=per_supplier_delivery,
            commission_amount=commission_amount,
            total_amount=total,
            delivery_slot=delivery_slot,
        )

        supplier = items[0].supplier_offer.supplier
        km = haversine_km(address.latitude, address.longitude, supplier.latitude, supplier.longitude)
        Delivery.objects.create(
            order=order,
            scheduled_time=delivery_slot,
            distance_km=km,
            fee=per_supplier_delivery,
        )

        for i in items:
            OrderItem.objects.create(
                order=order,
                product=i.supplier_offer.product,
                supplier_offer=i.supplier_offer,
                quantity=i.quantity,
                unit_price=i.supplier_offer.price,
                line_total=(i.supplier_offer.price * i.quantity),
            )

        TrackingEvent.objects.create(order=order, status=OrderStatus.PREPARING)
        create_payment_intent(order, payment_method)
        orders.append(order)

    cart.items.all().delete()
    return orders
