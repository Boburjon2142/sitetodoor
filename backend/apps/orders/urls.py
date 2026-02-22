from django.urls import path

from .views import AdminOrderListView, AssignDriverView, OrderDetailView, OrderListView

urlpatterns = [
    path('', OrderListView.as_view(), name='order-list'),
    path('<int:pk>/', OrderDetailView.as_view(), name='order-detail'),
    path('admin/list/', AdminOrderListView.as_view(), name='admin-orders'),
    path('<int:pk>/assign-driver/', AssignDriverView.as_view(), name='assign-driver'),
]
