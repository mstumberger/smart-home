settings = {
	"id": 1,
	"name": "Dnevna soba",
	"ip": "192.168.88.250",
	"show_cpus": True,
	"show_memory": True,
	"show_disk": True,
	"disabled": False,
	"frequency": 3,
	"boardType": {
		"id": 1,
		"boardType": "Raspberry Pi 2B",
		"boardImageUrl": "https://www.bigmessowires.com/wp-content/uploads/2018/05/Raspberry-GPIO.jpg",
		"availablePins": [
			3,
			5,
			7,
			8,
			11,
			12,
			13,
			15,
			16,
			18,
			19,
			21,
			22,
			23,
			24,
			26,
			29,
			31,
			32,
			33,
			35,
			36,
			37,
			38,
			40
		],
		"availableGPIOPins": [
			2,
			3,
			4,
			14,
			15,
			17,
			18,
			27,
			22,
			23,
			24,
			10,
			9,
			25,
			11,
			8,
			7,
			5,
			6,
			12,
			13,
			19,
			16,
			26,
			20,
			21
		]
	},
	"configured_modules": [
		{
			"id": 14,
			"client": 1,
			"name": "Relay 1 - Dnevna soba",
			"type": {
				"id": 2,
				"type": "8-channel-relay",
				"power_pins": 0,
				"ground_pins": 1,
				"signal_pins": 8,
				"inputType": "pull_down"
			},
			"description": "Used to turn off and on mixing aplyances",
			"used_pins": [
				{
					"id": 56,
					"type": "ground",
					"pinModuleNumber": -1,
					"pin": 39,
					"gpioPin": -1,
					"client": 1,
					"module": 14
				},
				{
					"id": 57,
					"type": "signal",
					"pinModuleNumber": 1,
					"pin": 3,
					"gpioPin": 2,
					"client": 1,
					"module": 14
				},
				{
					"id": 58,
					"type": "signal",
					"pinModuleNumber": 2,
					"pin": 5,
					"gpioPin": 3,
					"client": 1,
					"module": 14
				},
				{
					"id": 59,
					"type": "signal",
					"pinModuleNumber": 3,
					"pin": 7,
					"gpioPin": 4,
					"client": 1,
					"module": 14
				},
				{
					"id": 60,
					"type": "signal",
					"pinModuleNumber": 4,
					"pin": 11,
					"gpioPin": 17,
					"client": 1,
					"module": 14
				},
				{
					"id": 61,
					"type": "signal",
					"pinModuleNumber": 5,
					"pin": 13,
					"gpioPin": 27,
					"client": 1,
					"module": 14
				},
				{
					"id": 62,
					"type": "signal",
					"pinModuleNumber": 6,
					"pin": 15,
					"gpioPin": 22,
					"client": 1,
					"module": 14
				},
				{
					"id": 63,
					"type": "signal",
					"pinModuleNumber": 7,
					"pin": 19,
					"gpioPin": 10,
					"client": 1,
					"module": 14
				},
				{
					"id": 64,
					"type": "signal",
					"pinModuleNumber": 8,
					"pin": 21,
					"gpioPin": 9,
					"client": 1,
					"module": 14
				}
			]
		}
	],
	"client_used_pins": [
		{
			"id": 56,
			"type": "ground",
			"pinModuleNumber": -1,
			"pin": 39,
			"gpioPin": -1,
			"client": 1,
			"module": 14
		},
		{
			"id": 57,
			"type": "signal",
			"pinModuleNumber": 1,
			"pin": 3,
			"gpioPin": 2,
			"client": 1,
			"module": 14
		},
		{
			"id": 58,
			"type": "signal",
			"pinModuleNumber": 2,
			"pin": 5,
			"gpioPin": 3,
			"client": 1,
			"module": 14
		},
		{
			"id": 59,
			"type": "signal",
			"pinModuleNumber": 3,
			"pin": 7,
			"gpioPin": 4,
			"client": 1,
			"module": 14
		},
		{
			"id": 60,
			"type": "signal",
			"pinModuleNumber": 4,
			"pin": 11,
			"gpioPin": 17,
			"client": 1,
			"module": 14
		},
		{
			"id": 61,
			"type": "signal",
			"pinModuleNumber": 5,
			"pin": 13,
			"gpioPin": 27,
			"client": 1,
			"module": 14
		},
		{
			"id": 62,
			"type": "signal",
			"pinModuleNumber": 6,
			"pin": 15,
			"gpioPin": 22,
			"client": 1,
			"module": 14
		},
		{
			"id": 63,
			"type": "signal",
			"pinModuleNumber": 7,
			"pin": 19,
			"gpioPin": 10,
			"client": 1,
			"module": 14
		},
		{
			"id": 64,
			"type": "signal",
			"pinModuleNumber": 8,
			"pin": 21,
			"gpioPin": 9,
			"client": 1,
			"module": 14
		}
	]
}