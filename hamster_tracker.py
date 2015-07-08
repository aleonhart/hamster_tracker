#!/usr/bin/env python

import RPi.GPIO as GPIO
from datetime import datetime

led_pin = 7
hall_effect_sensor_pin = 18

is_led_on = False
is_hall_effect_sensor_on = False

GPIO.setmode(GPIO.BOARD)

GPIO.setup(led_pin, GPIO.OUT)                # set LED pin to OUTPUT
GPIO.setup(hall_effect_sensor_pin, GPIO.IN)  # set HALL pin to INPUT

GPIO.output(led_pin, is_led_on)

previous_state = 1
while True:
    try:

        # HE sensor is HIGH normally and LOW if magnet
        is_hall_effect_sensor_on = GPIO.input(hall_effect_sensor_pin)
        if is_hall_effect_sensor_on != previous_state:
            if is_hall_effect_sensor_on == 0:
                print(datetime.now())
		
            previous_state = is_hall_effect_sensor_on

        GPIO.output(led_pin, is_led_on)

    except KeyboardInterrupt:
        GPIO.output(led_pin, False)
        GPIO.cleanup()

GPIO.output(led_pin, False)
GPIO.cleanup()



