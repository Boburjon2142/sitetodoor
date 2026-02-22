from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import SupplierReviewViewSet

router = DefaultRouter()
router.register('supplier', SupplierReviewViewSet, basename='supplier-review')

urlpatterns = [
    path('', include(router.urls)),
]
