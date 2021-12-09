from django.contrib.auth.models import User
from django.db import models

# Create your models here.
# class Access_token(models.Model):

roles = (('normal', 'Normal'), ('admin', 'Admin'))


class Tokens(models.Model):
    user = models.OneToOneField(User, related_name='tokens', on_delete=models.CASCADE)
    phone_number = models.CharField(max_length=12, default="")
    role = models.CharField(choices=roles, default='normal', max_length=20)
    profile = models.ImageField(upload_to='meadia', blank=True, null=True)
    admin = models.BooleanField(default=False)
    google_token = models.CharField(max_length=1000, default='')

    def __str__(self):
        return f"{self.user} "
