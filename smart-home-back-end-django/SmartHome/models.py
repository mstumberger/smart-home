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

AVAILABLE_BOARDS = (
    ('Raspberry Pi 2B', 'Raspberry Pi 2B'),
    ('Banana Pro', 'Banana Pro'),
    ('ESP32', 'ESP32'),
)


class BoardType(models.Model):
    name = models.CharField(max_length=30, default='NoName')
    boardType = models.CharField(max_length=20, choices=AVAILABLE_BOARDS, default='Raspberry Pi 2B')
    # file will be uploaded to MEDIA_ROOT / uploads
    boardImageUrl = models.CharField(max_length=100, default='https://www.bigmessowires.com/wp-content/uploads/2018/05/Raspberry-GPIO.jpg')
    # boardImage = models.ImageField(upload_to='uploads/')


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
    boardType = models.ForeignKey(BoardType, on_delete=models.CASCADE, null=True)
    enabledSensors = models.CharField(max_length=100, default=json.dumps([]))
    usedPins = models.CharField(max_length=100, default=json.dumps([]))
    availablePins = models.CharField(max_length=100, default=json.dumps(
        [3, 5, 7, 8, 11, 12, 13, 15, 16, 18, 19, 21, 22, 23, 24, 26, 29, 31, 32, 33, 35, 36, 37, 38, 40]))
    availableGPIOPins = models.CharField(max_length=100, default=json.dumps(
        [2, 3, 4, 14, 15, 17, 18, 27, 22, 23, 24, 10, 9, 25, 11, 8, 7, 5, 6, 12, 13, 19, 16, 26, 20, 21]))

    def __str__(self):
        return f'{self.name} - {self.ip}'

@receiver(post_save, sender=Client, dispatch_uid="server_post_save")
def notify_server_config_changed(sender, instance, **kwargs):
    """ Notifies a client that its config has changed.

        This function is executed when we save a Client model, and it
        makes a POST request on the WAMP-HTTP bridge, allowing us to
        make a WAMP publication from Django.
    """

    requests.post("http://127.0.0.1:8080/notify",
                  json={
                      'topic': 'clientconfig.' + instance.ip,
                      'args': [model_to_dict(instance)]
                  })


AVAILABLE_SENSORS = (
    ('1-channel-relay', 'Relay'),
    ('8-channel-relay', 'Relay-8'),
    ('IRSensor', 'IRSensor'),
    ('TemperatureSensorDallas', 'TemperatureSensorDallas'),
    ('TemperatureSensorDH11', 'TemperatureSensorDH11'),
    ('HumiditySensor', 'HumiditySensor'),
    ('RFIDSensor', 'RFIDSensor'),
    ('CO2Sensor', 'CO2Sensor'),
)


class Sensor(models.Model):
    name = models.CharField(max_length=30, default='NoName')
    type = models.CharField(max_length=30, choices=AVAILABLE_SENSORS, default='Raspberry Pi 2B')
    description = models.CharField(max_length=100)
    pins = models.CharField(max_length=30)

    def __str__(self):
        return f'{self.name} - pins {self.pins}'
    # "Relay": {
    #     requiredPins: 1,
    #     details: "Relay requires at least one active GPIO pin"
    # },
    # "IRSensor": {
    #     requiredPins: 1,
    #     details: "Relay requires at least one active GPIO pin"
    # },
    # "TemperatureSensorDallas": {
    #     requiredPins: [],
    #     details: "Relay requires at least one active GPIO pin"
    # },
    # "TemperatureSensorDH11": {
    #     requiredPins: [],
    #     details: "Relay requires at least one active GPIO pin"
    # },
    # "HumiditySensor": {
    #     requiredPins: [],
    #     details: "Relay requires at least one active GPIO pin"
    # },
    # "RFIDSensor": {
    #     requiredPins: [],
    #     details: "Relay requires at least one active GPIO pin"
    # },
    # "CO2Sensor": {
    #     requiredPins: [],
    #     details: "Relay requires at least one active GPIO pin"
    # },


class GPIOPinConfig(models.Model):
    client_id = models.ForeignKey(Client, on_delete=models.CASCADE, null=True)
    sensor_id = models.ForeignKey(Sensor, on_delete=models.CASCADE, null=True)
    pins = models.CharField(max_length=256)

    def __str__(self):
        return f'{self.client_id} - {self.sensor_id}'


class Dashboard(models.Model):
    name = models.CharField(max_length=30, default='NoName')
    description = models.CharField(max_length=30)
    sensor_id = models.ForeignKey(Sensor, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.name} - {self.description}'
