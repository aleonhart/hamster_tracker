"""
Processes data and inserts it into our local database
.
Intended to be run as a cron job every X minutes.
Looks for all files in raw_data_dir, and moves them
to processed_data_dir after processing.
"""


import os
import time
import sqlite3


data_dir = '/home/pi/Desktop/hamster_tracker/data/'
processed_data_dir = '/home/pi/Desktop/hamster_tracker/data/processed_files/'
WHEEL_CIRCUMFERENCE_INCHES = 18.0
INCHES_PER_FOOT = 12.0
FEET_PER_MILE = 5280.0

conn = sqlite3.connect('hamstrometer.db')
curs = conn.cursor()

# process each file of raw sprint data into the sprints database
for raw_data_file in os.listdir(data_dir):
    if raw_data_file.startswith('raw_'):
        sprint_start_time = None
        sprint_end_time = None

        print "Processing: %s" % raw_data_file
        # calculate number of rotations in the sprint
        with open(data_dir + raw_data_file) as f:
            rotations = 0
            for line in f:
                if not sprint_start_time:
                    sprint_start_time = line[:-1]
                    print sprint_start_time
                rotations = rotations + 1
                sprint_end_time = line[:-1]

        try:
            # write line to table if it does not already exist
            # !relying on uniqueness of timestamps to ensure rerunnability
            print "INSERT INTO sprints VALUES ('{}', '{}', {});".format(sprint_start_time, sprint_end_time, rotations)

            curs.execute('INSERT INTO sprints (start_datetime, end_datetime, rotations) VALUES(?,?,?)',
                         (sprint_start_time, sprint_end_time, rotations))

            conn.commit()

            # DEBUG
            # curs.execute('select * from sprints;')
            # print curs.fetchall()

            # move the file to the processed folder  -- this is off during debug
            # os.rename(data_dir + raw_data_file, processed_data_dir + raw_data_file)
            time.sleep(1)

        except Exception as e:
            print "EXCEPTION: %s" % e

conn.close()



