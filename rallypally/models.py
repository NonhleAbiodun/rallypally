from django.db import models


class ReceivedMessage(models.Model):
    twilio_number = models.CharField(max_length=64)
    message = models.CharField(max_length=255)
    datetime_received = models.DateTimeField(auto_now_add=True)
