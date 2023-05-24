from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.exceptions import AirflowSkipException
from airflow.operators.bash import BashOperator
from datetime import datetime, timedelta
from pyspark.sql import SparkSession
from pyspark.sql.types import *
from pyspark.sql.functions import *
import pyspark
import pandas as pd
import requests
import json
import os

now = datetime.now()
update_dt = now.strftime("%Y-%m-%d %H:%M:%S")
today = now.strftime("%Y-%m-%d")

os.environ['HADOOP_CONF_DIR'] = '/etc/hadoop/conf'
os.environ['JAVA_HOME'] = '/usr/local/jdk8u222-b10'
os.environ['HADOOP_USER_NAME']='hive'
os.environ['PYSPARK_PYTHON'] ='/HDFS01/anaconda3/envs/main/bin/python'
conf = pyspark.SparkConf().setAll([
     ('spark.driver.maxResultSize', '0'),
     ('spark.driver.memory', '2g'),
     ('spark.sql.repl.eagerEval.enabled','true'),
     ('hive.strict.managed.tables','false'),
     ('hive.metastore.uris', 'thrift://nn01.bigdata:9083'),
     ('metastore.client.capability.check','false')
    ])
spark = SparkSession.builder \
        .master("local[*]") \
        .appName("Engineer") \
        .config(conf=conf) \
        .enableHiveSupport() \
        .getOrCreate()

schema = StructType([
    StructField("id", IntegerType(), True),
    StructField("workby", StringType(), True),
    StructField("customer", StringType(), True),
    StructField("site", StringType(), True),
    StructField("malltype", StringType(), True),
    StructField("worktype", StringType(), True),
    StructField("details", StringType(), True),
    StructField("onsite", StringType(), True),
    StructField("time", StringType(), True),
    StructField("travel", StringType(), True),
    StructField("engineer", StringType(), True),
    StructField("status", StringType(), True),
    StructField("day", StringType(), True),
    StructField("date_start", StringType(), True),
    StructField("date_end", StringType(), True),
    StructField("status_work", StringType(), True),
    StructField("end_job_detail", StringType(), True),
    StructField("file_location", StringType(), True),
    StructField("update_by", StringType(), True)
])

args = {
    'owner': 'test_engineer',
    'depends_on_past': False,    
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}

def savetoTable():
    df = spark.createDataFrame(pd.read_json(f"http://engineer.da.co.th/api_json.php?from_date={today}&to_date={today}"), schema=schema)
    check_tb = os.system("sudo -u hdfs hdfs dfs -ls /user/hive/warehouse/pyspark.db | grep engineer")
    if check_tb == 0:
        df.write.mode("append").saveAsTable("pyspark.engineer")
    else:
        os.system("sudo -u hdfs hdfs dfs -rmr /user/hive/warehouse/pyspark.db/engineer/")
        df.write.mode("overwrite").saveAsTable("pyspark.engineer")
    
def clearspark():
    spark.stop()
    
dag = DAG(
    dag_id='get_engineer',
    default_args=args,
    start_date= datetime(2023, 2, 10),
    description='get_engineer',
    catchup=False,
    schedule_interval='15 15 * * *',
)

t1 = PythonOperator(
    task_id='Save_to_Hive',
    python_callable=savetoTable,
    dag=dag
)

t2 = PythonOperator(
    task_id="Clear_Session_Pyspark",
    python_callable=clearspark,
    dag=dag
)

t1 >> t2