from datetime import timedelta

from django.contrib.auth import get_user_model
from django.utils import timezone
from rest_framework.test import APITestCase

from apps.users.models import OTPCode

User = get_user_model()


class OTPFlowTests(APITestCase):
    def test_otp_verify_success(self):
        phone = '998911111111'
        OTPCode.objects.create(phone=phone, code='123456', expires_at=timezone.now() + timedelta(minutes=5))
        response = self.client.post('/api/v1/auth/otp/verify/', {'phone': phone, 'code': '123456'}, format='json')
        self.assertEqual(response.status_code, 200)
        self.assertIn('access', response.data)
        self.assertTrue(User.objects.filter(phone=phone).exists())
