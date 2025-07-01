# Python inbuilt modules
from zoneinfo import ZoneInfo
from datetime import datetime

# Django inbuilt modules
from django.utils import timezone

# Django REST framework modules
from rest_framework.exceptions import APIException
from rest_framework import status


def get_current_time_in_timezone(usr_timezone='Asia/Kolkata'):
    """
    :param usr_timezone: Timezone of the user
    :return: Current time in the timezone
    """
    u_tz = ZoneInfo(usr_timezone)
    time = timezone.now().astimezone(u_tz)
    return time


def convert_ist_to_any_timezone(time, usr_timezone='Asia/Kolkata'):
    """
    :param time: Time to be converted
    :param usr_timezone: Timezone of the user
    :return: Time in the timezone
    """
    if isinstance(time, str):
        time = datetime.strptime(time, '%Y-%m-%d %H:%M:%S')
    u_tz = ZoneInfo(usr_timezone)
    time = time.astimezone(u_tz)
    return time


def convert_anytime_to_ist(dt):
    if not dt:
        return None

    if isinstance(dt, str):
        # Convert string with timezone into datetime
        dt = datetime.fromisoformat(dt.replace("Z", "+00:00"))  # handle Zulu UTC

    if dt.tzinfo is None:
        # Assume input is in UTC if naive
        dt = dt.replace(tzinfo=ZoneInfo('UTC'))

    # Convert to IST
    return dt.astimezone(ZoneInfo('Asia/Kolkata'))



class Pagination:
    def __init__(self, request=None, offset=0, limit=10):
        self.request = request
        if request is not None:
            self.set_offset_limit()
        else:
            self.offset = offset
            self.limit = limit

    def set_offset_limit(self):
        offset, limit = None, None
        if self.request.method == 'GET':
            offset = eval(self.request.GET.get('offset', '0'))
            limit = eval(self.request.GET.get('limit', '10'))
        elif self.request.method == 'POST':
            offset = eval(self.request.POST.get('offset', '0'))
            limit = eval(self.request.POST.get('limit', '10'))
        self.offset = offset
        self.limit = limit

# Custom Exception
class CustomAPIException(APIException):
    def __init__(self, message, status_code=status.HTTP_400_BAD_REQUEST):
        self.status_code = status_code
        self.detail = {"message": message}
