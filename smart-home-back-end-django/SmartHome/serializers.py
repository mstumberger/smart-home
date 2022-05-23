from rest_framework import serializers
from User.models import User


class UserSerializer(serializers.ModelSerializer):

    password = serializers.CharField(required=False)

    class Meta:
        model = User
        fields = '__all__'


class SettingsSerializer(serializers.ModelSerializer):

    class Meta:
        model = User.settings
        fields = '__all__'