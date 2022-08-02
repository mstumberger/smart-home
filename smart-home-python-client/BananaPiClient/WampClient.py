from autobahn.twisted.wamp import ApplicationSession, ApplicationRunner
from autobahn.wamp import ApplicationError
from twisted.internet.defer import inlineCallbacks
from twisted.internet.error import NoRouteError
from autobahn.twisted.util import sleep
from datetime import datetime
import argparse
import socket
import txaio
import signal
import sys
import six
import os
from models.ClientInterface import Client, NoopClient
from models.helpers import to_gib, get_stats, is_raspberrypi
from models.constants import REGISTER_OPTIONS, SUBSCRIBE_OPTIONS, TOPIC, PinType, Sensor

import RPi.GPIO as GPIO
import dht11
try:
    from picamera import PiCamera
except ImportError as e:
    PiCamera = None
    print(e)

txaio.use_twisted()


class RaspberryClientSettings(Client):
    log = txaio.make_logger()

    def __init__(self):
        # Configuration
        self.id = 0
        self.ip = None
        self.name = None
        self.publish_status = False
        self.loop_interval = 10
        self.board_mode = None
        self.positive_pins = []
        self.negative_pins = []
        self.output_pin_list = [2, 3, 4, 17, 27, 22, 10, 9]
        self.input_pin_list = [14]

        self.configured_io = {}
        self.configured_pins = {}

        # Sensor usages
        self.reader_instances = {}
        self.camera = None
        if PiCamera is not None:
            self.camera = PiCamera()

    def apply_config(self, config):
        self.set_board_mode(GPIO.BCM)
        sensor_id = self.add_sensor("Relay_8", "Dnevna soba")
        for i in self.output_pin_list:
            self.configure_pin(i, sensor_id, PinType.OUTPUT)

        sensor_id_temp = self.add_sensor("TemperatureSensorDH11", "Dnevna soba - okno")
        for i in self.input_pin_list:
            self.configure_pin(i, sensor_id_temp, PinType.INPUT)

    def initialize_board(self):
        GPIO.cleanup()
        GPIO.setmode(self.board_mode)
        GPIO.setwarnings(False)

    def set_board_mode(self, board_mode):
        self.board_mode = board_mode
        self.initialize_board()

    def add_input_callback(self, pin, callback):
        GPIO.add_event_detect(pin, GPIO.BOTH, callback=callback, bouncetime=50)

    @staticmethod
    def button_callback(channel):
        if not GPIO.input(14):
            print("Button pressed!")
        else:
            print("Button released!")

    def initialize_temperature_reader_DHT(self, pin):
        # read data using pin 14
        instance = dht11.DHT11(pin=pin)
        self.reader_instances[pin] = instance

    def change_output(self, pin,  value):
        print(f'Set pin {pin} value {value}')
        GPIO.output(pin, GPIO.LOW if value else GPIO.HIGH)
        sensor_id = None
        for sensor in self.configured_pins.keys():
            print(sensor, self.configured_pins[sensor])
            if pin in self.configured_pins[sensor].keys():
                sensor_id = sensor
                break

        if sensor_id is not None:
            previous_value = self.configured_pins[sensor_id][pin]["value"]
            self.configured_pins[sensor_id][pin]["value"] = value
            print(f"Change sensor {self.configured_io[sensor_id]} pin {pin} from {previous_value} to {value}")
        else:
            print(f"Pin {pin} is not added to sensor")

    def read_sensors(self):
        for pin in self.reader_instances.keys():
            result = self.reader_instances[pin].read()
            if result.is_valid():
                print("Last valid input: " + str(datetime.now()))
                print("Temperature: %d C" % result.temperature)
                print("Humidity: %d %%" % result.humidity)
            return result
        return None

    def add_sensor(self, sensor_type, sensor_name):
        sensor = Sensor.get_by_name(sensor_type)

        print("id", sensor.get_id())
        sensor.value[0]["name"] = sensor_name
        sensor_id = sensor.get_id()
        self.configured_io[sensor_id] = sensor
        self.configured_pins[sensor_id] = {}
        return sensor.get_id()

    def configure_pin(self, pin: int, sensor_id: str, pin_type: PinType):
        GPIO.setup(pin, pin_type.get())
        print(f'Set pin {pin} to type {pin_type}')
        pin_value = {"number": pin, "name": f'Pin {pin}', "value": None, "board_mode": self.board_mode}
        if pin_type == PinType.OUTPUT:
            GPIO.output(pin, GPIO.HIGH)
            pin_value.update(value=GPIO.HIGH)
        elif pin_type == PinType.INPUT:
            GPIO.setup(pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)
        else:
            print(f"{pin_type} not supported yet")
        self.configured_pins[sensor_id][pin] = pin_value

    @inlineCallbacks
    def take_picture(self):
        if self.camera is not None:
            self.camera.resolution = (2592, 1944)
            self.camera.framerate = 15
            self.camera.start_preview()
            yield sleep(5)
            self.camera.capture('/home/pi/Desktop/max.jpg')
            self.camera.stop_preview()


