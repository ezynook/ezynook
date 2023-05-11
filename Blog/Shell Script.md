## ตรวจสอบ Service ด้วย Grep Check Contains String

```
#!/bin/bash

STATE=`systemctl status server_status.service | grep active | awk '{print $3}'`

if [[ "$STATE" == "(running)" ]]; then
        echo "Active"
else
        echo "Inactive"
fi
```

## วิธีทำ Shell Script ให้รันบน SystemD

```
Step1 สร้างไฟล์ Shell Script
	- sudo vi /usr/bin/memory.sh (ใส่โค๊ดที่จะใช้ในการเช็ค Service ต่างๆ)
	- sudo chmod 775 /usr/bin/memory.sh 
Step2 สร้าง Systemd ไฟล์
	- sudo vi /lib/systemd/system/memory.service 
	- ใส่ Command
[Unit]
	Description=MemoryChecker
	After=systemd-journald.service
	After=systemd-networkd.service

[Service]
	TimeoutStopSec=5
	Restart=always
	RestartSec=30s
	ExecStart=/usr/bin/memory.sh

[Install]
	WantedBy=multi-user.target
Step3 Enable New Service
	- sudo systemctl daemon-reload 
	- sudo systemctl enable memory.service 
	- sudo systemctl start memory.service
	- sudo systemctl status memory.service 
```

## Airflow Service Checker

```
#!/bin/bash
#==============Script Service Apache======================
TODAY=$(date +%d-%m-%Y:%H-%M-%S)
while true; do
	echo "Task Check Apache Service is Running!"
	SERVER="192.168.10.127"
	PORT="8080"
	state=$(nmap -p $PORT "$SERVER" | grep "$PORT" | grep open)

	if [ -z "$state" ]; then
		conda activate airflow
		airflow scheduler &
		airflow webserver --port 8080 --ip 0.0.0.0
		echo "$TODAY Offline"
	else
		echo "$TODAY Service is Normal"
	fi
	sleep 300
done
```

## Check Disk Space Linux

```
#!/bin/bash
                                                                     
df -H | grep -vE '^Filesystem|tmpfs|cdrom' | awk '{ print $5 " " $1 }' | while read output;
do
  echo $output
  usep=$(echo $output | awk '{ print $1}' | cut -d'%' -f1  )
  partition=$(echo $output | awk '{ print $2 }' )
  if [ $usep -ge 90 ]; then
    echo "Disk Space is Full: $usep"
  else
    echo "Disk Space is Normal: $usep"
  fi
done
```

## Linux Ram Check

```
#!/bin/bash


while true; do

	MEM=$(free -mt | grep Mem | awk '{print $4}')

	if [ "$MEM" -le 500 ]; then
		sync; echo 3 > /proc/sys/vm/drop_caches 
	fi
	sleep 300
done
```

## Docker Container Checker

```
#!/bin/bash

COUNT=1
while true; do
	CONTAINER_NAME='trino'

	CID=$(docker ps -q -f status=running -f name=${CONTAINER_NAME})
	if [ ! "${CID}" ]; then
	  	docker run -p 8080:8080 --name trino -v trino:/etc/trino --restart=always trinodb/trino
	  	echo "$COUNT -> Trino Container is Down"
	else
		echo "$COUNT -> Trino Container is Normal"
	fi
	COUNT=$((COUNT+1))
	sleep 10
done
```

## If Check Condition

```
If Condition Shell Script

-n VAR - ค่าเป็นจริงถ้าค่าตรงกับตัวแปร
-z VAR - เป็นเท็จถ้าค่าไม่ตรงกับตัวแปร
STRING1 == STRING2 - เป็นจริงถ้าค่า 2 ค่าตรงกัน (String only)
STRING1 != STRING2 - เป็นเท็จถ้าค่า 2 ค่าไม่ตรงกัน (String only)
INTEGER1 -eq INTEGER2 (==)
INTEGER1 -gt INTEGER2 (>)
INTEGER1 -lt INTEGER2 (<)
INTEGER1 -ge INTEGER2 (>=)
INTEGER1 -le INTEGER2 (<=)
INTEGER1 -ne INTEGER2 (!=)
```

## Jupyter Checker Services

```
#!/bin/bash -i
#export CONDA_EXE='/root/anaconda3/bin/conda'
#export _CE_M=''
#export _CE_CONDA=''
#export CONDA_PYTHON_EXE='/root/anaconda3/bin/python'
TODAY=`date +%d-%m-%Y:%H-%M-%S`
while true
do
  	    echo "Task Check Jupyter Service is Running!"
        SERVER=192.168.10.127
        PORT=8888
        state=`nmap -p $PORT $SERVER | grep "$PORT" | grep open`

        if [ -z "$state" ]; then
		    conda activate airflow
		    jupyter notebook --allow-root
        else
            	echo "$TODAY -> Service Jupyter is Normal"
        fi

	sleep 300
done
```

## Linux Log Cleaner

```
#!/bin/bash

tdate=$(date -d "90 days ago" "+%Y-%m-%d")
path="/root/nook/"

find ${path} -type d -maxdepth 1 -printf "%P\n" |
while ps= read -r LOG; do
    if [ "${tdate}" ">" "${LOG%.*}" ]; then
        rm -rf ${path}${LOG}
    fi
done




# Generate the date in the proper format
discriminant=$(date -d "30 days ago" "+%Y_%m_%d")

# Find files based on the filename pattern and test against the date.
find . -type f -maxdepth 1 -name "*_*_*.txt" -printf "%P\n" |
while IFS= read -r FILE; do
    if [ "${discriminant}" ">" "${FILE%.*}" ]; then
        echo "${FILE}";
    fi
done
```

## Linux Send Line

```
curl -X POST -H "Authorization: Bearer LINE_TOKEN" -F "message=testtest" https://notify-api.line.me/api/notify
```

## Shell Script Switch Case

```
#!/bin/bash

read -p "Enter Your Age: " AGE

case "$AGE" in
   "20") echo "You are Young." 
   ;;
   "30") echo "You are old Young." 
   ;;
   "40") echo "You are old." 
   ;;
    *)
   echo "Another Age" 
    ;;
esac
```
