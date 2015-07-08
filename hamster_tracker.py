#!/usr/bin/env python

import RPi.GPIO as GPIO

led_pin = 7
hall_effect_sensor_pin = 18

is_led_on = False
is_hall_effect_sensor_on = False

GPIO.setmode(GPIO.BOARD)

GPIO.setup(led_pin, GPIO.OUT)                # set LED pin to OUTPUT
GPIO.setup(hall_effect_sensor_pin, GPIO.IN)  # set HALL pin to INPUT

GPIO.output(led_pin, is_led_on)

while True:
    try:
        # HE sensor is HIGH normally and LOW if magnet
        
        is_hall_effect_sensor_on = GPIO.input(hall_effect_sensor_pin)

		if (is_hall_effect_sensor_on == False):
			#print("LED ON")
			is_led_on = True
		else:
			#print("LED OFF")
			is_led_on = False

		print(is_led_on)		
		GPIO.output(led_pin, is_led_on)

	except KeyboardInterrupt:
		GPIO.output(led_pin, False)
		GPIO.cleanup()

GPIO.output(led_pin, False)
GPIO.cleanup()



