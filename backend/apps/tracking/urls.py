from django.urls import path

from .views import (
    DriverAcceptDeliveryView,
    DriverCompleteDeliveryView,
    DriverLocationUpdateView,
    TrackingTimelineView,
)

urlpatterns = [
    path('orders/<int:order_id>/', TrackingTimelineView.as_view(), name='tracking-timeline'),
    path('driver/orders/<int:order_id>/accept/', DriverAcceptDeliveryView.as_view(), name='driver-accept'),
    path('driver/orders/<int:order_id>/complete/', DriverCompleteDeliveryView.as_view(), name='driver-complete'),
    path('driver/location/', DriverLocationUpdateView.as_view(), name='driver-location'),
]
