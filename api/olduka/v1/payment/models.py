from django.contrib.auth.models import User
from django.utils import timezone
from djongo import models

import olduka.v1.product.models as product_models


class InvoiceItem(models.Model):
    item = models.ForeignKey(
        product_models.Item,
        on_delete=models.CASCADE,
        related_name='invoice_item'
    )
    quantity = models.IntegerField()


class Invoice(models.Model):
    INVOICE_STATUS_CHOICES = (
        ('OP', 'Open'),
        ('PA', 'Paid'),
    )
    _id = models.ObjectIdField()
    user = models.ForeignKey(
        User, on_delete=models.CASCADE,
        related_name='user_invoice'
    )
    items = models.ArrayReferenceField(
        to=InvoiceItem,
        on_delete=models.SET_NULL,
        related_name='invoice',
        null=True
    )
    status = models.CharField(
        max_length=2,
        choices=INVOICE_STATUS_CHOICES
    )
    created_at = models.DateTimeField(
        default=timezone.now
    )
    reminder_sent_at = models.DateTimeField(
        null=True, blank=True
    )
    quantities_updated = models.BooleanField(
        default=False
    )
