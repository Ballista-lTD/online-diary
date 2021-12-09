import json

import requests
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from oauth2_provider.models import AccessToken

from .models import Event
from .serializers import EventSerializer


class EventApiViewSet(viewsets.ModelViewSet):
    serializer_class = EventSerializer
    permission_classes = [IsAuthenticated]
    queryset = Event.objects.all()
    http_method_names = ['get', 'post', 'patch', 'delete']

    def perform_create(self, serializer):
        serializer.save(organizer=self.request.user)

        url = f'https://www.googleapis.com/calendar/v3/calendars/primary/events?sendNotifications=true&sendUpdates' \
              f'=all&supportsAttachments=true&key=AIzaSyDXLyCuugAMejJ0KMPEJ8-XGiVXloIZ0kw'

        event = {
            'summary': serializer.data['name'],
            'description': serializer.data['description'],
            'start': {
                'dateTime': f'{serializer.data["start_date"]}T{serializer.data["start_time"]}+05:30'
            },
            'end': {
                'dateTime': f'{serializer.data["end_date"]}T{serializer.data["end_time"]}+05:30'
            }
        }

        print(AccessToken.objects.filter(user_id=self.request.user.id)[0].token)

        response = requests.post(url, headers={
            'Authorization': f'Bearer {AccessToken.objects.filter(user_id=self.request.user.id)[1].token}',
            'Accept': 'application/json',
            'Content-Type': 'application/json'
        }, data=json.dumps(event)).text

        print(response)
