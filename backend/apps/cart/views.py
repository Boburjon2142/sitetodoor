from django.conf import settings
from django.db import transaction
from rest_framework import generics, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.orders.services import create_orders_from_cart
from apps.users.models import UserAddress
from .models import Cart, CartItem
from .serializers import AddCartItemSerializer, CartSerializer, CheckoutSerializer, estimate_delivery_fee


class CartView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        cart, _ = Cart.objects.get_or_create(customer=request.user)
        return Response(CartSerializer(cart).data)


class CartItemAddView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = AddCartItemSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        cart, _ = Cart.objects.get_or_create(customer=request.user)
        offer_id = serializer.validated_data['supplier_offer_id']
        quantity = serializer.validated_data['quantity']

        item, created = CartItem.objects.get_or_create(cart=cart, supplier_offer_id=offer_id, defaults={'quantity': quantity})
        if not created:
            item.quantity += quantity
            item.save(update_fields=['quantity'])
        return Response({'message': 'Savatga qo`shildi'}, status=status.HTTP_201_CREATED)


class CartItemDeleteView(generics.DestroyAPIView):
    permission_classes = [IsAuthenticated]
    queryset = CartItem.objects.all()

    def get_queryset(self):
        return super().get_queryset().filter(cart__customer=self.request.user)


class CheckoutView(APIView):
    permission_classes = [IsAuthenticated]

    @transaction.atomic
    def post(self, request):
        serializer = CheckoutSerializer(data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        method = serializer.validated_data['payment_method']
        if method == 'payme' and not settings.PAYME_ENABLED:
            return Response({'message': 'Payme vaqtincha o`chiq'}, status=status.HTTP_400_BAD_REQUEST)
        if method == 'click' and not settings.CLICK_ENABLED:
            return Response({'message': 'Click vaqtincha o`chiq'}, status=status.HTTP_400_BAD_REQUEST)
        if method == 'uzum' and not settings.UZUM_ENABLED:
            return Response({'message': 'Uzum vaqtincha o`chiq'}, status=status.HTTP_400_BAD_REQUEST)

        cart, _ = Cart.objects.get_or_create(customer=request.user)
        if not cart.items.exists():
            return Response({'message': 'Savat bo`sh'}, status=status.HTTP_400_BAD_REQUEST)

        address = UserAddress.objects.get(id=serializer.validated_data['address_id'])
        delivery_fee = estimate_delivery_fee(
            cart,
            address,
            settings.DELIVERY_BASE_FEE,
            settings.DELIVERY_PER_KM_FEE,
        )

        orders = create_orders_from_cart(
            user=request.user,
            cart=cart,
            address=address,
            delivery_slot=serializer.validated_data['delivery_slot'],
            payment_method=method,
            delivery_fee=delivery_fee,
            commission_percent=settings.COMMISSION_PERCENT,
        )

        return Response({'orders': [o.id for o in orders], 'delivery_fee': delivery_fee})
