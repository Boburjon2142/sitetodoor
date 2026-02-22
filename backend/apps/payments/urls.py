from django.urls import path

from .views import PaymentIntentListView, PaymentWebhookView

urlpatterns = [
    path('intents/', PaymentIntentListView.as_view(), name='payment-intents'),
    path('webhooks/<str:provider>/', PaymentWebhookView.as_view(), name='payment-webhook'),
]
