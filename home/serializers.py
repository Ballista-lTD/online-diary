from rest_framework import serializers

from .models import Event, EVENT_TYPES, Report


class EventSerializer(serializers.ModelSerializer):
    class Meta:
        model = Event
        fields = [
            'id', 'name', 'description', 'start_date', 'start_time', 'end_date', 'end_time', 'participants',
            'organizer', 'type', 'meet', 'attachments', 'location'
        ]
        extra_kwargs = {'organizer': {'read_only': True}, 'meet': {'read_only': True}}

    def validate_type(self, value: str):
        if not value:
            raise serializers.ValidationError({"type": "Event type is required"})

        if value not in EVENT_TYPES:
            raise serializers.ValidationError({"type": f"Unknown event type {value}"})

        if value not in self.data.get('organizer').token.roles:
            raise serializers.ValidationError({"type": f"Insufficient privilege to create event of type {value}"})

        return value


class ReportSerializer(serializers.ModelSerializer):
    class Meta:
        model = Report
        fields = [
            'id', 'event', 'attachments', 'participants_count', 'report'
        ]
