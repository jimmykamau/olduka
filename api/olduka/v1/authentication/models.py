from django.db import models
from django.contrib.auth.models import User
from django.utils.translation import ugettext_lazy as _


class UserProfile(models.Model):
    user = models.OneToOneField(
        User, on_delete=models.CASCADE,
        related_name='user_profile'
    )
    mobile = models.CharField(
        _('mobile'), max_length=15, null=True
    )

    def __str__(self):
        return "{} - {}".format(self.user.email, self.mobile)
