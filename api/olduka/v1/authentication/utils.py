import uuid

from django.conf import settings

import olduka.v1.tasks as olduka_tasks
from olduka.v1.authentication import logger


def get_jwt_secret(user):
    return user.user_profile.jwt_secret


def change_jwt_secret(user):
    user.user_profile.jwt_secret = uuid.uuid4()
    user.user_profile.save()


def send_password_changed_email(user, from_address=settings.EMAIL_HOST_USER,
                                subject="Your password has been updated"):
    email_data = (subject, "Your password has been updated successfully!",
                  from_address, [user.email])
    olduka_tasks.send_email.delay(email_data)
