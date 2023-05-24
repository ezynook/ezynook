#!/bin/bash


while true; do

	MEM=$(free -mt | grep Mem | awk '{print $4}')

	if [ "$MEM" -le 500 ]; then
		sync; echo 3 > /proc/sys/vm/drop_caches 
	fi
	sleep 300
done