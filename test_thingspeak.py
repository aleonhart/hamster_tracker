
import httplib
import urllib
import os
import time

data_dir = 'data/'
sprint_start_time = None

for raw_data_file in os.listdir('data'):
    if raw_data_file.startswith('raw'):
        print("file name:")
        print(raw_data_file)
        with open(data_dir + raw_data_file) as file:
            rotations = 0 
            for line in file:
                print("line:")
                print line
                if not sprint_start_time:
                    sprint_start_time = line[:-1]
		    print("sprint start time:")
                    print(sprint_start_time)
                rotations = rotations + 1
        
        params = urllib.urlencode({'field1': rotations, 'created_at': sprint_start_time, 'timezone': 'America/Los_Angeles', 'key': ''})
        headers = {"Content-type": "application/x-www-form-urlencoded", "Accept": "text/plain"}

	conn = httplib.HTTPConnection("api.thingspeak.com:80")
	try:
            conn.request("POST", "/update", params, headers)
            response = conn.getresponse()
            print("params:")
            print params
            print response.status, response.reason
            conn.close()
        except Exception as e:
            print e

        sprint_start_time = None    


#distance = 50

#headers = {"Content-typZZe": "application/x-www-form-urlencoded", "Accept": "text/plain"}

#conn = httplib.HTTPConnection("api.thingspeak.com:80")

#try:
#	conn.request("POST", "/update", params, headers)
#	response = conn.getresponse()
#	print distance
#	print response.status, response.reason
#	conn.close()
#except Exception as e:
#	print e



