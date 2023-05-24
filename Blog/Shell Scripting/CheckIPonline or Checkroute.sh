#!/bin/sh

#Check IP Online
ping -c1 8.8.8.8 >/dev/null
if [ $? -eq 0 ]; then
        echo "Normal" >/dev/null
else
        sudo ifdown -a && sudo ifup -a
        echo "fail"
fi
#Check Interface Up
IPA=$(ip a | grep ens36 | sed -n '2,2p' | awk '{print $2}')

if [ -n "$IPA" ]; then
        echo "Normal" >/dev/null
else
        init 6
fi
#Check Route Available
ROUTE=$(ip r | grep default | awk '{print $3}')

if [ -n "$ROUTE" ]; then
        echo "Normal" >/dev/null
else
        route add -net 0.0.0.0 netmask 0.0.0.0 gw 192.168.10.1
        route add -net 192.168.10.0 netmask 255.255.255.0 gw 0.0.0.0
fi
