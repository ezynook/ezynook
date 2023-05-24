#!/bin/bash
Gre='\e[0;32m'
Red='\e[0;31m'
Whi='\e[0;37m'
bold=$(tput bold)
reg=$(tput sgr0)

STATE=$(systemctl status sshd | grep active)
echo "---------------------------"
echo "id        name    status"
echo "---------------------------"
if [ -n "$STATE" ]; then
    echo -e "1	sshd	${Gre}${bold}Online${Whi}"
fi
echo "---------------------------"
