from djongo import models
from django.utils import timezone
import olduka.v1.payment.models as payment_models


class MpesaPayment(models.Model):
    invoice = models.ForeignKey(
        payment_models.Invoice,
        on_delete=models.CASCADE,
        related_name='mpesa_payment'
    )
    merchant_request_id = models.CharField(max_length=20, null=True)
    checkout_request_id = models.CharField(max_length=50, null=True)
    amount = models.FloatField(null=True)
    receipt_number = models.CharField(max_length=15, null=True)
    transaction_date = models.DateTimeField(default=timezone.now)
    phone_number = models.CharField(max_length=15, null=True)
    response_description = models.TextField(null=True)
