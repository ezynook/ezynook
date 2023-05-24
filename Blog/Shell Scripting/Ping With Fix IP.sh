#!/bin/bash
echo "
===============================================
1. Ping between = 100 110 (without special chalector)
2. Insert IP Address = 192.168.1 (Only 3 Step)
===============================================
"
read -p "1. Enter Your Range Subnet: " NUMBER
read -p "2. Enter Your IP Address: " BC
checklog=$(ls | grep pinglog.txt)
if [ -z "$checklog" ]; then
	touch pinglog.txt && chmod +x pinglog.txt
else
	rm -f pinglog.txt
fi

for lookcheck in $(seq $NUMBER); do
	echo "Please wait in progress ..."
	ping -c 1 $BC.$lookcheck >/dev/null
	if ping -c 1 $BC.$lookcheck &>/dev/null; then
		echo "$BC.$lookcheck -> is Online" >>./pinglog.txt
	else
		echo "$BC.$lookcheck -> is Offline" >>./pinglog.txt
	fi
done
while read p; do
	echo "
 ==============Output==============
 $p
 ==============Output==============
  "
done <pinglog.txt
rm -f pinglog.txt
