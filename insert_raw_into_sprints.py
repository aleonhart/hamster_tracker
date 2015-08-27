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
import sqlite3


# api_key = ''
data_dir = '/home/pi/Desktop/hamster_tracker/data/'
processed_data_dir = '/home/pi/Desktop/hamster_tracker/data/processed_files/'
WHEEL_CIRCUMFERENCE_INCHES = 18.0
INCHES_PER_FOOT = 12.0
FEET_PER_MILE = 5280.0

conn=sqlite3.connect('hamstrometer.db')
curs=conn.cursor()

for raw_data_file in os.listdir('/home/pi/Desktop/hamster_tracker/data'):
    if raw_data_file.startswith('raw_'):
        sprint_start_time = None
        sprint_end_time = None
        with open(data_dir + raw_data_file) as f:
            rotations = 0
            for line in f:
                if not sprint_start_time:
                    sprint_start_time = line[:-1]
                    print sprint_start_time
                rotations = rotations + 1
                sprint_end_time = line[:-1]

        human_feet = rotations * WHEEL_CIRCUMFERENCE_INCHES / INCHES_PER_FOOT
        human_miles = human_feet / FEET_PER_MILE

        try:
            print "Verify that data does not already exist in table..."
            print "SELECT * FROM sprints WHERE start_datetime = '{}'".format(sprint_start_time)
            rows = curs.execute("SELECT * FROM sprints WHERE start_datetime = '{}'".format(sprint_start_time))
            if rows:
                print rows.arraysize
            # print "INSERT INTO sprints (start_datetime, end_datetime, rotations) " \
            #       "VALUES ({}, {}, {})".format(sprint_start_time, sprint_end_time, rotations)

            # curs.execute("INSERT INTO sprints (start_datetime, end_datetime, rotations) VALUES ({}, {}, {})".format())
            conn.commit()
            # os.rename(data_dir + raw_data_file, processed_data_dir + raw_data_file)
            time.sleep(1)

        except Exception as e:
            print e
            conn.close()

conn.close()



