import datetime
import json

import requests
from django.contrib.auth.models import User
from django.db.models import Q
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAuthenticated
from shortuuid import random

from user.models import Group
from .models import Event, PROTECTED_EVENTS, UNPROTECTED_EVENTS, Report
from .serializers import EventSerializer, ReportSerializer


class EventApiViewSet(viewsets.ModelViewSet):
    serializer_class = EventSerializer
    queryset = Event.objects.all()
    permission_classes = [IsAuthenticatedOrReadOnly]
    http_method_names = ['get', 'post', 'patch', 'delete']

    def get_queryset(self):
        if self.request.user.is_authenticated:
            events = Event.objects.filter(
                Q(type__in=UNPROTECTED_EVENTS) | Q(access_code__startswith=self.request.user.tokens.access_code))
        else:
            events = Event.objects.filter(type__in=UNPROTECTED_EVENTS)

        return events.filter(end_date__gte=datetime.date.today()).order_by("start_date")

    def create_calender_event(self, serializer: EventSerializer):
        url = 'https://www.googleapis.com/calendar/v3/calendars/primary/events?conferenceDataVersion=1' \
              '&sendNotifications=true&sendUpdates=all&supportsAttachments=true&key=AIzaSyDXLyCuugAMejJ0KMPEJ8' \
              '-XGiVXloIZ0kw'

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

        return result["hangoutLink"] if "hangoutLink" in result else None

    def perform_create(self, serializer: EventSerializer):

        participants = [*serializer.data.get("participants"),
                        *[group.members.all() for group in Group.objects.filter(pk__in=self.request["groups"])]]

        serializer = EventSerializer(data={**serializer.data, "organizer": self.request.user,
                                           "type": self.request.data["type"], "participants": participants})

        serializer.is_valid(raise_exception=True)
        meet = self.create_calender_event(serializer) if serializer.data.get("type") in PROTECTED_EVENTS else None

        serializer.save(meet=meet)


class ReportApiViewSet(viewsets.ModelViewSet):
    serializer_class = ReportSerializer
    queryset = Report.objects.all()
    permission_classes = [IsAuthenticated]
    http_method_names = ['get', 'post', 'patch', 'delete']

    def get_queryset(self):
        return Report.objects.filter(event__access_code__startswith=self.request.user.tokens.access_code) \
            .order_by("event__end_date").reverse()
