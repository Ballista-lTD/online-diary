from django.contrib.auth.models import User
from django.contrib.postgres.fields import ArrayField
from django.db import models

from home.models import EVENT_TYPES


def get_default_role():
    return list(("Private",))


class Tokens(models.Model):
    user = models.OneToOneField(User, related_name='tokens', on_delete=models.CASCADE)
    phone_number = models.CharField(max_length=12, default="")
    avatar = models.ImageField(upload_to='media', blank=True, null=True)
    google_token = models.CharField(max_length=1000, default='')
    access_code = models.CharField(max_length=100, default='*')
    roles = ArrayField(models.CharField(max_length=15, choices=((e, e) for e in EVENT_TYPES)),
                       default=get_default_role)

    @property
    def users_under(self):
        return Tokens.objects.filter(access_code__regex=r"^{}-\d+$".format(self.access_code)).count()

    def __str__(self):
        return f"{self.user} "
