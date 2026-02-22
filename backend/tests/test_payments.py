from django.contrib.auth import get_user_model
from rest_framework.test import APITestCase

from apps.orders.models import Order
from apps.payments.models import PaymentIntent, PaymentProviderType
from apps.users.models import UserAddress
from apps.catalog.models import ProductCategory, Product, SupplierProfile

User = get_user_model()


class WebhookIdempotencyTests(APITestCase):
    def setUp(self):
        customer = User.objects.create_user(phone='998933333331', role='customer')
        supplier_user = User.objects.create_user(phone='998933333332', role='supplier')
        supplier = SupplierProfile.objects.create(user=supplier_user, company_name='B', is_approved=True)
        address = UserAddress.objects.create(user=customer, name='A', city='T', street='S')
        self.order = Order.objects.create(
            customer=customer,
            supplier=supplier,
            address=address,
            payment_method='mockpay',
            subtotal='100000.00',
            delivery_fee='20000.00',
            total_amount='120000.00',
            delivery_slot='2026-01-01T10:00:00Z',
        )
        self.intent = PaymentIntent.objects.create(order=self.order, amount='120000.00', provider=PaymentProviderType.MOCK, external_id='mock-123')

    def test_idempotent_webhook(self):
        payload = {'external_id': 'mock-123', 'status': 'success'}
        headers = {'HTTP_X_IDEMPOTENCY_KEY': 'key-1'}
        first = self.client.post('/api/v1/payments/webhooks/mockpay/', payload, format='json', **headers)
        second = self.client.post('/api/v1/payments/webhooks/mockpay/', payload, format='json', **headers)
        self.assertEqual(first.status_code, 200)
        self.assertEqual(second.status_code, 200)
        self.intent.refresh_from_db()
        self.assertEqual(self.intent.idempotency_key, 'key-1')
