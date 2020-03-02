from django.conf import settings
from django.contrib.auth.models import User
from django.contrib.sites.models import Site

import olduka.v1.tasks as olduka_tasks


CURRENT_SITE = Site.objects.get_current()

def get_item_totals(items):
    totals = 0.0
    if items.all():
        for item in items.all():
            totals += (
                item.item.price.price - item.item.price.discount
            ) * item.quantity
    return totals


def send_invoice_email(
        invoice, subject, message,
        from_address=settings.EMAIL_HOST_USER):
    user = User.objects.get(pk=invoice.user_id)
    email_data = (
        subject, message, from_address, [user.email]
    )
    olduka_tasks.send_email.delay(email_data)
