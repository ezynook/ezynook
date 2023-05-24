#!/bin/bash
while true; do
    DATETIME=$(date +'%d-%m-%Y-%H:%M:%S')
    echo "" >/home/engineer/server.php # Clear old Code
    #HTML HEADER
    echo '<!DOCTYPE html>
    <html>
    <head>
        <meta charset="utf-8">
        <meta name="viewport" content="width=device-width, initial-scale=1, shrink-to-fit=no">
        <meta http-equiv="Content-Type" content="text/html; charset=utf-8">
        <title>Server Monitoring</title>
        <link rel="preconnect" href="https://fonts.googleapis.com">
        <link href="https://fonts.googleapis.com/css2?family=IBM+Plex+Sans+Thai&display=swap" rel="stylesheet">
        <link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/3.4.1/css/bootstrap.min.css">
        <script src="https://ajax.googleapis.com/ajax/libs/jquery/3.5.1/jquery.min.js"></script>
        <script src="https://maxcdn.bootstrapcdn.com/bootstrap/3.4.1/js/bootstrap.min.js"></script>
        <script src="https://ajax.googleapis.com/ajax/libs/jquery/3.5.1/jquery.min.js"></script>
        <style>
            body {
                font-family: "IBM Plex Sans Thai", sans-serif;
            }
        </style>
    </head>
    <body>
    <div class="container" style="margin-top: 20px;" id="autoload">
    <h3>Server Monitoring '"$DATETIME"' <p style="background-color:MediumSeaGreen;">(Every 1 Minute)</p></h3>
    <hr>
    ' >>/home/engineer/server.php
    ###########################################################################################################
    DOCKER=$(systemctl status docker | grep Active | awk '{print $2}')                         #Return active
    WEB=$(docker inspect myweb | grep Status | awk '{print $2}' | cut -c2-8)                   #Return running
    DB=$(docker inspect mydatabase | grep Status | awk '{print $2}' | cut -c2-8)               #Return running
    PORTAINER=$(docker inspect portainer | grep Status | awk '{print $2}' | cut -c2-8)         # Return running
    MEM=$(free | grep Mem | awk '{print $4}')                                                  #Return KB
    DISK=$(df -h | grep /dev/mapper/ubuntu--vg-ubuntu--lv | awk '{print $5}' | cut -d "%" -f1) #Return %
    SHELL=$(nmap -p 22 127.0.0.1 | grep open | awk '{print $2}')                               #Return open
    SHELLDETAIL=$(systemctl status sshd | grep -m 1 "active" | awk '{print $2 " " $3}')
    MEMSHOW=$(free -h | grep Mem | awk '{print $4}')
    DISKSIZE=$(df -h | grep /dev/mapper/ubuntu--vg-ubuntu--lv | awk '{print $4}')

    if [ -n "$DOCKER" ]; then
        echo "<h4>Docker Engine status: <i style='color: green;' class='blink_me'>$DOCKER</i></h4>" >>/home/engineer/server.php
    else
        echo "<h4>Docker Engine status: <i style='color: red;' class='blink_me'>$DOCKER</i></h4>" >>/home/engineer/server.php
    fi
    if [ -n "$WEB" ]; then
        echo "<h4>Web Server status: <i style='color: green;' class='blink_me'>$WEB</i></h4>" >>/home/engineer/server.php
    else
        echo "<h4>Web Server status: <i style='color: red;' class='blink_me'>$WEB</i></h4>" >>/home/engineer/server.php
    fi
    if [ -n "$DB" ]; then
        echo "<h4>Database status: <i style='color: green;' class='blink_me'>$DB</i></h4>" >>/home/engineer/server.php
    else
        echo "<h4>Database status: <i style='color: red;' class='blink_me'>$DB</i></h4>" >>/home/engineer/server.php
    fi
    if [ -n "$PORTAINER" ]; then
        echo "<h4>Portainer Dashboard status: <i style='color: green;' class='blink_me'>$PORTAINER</i></h4>" >>/home/engineer/server.php
    else
        echo "<h4>Portainer Dashboard status: <i style='color: red;' class='blink_me'>$PORTAINER</i></h4>" >>/home/engineer/server.php
    fi
    if [ -n "$SHELL" ]; then
        echo "<h4>Remote SSH status: <i style='color: green;' class='blink_me'>$SHELLDETAIL</i></h4>" >>/home/engineer/server.php
    else
        systemctl restart sshd
        echo "<h4>Remote SSH status: <i style='color: red;' class='blink_me'>$SHELLDETAIL</i></h4>" >>/home/engineer/server.php
    fi
    if [ "$MEM" -le 262144 ]; then
        sync
        echo 3 >/proc/sys/vm/drop_caches
        echo "<h4>Memory free available: <i style='color: red;' class='blink_me'>$MEMSHOW Waiting to clear...</i></h4>" >>/home/engineer/server.php
    else
        echo "<h4>Memory free available: <i style='color: green;' class='blink_me'>$MEMSHOW is Normal</i></h4>" >>/home/engineer/server.php
    fi
    if [ "$DISK" -ge 85 ]; then
        echo "<h4>Disk Used: <i style='color: red;' class='blink_me'>$DISK % (free $DISKSIZE) is Full</i></h4>" >>/home/engineer/server.php
    else
        echo "<h4>Disk Used: <i style='color: green;' class='blink_me'>$DISK % (free $DISKSIZE) is Normal</i></h4>" >>/home/engineer/server.php
    fi
    ###########################################################################################################
    echo '<div align="center">
    <p style="background-color:LightGray;">Dev by Pasit Yodsoi.</p>
    </div>
    ' >>/home/engineer/server.php
    #HTML END
    echo '</div>
    </body>
    </html>
    <script>
        window.setInterval("refresh()", 5000);     

        function refresh() {
            window.location.reload();
        }
    </script>' >>/home/engineer/server.php
    cp /home/engineer/server.php /home/engineer/pasit/service/server.php
    sudo chown engineer:engineer /home/engineer/pasit/service/server.php
    sudo chmod 777 /home/engineer/pasit/service/server.php
    sleep 5
done
