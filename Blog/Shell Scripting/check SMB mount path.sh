#!/bin/bash

echo "Check Mounted Samba directory mnt"
diskmount=$(df -h | grep '//192.168.10.190/admin')
if [ -z "$diskmount" ]; then
        mount -t cifs -o username=admin //192.168.10.190/admin /mnt
        echo "Mount /mnt Successfully"
else
        echo "Mounted already exists!"
fi
