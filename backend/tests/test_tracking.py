from django.contrib.auth import get_user_model
from django.utils import timezone
from rest_framework.test import APITestCase

from apps.catalog.models import SupplierProfile
from apps.orders.models import Delivery, Order, OrderStatus
from apps.tracking.models import TrackingEvent
from apps.users.models import UserAddress

User = get_user_model()


class StatusTransitionTests(APITestCase):
    def setUp(self):
        self.customer = User.objects.create_user(phone='998944444441', role='customer')
        self.driver = User.objects.create_user(phone='998944444442', role='driver')
        supplier_user = User.objects.create_user(phone='998944444443', role='supplier')
        supplier = SupplierProfile.objects.create(user=supplier_user, company_name='C', is_approved=True)
        address = UserAddress.objects.create(user=self.customer, name='A', city='T', street='S')
        self.order = Order.objects.create(
            customer=self.customer,
            supplier=supplier,
            address=address,
            payment_method='cash',
            subtotal='100000.00',
            delivery_fee='20000.00',
            total_amount='120000.00',
            delivery_slot=timezone.now(),
        )
        Delivery.objects.create(order=self.order, scheduled_time=timezone.now(), fee='20000.00', driver=self.driver)
        TrackingEvent.objects.create(order=self.order, status=OrderStatus.PREPARING)
        self.client.force_authenticate(self.driver)

    def test_transition_to_delivered(self):
        accept = self.client.post(f'/api/v1/tracking/driver/orders/{self.order.id}/accept/', {}, format='json')
        complete = self.client.post(f'/api/v1/tracking/driver/orders/{self.order.id}/complete/', {}, format='json')
        self.order.refresh_from_db()
        self.assertEqual(accept.status_code, 200)
        self.assertEqual(complete.status_code, 200)
        self.assertEqual(self.order.status, OrderStatus.DELIVERED)
