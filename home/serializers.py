from rest_framework import serializers

from .models import Event


class EventSerializer(serializers.ModelSerializer):
    class Meta:
        model = Event
        fields = [
            'id', 'name', 'description', 'start_date', 'start_time', 'end_date', 'end_time', 'participants',
            'organizer', 'public'
        ]
        extra_kwargs = {'organizer': {'read_only': True}, 'meet': {'read_only': True}}
