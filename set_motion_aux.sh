#!/bin/sh
/etc/init.d/motion stop
#/etc/init.d/mjpg-streamer-start.sh stop
#sudo rmmod uvcvideo
#sleep 5
#sudo modprobe uvcvideo quirks=0x100
#/etc/init.d/mjpg-streamer-start.aux.sh start
sudo cp /etc/motion/motion.conf.aux /etc/motion/motion.conf
/etc/init.d/motion start
