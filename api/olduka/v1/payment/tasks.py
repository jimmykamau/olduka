from datetime import timedelta

from celery import shared_task
from django.contrib.sites.models import Site
from django.utils import timezone

import olduka.v1.payment.models as payment_models
import olduka.v1.payment.utils as payment_utils
from olduka.v1.utils import get_object_id_value

CURRENT_SITE = Site.objects.get_current()


@shared_task
def update_item_quantities():
    orphan_invoice_items = payment_models.InvoiceItem.objects.filter(
        invoice=None).prefetch_related('item')
    for invoice_item in orphan_invoice_items:
        invoice_item.item.quantity += invoice_item.quantity
        invoice_item.item.save()
    orphan_invoice_items.delete()
    invoices_to_update = payment_models.Invoice.objects.filter(
        quantities_updated=False)
    for invoice in invoices_to_update:
        for item in invoice.items.all():
            item.item.quantity -= item.quantity
            item.item.save()
    invoices_to_update.update(quantities_updated=True)


@shared_task
def check_invoices():
    current_time = timezone.now()
    reminder_date = current_time - timedelta(hours=16)
    expiry_date = current_time - timedelta(hours=24)
    unpaid_invoices = payment_models.Invoice.objects.filter(
        status='OP', created_at__lte=reminder_date)
    for invoice in unpaid_invoices:
        if not invoice.reminder_sent_at:
            email_subject = f"You have an unpaid {CURRENT_SITE.name} invoice"
            email_message = (
                f"Kindly note that invoice number {get_object_id_value(invoice)} will soon expire if left unpaid.\n"
                "Kindly click the link below to settle the invoice and ensure that you get your items."
            )
            payment_utils.send_invoice_email(
                invoice, email_subject, email_message)
            invoice.reminder_sent_at = timezone.now()
            invoice.save()
        elif invoice.created_at <= expiry_date:
            email_subject = f"Your {CURRENT_SITE.name} invoice has expired"
            email_message = (
                f"Kindly note that invoice number {get_object_id_value(invoice)} has expired."
                "The reserved items have been returned to stock and may soon run out."
            )
            payment_utils.send_invoice_email(
                invoice, email_subject, email_message)
            invoice.delete()
