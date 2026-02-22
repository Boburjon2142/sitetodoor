from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.response import Response

from apps.common.permissions import IsAdmin
from .models import Order
from .serializers import OrderAdminSerializer, OrderSerializer


class OrderListView(generics.ListAPIView):
    serializer_class = OrderSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Order.objects.filter(customer=self.request.user).prefetch_related('items').select_related('delivery').order_by('-id')


class OrderDetailView(generics.RetrieveAPIView):
    serializer_class = OrderSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Order.objects.filter(customer=self.request.user).prefetch_related('items').select_related('delivery')


class AdminOrderListView(generics.ListAPIView):
    serializer_class = OrderAdminSerializer
    permission_classes = [IsAdmin]
    queryset = Order.objects.all().prefetch_related('items', 'payment_intents').select_related('delivery').order_by('-id')


class AssignDriverView(APIView):
    permission_classes = [IsAdmin]

    def post(self, request, pk):
        order = Order.objects.get(pk=pk)
        driver_id = request.data.get('driver_id')
        order.delivery.driver_id = driver_id
        order.delivery.save(update_fields=['driver'])
        return Response({'message': 'Driver biriktirildi'})
