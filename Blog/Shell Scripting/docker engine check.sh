#!/usr/bin/env bash
TODAY=$(date +%d-%m-%Y:%H-%M-%S)
$docker=$(systemctl status docker | grep "Active: active" | cut -c 11-17)
while true; do
        if [ -n "$docker" ]; then
                echo "
  _____         _____ _____ _______ _____  ________      __
 |  __ \ /\    / ____|_   _|__   __|  __ \|  ____\ \    / /
 | |__) /  \  | (___   | |    | |  | |  | | |__   \ \  / / 
 |  ___/ /\ \  \___ \  | |    | |  | |  | |  __|   \ \/ /  
 | |  / ____ \ ____) |_| |_   | |  | |__| | |____   \  /   
 |_| /_/    \_\_____/|_____|  |_|  |_____/|______|   \/                                               
 $TODAY Docker Engine is Running
                "
        else
                systemctl restart docker
        fi
        sleep 2
done
