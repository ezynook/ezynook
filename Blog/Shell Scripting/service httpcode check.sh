#!/bin/bash

URL="http://engineer.da.co.th"
message="Engineer.da.co.th HTTP Response Error!"
RESPONSE=$(curl --write-out %{http_code} --silent --output /dev/null ${URL})
TIMEDATE=$(timedatectl | grep "Local time" | awk '{print $4 " " $5}')
if [ $RESPONSE -ne 200 ]; then
        echo "*Http* is Down -> $TIMEDATE"
        echo "Subject: *HTTP* is Down
Web Server Port 80 is Down at: $TIMEDATE
" >msg.txt
        ssmtp ezynook@gmail.com <msg.txt
        rm -f msg.txt
        echo "*HTTP* is down at: $TIMEDATE" >>/var/log/pasit/pasit.txt
        curl -X POST -H "Authorization: Bearer 4r9lf2YEjsm4qYIMoMJcXo5IGqPrIyaBmeSI4SntJYV" -F "message=$message" https://notify-api.line.me/api/notify
else
        echo "*Http* is Normal -> $TIMEDATE"
fi
