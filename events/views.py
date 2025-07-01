# Python inbuilt modules

# Django REST framework modules
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

# Local modules
from events.serializers import (EventSerializer, EventRegistrationSerializer,
                                EventAttendeesSerializer, EventValidationSerializer)
from events.models import Event, EventRegistration
from utils.utils import (get_current_time_in_timezone, covert_time_to_timezone, Pagination)



# Create an API view with get and post method, where post method is used to create a new event and get method is used to retrieve all events

class EventView(APIView):

    allowed_methods = ('GET', 'POST')

    def post(self, request):
        """
        :param request: Request object
        :return: Returns a response object with the status code and data, which is a dictionary containing the event details
        if the request is valid, otherwise returns a response object with the status code and errors,
        which is a dictionary containing the error messages
        """
        request_data = request.data
        # Converting time to IST timezone
        request_data['start_time'] = covert_time_to_timezone(request_data['start_time'])
        request_data['end_time'] = covert_time_to_timezone(request_data['end_time'])
        serializer = EventSerializer(data=request_data)
        if serializer.is_valid():
            serializer.save()
            return  Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def get(self, request):
        """
        :param request: Request object
        :return: Returns a response object with the status code and data, which is a list of dictionaries containing the event details
        """
        # Getting offset, limit and timezone from the request
        pagination = Pagination(request)
        user_timezone = request.GET.get('timezone', 'Asia/Kolkata')

        timeframe = get_current_time_in_timezone(user_timezone)
        events = Event.objects.all().order_by(
            '-start_time', 'name')[pagination.offset:pagination.offset +pagination.limit]
        serializer = EventSerializer(events, many=True)
        data = serializer.data

        # Identifying the status of the event
        for event in data:
            status = 'closed'
            end_time = covert_time_to_timezone(event['end_time'])
            start_time = covert_time_to_timezone(event['start_time'])
            if start_time >= timeframe:
                status = 'open'
            elif timeframe >= start_time and timeframe <= end_time:
                status = 'ongoing'
            event['status'] = status
        return Response(data)


class EventRegister(APIView):

    allowed_methods = ('POST',)

    def post(self, request, event_id):
        """
        Create a new event
        :param request: Request object
        :param event_id: Event id
        :return: Returns a response object with the status code and data, which is a dictionary containing the registration details
        """
        request_data = request.data

        # Check if the event exists
        event_validation_serializer = EventValidationSerializer(data=request.data, context={'event_id': event_id})
        if not event_validation_serializer.is_valid():
            return Response(event_validation_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        # Create the registration
        serializer = EventRegistrationSerializer(data=request_data, context={'event_id': event_id})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class EventAttendees(APIView):

    allowed_methods = ('GET',)

    def get(self, request, event_id):
        """
        Get the attendees of the event
        :param request: Request object
        :param event_id: Event id
        :return: Returns a response object with the status code and data, which is a list of dictionaries containing
        the registration details of the attendees.
        """
        # Getting offset, limit and timezone from the request
        pagination = Pagination(request)

        # Serialize the registrations
        registrations = EventRegistration.objects.filter(
            event_id=event_id
        ).order_by('-attendee_name')[pagination.offset: pagination.offset + pagination.limit]
        serializer = EventAttendeesSerializer(registrations, many=True, context={'event_id': event_id})
        return Response(serializer.data, status=status.HTTP_200_OK)