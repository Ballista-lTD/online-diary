import json

import requests
from django.contrib.auth.models import User
from django.contrib.postgres.fields import ArrayField
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from oauth2_provider.models import AccessToken


class Event(models.Model):
    name = models.CharField(max_length=50)
    start_date = models.DateField()
    start_time = models.TimeField()
    organizer = models.ForeignKey(User, blank=True, null=True, related_name='event_organizer', on_delete=models.PROTECT)
    end_date = models.DateField(blank=True, null=True)
    end_time = models.TimeField(blank=True, null=True)
    participants = models.ManyToManyField(User, blank=True, null=True)
    description = models.TextField()
    attachments = ArrayField(models.FileField(upload_to="docs"), null=True, blank=True)
    public = models.BooleanField(default=False)

    def __str__(self):
        return f"Event : {self.name} ({self.start_date} / {self.start_time})"


@receiver(post_save, sender=Event)
def create(sender, instance: Event, created, **kwargs):
    if created:
        # event = {
        #     'summary': 'Google I/O 2015',
        #     'location': '800 Howard St., San Francisco, CA 94103',
        #     'description': instance.description,
        #     'start': {
        #         'dateTime': '2015-05-28T09:00:00-07:00',
        #         'timeZone': 'America/Los_Angeles',
        #     },
        #     'end': {
        #         'dateTime': '2015-05-28T17:00:00-07:00',
        #         'timeZone': 'America/Los_Angeles',
        #     },
        #     'recurrence': [
        #         'RRULE:FREQ=DAILY;COUNT=2'
        #     ],
        #     'reminders': {
        #         'useDefault': False,
        #         'overrides': [
        #             {'method': 'email', 'minutes': 24 * 60},
        #             {'method': 'popup', 'minutes': 10},
        #         ],
        #     },
        # }
        url = f'https://www.googleapis.com/calendar/v3/calendars/primary/events?sendNotifications=true&sendUpdates' \
              f'=all&supportsAttachments=true&key=AIzaSyDXLyCuugAMejJ0KMPEJ8-XGiVXloIZ0kw'

        event = {
            'summary': instance.name,
            'description': instance.description,
            'start': {
                'dateTime': f'{instance.start_date}T{instance.end_time}+05:30'
            },
            'end': {
                'dateTime': f'{instance.end_date}T{instance.end_time}+05:30'
            },
            'attendees': [
                [{'email': user.email} for user in instance.participants.all()]
            ]
        }

        requests.post(url, headers={
            'Authorization': f'Bearer {instance.organizer.tokens.google_token}',
            'Accept': 'application/json',
            'Content-Type': 'application/json'
        }, data=json.dumps(event))
