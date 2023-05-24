from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.exceptions import AirflowSkipException
from airflow.operators.bash import BashOperator
from datetime import datetime, timedelta
import pandas as pd
import os
import subprocess
from sqlalchemy import create_engine
import pymysql

now = datetime.now()
today = now.strftime("%Y-%m-%d %H:%M:%S")

args = {
    'owner': 'Pasit Y.',
    'depends_on_past': False,    
    'retries': 1,
    'retry_delay': timedelta(minutes=2),
}  
dag = DAG(
    dag_id='Sending_Dags_Status_to_ZBX',
    default_args=args,
    start_date= datetime(2023, 2, 10),
    description='ส่งข้อมูล Dag Status ไปยัง Zabbix (Local Tesing Zone)',
    catchup=False,
    schedule_interval='*/15 * * * *',
)

#Defind Global Variable
ZBX_HOST = "192.168.10.219"
MY_HOST = "airflow"
DISCOVERY_KEY = "dagkey"

try:
    engine = create_engine("mysql+pymysql://root:airflow@192.168.10.41:3306/airflow")
except Exception as e:
    print('Error ->', e)
    
def getData():
    sql = """   
            SELECT 
                MAX(dag_run.dag_id) as dag_id, 
                MAX(DATE_FORMAT(dag_run.start_date, '%%Y/%%m/%%d %%H:%%i:%%s')) as start_date, 
                MAX(dag_run.state) as state,
                dag.is_paused as Active
            FROM 
                dag_run 
            INNER JOIN
                dag ON dag_run.dag_id = dag.dag_id
            GROUP BY
            	dag_run.dag_id
        """
    query = pd.read_sql(sql, con=engine)
    return query

def createItemKey(key):
    proc = subprocess.Popen(f'zabbix_sender -z {ZBX_HOST} \
    						-p 10051 \
    						-s "{MY_HOST}" \
                            -k {DISCOVERY_KEY} \
                            -o '+"'"+'{"data":[{"{#KEYNAME}":"'+str(key)+'"}]}'+"'", 
                            stdout=subprocess.PIPE, shell=True)
    (out, err) = proc.communicate()
    if 'failed: 0' in str(out):
        print("Create/Replace Item Key Successfully")
    else:
        print("Create/Replace Item Key Failure")
    
def explodeData(data, key):
    proc = subprocess.Popen(f'zabbix_sender -z {ZBX_HOST} \
    						-p 10051 \
    						-s "{MY_HOST}" \
                            -k {key} \
                            -o "{str(data)}"', 
                            stdout=subprocess.PIPE, shell=True)
    (out, err) = proc.communicate()
    if 'failed: 0' in str(out):
        print("Send Trapper Successfully")
    else:
        print("Send Trapper Failure")

def zbx_sender():
    strData = ""
    query = getData()
    for idx, row in query.iterrows():
        strData = "[Dagname:] " + row['dag_id'] + " [Update Date:] " \
                + str(row['start_date']) + " [Status:] " + row['state'] \
                + " [Send at:] "+today
        createItemKey(row['dag_id'])
        explodeData(strData, 'key'+'['+ row['dag_id']+']')

fill_task = PythonOperator(
    task_id='Load_Status_To_ZBX',
    python_callable=zbx_sender,
    dag=dag
)


fill_task