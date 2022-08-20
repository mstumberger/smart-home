import json

from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.forms.models import model_to_dict

import requests


# "Raspberry Pi 2B": {
#     image: "https://www.bigmessowires.com/wp-content/uploads/2018/05/Raspberry-GPIO.jpg",
#     availablePins: [3,5,7,8,11,12,13,15,16,18,19,21,22,23,24,26,29,31,32,33,35,36,37,38,40],
#     availableGPIOPins: [2,3,4,14,15,17,18,27,22,23,24,10,9,25,11,8,7,5,6,12,13,19,16,26,20,21]
# },
# "Banana Pro": {
#     image: "https://www.bigmessowires.com/wp-content/uploads/2018/05/Raspberry-GPIO.jpg",
#     availablePins: []
# },
# "ESP32": {
#     image: "https://www.bigmessowires.com/wp-content/uploads/2018/05/Raspberry-GPIO.jpg",
#     availablePins: []
# }
from rest_framework.fields import JSONField

AVAILABLE_BOARDS = (
    ('Raspberry Pi 2B', 'Raspberry Pi 2B'),
    ('Banana Pro', 'Banana Pro'),
    ('ESP32', 'ESP32'),
)


class BoardType(models.Model):
    boardType = models.CharField(max_length=20, choices=AVAILABLE_BOARDS, default='Raspberry Pi 2B')
    # file will be uploaded to MEDIA_ROOT / uploads
    boardImageUrl = models.CharField(max_length=100, default='https://www.bigmessowires.com/wp-content/uploads/2018/05/Raspberry-GPIO.jpg')
    # boardImage = models.ImageField(upload_to='uploads/')
    availablePins = models.JSONField(max_length=100, default=[3, 5, 7, 8, 11, 12, 13, 15, 16, 18, 19, 21, 22, 23, 24, 26, 29, 31, 32, 33, 35, 36, 37, 38, 40])
    availableGPIOPins = models.JSONField(max_length=100, default=[2, 3, 4, 14, 15, 17, 18, 27, 22, 23, 24, 10, 9, 25, 11, 8, 7, 5, 6, 12, 13, 19, 16, 26, 20, 21])

    def __str__(self):
            return f'{self.boardType}'


AVAILABLE_GPIO_BOARD_MODES = (
    ('None', 'None'),
    ('pull_up', 'pull_up'),
)


class Client(models.Model):
    """ Our client configuration """

    name = models.CharField(max_length=30, default='NoName')

    # Client unique identifier
    ip = models.GenericIPAddressField()

    # What data to send to the dashboard
    show_cpus = models.BooleanField(default=True)
    show_memory = models.BooleanField(default=True)
    show_disk = models.BooleanField(default=True)

    # Stop sending data
    disabled = models.BooleanField(default=False)

    # Data refresh frequency
    frequency = models.IntegerField(default=1)
    boardType = models.ForeignKey(BoardType, related_name='board_type', on_delete=models.CASCADE, null=True)
    gpio_mode = models.CharField(max_length=20, choices=AVAILABLE_GPIO_BOARD_MODES, default='None')

    def __str__(self):
        return f'{self.name} - {self.ip}'


@receiver(post_save, sender=Client, dispatch_uid="server_post_save")
def notify_server_config_changed(sender, instance, **kwargs):
    """ Notifies a client that its config has changed.

        This function is executed when we save a Client model, and it
        makes a POST request on the WAMP-HTTP bridge, allowing us to
        make a WAMP publication from Django.
    """

    requests.post("http://127.0.0.1:8082/notify",
                  json={
                      'topic': 'clientconfig.' + instance.ip,
                      'args': [model_to_dict(instance)]
                  })


AVAILABLE_GPIO_INPUT_TYPES = (
    ('pull_up', 'pull_up'),
    ('pull_down', 'pull_down'),
)


