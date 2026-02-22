from rest_framework import serializers, viewsets
from rest_framework.permissions import IsAuthenticated

from .models import SupplierReview


class SupplierReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = SupplierReview
        fields = ['id', 'supplier', 'rating', 'comment', 'created_at']
        read_only_fields = ['id', 'created_at']


class SupplierReviewViewSet(viewsets.ModelViewSet):
    serializer_class = SupplierReviewSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return SupplierReview.objects.filter(customer=self.request.user)

    def perform_create(self, serializer):
        serializer.save(customer=self.request.user)
