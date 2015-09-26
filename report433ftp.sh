#!/bin/bash
rm /home/pi/Surveillance/tmp/433tmp.log
/home/pi/Surveillance/extractLast433.sh 1 >> /home/pi/Surveillance/tmp/433tmp.log
/home/pi/Surveillance/extractLast433.sh 2 >> /home/pi/Surveillance/tmp/433tmp.log
/home/pi/Surveillance/extractLast433.sh 10 >> /home/pi/Surveillance/tmp/433tmp.log
/home/pi/Surveillance/upload2FTP.py /home/pi/Surveillance/uploader-no-ip.cfg /home/pi/Surveillance/tmp/433tmp.log
