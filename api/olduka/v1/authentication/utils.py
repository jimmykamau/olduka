import uuid

from django.conf import settings
from django.contrib.sites.models import Site
from django.urls import reverse_lazy
from itsdangerous import URLSafeTimedSerializer

import olduka.v1.tasks as olduka_tasks
from olduka.v1.authentication import logger


def get_jwt_secret(user):
    return user.user_profile.jwt_secret


def change_jwt_secret(user):
    user.user_profile.jwt_secret = uuid.uuid4()
    user.user_profile.save()


def send_password_changed_email(user, from_address=settings.EMAIL_HOST_USER,
                                subject="Your password has been updated"):
    current_site = Site.objects.get_current()
    email_data = (subject,
                  "Your {} password has been updated successfully!".format(
                      current_site.name),
                  from_address, [user.email])
    olduka_tasks.send_email.delay(email_data)


def send_account_confirmation_email(user, from_address=settings.EMAIL_HOST_USER,
                                    subject="Please confirm your account"):
    user_email_address = user.email
    serializer = URLSafeTimedSerializer(settings.SECRET_KEY, "auth")
    token = serializer.dumps(user_email_address)
    current_site = Site.objects.get_current()
    validate_endpoint = reverse_lazy('v1:validate-email')
    token_url = "http://{}{}?token={}".format(
        current_site.domain, validate_endpoint, token
    )
    email_data = (
        subject,
        "Kindly visit the link below to activate your {} account.\n\n{}".format(
            current_site.name, token_url
        ),
        from_address, [user_email_address]
    )
    olduka_tasks.send_email.delay(email_data)
