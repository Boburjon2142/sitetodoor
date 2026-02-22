from django.db import transaction
from rest_framework import status
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import PaymentIntent, PaymentStatus
from .providers import PROVIDERS
from .serializers import PaymentIntentSerializer


class PaymentIntentListView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        qs = PaymentIntent.objects.filter(order__customer=request.user).order_by('-id')
        return Response(PaymentIntentSerializer(qs, many=True).data)


class PaymentWebhookView(APIView):
    permission_classes = [AllowAny]

    @transaction.atomic
    def post(self, request, provider):
        idempotency_key = request.headers.get('X-Idempotency-Key') or request.data.get('idempotency_key')
        external_id = request.data.get('external_id')
        status_value = request.data.get('status', 'pending')

        if idempotency_key and PaymentIntent.objects.filter(idempotency_key=idempotency_key).exists():
            intent = PaymentIntent.objects.get(idempotency_key=idempotency_key)
            return Response(PaymentIntentSerializer(intent).data)

        intent = PaymentIntent.objects.filter(external_id=external_id, provider=provider).first()
        if not intent:
            return Response({'message': 'Payment not found'}, status=status.HTTP_404_NOT_FOUND)

        provider_impl = PROVIDERS[provider]
        signature = request.headers.get('X-Signature', '')
        if not provider_impl.verify_callback(request.data, signature):
            return Response({'message': 'Invalid signature'}, status=status.HTTP_400_BAD_REQUEST)

        intent.status = status_value if status_value in PaymentStatus.values else PaymentStatus.PENDING
        intent.idempotency_key = idempotency_key
        intent.raw_payload = request.data
        intent.save(update_fields=['status', 'idempotency_key', 'raw_payload', 'updated_at'])
        return Response(PaymentIntentSerializer(intent).data)
