from rest_framework import serializers

from User.serializers import CustomUserSerializerEvent
from .models import Event


class EventSerializer(serializers.ModelSerializer):
    user = CustomUserSerializerEvent()

    class Meta:
        model = Event
        fields = '__all__'
