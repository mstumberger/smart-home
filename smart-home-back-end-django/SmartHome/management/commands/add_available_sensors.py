from django.core.management.base import BaseCommand

from SmartHome.constants import AVAILABLE_MODULES_DICT
from SmartHome.models import AvailableModule


class Command(BaseCommand):
	help = 'Creates available modules'

	def handle(self, *args, **options):
		available_modules = []
		for module in AVAILABLE_MODULES_DICT:
			available_modules.append(AvailableModule(
				type=module['type'],
				power_pins=module['powerPins'],
				ground_pins=module['groundPins'],
				signal_pins=module['signalPins'],
				inputType=module['inputType']
			))

		AvailableModule.objects.bulk_create(available_modules)
		self.stdout.write(self.style.SUCCESS('Successfully created available modules'))
