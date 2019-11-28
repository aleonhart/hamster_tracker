#!/usr/bin/env python

"""
Listens to sensor input on PIN 18 and logs
the current time upon signal.
"""


import RPi.GPIO as GPIO
from datetime import datetime, timedelta
import time
import os

led_pin = 7
hall_effect_sensor_pin = 18

is_hall_effect_sensor_on = False
is_sprint = False

in_progress_data_dir = "data/in_progress_data/"
data_dir = "data/"

GPIO.setmode(GPIO.BOARD)

GPIO.setup(led_pin, GPIO.OUT)                # set LED pin to OUTPUT
GPIO.setup(hall_effect_sensor_pin, GPIO.IN)  # set HALL pin to INPUT

previous_state = 1
time_of_last_recording = datetime.now()
current_time_str = time.strftime("%Y%m%d-%H%M%S")
current_file_name = ''

while True:
    try:
        if is_sprint == True and datetime.now() - time_of_last_recording > timedelta(seconds=10):
            print("Sprint Ending. Closing file.")
            is_sprint = False
            os.rename(in_progress_data_dir + current_file_name, data_dir + current_file_name)
        
        # HE sensor is HIGH normally and LOW if magnet
        is_hall_effect_sensor_on = GPIO.input(hall_effect_sensor_pin)
        if is_hall_effect_sensor_on != previous_state:
            if is_hall_effect_sensor_on == 0:
                if not is_sprint:
                    is_sprint = True
                    current_time_str = time.strftime("%Y%m%d-%H%M%S")
                    current_file_name = 'raw_data_' + current_time_str
                    raw_data_file = open(in_progress_data_dir + current_file_name, 'wb')
                    print("Sprint Starting. Opening file: %s" % raw_data_file.name)

                print(time.strftime("%Y-%m-%d %H:%M:%S"))
                raw_data_file.write(time.strftime("%Y-%m-%d %H:%M:%S"))
                raw_data_file.write("\n")
                GPIO.output(led_pin, True)
                time_of_last_recording = datetime.now()

            previous_state = is_hall_effect_sensor_on

            GPIO.output(led_pin, False)

    except KeyboardInterrupt:
        GPIO.output(led_pin, False)
        GPIO.cleanup()
        if not raw_data_file.closed:
            raw_data_file.close()

GPIO.output(led_pin, False)
GPIO.cleanup()
if not raw_data_file.closed:
    raw_data_file.close()

os.rename(in_progress_data_dir + current_file_name, data_dir + current_file_name)




