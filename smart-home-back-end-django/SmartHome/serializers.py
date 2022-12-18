from pprint import pprint

from SmartHome.models import ConfiguredModule, Dashboard, Client, GPIOPinConfig, BoardType, AvailableModule
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
class GPIOPinConfigSerializer(serializers.ModelSerializer):
    class Meta:
        model = GPIOPinConfig
        fields = '__all__'


# Serializers define the API representation.
class AvailableModuleSerializer(serializers.ModelSerializer):
    class Meta:
        model = AvailableModule
        fields = [
            'id',
            'type',
            'power_pins',
            'ground_pins',
            'signal_pins',
            'inputType',
        ]


# Serializers define the API representation.
class ModuleSerializer(serializers.ModelSerializer):
    used_pins = GPIOPinConfigSerializer(many=True)
    type = AvailableModuleSerializer(many=False)

    class Meta:
        model = ConfiguredModule
        fields = [
            'id',
            'client',
            'name',
            'type',
            'description',
            'used_pins',
        ]

    def create(self, validated_data):
        module_type = validated_data.pop('type', [])
        used_pins = validated_data.pop('used_pins', [])
        instance = ConfiguredModule.objects.create(**validated_data)
        try:
            instance.type = AvailableModule.objects.get(type__exact=module_type['type'])
        except Exception as e:
            print(e)
        try:
            for used_pin in used_pins:
                used_pin_object = GPIOPinConfig.objects.create(client=instance.client, module=instance, **used_pin)
                used_pin_object.save()

        except Exception as e:
            print(e)

        return instance


# Serializers define the API representation.
class ClientSerializerLite(serializers.ModelSerializer):
    class Meta:
        model = Client
        fields = ["ip"]


# Serializers define the API representation.
class ModuleWithClientSerializer(serializers.ModelSerializer):
    used_pins = GPIOPinConfigSerializer(many=True)
    client = ClientSerializerLite(many=False)

    class Meta:
        model = ConfiguredModule
        fields = [
            'id',
            'client',
            'name',
            'type',
            'description',
            'used_pins',
        ]

    def create(self, validated_data):
        used_pins = validated_data.pop('used_pins', [])
        instance = ConfiguredModule.objects.create(**validated_data)
        try:
            for used_pin in used_pins:
                used_pin_object = GPIOPinConfig.objects.create(client=instance.client, module=instance, **used_pin)
                used_pin_object.save()

        except Exception as e:
            print(e)

        return instance


# Serializers define the API representation.
class BoardTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = BoardType
        fields = '__all__'


# Serializers define the API representation.
class ClientSerializer(serializers.ModelSerializer):
    # sensors = serializers.PrimaryKeyRelatedField(many=True, read_only=True)
    configured_modules = ModuleSerializer(many=True)
    boardType = BoardTypeSerializer(many=False)
    client_used_pins = GPIOPinConfigSerializer(many=True)

    class Meta:
        model = Client
        fields = [
            'id',
            'name',
            'ip',
            'show_cpus',
            'show_memory',
            'show_disk',
            'disabled',
            'frequency',
            'boardType',
            'configured_modules',
            'client_used_pins'
        ]

    def create(self, validated_data):
        try:
            sensors = validated_data.pop('sensors', [])
            instance = Client.objects.create(**validated_data)
            for sensor in sensors:
                sensor_object = ConfiguredModule.objects.create(client=instance, **sensor)
                sensor_object.save()
            return instance

        except Exception as e:
            print(e)


# Serializers define the API representation.
class DashboardSerializer(serializers.ModelSerializer):
    class Meta:
        model = Dashboard
        fields = '__all__'

