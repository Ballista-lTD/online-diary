import datetime

from django.db.models import Q
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticatedOrReadOnly

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

    def perform_create(self, serializer):
        serializer.save(organizer=self.request.user,
                        public=self.request.user.tokens.admin and serializer.data["public"])
