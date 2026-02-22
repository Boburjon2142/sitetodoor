import logging

from celery import shared_task

logger = logging.getLogger(__name__)


@shared_task
def send_otp_task(phone: str, code: str):
    logger.info('Mock OTP sent', extra={'phone': phone, 'code': code})
    print(f'[OTP] phone={phone} code={code}')
