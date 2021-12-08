from django.contrib.auth.models import User
from django.contrib.postgres.fields import ArrayField
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver


class Event(models.Model):
    name = models.CharField(max_length=50)
    start_date = models.DateField()
    start_time = models.TimeField()
    organizer = models.ForeignKey(User, blank=True, null=True, related_name='event_organizer', on_delete=models.PROTECT)
    end_date = models.DateField(blank=True, null=True)
    end_time = models.TimeField(blank=True, null=True)
    participants = models.ManyToManyField(User)
    description = models.TextField()
    attachments = ArrayField(models.FileField(upload_to="docs"), null=True, blank=True)

    def __str__(self):
        return f"Event : {self.name} ({self.start_date} / {self.start_time})"


@receiver(post_save, sender=Event)
def create(sender, instance: Event, created, **kwargs):
    if created:
        event = {
            'summary': 'Google I/O 2015',
            'location': '800 Howard St., San Francisco, CA 94103',
            'description': instance.description,
            'start': {
                'dateTime': '2015-05-28T09:00:00-07:00',
                'timeZone': 'America/Los_Angeles',
            },
            'end': {
                'dateTime': '2015-05-28T17:00:00-07:00',
                'timeZone': 'America/Los_Angeles',
            },
            'recurrence': [
                'RRULE:FREQ=DAILY;COUNT=2'
            ],
            'attendees': [
                {'email': 'sunithvazhenkada@gmail.com'},
                {'email': '20cs098suni@ug.cusat.ac.in'},
            ],
            'reminders': {
                'useDefault': False,
                'overrides': [
                    {'method': 'email', 'minutes': 24 * 60},
                    {'method': 'popup', 'minutes': 10},
                ],
            },
        }
