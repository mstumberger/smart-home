import uuid

from autobahn.wamp import SubscribeOptions, RegisterOptions
import RPi.GPIO as GPIO
import enum


REGISTER_OPTIONS = RegisterOptions(details_arg='details')
SUBSCRIBE_OPTIONS = SubscribeOptions(details_arg='details')

TOPIC = u'smart.home.clients.updates'


class PinType(enum.Enum):
    INPUT = {"name": "input", "value": GPIO.IN}
    OUTPUT = {"name": "output", "value": GPIO.OUT}
    PWM = {"name": "pwm", "value": GPIO.PWM}

    # power
    POSITIVE = {"name": "positive", "value": None}
    NEGATIVE = {"name": "negative", "value": None}

    def get(self):
        return self.value["value"]

    @classmethod
    def get_type(cls, pin_type):
        for e in cls:
            if e.value["name"] == pin_type:
                return e
        raise AttributeError(f'Could not find type {pin_type}')

    @classmethod
    def to_dict(cls):
        """Returns a dictionary representation of the enum."""
        return {e.name: e.value for e in cls}

    @classmethod
    def keys(cls):
        """Returns a list of all the enum keys."""
        return cls._member_names_

    @classmethod
    def values(cls):
        """Returns a list of all the enum values."""
        return list(cls._value2member_map_.keys())


class Sensor(enum.Enum):
    Relay_1 = {
        "id": 1,
        "requiredPins": 1,
        "powerPin": 1,
        "negativePins": 1,
        "pinType": PinType.OUTPUT
    },
    Relay_2 = {
          "id": 2,
          "requiredPins": 1,
          "powerPin": 1,
          "negativePins": 1,
          "pinType": PinType.OUTPUT
      },
    Relay_4 = {
          "id": 3,
          "requiredPins": 1,
          "powerPin": 1,
          "negativePins": 1,
          "pinType": PinType.OUTPUT
      },
    Relay_8 = {
          "id": 4,
          "requiredPins": 1,
          "powerPin": 1,
          "negativePins": 1,
          "pinType": PinType.OUTPUT
      },
    IRSensor = {
           "id": 5,
           "requiredPins": 1,
           "powerPin": 1,
           "negativePins": 1,
           "pinType": PinType.INPUT
       },
    TemperatureSensorDallas = {
          "id": 6,
          "requiredPins": 1,
          "powerPin": 1,
          "negativePins": 1,
          "pinType": PinType.INPUT
      },
    TemperatureSensorDH11 = {
        "id": 7,
        "requiredPins": 1,
        "powerPin": 1,
        "negativePins": 1,
        "pinType": PinType.INPUT
    },
    HumiditySensor = {
         "id": 8,
         "requiredPins": 1,
         "powerPin": 1,
         "negativePins": 1,
         "pinType": PinType.INPUT
     },
    RFIDSensor = {
         "id": 9,
         "requiredPins": 1,
         "powerPin": 1,
         "negativePins": 1,
         "pinType": PinType.INPUT
     },
    CO2Sensor = {
        "id": 10,
        "requiredPins": 1,
        "powerPin": 1,
        "negativePins": 1,
        "pinType": PinType.INPUT
    },

    def get(self):
        self.value[0]["id"] = uuid.uuid4()
        return self.value

    def get_id(self) -> str:
        return self.value[0]['id']

    @classmethod
    def get_by_name(cls, name):
        for e in cls:
            if e.name == name:
                e.value[0]["id"] = uuid.uuid4()
                return e
        raise AttributeError(f'Could not find type {name}')

    @classmethod
    def to_dict(cls):
        """Returns a dictionary representation of the enum."""
        return {e.name: e.value for e in cls}

    def get_details(self):
        return f"Sensor {self.name} with id {self.value['id']} requires {self.value['powerPin']} power," \
               f" {self.value['negativePins']} negative and {self.value['requiredPins']} GPIO signal pins, " \
               f"{self.value['pinType'].name}"


if __name__ == '__main__':
    print(PinType.get_type("input"))
    print(PinType.get_type("output").get())
    print(Sensor.get_by_name("HumiditySensor"))
    sensor = Sensor.get_by_name("TemperatureSensorDH11")
    print(sensor.get_id())

