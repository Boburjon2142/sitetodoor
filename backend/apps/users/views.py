from django.utils import timezone
from rest_framework import generics, permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken

from .models import OTPCode, User, UserAddress
from .serializers import AddressSerializer, OTPRequestSerializer, OTPService, OTPVerifySerializer, UserSerializer
from .tasks import send_otp_task
from .throttles import OTPRateThrottle


class OTPRequestView(APIView):
    permission_classes = [permissions.AllowAny]
    throttle_classes = [OTPRateThrottle]

    def post(self, request):
        serializer = OTPRequestSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        phone = serializer.validated_data['phone']
        otp = OTPService.create_code(phone)
        send_otp_task.delay(phone, otp.code)
        return Response({'message': 'OTP yuborildi (mock)'}, status=status.HTTP_200_OK)


class OTPVerifyView(APIView):
    permission_classes = [permissions.AllowAny]
    throttle_classes = [OTPRateThrottle]

    def post(self, request):
        serializer = OTPVerifySerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        phone = serializer.validated_data['phone']
        code = serializer.validated_data['code']
        role = serializer.validated_data.get('role', 'customer')

        otp = OTPCode.objects.filter(phone=phone, is_used=False, expires_at__gte=timezone.now()).order_by('-created_at').first()
        if not otp or not otp.is_valid(code):
            return Response({'message': 'Noto`g`ri yoki muddati tugagan OTP'}, status=status.HTTP_400_BAD_REQUEST)

        otp.is_used = True
        otp.save(update_fields=['is_used'])
        user, _ = User.objects.get_or_create(phone=phone, defaults={'role': role})
        if user.role != role and user.role != 'admin':
            user.role = role
            user.save(update_fields=['role'])

        refresh = RefreshToken.for_user(user)
        return Response(
            {
                'access': str(refresh.access_token),
                'refresh': str(refresh),
                'user': UserSerializer(user).data,
            }
        )


class AddressListCreateView(generics.ListCreateAPIView):
    serializer_class = AddressSerializer

    def get_queryset(self):
        return UserAddress.objects.filter(user=self.request.user).order_by('-is_default', '-id')

    def perform_create(self, serializer):
        if serializer.validated_data.get('is_default'):
            UserAddress.objects.filter(user=self.request.user, is_default=True).update(is_default=False)
        serializer.save(user=self.request.user)


class AddressDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = AddressSerializer

    def get_queryset(self):
        return UserAddress.objects.filter(user=self.request.user)

    def perform_update(self, serializer):
        if serializer.validated_data.get('is_default'):
            UserAddress.objects.filter(user=self.request.user, is_default=True).exclude(id=self.get_object().id).update(is_default=False)
        serializer.save()
