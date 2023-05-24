#!/bin/bash
#  _____         _____ _____ _______ _____  ________      __
# |  __ \ /\    / ____|_   _|__   __|  __ \|  ____\ \    / /
# | |__) /  \  | (___   | |    | |  | |  | | |__   \ \  / /
# |  ___/ /\ \  \___ \  | |    | |  | |  | |  __|   \ \/ /
# | |  / ____ \ ____) |_| |_   | |  | |__| | |____   \  /
# |_| /_/    \_\_____/|_____|  |_|  |_____/|______|   \/

while true; do
        echo "Pasitsoft Automate Scripting"
        TODAY=$(date +%d-%m-%Y:%H-%M-%S)
        SERVER=127.0.0.1
        PORT=80
        PORT2=3306
        state=$(nmap -p $PORT $SERVER | grep "$PORT" | grep open)
        statedb=$(nmap -p $PORT2 $SERVER | grep "$PORT2" | grep open)
        #Check Docker service
        if systemctl status docker | grep "Active: active"; then
                echo "Docker Engine Online: $TODAY"
                echo "(Action) -> Docker Engine service is Normal: $TODAY" >>/var/log/pasit/pasit.txt
        else
                systemctl restart docker
                curl -X POST -H "Authorization: Bearer 4r9lf2YEjsm4qYIMoMJcXo5IGqPrIyaBmeSI4SntJYV" -F "message=Automate restart | Docker engine is down: $TODAY" https://notify-api.line.me/api/notify
                echo "(Action) -> Docker Engine is down: $TODAY" >>/var/log/pasit/pasit.txt
        fi
        #Check database
        if [ -z "$statedb" ]; then
                docker restart mydatabase
                curl -X POST -H "Authorization: Bearer 4r9lf2YEjsm4qYIMoMJcXo5IGqPrIyaBmeSI4SntJYV" -F "message=Automate restart | Service Database is down: $TODAY" https://notify-api.line.me/api/notify
                echo "(Action) -> Database is down: $TODAY" >>/var/log/pasit/pasit.txt
        else
                echo "Database Online: $TODAY"
                echo "(Action) -> Database service is Normal: $TODAY" >>/var/log/pasit/pasit.txt
        fi
        #Check Apache webservice
        if [ -z "$state" ]; then
                docker restart myweb
                curl -X POST -H "Authorization: Bearer 4r9lf2YEjsm4qYIMoMJcXo5IGqPrIyaBmeSI4SntJYV" -F "message=Automate restart | Service Apache is down: $TODAY" https://notify-api.line.me/api/notify
                echo "(Action) -> Web service is down: $TODAY" >>/var/log/pasit/pasit.txt
        else
                echo "Web server Online: $TODAY"
                echo "(Action) -> Web service is Normal: $TODAY" >>/var/log/pasit/pasit.txt
        fi
        sleep 60
done
