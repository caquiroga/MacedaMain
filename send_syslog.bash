#!/bin/bash
_now=$(date +"%Y%m%d")
_file="/var/log/syslog.$_now"
echo $_file
sudo rm $_file
sudo rm $_file.gz
sudo cp /var/log/syslog $_file
echo "Compressing file..."
sudo gzip $_file
echo "Sending file..."
sudo /home/pi/Surveillance/upload2FTP.py /home/pi/Surveillance/uploader-no-ip.cfg $_file.gz 0 0
echo "Done."
