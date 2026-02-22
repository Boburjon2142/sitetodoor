from celery import shared_task

from apps.orders.models import Order, OrderStatus
from .models import DriverLocation


@shared_task
def simulate_driver_location(order_id: int):
    order = Order.objects.filter(id=order_id, status=OrderStatus.ON_THE_WAY).select_related('delivery').first()
    if not order or not order.delivery.driver_id:
        return

    base_lat = order.address.latitude or 41.3111
    base_lng = order.address.longitude or 69.2797
    DriverLocation.objects.create(
        order=order,
        driver_id=order.delivery.driver_id,
        latitude=base_lat + 0.001,
        longitude=base_lng + 0.001,
    )
