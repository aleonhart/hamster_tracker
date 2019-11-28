"""
Takes data available in files and sends it to ThingSpeak
"""


import requests
import os
import time


# ThingSpeak Data
thingspeak_api_key = ''  # Put your ThingSpeak API key here
thingspeak_headers = {"Content-type": "application/x-www-form-urlencoded", "Accept": "text/plain"}

# Data Directories
data_dir_ready = '/home/pi/Desktop/The_Hamstrometer/data/2_data_ready/'
data_dir_processed = '/home/pi/Desktop/The_Hamstrometer/data/3_data_processed/'

# Calculation Constants
WHEEL_CIRCUMFERENCE_INCHES = 18.0  # Put your wheel circumference here
INCHES_PER_FOOT = 12.0
FEET_PER_MILE = 5280.0

# Process all files in the "ready" directory
for data_file in os.listdir(data_dir_ready):
    if data_file.startswith('raw_'):

        # Count the number of wheel rotations in the sprint
        sprint_start_time = None
        with open(data_dir_ready + data_file) as f:
            rotations = 0 
            for line in f:
                if not sprint_start_time:
                    sprint_start_time = line[:-1]
                rotations = rotations + 1

        # Calculate how far those wheel rotations translate to
        human_feet = rotations * WHEEL_CIRCUMFERENCE_INCHES / INCHES_PER_FOOT
        human_miles = human_feet / FEET_PER_MILE

        # Send the data to ThingSpeak
        request_data = {
           'field1': rotations,
           'field2': human_feet,
           'field3': human_miles,
           'created_at': sprint_start_time,
           'timezone': 'America/Los_Angeles',
           'key': thingspeak_api_key
        }

        print("Sending to ThingSpeak: Params {}".format(request_data))
        r = requests.post('https://api.thingspeak.com/update', data=request_data, headers=thingspeak_headers)

        if r.status_code == 200:
            # Move finished files to the "processed" directory
            os.rename(data_dir_ready + data_file, data_dir_processed + data_file)
        else:
            print("Failed to send data to ThingSpeak: {} {}".format(r.status_code, r.text))

        # Prevent us from hitting ThingSpeak's throttles
        time.sleep(15)
