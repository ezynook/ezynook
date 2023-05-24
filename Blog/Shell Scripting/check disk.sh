#!/bin/bash

DISK=$(df -h | grep /dev/mapper/ubuntu--vg-ubuntu--lv | awk '{print $5}' | cut -d "%" -f1)

if [ "$DISK" -le "5" ]; then
        echo "Disk is Full"
else
        echo "Disk is Normal"
fi
