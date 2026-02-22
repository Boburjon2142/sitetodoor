from datetime import timedelta
import random

from django.conf import settings
from django.utils import timezone
from rest_framework import serializers

from .models import OTPCode, User, UserAddress, UserRole


class OTPRequestSerializer(serializers.Serializer):
    phone = serializers.CharField(max_length=20)


class OTPVerifySerializer(serializers.Serializer):
    phone = serializers.CharField(max_length=20)
    code = serializers.CharField(max_length=6)
    role = serializers.ChoiceField(choices=UserRole.choices, required=False)


class AddressSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserAddress
        fields = ['id', 'name', 'city', 'street', 'latitude', 'longitude', 'is_default', 'created_at']
        read_only_fields = ['id', 'created_at']


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'phone', 'email', 'role']


class OTPService:
    @staticmethod
    def create_code(phone: str) -> OTPCode:
        code = f"{random.randint(100000, 999999)}"
        expires_at = timezone.now() + timedelta(seconds=settings.OTP_TTL_SECONDS)
        return OTPCode.objects.create(phone=phone, code=code, expires_at=expires_at)
