from rest_framework import serializers

from apps.reviews.models import SupplierReview
from .models import Product, ProductCategory, SupplierOffer, SupplierProfile


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductCategory
        fields = ['id', 'name', 'slug']


class SupplierOfferSerializer(serializers.ModelSerializer):
    supplier_name = serializers.CharField(source='supplier.company_name', read_only=True)
    supplier_rating = serializers.SerializerMethodField()

    class Meta:
        model = SupplierOffer
        fields = [
            'id', 'supplier', 'supplier_name', 'supplier_rating', 'price', 'stock',
            'min_order_qty', 'delivery_eta_hours', 'is_active',
        ]

    def get_supplier_rating(self, obj):
        return SupplierReview.avg_rating_for_supplier(obj.supplier_id)


class ProductSerializer(serializers.ModelSerializer):
    category_name = serializers.CharField(source='category.name', read_only=True)
    best_price = serializers.SerializerMethodField()

    class Meta:
        model = Product
        fields = ['id', 'name', 'description', 'unit', 'category', 'category_name', 'best_price']

    def get_best_price(self, obj):
        price = obj.offers.filter(is_active=True, stock__gt=0).order_by('price').values_list('price', flat=True).first()
        return price


class ProductDetailSerializer(ProductSerializer):
    offers = SupplierOfferSerializer(many=True, read_only=True)

    class Meta(ProductSerializer.Meta):
        fields = ProductSerializer.Meta.fields + ['offers']


class SupplierOfferManageSerializer(serializers.ModelSerializer):
    class Meta:
        model = SupplierOffer
        fields = ['id', 'product', 'price', 'stock', 'min_order_qty', 'delivery_eta_hours', 'is_active']
