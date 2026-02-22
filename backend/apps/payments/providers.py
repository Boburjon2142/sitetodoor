import uuid
from dataclasses import dataclass

from django.conf import settings

from .models import PaymentIntent, PaymentProviderType, PaymentStatus


@dataclass
class ProviderResponse:
    status: str
    external_id: str
    payload: dict


class PaymentProvider:
    provider_name = ''

    def create_payment(self, order, amount) -> ProviderResponse:
        raise NotImplementedError

    def verify_callback(self, payload, signature):
        return True

    def parse_status(self, payload):
        return PaymentStatus.PENDING


class CashProvider(PaymentProvider):
    provider_name = PaymentProviderType.CASH

    def create_payment(self, order, amount):
        return ProviderResponse(status=PaymentStatus.PENDING, external_id=f'cash-{order.id}', payload={})


class MockProvider(PaymentProvider):
    provider_name = PaymentProviderType.MOCK

    def create_payment(self, order, amount):
        status = PaymentStatus.SUCCESS if settings.MOCK_PAY_AUTO_SUCCESS else PaymentStatus.PENDING
        return ProviderResponse(
            status=status,
            external_id=f'mock-{uuid.uuid4().hex[:12]}',
            payload={'auto_success': settings.MOCK_PAY_AUTO_SUCCESS},
        )


class ExternalStubProvider(PaymentProvider):
    def create_payment(self, order, amount):
        return ProviderResponse(
            status=PaymentStatus.PENDING,
            external_id=f'{self.provider_name}-{uuid.uuid4().hex[:10]}',
            payload={'redirect_url': 'https://example.com/pay'},
        )


class PaymeProvider(ExternalStubProvider):
    provider_name = PaymentProviderType.PAYME


class ClickProvider(ExternalStubProvider):
    provider_name = PaymentProviderType.CLICK


class UzumProvider(ExternalStubProvider):
    provider_name = PaymentProviderType.UZUM


PROVIDERS = {
    PaymentProviderType.CASH: CashProvider(),
    PaymentProviderType.MOCK: MockProvider(),
    PaymentProviderType.PAYME: PaymeProvider(),
    PaymentProviderType.CLICK: ClickProvider(),
    PaymentProviderType.UZUM: UzumProvider(),
}


def create_payment_intent(order, provider_name):
    provider = PROVIDERS[provider_name]
    response = provider.create_payment(order, order.total_amount)
    return PaymentIntent.objects.create(
        order=order,
        amount=order.total_amount,
        provider=provider_name,
        status=response.status,
        external_id=response.external_id,
        raw_payload=response.payload,
    )
