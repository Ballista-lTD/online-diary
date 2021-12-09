from django.db.models import Q
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated

from .models import Event
from .serializers import EventSerializer


class EventApiViewSet(viewsets.ModelViewSet):
    serializer_class = EventSerializer
    permission_classes = [IsAuthenticated]
    queryset = Event.objects.all()
    http_method_names = ['get', 'post', 'patch', 'delete']

    def get_queryset(self):
        return Event.objects.filter(Q(public=True) | Q(organizer=self.request.user))

    def perform_create(self, serializer):
        serializer.save(organizer=self.request.user,
                        public=self.request.user.tockens.admin and serializer.data["public"])

