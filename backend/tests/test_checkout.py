from datetime import timedelta

from django.contrib.auth import get_user_model
from django.utils import timezone
from rest_framework.test import APITestCase

from apps.cart.models import Cart, CartItem
from apps.catalog.models import Product, ProductCategory, SupplierOffer, SupplierProfile
from apps.users.models import UserAddress

User = get_user_model()


class CartCheckoutTests(APITestCase):
    def setUp(self):
        self.customer = User.objects.create_user(phone='998922222221', role='customer')
        self.supplier_user = User.objects.create_user(phone='998922222222', role='supplier')
        self.supplier = SupplierProfile.objects.create(user=self.supplier_user, company_name='Supplier A', latitude=41.3, longitude=69.2, is_approved=True)
        cat = ProductCategory.objects.create(name='Sement', slug='sement')
        prod = Product.objects.create(name='M400', category=cat, unit='qop')
        offer = SupplierOffer.objects.create(supplier=self.supplier, product=prod, price='70000.00', stock=50, min_order_qty=1)
        cart = Cart.objects.create(customer=self.customer)
        CartItem.objects.create(cart=cart, supplier_offer=offer, quantity=2)
        self.address = UserAddress.objects.create(user=self.customer, name='Site', city='Toshkent', street='X', latitude=41.2, longitude=69.1)

        self.client.force_authenticate(self.customer)

    def test_checkout_creates_order(self):
        response = self.client.post(
            '/api/v1/cart/checkout/',
            {
                'address_id': self.address.id,
                'delivery_slot': (timezone.now() + timedelta(hours=3)).isoformat(),
                'payment_method': 'mockpay',
            },
            format='json',
        )
        self.assertEqual(response.status_code, 200)
        self.assertTrue(len(response.data['orders']) >= 1)
