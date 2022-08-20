from django.core.management.base import BaseCommand, CommandError
from SmartHome.models import AvailableModule, AVAILABLE_MODULES_DICT


class Command(BaseCommand):
	help = 'Creates available modules'

	def handle(self, *args, **options):
		available_modules = []
		for module in AVAILABLE_MODULES_DICT:
			new_module = AvailableModule(
				type=module['type'],
				power_pins=module['powerPins'],
				ground_pins=module['groundPins'],
				signal_pins=module['signalPins'],
				inputType=module['inputType']
			)
			available_modules.append(new_module)

		AvailableModule.objects.bulk_create(available_modules)
		self.stdout.write(self.style.SUCCESS('Successfully created available modules'))
