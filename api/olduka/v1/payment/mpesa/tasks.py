import json

import requests
from celery import shared_task
from django.conf import settings
from django.contrib.sites.models import Site
from django.core.cache import cache
from django.core.cache.backends.base import DEFAULT_TIMEOUT
from django.urls import reverse_lazy

import olduka.v1.payment.mpesa.models as mpesa_models
import olduka.v1.payment.utils as payment_utils
from olduka.v1.payment import logger
from olduka.v1.payment.mpesa.utils import (generate_auth_string,
                                           generate_lipa_password)
from olduka.v1.utils import get_object_id_value

CACHE_TTL = getattr(settings, 'CACHE_TTL', DEFAULT_TIMEOUT)


@shared_task
def get_access_token():
    auth_string = generate_auth_string().decode('utf-8')
    try:
        response = requests.get(
            f"{settings.MPESA_BASE_URL}/oauth/v1/generate?grant_type=client_credentials",
            headers={
                "Authorization": f"Basic {auth_string}",
                "Content-Type": "application/json"
            }
        )
        response.raise_for_status()
    except Exception:
        logger.warning("Error getting auth key", exc_info=True)
    else:
        cache.set(
            'mpesa_auth_key', response.json()["access_token"],
            timeout=CACHE_TTL
        )


@shared_task
def initiate_mpesa_payment(pk, description=None):
    auth_key = cache.get('mpesa_auth_key')
    mpesa_payment_model = mpesa_models.MpesaPayment.objects.get(pk=pk)
    timestamp = mpesa_payment_model.transaction_date.strftime("%Y%m%d%H%M%S")
    password = generate_lipa_password(timestamp).decode('utf-8')
    current_site = Site.objects.get_current()
    callback_url = f"https://{current_site.domain}{reverse_lazy('v1:mpesa-callback')}"
    invoice_id = get_object_id_value(mpesa_payment_model.invoice)
    description = f"{current_site.name} invoice" if not description else description

    data = dict(
        BusinessShortCode=settings.MPESA_BUSINESS_SHORTCODE,
        Password=password,
        Timestamp=timestamp,
        TransactionType="CustomerPayBillOnline",
        Amount=mpesa_payment_model.amount,
        PartyA=mpesa_payment_model.phone_number,
        PartyB=settings.MPESA_BUSINESS_SHORTCODE,
        PhoneNumber=mpesa_payment_model.phone_number,
        CallBackURL=callback_url,
        AccountReference=invoice_id,
        TransactionDesc=description
    )

    try:
        response = requests.post(
            f"{settings.MPESA_BASE_URL}mpesa/stkpush/v1/processrequest",
            headers={
                "Authorization": f"Bearer {auth_key}",
                "Content-Type": "application/json"
            },
            data=json.dumps(data)
        )
        response_data = response.json()
        response.raise_for_status()
    except Exception:
        if response_data['errorMessage'] == "Invalid Access Token":
            get_access_token.delay()
            initiate_mpesa_payment.delay(pk, description)
        logger.warning(f"Error initiating Mpesa payment: {response_data}", exc_info=True)
    else:
        mpesa_payment_model.merchant_request_id = response_data['MerchantRequestID']
        mpesa_payment_model.checkout_request_id = response_data['CheckoutRequestID']
        mpesa_payment_model.response_description = response_data['ResponseDescription']
        mpesa_payment_model.save()


@shared_task
def process_mpesa_payment(payment_info):
    mpesa_payment_model = mpesa_models.MpesaPayment.objects.get(
        pk=payment_info['payment_pk']
    )
    if float(payment_info['Amount']) == mpesa_payment_model.amount:
        mpesa_payment_model.invoice.status = 'PA'
        mpesa_payment_model.invoice.save()
        mpesa_payment_model.receipt_number = payment_info['MpesaReceiptNumber']
        mpesa_payment_model.save()
        email_subject = f"Thank you for your payment"
        email_body = f"Invoice {get_object_id_value(mpesa_payment_model.invoice)} is now fully paid."
        payment_utils.send_invoice_email(
            mpesa_payment_model.invoice, email_subject, email_body
        )
