from abc import ABC, abstractmethod


class Client(ABC):
    @abstractmethod
    def initialize_board(self):
        pass

    @abstractmethod
    def set_board_mode(self, board_mode):
        pass

    @abstractmethod
    def add_input_callback(self, pin, callback):
        pass

    @abstractmethod
    def initialize_temperature_reader_DHT(self, pin):
        pass

    @abstractmethod
    def change_output(self, pin,  value):
        pass

    @abstractmethod
    def read_sensors(self):
        pass

    @abstractmethod
    def configure_pin(self, pin, sensor, pin_type):
        pass


class NoopClient(Client):
    def initialize_board(self):
        print("initialize_board")

    def set_board_mode(self, board_mode):
        print("set_board_mode")

    def add_input_callback(self, pin, callback):
        print("add_input_callback")

    def initialize_temperature_reader_DHT(self, pin):
        print("initialize_temperature_reader_DHT")

    def change_output(self, pin, value):
        print("change_output")

    def read_sensors(self):
        print("read_sensors")

    def configure_pin(self, pin, sensor, pin_type):
        print("configure_pin")