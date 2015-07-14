"""
Processes data and uploads it to ThingSpeak.
Intended to be run as a cron job every X minutes.
Looks for all files in raw_data_dir, and moves them
to processed_data_dir after processing.

Michelle Leonhart
michelle@tinwhiskers.net
"""


import httplib
import urllib
import os
import time


api_key = ''
data_dir = '/home/pi/Desktop/hamster_tracker/data/'
processed_data_dir = '/home/pi/Desktop/hamster_tracker/data/processed_files/'
WHEEL_CIRCUMFERENCE_INCHES = 18.0
INCHES_PER_FOOT = 12.0
FEET_PER_MILE = 5280.0

# omega = rotations per second
# kinetic energy = 0.5 * mass * (radius * omega)^2
#                = 0.5 * 0.025g * (0.075m * omega)^2

# TODO calculate rotations per second for each sprint
# omega = rotations / (end_time - start_time)

for raw_data_file in os.listdir('/home/pi/Desktop/hamster_tracker/data'):
    if raw_data_file.startswith('raw_'):
        sprint_start_time = None
        with open(data_dir + raw_data_file) as f:
            rotations = 0 
            for line in f:
                if not sprint_start_time:
                    sprint_start_time = line[:-1]
                    print sprint_start_time
                rotations = rotations + 1

        human_feet = rotations * WHEEL_CIRCUMFERENCE_INCHES / INCHES_PER_FOOT
        human_miles = human_feet / FEET_PER_MILE
        params = urllib.urlencode({
                                   'field1': rotations,
                                   'field2': human_feet,
                                   'field3': human_miles,
                                   'created_at': sprint_start_time,
                                   'timezone': 'America/Los_Angeles',
                                   'key': api_key
                                   })
        headers = {"Content-type": "application/x-www-form-urlencoded", "Accept": "text/plain"}
        conn = httplib.HTTPConnection("api.thingspeak.com:80")
        try:
            conn.request("POST", "/update", params, headers)
            response = conn.getresponse()
            print("params:")
            print params
            print response.status, response.reason
            conn.close()
            os.rename(data_dir + raw_data_file, processed_data_dir + raw_data_file)
            time.sleep(15)

        except Exception as e:
            print e
    


