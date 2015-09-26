#!/bin/sh
#/home/pi/Surveillance/pcsensor/pcsensor -c  >> /home/pi/Surveillance/tmp/pcsensor.log 
#PCSENSOR=$(tail -n1 /home/pi/Surveillance/tmp/pcsensor.log | awk 'BEGIN { FS = "," } ; {print "Int.: "$2""}')
#echo $PCSENSOR
#wget "http://www2.meteogalicia.es/servizos/MComunicacion/xml/observacion/estacions/estado_actual_p.asp?idEst=10053" 
#grep "temperature" estado_actual_p.asp?idEst=10053 
#OUTDOOR2=$(grep "temperatura" estado_actual_p.asp?idEst=10053 | awk 'BEGIN { FS = "\"" } ; { printf "Lugo: %.1f", $2}') 
#echo $OUTDOOR2
OREGON_TI=$(more /home/pi/Surveillance/tmp/433.log | awk 'BEGIN { FS = "," } ; {if($2=="2") print "Int.: "$3""}' | tail -n1)
echo $OREGON_TI
OREGON_T=$(more /home/pi/Surveillance/tmp/433.log | awk 'BEGIN { FS = "," } ; {if($2=="1") print "Ext.: "$3""}' | tail -n1)
echo $OREGON_T
OREGON_H=$(more /home/pi/Surveillance/tmp/433.log | awk 'BEGIN { FS = "," } ; {if($2=="1") print "Hum.: "$4"'%'"}' | tail -n1)
echo $OREGON_H
RAIN=$(more /home/pi/Surveillance/tmp/433.log | awk 'BEGIN { FS = "," } ; {if($2=="10") print "Rain: "$3"l/m2 "}' | tail -n1)
echo $RAIN
/usr/bin/wget --delete-after "http://localhost:8082/0/config/set?text_left=$OREGON_TI\n$OREGON_T\n$OREGON_H\n$RAIN\n"
/usr/bin/wget --delete-after "http://localhost:8083/0/config/set?text_left=$OREGON_TI\n$OREGON_T\n$OREGON_H\n$RAIN\n"
#rm "estado_actual_p.asp?idEst=10053"

