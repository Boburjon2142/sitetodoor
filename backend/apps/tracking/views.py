from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.common.permissions import IsDriver
from apps.orders.models import Order, OrderStatus
from .models import DriverLocation, TrackingEvent
from .serializers import DriverLocationSerializer, TrackingEventSerializer
from .tasks import simulate_driver_location


class TrackingTimelineView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, order_id):
        order = Order.objects.get(id=order_id, customer=request.user)
        events = TrackingEvent.objects.filter(order=order).order_by('created_at')
        last_location = DriverLocation.objects.filter(order=order).order_by('-created_at').first()
        return Response(
            {
                'order_id': order.id,
                'status': order.status,
                'timeline': TrackingEventSerializer(events, many=True).data,
                'last_location': DriverLocationSerializer(last_location).data if last_location else None,
            }
        )


class DriverAcceptDeliveryView(APIView):
    permission_classes = [IsDriver]

    def post(self, request, order_id):
        order = Order.objects.get(id=order_id)
        if not order.delivery.driver_id:
            order.delivery.driver = request.user
            order.delivery.save(update_fields=['driver'])
        order.status = OrderStatus.ON_THE_WAY
        order.save(update_fields=['status'])
        TrackingEvent.objects.create(order=order, status=OrderStatus.ON_THE_WAY)
        simulate_driver_location.delay(order.id)
        return Response({'message': 'Yetkazib berish qabul qilindi'})


class DriverLocationUpdateView(APIView):
    permission_classes = [IsDriver]

    def post(self, request):
        serializer = DriverLocationSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        order = Order.objects.get(id=serializer.validated_data['order'].id)
        if order.delivery.driver_id != request.user.id and request.user.role != 'admin':
            return Response({'message': 'Bu buyurtma sizga tegishli emas'}, status=status.HTTP_403_FORBIDDEN)
        DriverLocation.objects.create(
            order=order,
            driver=request.user,
            latitude=serializer.validated_data['latitude'],
            longitude=serializer.validated_data['longitude'],
        )
        return Response({'message': 'Lokatsiya saqlandi'})


class DriverCompleteDeliveryView(APIView):
    permission_classes = [IsDriver]

    def post(self, request, order_id):
        order = Order.objects.get(id=order_id)
        if order.delivery.driver_id != request.user.id and request.user.role != 'admin':
            return Response({'message': 'Bu buyurtma sizga tegishli emas'}, status=status.HTTP_403_FORBIDDEN)
        order.status = OrderStatus.DELIVERED
        order.save(update_fields=['status'])
        TrackingEvent.objects.create(order=order, status=OrderStatus.DELIVERED)
        return Response({'message': 'Yetkazildi'})
