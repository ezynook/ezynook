#!/bin/bash

COUNT=1
while true; do
	CONTAINER_NAME='trino'

	CID=$(docker ps -q -f status=running -f name=${CONTAINER_NAME})
	if [ ! "${CID}" ]; then
	  	docker run -p 8080:8080 --name trino -v trino:/etc/trino --restart=always trinodb/trino
	  	echo "$COUNT -> Trino Container is Down"
	else
		echo "$COUNT -> Trino Container is Normal"
	fi
	COUNT=$((COUNT+1))
	sleep 10
done