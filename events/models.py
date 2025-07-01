from django.db import models

class Event(models.Model):
    name = models.CharField(max_length=255, blank=False, null=False)
    location = models.CharField(max_length=255, blank=False, null=False)
    start_time = models.DateTimeField(blank=False, null=False)
    end_time = models.DateTimeField(blank=False, null=False)
    max_capacity = models.IntegerField(blank=False, null=False)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = "Events"
        verbose_name = "Event"
        unique_together = ('name', 'location', 'start_time', 'end_time')


class EventRegistration(models.Model):
    event = models.ForeignKey(Event, on_delete=models.CASCADE)
    attendee_name = models.CharField(max_length=255, blank=False, null=False)
    attendee_email = models.EmailField(blank=False, null=False)


    def __str__(self):
        return f'{self.attendee_name} - {self.attendee_email} - {self.event.name}'

    class Meta:
        verbose_name_plural = "Event Registrations"
        verbose_name = "Event Registration"
        unique_together = ('event', 'attendee_name', 'attendee_email')