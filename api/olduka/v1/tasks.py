from celery import shared_task
from django.core.mail import send_mass_mail


@shared_task
def send_email(datatuple):
    send_mass_mail((datatuple,), fail_silently=False)
