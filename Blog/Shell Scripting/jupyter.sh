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
            	echo "
   _____  ____  ______ _______ _   _ _______   __
  / ____|/ __ \|  ____|__   __| \ | |_   _\ \ / /
 | (___ | |  | | |__     | |  |  \| | | |  \ V / 
  \___ \| |  | |  __|    | |  | . ` | | |   > <  
  ____) | |__| | |       | |  | |\  |_| |_ / . \ 
 |_____/ \____/|_|       |_|  |_| \_|_____/_/ \_\
  $TODAY -> Service Jupyter is Normal
                "
        fi

	sleep 300
done