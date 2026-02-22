from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import CategoryListView, ProductDetailView, ProductListView, SupplierOfferViewSet

router = DefaultRouter()
router.register('supplier/offers', SupplierOfferViewSet, basename='supplier-offers')

urlpatterns = [
    path('categories/', CategoryListView.as_view(), name='categories'),
    path('products/', ProductListView.as_view(), name='products'),
    path('products/<int:pk>/', ProductDetailView.as_view(), name='product-detail'),
    path('', include(router.urls)),
]
