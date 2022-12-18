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
