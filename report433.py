#!/usr/bin/env python
import csv
import urllib
import os
import ConfigParser
from subprocess import Popen, PIPE
import urllib2
from pynma import PyNMA
import shelve

def reportSensor( sensorId ):

        myconfig = ConfigParser.ConfigParser()
        myconfig.read("/home/pi/Surveillance/uploader-no-ip.cfg")

        #Domoticz account credentials
        username = myconfig.get('domoticz', 'user')
        password = myconfig.get('domoticz', 'password')

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
			if (float(csv_data[3]) < 40):	humStat = 2
			elif(float(csv_data[3]) > 70):	humStat = 3
	                url = "http://caquiroga.no-ip.biz:8081/json.htm?type=command&param=udevice&idx=8&nvalue=0&svalue=" +  str(csv_data[2]) + ";" + str(csv_data[3]) + ";" + str(humStat) + ";"
	        elif sensorId==1:
                        if (float(csv_data[3]) < 40):      humStat = 2
                        elif(float(csv_data[3]) > 70):     humStat = 3
	                url = "http://caquiroga.no-ip.biz:8081/json.htm?type=command&param=udevice&idx=9&nvalue=0&svalue=" +  str(csv_data[2]) + ";" + str(csv_data[3]) + ";" + str(humStat) + ";"
	        elif sensorId==10:
        	        nma = PyNMA()
			temp = shelve.open("/home/pi/Surveillance/tmp/raintemp")
			nma.addkey(temp['nmakey'])
			print temp['nmakey']
        	        url = "http://caquiroga.no-ip.biz:8081/json.htm?type=command&param=udevice&idx=11&nvalue=0&svalue=0;" + str(csv_data[2]) + ";"
			if (float(csv_data[2]) > temp['rain']+2): nma.push("Maceda", 'Plou molt a Maceda', '', '', batch_mode=False)
			elif (float(csv_data[2]) > temp['rain']): nma.push("Maceda", 'Plou a Maceda', '', '', batch_mode=False)
			temp['rain'] = float(csv_data[2])		
			temp.close()
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

