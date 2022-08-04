#!/bin/bash

for i in $(seq 1 1 100)
do 
	temp=$RANDOM
	let "temp %=100"
	frec=$RANDOM
	let "frec %=100"
	ampl=$RANDOM
	let "ampl %=100"
	temp2=$RANDOM
	let "temp2 %=100"
	frec2=$RANDOM
	let "frec2 %=100"
	ampl2=$RANDOM
	let "ampl2 %=100"
	temp3=$RANDOM
	let "temp3 %=100"
	frec3=$RANDOM
	let "frec3 %=100"
	ampl3=$RANDOM
	let "ampl3 %=100"
	mosquitto_pub -d -h localhost -p 1883 -t "mqtt-vibraciones" -m "[{\"sensor\":\"Sensor1\",\"temperatura\":$temp,\"frecuencia\":$frec,\"amplitud\":$ampl},{\"sensor\":\"Sensor2\",\"temperatura\":$temp2,\"frecuencia\":$frec2,\"amplitud\":$ampl2},{\"sensor\":\"Sensor3\",\"temperatura\":$temp3,\"frecuencia\":$frec3,\"amplitud\":$ampl3}]"
	sleep 1
done