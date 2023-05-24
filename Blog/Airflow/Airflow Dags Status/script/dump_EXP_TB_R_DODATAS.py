#!/root/anaconda3/bin/python

from datetime import datetime
import os, time
from sqlalchemy import create_engine
import pymysql as pymysql

now = datetime.now()
today = now.strftime("%Y-%m-%d")

try:
    conn = create_engine('mysql+pymysql://root:airflow@10.30.99.246/airflow')
except Exception as e:
    print('Error ->', e)

sql = f"""
        SELECT 
            MAX(dag_id), 
            MAX(start_date) as start_date, 
            MAX(state) as state 
        FROM 
            dag_run 
        WHERE
            dag_id = 'dump_EXP_TB_R_DODATAS'
        ORDER BY 
            start_date DESC
        LIMIT 1 
    """
cursor = conn.execute(sql)
strData = ""
print("----------------------------")
for row in cursor:
    strData += "Dagname: " + row[0]+"\n"
    strData += "Date: " + str(row[1])+"\n"
    strData += "Status: " + row[2]+"\n"

print(strData)
print("----------------------------")
os.system(f'zabbix_sender \
            -z 10.30.99.242 \
            -s "hdfs-airflow.btmt.com" \
            -k DagName \
            -o "{str(strData)}"')