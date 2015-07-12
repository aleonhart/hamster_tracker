#!/usr/bin/env python

import RPi.GPIO as GPIO
from datetime import datetime, timedelta
import time

led_pin = 7
hall_effect_sensor_pin = 18

is_led_on = False
is_hall_effect_sensor_on = False
is_sprint = False

data_dir = "data/"

GPIO.setmode(GPIO.BOARD)

GPIO.setup(led_pin, GPIO.OUT)                # set LED pin to OUTPUT
GPIO.setup(hall_effect_sensor_pin, GPIO.IN)  # set HALL pin to INPUT

GPIO.output(led_pin, is_led_on)

previous_state = 1
time_of_last_recording = datetime.now()
current_time_str = time.strftime("%Y%m%d-%H%M%S")

while True:
    try:
	if is_sprint == True and datetime.now() - time_of_last_recording > timedelta(seconds=5):
            print("Sprint Ending. Closing file: %s" % raw_data_file.name)
            is_sprint = False
        
        # HE sensor is HIGH normally and LOW if magnet
        is_hall_effect_sensor_on = GPIO.input(hall_effect_sensor_pin)
        if is_hall_effect_sensor_on != previous_state:
            if is_hall_effect_sensor_on == 0:
		if is_sprint == False:
                    is_sprint = True
                    current_time_str = time.strftime("%Y%m%d-%H%M%S")
                    raw_data_file = open(data_dir + 'raw_data_' + current_time_str, 'wb')
                    print("Sprint Starting. Opening file: %s" % raw_data_file.name)

		print(time.strftime("%Y-%m-%d %H:%M:%S"))
		raw_data_file.write(time.strftime("%Y-%m-%d %H:%M:%S"))
		raw_data_file.write("\n")
                time_of_last_recording = datetime.now()

        previous_state = is_hall_effect_sensor_on

        GPIO.output(led_pin, is_led_on)

    except KeyboardInterrupt:
        GPIO.output(led_pin, False)
        GPIO.cleanup()
        if not raw_data_file.closed:
            raw_data_file.close()

GPIO.output(led_pin, False)
GPIO.cleanup()
if not raw_data_file.closed:
    raw_data_file.close()



