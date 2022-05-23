from django.contrib.auth import get_user_model

from rest_framework import serializers

User = get_user_model()


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = tuple(User.REQUIRED_FIELDS) + (
            User._meta.pk.name,
            User.USERNAME_FIELD,
        )
        read_only_fields = (
            User.USERNAME_FIELD,
        )


class CustomUserSerializerEvent(serializers.ModelSerializer):

    password = serializers.CharField(required=False)

    class Meta:
        model = User
        fields = '__all__'


class CustomUserSerializer(serializers.ModelSerializer):

    password = serializers.CharField(required=False)

    class Meta:
        model = User
        fields = '__all__'
