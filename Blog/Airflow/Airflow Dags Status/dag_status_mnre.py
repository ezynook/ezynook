from datetime import datetime
import os, time
from sqlalchemy import create_engine
from urllib.parse import quote
import pandas as pd

try:
    engine = create_engine("postgresql://postgres:%s@172.16.23.207:5432/airflow_db" % quote('postgres'))
except Exception as e:
    print('Error ->', e)

sql = """
        SELECT DISTINCT ON (dag_run.dag_id)
            dag_run.dag_id, 
            dag_run.start_date as start_date, 
            dag_run.state as state
        FROM 
            dag_run 
        INNER JOIN
            dag ON dag_run.dag_id = dag.dag_id
        WHERE
            dag.is_paused = False
        ORDER BY 
            dag_run.dag_id, dag_run.start_date DESC
    """
query = pd.read_sql(sql, con=engine)

strData = ""

for i, row in query.iterrows():
    i = i+1
    strData += "[Dag No.] " + str(i)+" "
    strData += "[Dagname:] " + row['dag_id']+" "
    strData += "[Status]: " + row['state']+"\n"
    os.system(f"zabbix_sender -z 172.16.23.212 -s 'airflow01' -k {row['dag_id']} -o '{str(strData)}'")
    print(f"Send Data: ", row['dag_id']," Success")