#!/bin/bash

HA_STATE=$(hdfs haadmin -getServiceState nn1)

if [ "$HA_STATE" == "active" ]; then
	exit 0
else
	sudo -u hdfs hdfs haadmin -transitionToActive nn1 --forceactive --forcemanual > /dev/null
	sudo -u hdfs hdfs haadmin -transitionToStandby nn2 --forcemanual > /dev/null
	exit 0
fi