class ClientSession(ApplicationSession):
    def __init__(self, config=None):
        super().__init__(config)
        self.log = txaio.make_logger()
        self.ip = config.extra.get('config', None).get('ip', None)
        self.log.info(f'Client ip {self.ip}')
        self.client = RaspberryClientSettings() if is_raspberrypi() else NoopClient()

    def onConnect(self):
        self.log.info("Client connected")
        self.join(self.config.realm, [u'anonymous'])

    def onChallenge(self, challenge):
        self.log.info("Challenge for method {authmethod} received", authmethod=challenge.method)
        raise RuntimeError("We haven't asked for authentication!")

    def onClose(self, was_clean):
        self.log.info("Client disconnected")
        GPIO.cleanup()
        return super().onClose(was_clean)

    @inlineCallbacks
    def onJoin(self, details):
        self.log.info("Client session joined {details}", details=details)

        response = yield self.call('add_client', details.session, f'RaspberryPi-{self.ip}', self.ip)
        print(response)
        # get client configs
        self.client.apply_config({})

        yield self.register(self.get_available_sensors, f'relay.{self.ip}.get.all.sensors', options=REGISTER_OPTIONS)
        yield self.register(self.get_added_sensors, f'relay.{self.ip}.get.added.sensors', options=REGISTER_OPTIONS)
        yield self.register(self.get_configured_pins, f'relay.{self.ip}.get.configured.pins', options=REGISTER_OPTIONS)
        yield self.register(self.configure_pin, f'relay.{self.ip}.configue.pin', options=REGISTER_OPTIONS)
        yield self.register(self.high, f'relay.{self.ip}.toggle', options=REGISTER_OPTIONS)
        try:
            # config = yield self.call('backend.getTerminalConfig', self.ip)
            # if config.get('ip', None) != (None or ''):
            #     self.config = config
            #     print(config)

            # Subscribe to terminals topic
            # The we loop for ever.
            print("Entering stats loop ..")
            while True:
                try:
                    # Every time we loop, we get the stats for our machine
                    stats = {'ip': self.ip, 'name': self.client.name}
                    stats.update(get_stats())

                    # If we are requested to send the stats, we publish them using WAMP.
                    if self.client.publish_status:
                        print('Publish stats to topic : ' + TOPIC)
                        self.publish(TOPIC, stats)

                    if True:
                        result = self.client.read_sensors()
                        if result is not None:
                            try:
                                res = yield self.call(u'temp', result.temperature, result.humidity)
                                self.log.info("AutobahnPython/CALL: 'temp' called with result: {result}", result=res)
                            except ApplicationError as e:
                                ## ignore errors due to the frontend not yet having
                                ## registered the procedure we would like to call
                                if e.error != 'wamp.error.no_such_procedure':
                                    raise e

                    # Then we wait. Thanks to @inlineCallbacks, using yield means we
                    # won't block here, so our client can still listen to WAMP events
                    # and react to them.
                    yield sleep(self.client.loop_interval)
                except Exception as e:
                    print("Error in stats loop: {}".format(e))
                    break

        except Exception as e:
            print('Add terminal to database')
            self.publish(TOPIC, 'Add terminal with IP: ' + self.config.extra.get('config', None).get('ip', None))
            print("Error in stats loop: {}".format(e))

    @staticmethod
    def get_available_sensors():
        return Sensor.to_dict()

    def get_added_sensors(self):
        return self.client.configured_io

    def get_configured_pins(self):
        return self.client.configured_pins

    def high(self, pin, value: bool, details=None):
        print(pin, value)
        if pin in self.client.output_pin_list:
            self.client.change_output(pin, value)
            self.publish(TOPIC, f'Set pin {pin}  value {value} -> DONE')
            return "Done"
        else:
            print(f'Pin {pin} is not in the list {self.pin_list}')

    def configure_pin(self, pin, sensor, pin_type):
        pin_type_enum: PinType = PinType.get_type(pin_type)
        self.log.info(f'Configure pin {pin} as {pin_type_enum} for sensor {sensor}')
        self.client.configure_pin(pin, sensor, pin_type)

    def add_sensor(self, sensor_type, sensor_name):
        self.log.info(f'Add sensor {sensor_name} with name {sensor_name}')
        self.client.add_sensor(sensor_type, sensor_name)

    def onLeave(self, details):
        self.log.info("Router session closed ({details})", details=details)
        self.disconnect()

    def onDisconnect(self):
        self.log.info("Router connection closed")
        # Reset GPIO settings
        GPIO.cleanup()


def signal_handler(sig, frame):
    GPIO.cleanup()
    sys.exit(0)


if __name__ == '__main__':

    # Crossbar.io connection configuration
    url = os.environ.get('CBURL', u'ws://192.168.0.20:8080/ws')
    realm = os.environ.get('CBREALM', u'realm1')

    # parse command line parameters
    parser = argparse.ArgumentParser()
    parser.add_argument('-d', '--debug', action='store_true', help='Enable debug output.')
    parser.add_argument('--url', dest='url', type=six.text_type, default=url, help='The router URL (default: "ws://192.168.1.120:8080/ws").')
    parser.add_argument('--realm', dest='realm', type=six.text_type, default=realm, help='The realm to join (default: "realm1").')

    args = parser.parse_args()

    # start logging
    if args.debug:
        txaio.start_logging(level='debug')
    else:
        txaio.start_logging(level='info')

    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.connect(("8.8.8.8", 80))

    # any extra info we want to forward to our ClientSession (in self.config.extra)
    extra = dict(config={'name': socket.gethostname(), 'ip': s.getsockname()[0]})
    s.close()

    # now actually run a WAMP client using our session class ClientSession
    runner = ApplicationRunner(url=args.url, realm=args.realm, extra=extra)
    try:
        runner.run(ClientSession, auto_reconnect=True)
        signal.signal(signal.SIGINT, signal_handler)
        signal.pause()
    except NoRouteError:
        print("Server is offline")
