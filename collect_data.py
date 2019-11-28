#!/usr/bin/env python

"""
Collects data from the sensor attached to the Raspberry Pi and saves that data to files.
"""

import time
import os
from datetime import datetime, timedelta
import RPi.GPIO as GPIO


# Raspberry Pi Pins
led_pin = 7      # The Raspberry Pi pin you plug your LED into
sensor_pin = 18  # The Raspberry Pi pin you plug the Hall Effect (HE) sensor into

# Raspberry Pi Setup
GPIO.setmode(GPIO.BOARD)
GPIO.setup(led_pin, GPIO.OUT)                # set LED pin to OUTPUT
GPIO.setup(sensor_pin, GPIO.IN)  # set sensor pin to INPUT

# Data Directories
data_dir_live = "data/1_data_live/"    # Files that are currently being written to
data_dir_ready = "data/2_data_ready/"  # Files that are ready to be handled by send_data.py

# HE sensor is HIGH normally and LOW if the magnet is present
MAGNET_PRESENT = 0
MAGNET_NOT_PRESENT = 1

# Initialize States
previous_sensor_state = MAGNET_NOT_PRESENT
is_magnet_present = False
sprint_is_active = False
time_of_last_recording = datetime.now()
current_file_name = ''

# This script is meant to be left running
while True:
    try:
        # If we're mid-sprint and the hamster is still for >10 seconds, close the sprint. The hamster has left the wheel.
        if sprint_is_active and (datetime.now() - time_of_last_recording) > timedelta(seconds=10):
            print("Sprint Ending. Closing file.")
            sprint_is_active = False
            # Move the finished sprint file to the "ready" directory
            os.rename(data_dir_live + current_file_name, data_dir_ready + current_file_name)

        # If the hamster starts running, we should sense the magnet passing by
        is_magnet_present = GPIO.input(sensor_pin)
        if is_magnet_present != previous_sensor_state:
            if is_magnet_present == MAGNET_PRESENT:
                # If we don't have an active sprint, we need to start one and create a new file
                if not sprint_is_active:
                    sprint_is_active = True
                    current_file_name = 'raw_data_{}'.format(time.strftime("%Y%m%d-%H%M%S"))
                    data_file = open(data_dir_live + current_file_name, 'wb')
                    print("Sprint Starting. Opening file: {}".format(data_file.name))

                # If we do have an active sprint, we can write to the existing sprint file
                print(time.strftime("%Y-%m-%d %H:%M:%S"))
                data_file.write(time.strftime("%Y-%m-%d %H:%M:%S"))
                data_file.write("\n")
                time_of_last_recording = datetime.now()

                # Turn on the LED for debugging
                GPIO.output(led_pin, True)

            # Take note of whether the magnet is here or not
            previous_sensor_state = is_magnet_present

            # Turn off the LED for debugging
            GPIO.output(led_pin, False)

    except KeyboardInterrupt:
        print("Script stopped!")


print("Cleaning up")
GPIO.output(led_pin, False)
GPIO.cleanup()
if not data_file.closed:
    print("Closing the file.")
    data_file.close()

os.rename(data_dir_live + current_file_name, data_dir_ready + current_file_name)




