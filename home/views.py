import datetime
import json

import requests
from django.contrib.auth.models import User
from django.db.models import Q
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from shortuuid import random

from .models import Event
from .serializers import EventSerializer


class EventApiViewSet(viewsets.ModelViewSet):
    serializer_class = EventSerializer
    queryset = Event.objects.all()
    permission_classes = [IsAuthenticatedOrReadOnly]
    http_method_names = ['get', 'post', 'patch', 'delete']

    def get_queryset(self):
        if self.request.user.is_authenticated:
            events = Event.objects.filter(
                Q(public=True) | Q(organizer=self.request.user))
        else:
            events = Event.objects.filter(public=True)

        return events.filter(end_date__gte=datetime.date.today()).order_by("end_date")

    def perform_create(self, serializer: EventSerializer):
        url = 'https://www.googleapis.com/calendar/v3/calendars/primary/events?conferenceDataVersion=1' \
              '&sendNotifications=true&sendUpdates=all&supportsAttachments=true&key=AIzaSyDXLyCuugAMejJ0KMPEJ8' \
              '-XGiVXloIZ0kw '

        serializer.is_valid(raise_exception=True)

        event = {
            'summary': serializer.validated_data["name"],
            'description': serializer.validated_data["description"],
            'location': 'Cochin University of Science and Technology',
            'start': {
                'dateTime': f'{serializer.validated_data["start_date"]}T{serializer.validated_data["end_time"]}+05:30'
            },
            'end': {
                'dateTime': f'{serializer.validated_data["end_date"]}T{serializer.validated_data["end_time"]}+05:30'
            },
            'attendees': [{'email': User.objects.get(id=uid).email} for uid in self.request.data["participants"]],
            'conferenceData': {
                "createRequest": {
                    "conferenceSolutionKey": {
                        "type": "hangoutsMeet"
                    },
                    'requestId': f'{random()}{self.request.user.id}'
                }
            },
        }

        result = requests.post(url, headers={
            'Authorization': f'Bearer {self.request.user.tokens.google_token}',
            'Accept': 'application/json',
            'Content-Type': 'application/json'
        }, data=json.dumps(event)).json()

        serializer.save(organizer=self.request.user,
                        public=self.request.user.tokens.admin and serializer.validated_data["public"],
                        meet=result["hangoutLink"])
