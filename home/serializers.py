from rest_framework import serializers

from .models import Event, Report


class EventSerializer(serializers.ModelSerializer):
    class Meta:
        model = Event
        fields = [
            'id', 'name', 'description', 'start_date', 'start_time', 'end_date', 'end_time', 'participants',
            'organizer', 'type', 'meet', 'attachments', 'location'
        ]
        extra_kwargs = {'organizer': {'read_only': True}, 'meet': {'read_only': True}}

    def is_valid(self, raise_exception=False):
        super().is_valid(raise_exception)

        if self.validated_data.get("organizer") and \
                self.validated_data.get("type") not in self.validated_data.get("organizer").token.roles:
            raise serializers.ValidationError(
                {"type": f"Insufficient privilege to create event of type {self.validated_data.get('type')}"})


class ReportSerializer(serializers.ModelSerializer):
    class Meta:
        model = Report
        fields = ['id', 'event', 'attachments', 'participants_count', 'report', 'access_code']
        extra_kwargs = {'access_code': {'read_only': True}, 'event': {'read_only': True}}
