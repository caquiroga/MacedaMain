#!/usr/bin/env python
import csv
import urllib
import os
import ConfigParser
from subprocess import Popen, PIPE
import urllib2


def reportSensor( sensorId ):

        config = ConfigParser.ConfigParser()
        config.read("./uploader-no-ip.cfg")

        #Domoticz account credentials
        username = config.get('domoticz', 'user')
        password = config.get('domoticz', 'password')

	print username
	print password

	output = ''
	p = urllib2.HTTPPasswordMgrWithDefaultRealm()

        process = Popen(["/home/pi/Surveillance/extractLast433.sh", str(sensorId)], stdout=PIPE)
        (output, err) = process.communicate()
        exit_code = process.wait()
        output = output[:-1]
	csv_data = output.split(",")
	if len(output)>0:
		csv_data = output.split(",")
                humStat = 0
	        if (sensorId==2):
			if (csv_data[3] < 40):	humStat = 2
			elif(csv_data[3] > 70):	humStat = 3
	                url = "http://caquiroga.no-ip.biz:8081/json.htm?type=command&param=udevice&idx=13&nvalue=0&svalue=" +  str(csv_data[2]) + ";" + str(csv_data[3]) + ";" + str(humStat) + ";"
	        elif sensorId==1:
                        if (csv_data[3] < 40):      humStat = 2
                        elif(csv_data[3] > 70):     humStat = 3
	                url = "http://caquiroga.no-ip.biz:8081/json.htm?type=command&param=udevice&idx=12&nvalue=0&svalue=" +  str(csv_data[2]) + ";" + str(csv_data[3]) + ";" + str(humStat) + ";"
	        elif sensorId==10:
        	        url = "http://caquiroga.no-ip.biz:8081/json.htm?type=command&param=udevice&idx=15&nvalue=0&svalue=0;" +  str(csv_data[2]) + ";"
	        print url
	        p.add_password(None, url, username, password)
	        handler = urllib2.HTTPBasicAuthHandler(p)
	        opener = urllib2.build_opener(handler)
	        urllib2.install_opener(opener)
	        page = urllib2.urlopen(url).read()
	return


try:
	reportSensor(1);
	reportSensor(2);
	reportSensor(10);

except Exception,e: print str(e)

