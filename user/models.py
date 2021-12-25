from django.contrib.auth.models import User
from django.db import models


class Group(models.Model):
    name = models.CharField(max_length=15)
    admins = models.ManyToManyField(to=User, related_name="group_admin")
    members = models.ManyToManyField(to=User, related_name="group_member")
