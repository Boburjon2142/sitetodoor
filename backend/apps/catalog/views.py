from django.db.models import Q
from rest_framework import generics, permissions, viewsets

from apps.common.permissions import IsSupplier
from .models import Product, ProductCategory, SupplierOffer
from .serializers import (
    CategorySerializer,
    ProductDetailSerializer,
    ProductSerializer,
    SupplierOfferManageSerializer,
)


class CategoryListView(generics.ListAPIView):
    queryset = ProductCategory.objects.all().order_by('name')
    serializer_class = CategorySerializer
    permission_classes = [permissions.AllowAny]


class ProductListView(generics.ListAPIView):
    serializer_class = ProductSerializer
    permission_classes = [permissions.AllowAny]

    def get_queryset(self):
        qs = Product.objects.select_related('category').all().order_by('name')
        category = self.request.query_params.get('category')
        q = self.request.query_params.get('q')
        min_price = self.request.query_params.get('min_price')
        max_price = self.request.query_params.get('max_price')
        available = self.request.query_params.get('available')

        if category:
            qs = qs.filter(category_id=category)
        if q:
            qs = qs.filter(Q(name__icontains=q) | Q(description__icontains=q))
        if min_price:
            qs = qs.filter(offers__price__gte=min_price)
        if max_price:
            qs = qs.filter(offers__price__lte=max_price)
        if available == '1':
            qs = qs.filter(offers__stock__gt=0, offers__is_active=True)
        return qs.distinct()


class ProductDetailView(generics.RetrieveAPIView):
    queryset = Product.objects.prefetch_related('offers__supplier').all()
    serializer_class = ProductDetailSerializer
    permission_classes = [permissions.AllowAny]


class SupplierOfferViewSet(viewsets.ModelViewSet):
    serializer_class = SupplierOfferManageSerializer
    permission_classes = [IsSupplier]

    def get_queryset(self):
        return SupplierOffer.objects.filter(supplier__user=self.request.user).select_related('product')

    def perform_create(self, serializer):
        serializer.save(supplier=self.request.user.supplier_profile)
