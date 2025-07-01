# Django inbuilt modules
from django.db import transaction

# Django REST framework modules
from rest_framework import serializers
from rest_framework.exceptions import APIException

# Local modules
from .models import Event, EventRegistration
from utils.utils import CustomAPIException

class EventSerializer(serializers.ModelSerializer):
    start_time = serializers.DateTimeField(format='%Y-%m-%d %H:%M:%S')
    end_time = serializers.DateTimeField(format='%Y-%m-%d %H:%M:%S')

    class Meta:
        model = Event
        fields = ['id', 'name', 'location', 'start_time', 'end_time', 'max_capacity']


class EventValidationSerializer(serializers.Serializer):
    def validate(self, data):
        event_id = self.context.get('event_id')
        if not Event.objects.filter(id=event_id).exists():
            raise CustomAPIException("Event does not exist", status_code=404)
        return data

class EventRegistrationSerializer(serializers.ModelSerializer):

    class Meta:
        model = EventRegistration
        fields = ['attendee_name', 'attendee_email']

    def validate(self, data):
        event = Event.objects.filter(id=self.context['event_id']).first()

        # Check if registration count is less than max capacity
        if event.eventregistration_set.count() >= event.max_capacity:
            raise CustomAPIException("Registration limit reached", status_code=400)

        if EventRegistration.objects.filter(event=event, attendee_name=data['attendee_name'],
                                            attendee_email=data['attendee_email']).exists():
            raise serializers.ValidationError({
                "attendee_name": ["Attendee already registered"],
                "attendee_email": ["Attendee already registered"]
            }, code=400)
        data['event'] = event
        return data


    def create(self, validated_data):

        @transaction.atomic
        def register_attendee():
            event = validated_data.pop('event')
            return EventRegistration.objects.create(event=event, **validated_data)

        return register_attendee()


class EventAttendeesSerializer(serializers.ModelSerializer):

    class Meta:
        model = EventRegistration
        fields = ['attendee_name', 'attendee_email']