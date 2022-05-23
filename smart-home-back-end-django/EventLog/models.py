from django.db import models
from User.models import User
from SmartHome.models import Client


class Event(models.Model):
    TYPES = (
        ('user_sign_in', 'user_sign_in'),
        ('user_added', 'user_added'),
        ('temperature_reading', 'temperature_reading'),
        ('sensor_state_changed', 'sensor_state_changed'),
    )

    type = models.CharField(max_length=50, choices=TYPES)
    user = models.ForeignKey(User, null=True, blank=True, on_delete=models.SET_NULL)
    client = models.ForeignKey(Client, null=True, blank=True, on_delete=models.SET_NULL)
    added_at = models.DateTimeField(auto_now_add=True)
    additional_data = models.CharField(max_length=255, blank=True, null=True)
