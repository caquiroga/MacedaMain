#!/bin/bash
awk -F "," -v sensorId="$1" '$2==sensorId {print $1","$2","$3","$4}' /home/pi/Surveillance/tmp/433.log | tail -n 1