AVAILABLE_MODULES_DICT = [
    {
        'type': '1-channel-relay',
        'displayName': 'Relay',
        'powerPins': 1,
        'groundPins': 1,
        'signalPins': 1,
        'inputType': AVAILABLE_GPIO_INPUT_TYPES[0][0]
    },
    {
        'type': '8-channel-relay',
        'displayName': 'Relay-8',
        'powerPins': 1,
        'groundPins': 1,
        'signalPins': 1,
        'inputType': AVAILABLE_GPIO_INPUT_TYPES[0][0]
    },
    {
        'type': 'IRSensor',
        'displayName': 'IRSensor',
        'powerPins': 1,
        'groundPins': 1,
        'signalPins': 1,
        'inputType': AVAILABLE_GPIO_INPUT_TYPES[0][0]
    },
    {
        'type': 'TemperatureSensorDallas',
        'displayName': 'TemperatureSensorDallas',
        'powerPins': 1,
        'groundPins': 1,
        'signalPins': 1,
        'inputType': AVAILABLE_GPIO_INPUT_TYPES[0][0]
    },
    {
        'type': 'TemperatureSensorDH11',
        'displayName': 'TemperatureSensorDH11',
        'powerPins': 1,
        'groundPins': 1,
        'signalPins': 1,
        'inputType': AVAILABLE_GPIO_INPUT_TYPES[0][0]
    },
    {
        'type': 'HumiditySensor',
        'displayName': 'HumiditySensor',
        'powerPins': 1,
        'groundPins': 1,
        'signalPins': 1,
        'inputType': AVAILABLE_GPIO_INPUT_TYPES[0][0]
    },
    {
        'type': 'RFIDSensor',
        'displayName': 'RFIDSensor',
        'powerPins': 1,
        'groundPins': 1,
        'signalPins': 6,
        'inputType': AVAILABLE_GPIO_INPUT_TYPES[0][0]
    },
    {
        'type': 'CO2Sensor',
        'displayName': 'CO2Sensor',
        'powerPins': 1,
        'groundPins': 1,
        'signalPins': 1,
        'inputType': AVAILABLE_GPIO_INPUT_TYPES[0][0]
    },
    {
        'type': 'Led-Output',
        'displayName': 'LedOutput',
        'powerPins': 0,
        'groundPins': 1,
        'signalPins': 1,
        'inputType': AVAILABLE_GPIO_INPUT_TYPES[0][0]
    },
]

AVAILABLE_MODULES = map(lambda module: (module['type'], module['displayName']), AVAILABLE_MODULES_DICT)


class AvailableModule(models.Model):
    type = models.CharField(max_length=30, choices=AVAILABLE_MODULES, default='Raspberry Pi 2B')
    power_pins = models.IntegerField(null=True, default=1)
    ground_pins = models.IntegerField(null=True, default=1)
    signal_pins = models.IntegerField(null=True, default=1)
    inputType = models.CharField(max_length=30, choices=AVAILABLE_GPIO_INPUT_TYPES, null=True, default=None)

    def __str__(self):
        return f'{self.type}: power pins {self.power_pins}, ground pins {self.ground_pins}, signal pins {self.signal_pins}'


class ConfiguredModule(models.Model):
    client = models.ForeignKey(Client, related_name='configured_modules', on_delete=models.CASCADE, null=True)
    type = models.ForeignKey(AvailableModule, related_name='available_modules', on_delete=models.CASCADE, null=True)
    name = models.CharField(max_length=30, default='NoName')
    description = models.CharField(max_length=100)

    def __str__(self):
        return f'{self.client} - {self.type.type} - {self.name} - {self.description}'


class GPIOPinConfig(models.Model):
    client = models.ForeignKey(Client, related_name='client_used_pins', on_delete=models.CASCADE, null=True)
    module = models.ForeignKey(ConfiguredModule, related_name='used_pins', on_delete=models.CASCADE, null=True)
    pinModuleNumber = models.IntegerField(null=True)
    pin = models.IntegerField(null=True)
    gpioPin = models.IntegerField(null=True)

    def __str__(self):
        return f'{self.module} - Pin {self.pin}'


class Dashboard(models.Model):
    name = models.CharField(max_length=30, default='NoName')
    description = models.CharField(max_length=30)
    module = models.ForeignKey(ConfiguredModule, on_delete=models.CASCADE, null=True)

    def __str__(self):
        return f'{self.name} - {self.description}'
