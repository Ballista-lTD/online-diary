from django.contrib.auth.models import User
from django.contrib.postgres.fields import ArrayField
from django.db import models
from oauth2_provider.models import AccessToken

PROTECTED_EVENTS = ["Private", "Memo"]
UNPROTECTED_EVENTS = ["Public", "Notification", "Circular"]

EVENT_TYPES = [*PROTECTED_EVENTS, *UNPROTECTED_EVENTS]


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
    location = models.CharField(max_length=100, null=True, blank=True)
    meet = models.CharField(max_length=36, null=True, blank=True)
    type = models.CharField(max_length=15, choices=tuple([(e, e) for e in EVENT_TYPES]), default="Private")

    @property
    def access_code(self):
        return self.organizer.tokens.access_code

    def __str__(self):
        return f"Event : {self.name} ({self.start_date} / {self.start_time})"

    def get_participants(self):
        return [{'email': user.email} for user in self.participants.all()]


class Report(models.Model):
    event = models.ForeignKey(to=Event, related_name='event', on_delete=models.CASCADE)
    attachments = ArrayField(models.FileField(upload_to="docs"), null=True, blank=True)
    participants_count = models.PositiveIntegerField(default=0)
    report = models.TextField()
