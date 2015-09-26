#!/bin/bash
for file in $( find /tmp/motion -type f -name "??????????????-cam?-snapshot.jpg" )
do
	echo $file
	/home/pi/Surveillance/upload2FTP.py /home/pi/Surveillance/uploader-no-ip.cfg $file 0 0 
done
