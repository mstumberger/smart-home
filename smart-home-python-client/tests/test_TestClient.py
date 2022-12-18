from unittest import TestCase

from BananaPiClient.TestClient import RaspberryClientSettings
from tests.constants import settings


class TestRaspberryClientSettings(TestCase):

	raspberry = RaspberryClientSettings()

	def test_apply_config(self):
		self.raspberry.apply_config(settings)
