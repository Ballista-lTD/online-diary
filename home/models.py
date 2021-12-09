from django.contrib.auth.models import User
from django.contrib.postgres.fields import ArrayField
from django.db import models
from oauth2_provider.models import AccessToken


class Event(models.Model):
    name = models.CharField(max_length=50)
    start_date = models.DateField()
    start_time = models.TimeField()
    organizer = models.ForeignKey(User, blank=True, null=True, related_name='event_organizer', on_delete=models.PROTECT)
    end_date = models.DateField(blank=True, null=True)
    end_time = models.TimeField(blank=True, null=True)
    participants = models.ManyToManyField(User, blank=True)
    description = models.TextField()
    attachments = ArrayField(models.FileField(upload_to="docs"), null=True, blank=True)
    public = models.BooleanField(default=False)
    meet = models.CharField(max_length=36, null=True, blank=True)

    def __str__(self):
        return f"Event : {self.name} ({self.start_date} / {self.start_time})"

    def get_participants(self):
        return [{'email': user.email} for user in self.participants.all()]
