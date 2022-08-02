from SmartHome.models import Sensor, Dashboard, Client
from User.models import User
from rest_framework import serializers, serializers, viewsets


class UserSerializer(serializers.ModelSerializer):

    password = serializers.CharField(required=False)

    class Meta:
        model = User
        fields = '__all__'


class SettingsSerializer(serializers.ModelSerializer):

    class Meta:
        model = User.settings
        fields = '__all__'


# Serializers define the API representation.
class ClientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Client
        fields = '__all__'


# Serializers define the API representation.
class SensorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Sensor
        fields = '__all__'


# Serializers define the API representation.
class DashboardSerializer(serializers.ModelSerializer):
    class Meta:
        model = Dashboard
        fields = '__all__'
