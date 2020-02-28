import base64
from django.conf import settings


def generate_auth_string():
    return base64.b64encode(
        f"{settings.MPESA_CONSUMER_KEY}:{settings.MPESA_CONSUMER_SECRET}".encode('utf-8'))


def generate_lipa_password(timestamp):
    return base64.b64encode(
        f"{settings.MPESA_BUSINESS_SHORTCODE}{settings.MPESA_ONLINE_PASSKEY}{timestamp}".encode('utf-8')
    )
