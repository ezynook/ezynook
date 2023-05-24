#!/usr/bin/ksh

echo "Please Wait ...."
sleep 10
echo > /etc/zabbix/scripts/Errpt_tmp.log

while read -r line ; do
    echo "$line Softnix" > /etc/zabbix/scripts/Errpt_tmp.log
done < /etc/zabbix/scripts/Errpt.log