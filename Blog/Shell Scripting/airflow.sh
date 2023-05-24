#!/bin/bash
#==============Script Service Apache======================
TODAY=$(date +%d-%m-%Y:%H-%M-%S)
while true; do
	echo "Task Check Apache Service is Running!"
	SERVER="192.168.10.127"
	PORT="8080"
	state=$(nmap -p $PORT "$SERVER" | grep "$PORT" | grep open)

	if [ -z "$state" ]; then
		conda activate airflow
		airflow scheduler &
		airflow webserver -D --port 8080
		echo "$TODAY Offline"
	else
		echo "$TODAY Service is Normal"
	fi
	sleep 300
done
#==============Script Service Apache======================
